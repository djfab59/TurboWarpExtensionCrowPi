# import speech_recognition as sr
# import pyaudio
 
# recognizer = sr.Recognizer()
 
# while True:
#     try:
#         with sr.Microphone() as source:
#             print("please speak...")
#             audio = recognizer.listen(source, timeout=10)
#     except sr.WaitTimeoutError:
#         print("No speaking, pass...")
#         continue
 
#     try:
#         text = recognizer.recognize_google(audio)
#         print("your said : " + text)
#     except sr.UnknownValueError:
#         print("Can not recognize")
#     except sr.RequestError as e:
#         print("request error; {0}".format(e))




import RPi.GPIO as GPIO
import pyaudio
import wave
import os
import sys

GPIO.setmode(GPIO.BCM)
BUTT = 17

def rec_fun():
    # 隐藏错误消息，因为会有一堆ALSA和JACK错误消息，但其实能正常录音
    # os.close(sys.stderr.fileno())
    GPIO.setmode(GPIO.BCM)
    # 设GPIO26脚为输入脚，电平拉高，也就是说26脚一旦读到低电平，说明按了按钮
    GPIO.setup(BUTT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    # wav文件是由若干个CHUNK组成的，CHUNK我们就理解成数据包或者数据片段。
    CHUNK = 512 
    FORMAT = pyaudio.paInt16  # pyaudio.paInt16表示我们使用量化位数 16位来进行录音
    RATE = 16000  # 采样率1.6k。
    WAVE_OUTPUT_FILENAME = "test.wav"
    print('请按住按钮开始录音...')
    GPIO.wait_for_edge(BUTT, GPIO.FALLING)
    # To use PyAudio, first instantiate PyAudio using pyaudio.PyAudio(), which sets up the portaudio system.
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = 1,    # cloud speecAPI只支持单声道
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    print("录音中...")
    frames = []
    # 按住按钮录音，放开时结束
    while GPIO.input(BUTT) == 0:
        data = stream.read(CHUNK)
        frames.append(data)
    print("录音完成，输出文件：" + WAVE_OUTPUT_FILENAME + '\n')
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(FORMAT))    # Returns the size (in bytes) for the specified sample format.
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return
if __name__ == '__main__':
    rec_fun()