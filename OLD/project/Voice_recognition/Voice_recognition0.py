# coding=utf-8
import sys
import json
import base64
import time
import snowboydecoder
import signal
import pyaudio
import wave
import speech_recognition as sr
import os
import requests
import logging
import traceback
# from vosk import KaldiRecognizer, Model
#import Adafruit_CharLCD as LCD

#   关闭所有没有必要的ALSA报错以及警告
os.close(sys.stderr.fileno())
#   关闭日志输出
logging.disable(logging.CRITICAL)


IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter
else:
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode
    if sys.platform == "win32":
        timer = time.clock
    else:
        # 在大多数其他平台上，最好的计时器是time.time()
        timer = time.time

'''class LCDModule():
	def __init__(self):
		self.address=0x21
		self.lcd_cloumns = 16
		self.lcd_rows = 2
		self.lcd = LCD.Adafruit_CharLCDBackpack(address=self.address)
		
	def turn_off(self):
		self.lcd.set_backlight(1)
	def turn_on(self):
		self.lcd.set_backlight(0)
	def clear(self):
		self.lcd.clear()
	def write_lcd(self,text):
		self.turn_on()
		time.sleep(0.0001)
		self.lcd.message(text)
		time.sleep(0.0001)
		#self.clear()
		time.sleep(1)
# 		self.turn_off()
lcd_screen = LCDModule()'''

interrupted = False

def print_line_number():
    stack = traceback.format_stack()
    print(stack[-2].strip())

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def callbacks():
    global detector
    # 语音唤醒后，提示ding两声
    snowboydecoder.play_audio_file()
    snowboydecoder.play_audio_file()
    #  关闭snowboy功能
    detector.terminate()
    # 打开snowboy功能
    wake_up()



# 定义语音唤醒函数
def wake_up():
    global detector
    model = 'Crowpi.pmdl'  #  唤醒词为 Crowpi
    # 获取中断信号
    signal.signal(signal.SIGINT, signal_handler)
    # 调整模型灵敏度
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.50)
    #lcd_screen.write_lcd(text=("Listening..."))
    print("\n\n**********************************************************************")
    print("**********************************************************************")
    print('\nPlease use the word "Crowpi" to wake me up...')
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.01)
    # 释放资源
    detector.terminate()

API_KEY = 'Wsjj93DuiuktBBD4Zhc59bfB'
SECRET_KEY = 'huULOjIGp777kCDW9TqLAGDdLdZMsUOo'

# 需要识别的文件
AUDIO_FILE = 'mytest.wav'
# 文件格式
FORMAT = AUDIO_FILE[-3:]
CUID = '123456PYTHON'
# 采样率
RATE = 16000
# 英语版，1737 表示识别英语
DEV_PID = 1737 
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'

class DemoError(Exception):
    pass

"""  TOKEN start """

# TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'

def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        result_str = err.read()
    if (IS_PY3):
        result_str =  result_str.decode()

    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if SCOPE and (not SCOPE in result['scope'].split(' ')):
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

"""  TOKEN end """

# 定义rec()函数进行录音
def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        #lcd_screen.clear()
        r.adjust_for_ambient_noise(source,2)
        r.adjust_for_ambient_noise(source,2)
        r.energy_threshold += 200
        #lcd_screen.write_lcd(text=("Please say: \n" ))
        print("\n")
        print("**********************************************************************")
        print("**********************************************************************")
        print("")
        print("Please ask about the weather or light, note that the sentence needs \nto contain the word 'weather' or 'light' ")
        print("")
        print("**********************************************************************")
        #print("please say something")
        audio = r.listen(source,phrase_time_limit=10)
    with open("mytest.wav", "wb") as f:
        f.write(audio.get_wav_data())

def speech_to_text():
    token = fetch_token()
    #signal.signal(signal.SIGINT, signal_handler)
    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)
    speech = base64.b64encode(speech_data)
    if (IS_PY3):
        speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        #print ("Request time cost %f" % (timer() - begin))
    except URLError as err:
        result_str = err.read()

    if (IS_PY3):
        result_str = str(result_str, 'utf-8')

    result = json.loads(result_str)
    # print(result_str)
    if('result' in result):
        result = str(result['result'])
        result = result.replace("[u'","")
        result = result.replace("']","")
        result = result.replace('["',"")
        result = result.replace('"]',"")
    else:
        result = str("**** >_< ****")
        #lcd_screen.clear()
        #lcd_screen.write_lcd(text=("Fail! \n" ))

    sys.stdout.write(str('                          '))
    print("\n")
    print("**********************************************************************")
    for i in range(len(str(result))):
        sys.stdout.write(str(result[i]))
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n")
    print("**********************************************************************")
    print("\n")
    with open("result.txt","w") as of:
        of.write(result_str)

    if "weather" in str(result):
        print("**********************************************************************")
        print("Got it!")
        print("**********************************************************************")
        os.system("sudo python /usr/share/code/project/Voice_recognition/crowpi_speech/dht11.py")
    elif "light" in str(result):
        print("**********************************************************************")
        print("Got it, the RGB matrix is working!")
        print("**********************************************************************")
        os.system("sudo python /usr/share/code/project/Voice_recognition/crowpi_speech/Lesson06.py")
    else:
        print("**********************************************************************")
        print("Failed, please try again!")
        print("**********************************************************************")

def formulateResult(resu):
    start = resu.index('"', resu.index('"', resu.index('"') + 1) + 1) + 1
    end = resu.index('"', start)
    return resu[start:end]

def useVosk2Recognize():
    r = sr.Recognizer()

    # test = sr.AudioFile('mytest.wav')
    test = sr.AudioFile('mytest.wav')

    with test as source:
        audio = r.record(source)

    r.vosk_model = Model(model_name="vosk-model-small-en-us-0.15")
    said = r.recognize_vosk(audio, language='en-US')
    result = formulateResult(said)
    print("==================================")
    print("==     Crowpi think you said----->  ", (result))
    print("==================================")

    if "weather" in str(result):
        print("**********************************************************************")
        print("Got it!")
        print("**********************************************************************")
        os.system("sudo python /usr/share/code/project/Voice_recognition/crowpi_speech/dht11.py")
    elif "light" in str(result):
        print("**********************************************************************")
        print("Got it, the RGB matrix is working!")
        print("**********************************************************************")
        os.system("sudo python /usr/share/code/project/Voice_recognition/crowpi_speech/Lesson06.py")
    else:
        print("**********************************************************************")
        print("Recognize failed, please try again!")
        print("**********************************************************************")    



if __name__ == '__main__':

    while True:
        wake_up()
        rec()
        # print_line_number()
        print('\n\n')
        print("**********************************************************************")
        print("Recognizing speech...")
        print("**********************************************************************")
        #lcd_screen.clear()
        #lcd_screen.write_lcd(text=("Waitting... \n" ))
        
        time.sleep(0.01)

        speech_to_text()
