import time
import spidev
# import RPi.GPIO as GPIO
from gpiozero import *
# from rpi_ws281x import PixelStrip, Color
import random
import copy
import pygame
import HD44780MCP
import MCP230XX
from elecrow_ws281x import *
import smbus

class LCDModule():

    def __init__(self):
        # Define LCD column and row size for 16x2 LCD.
        self.address    = 0x21
        self.lcd_cols   = 16
        self.lcd_rows   = 2
        self.bl_pin     = 7
        # Initialize the LCD using the pins
        self.mcp = MCP230XX.MCP230XX('MCP23008', self.address)
        self.lcd = HD44780MCP.HD44780(self.mcp, 1, -1, 2, dbList = [3, 4, 5, 6], rows = self.lcd_rows, characters = self.lcd_cols, mode = 0, font = 0)
        self.mcp.set_mode(self.bl_pin, 'output')

    def turn_off(self):
        # Turn backlight off
        self.lcd.set_display()
        self.mcp.output(self.bl_pin, 0)

    def turn_on(self):
        # Turn backlight on
        self.mcp.output(self.bl_pin, 1)
        self.lcd.set_display(on = 1, cursor = 1)

    def clear(self):
        # clear the LCD screen
        self.lcd.clear_display()

    def write_lcd(self,text):
        self.turn_on()
        self.lcd.display_string(text)

# define LCD module
lcd_screen = LCDModule()

pygame.mixer.init()


x_channel = 1
y_channel = 0

win_val = True
shake_pin = 27
touch_pin = 17

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(touch_pin, GPIO.IN)
# GPIO.setup(shake_pin, GPIO.OUT)

touch = InputDevice(touch_pin)
shake = OutputDevice(shake_pin)
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000

up_list = [0,1,2,3,4,5,6,7]
down_list = [56,57,58,59,60,61,62,63]
left_list = [0,8,16,24,32,40,48,56]
right_list = [7,15,23,31,39,47,55,63]
win_list = [[48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63],[40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55],
            [32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47],[24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39],
            [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],[8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], [56,57,58,59,60,61,62,63],[48,49,50,51,52,53,54,55],
            [40,41,42,43,44,45,46,47],[32,33,34,35,36,37,38,39],[24,25,26,27,28,29,30,31],[16,17,18,19,20,21,22,23],
            [8,9,10,11,12,13,14,15],[0,1,2,3,4,5,6,7]]


changtiao = [3,4]
L = [3,11,12]
zuoz = [2,3,11,12]
youz = [5,4,12,11]
zhengfang = [3,4,11,12]
sanjiao = [3,11,10,12]

xialuo_list = []
quanju_list = []
kong = []

suiji_val = 0
red_val = 0
green_val = 0
blue_val = 0
go = False
suiji_val = 0
number_val = 0
point = 0



def panduan_val(a,b):
    if a in b:
        return True
    else:
        return False

def list_panduan_val(a,b,val):
    c = []
    c = [x for x in a if x in b]
    if len(c) == val:
        return True
    else:
        return False

def bianxing():
    global changtiao
    global changtiao1
    global L
    global L1
    global L2
    global L3
    global zuoz
    global zuoz1
    global youz
    global youz1
    global zhengfang
    global sanjiao
    global sanjiao1
    global sanjiao2
    global sanjiao3
    global suiji_val
    global xialuo_list
    global number_val
    old_list = xialuo_list
    a = 0
    b = 0
    c = 0
    # if(GPIO.input(touch_pin)):
    if(touch.value):
        clearTrace(old_list)
        number_val += 1
        if suiji_val == 1:
            if number_val % 2 == 1:
                if list_panduan_win(xialuo_list,left_list):
                    xialuo_list[0] = xialuo_list[0]
                    number_val -= 1
                else:
                    xialuo_list[0] = xialuo_list[0] + 9
                    if list_panduan(xialuo_list,quanju_list) or panduan_val(xialuo_list[0]-1,quanju_list):
                        xialuo_list[0] = xialuo_list[0] - 9
                        number_val -= 1
            else:
                if list_panduan_win(xialuo_list,left_list):
                    xialuo_list[0] = xialuo_list[0]
                    number_val -= 1
                else:
                    xialuo_list[0] = xialuo_list[0] - 9
                    if list_panduan(xialuo_list,quanju_list) or panduan_val(xialuo_list[0]+8,quanju_list):
                        xialuo_list[0] = xialuo_list[0] + 9
                        number_val -= 1
                    
        elif suiji_val == 2:
            if number_val % 2 == 1:
                if list_panduan_val(xialuo_list,left_list,2) or list_panduan_val(xialuo_list,right_list,2) or list_panduan_val(xialuo_list,down_list,2) or panduan_val(xialuo_list[0]+8,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[0] = xialuo_list[0] + 16
                    xialuo_list[3] = xialuo_list[3] - 2
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[0] = xialuo_list[0] - 16
                        xialuo_list[3] = xialuo_list[3] + 2
                        number_val -= 1
            else:
                if list_panduan_val(xialuo_list,left_list,2) or list_panduan_val(xialuo_list,right_list,2) or list_panduan_val(xialuo_list,down_list,2) or panduan_val(xialuo_list[0]-1,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[0] = xialuo_list[0] - 16
                    xialuo_list[3] = xialuo_list[3] + 2
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[0] = xialuo_list[0] + 16
                        xialuo_list[3] = xialuo_list[3] - 2
                        number_val -= 1

        elif suiji_val == 3:
            if number_val % 2 == 1:
                if list_panduan_val(xialuo_list,left_list,2) or list_panduan_val(xialuo_list,right_list,2) or list_panduan_val(xialuo_list,down_list,2) or panduan_val(xialuo_list[0]+8,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[0] = xialuo_list[0] + 16
                    xialuo_list[3] = xialuo_list[3] + 2
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[0] = xialuo_list[0] - 16
                        xialuo_list[3] = xialuo_list[3] - 2
                        number_val -= 1
            else:
                if list_panduan_val(xialuo_list,left_list,2) or list_panduan_val(xialuo_list,right_list,2) or list_panduan_val(xialuo_list,down_list,2) or panduan_val(xialuo_list[0]+1,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[0] = xialuo_list[0] - 16
                    xialuo_list[3] = xialuo_list[3] - 2
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[0] = xialuo_list[0] + 16
                        xialuo_list[3] = xialuo_list[3] + 2
                        number_val -= 1

        elif suiji_val == 4:
            number_val = 0
                
        elif suiji_val == 5:
            if number_val % 4 == 1:
                if panduan_val(xialuo_list[0]-1,quanju_list) or panduan_val(xialuo_list[0]+1,quanju_list) or list_panduan_val(xialuo_list,down_list,3) or panduan_val(xialuo_list[3]+8,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[2] = xialuo_list[2] + 9
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[2] = xialuo_list[2] - 9
                        number_val -= 1
                
            elif number_val % 4 == 2:
                if panduan_val(xialuo_list[2]-1,quanju_list) or panduan_val(xialuo_list[3]+8,quanju_list) or panduan_val(xialuo_list[3]-8,quanju_list) or list_panduan_val(xialuo_list,left_list,3) or panduan_val(xialuo_list[3],right_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[0] = xialuo_list[0] + 7
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[0] = xialuo_list[0] - 7
                        number_val -= 1

            elif number_val % 4 == 3:
                if list_panduan_val(xialuo_list,down_list,1) or panduan_val(xialuo_list[0]-8,quanju_list) or panduan_val(xialuo_list[2]-1,quanju_list) or panduan_val(xialuo_list[2]+1,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[3] = xialuo_list[3] - 9
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[3] = xialuo_list[3] + 9
                        number_val -= 1
                        
            elif number_val % 4 == 0:
                if panduan_val(xialuo_list[3]+1,quanju_list) or panduan_val(xialuo_list[0]+8,quanju_list) or panduan_val(xialuo_list[0]-8,quanju_list) or list_panduan_val(xialuo_list,right_list,3) or panduan_val(xialuo_list[0],left_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[2] = xialuo_list[2] - 7
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[2] = xialuo_list[2] + 7
                        number_val -= 1
                    a = xialuo_list[0]
                    b = xialuo_list[2]
                    c = xialuo_list[3]
                    xialuo_list[3] = b
                    xialuo_list[0] = c
                    xialuo_list[2] = a
                
                
        elif suiji_val == 6:
            if number_val % 4 == 1:
                if panduan_val(xialuo_list[0]+1,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[2] = xialuo_list[2] - 8
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[2] = xialuo_list[2] + 8
                        number_val -= 1
                
            elif number_val % 4 == 2:
                if panduan_val(xialuo_list[2]+8,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[1] = xialuo_list[1] + 1
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[1] = xialuo_list[1] - 1
                        number_val -= 1
                
            elif number_val % 4 == 3:
                if panduan_val(xialuo_list[0]+8,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[0] = xialuo_list[0] + 8
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[0] = xialuo_list[0] - 8
                        number_val -= 1
            else:
                if panduan_val(xialuo_list[0]-8,quanju_list):
                    xialuo_list = xialuo_list
                    number_val -= 1
                else:
                    xialuo_list[2] = xialuo_list[2] - 1
                    if list_panduan(xialuo_list,quanju_list):
                        xialuo_list[2] = xialuo_list[2] + 1
                        number_val -= 1
                    a = xialuo_list[0]
                    b = xialuo_list[1]
                    c = xialuo_list[2]
                    xialuo_list[0] = c
                    xialuo_list[1] = a
                    xialuo_list[2] = b
        time.sleep(0.1)


        

def suiji():
    global suiji_val
    global xialuo_list
#    global changtiao
#    global zuoqi
#    global youqi
#    global zhengfang
#    global zuoz
#    global youz
#    global sanjiao
    global changtiao
    global zuoz
    global youz
    global zhengfang
    global sanjiao
    global L
    
    global red_val
    global green_val
    global blue_val
    
    global suiji_val
    
    global number_val
    
    changtiao = [3,4]
    L = [3,11,12]
    zuoz = [2,3,11,12]
    youz = [5,4,12,11]
    zhengfang = [3,4,11,12]
    sanjiao = [3,11,10,12]
    
    suiji_val = random.randint(1,6)
    xialuo_list = []
    red_val = 0
    green_val = 0
    blue_val = 0
    number_val = 0
    if suiji_val == 1:
        xialuo_list = changtiao
        red_val = 128
        green_val = 255
        blue_val = 255

    elif suiji_val == 2:
        xialuo_list = zuoz
        red_val = 0
        green_val = 0
        blue_val = 255

    elif suiji_val == 3:
        xialuo_list = youz
        red_val = 255
        green_val = 128
        blue_val = 64

    elif suiji_val == 4:
        xialuo_list = zhengfang
        red_val = 255
        green_val = 255
        blue_val = 0

    elif suiji_val == 5:
        xialuo_list = sanjiao
        red_val = 128
        green_val = 128
        blue_val = 192

    elif suiji_val == 6:
        xialuo_list = L
        red_val = 0
        green_val = 255
        blue_val = 0

def show(what,R,G,B):
    global quanju_list
    # for i in what:
    #     rp.setPixelColor(i,Color(R,G,B))
    # for i in quanju_list:   ##  这里的刷灯因为iic的慢速，就会产生闪烁的现象，对眼睛不好，需要去除这种闪烁的现象
    #     print(i)
    #     rp.setPixelColor(i,Color(255,255,255))
    # rp.show()

    rp.sendPos2Show(what, R, G, B)
    rp.sendPos2Show(quanju_list, 255, 255, 255)


def clearTrace(oldBlock):
    rp.sendPos2Show(oldBlock, 0, 0, 0)

def ReadChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def kongzhi():
    global xialuo_list
    global red_val
    global green_val
    global blue_val
    global down_list
    global quanju_list
    old_list = xialuo_list
    x_value = ReadChannel(x_channel)
    y_value = ReadChannel(y_channel)
    if y_value > 650:
        print("Up")
        
    if y_value < 400:
        print("Down")
        if list_panduan(xialuo_list,down_list) or list_panduan(xialuo_list,quanju_list):
            xialuo_list = xialuo_list
        else:
            xialuo_list = [i + 8 for i in xialuo_list]
            if list_panduan(xialuo_list,quanju_list):
                xialuo_list = [i - 8 for i in xialuo_list]


    if x_value > 650:
        print("Left")
        if list_panduan(xialuo_list,left_list):
            xialuo_list = xialuo_list
        else:
            xialuo_list = [i - 1 for i in xialuo_list]
            if list_panduan(xialuo_list,quanju_list):
                xialuo_list = [i + 1 for i in xialuo_list]
                
    if x_value < 400:
        print("Right")
        if list_panduan(xialuo_list,right_list):
            xialuo_list = xialuo_list
        else:
            xialuo_list = [i + 1 for i in xialuo_list]
            if list_panduan(xialuo_list,quanju_list):
                xialuo_list = [i - 1 for i in xialuo_list]
    # RGB_OFF() ##  不清全屏，只清除旧的痕迹
    clearTrace(old_list)
    show(xialuo_list,red_val,green_val,blue_val)

def list_panduan(a,b):
    c = []
    c = [x for x in a if x in b]
    if len(c) > 0:
        return True
    else:
        return False

def xialuo():
    global suiji_val
    global xialuo_list
    global changtiao
    global zuoqi
    global youqi
    global zhengfang
    global zuoz
    global youz
    global sanjiao
    global red_val
    global green_val
    global blue_val
    global go
    global quanju_list
    global kong
    global point

    suiji()
    go = True
    while go == True:
        show(xialuo_list,red_val,green_val,blue_val)
#         time.sleep(0.6)
        lcd_screen.write_lcd("Score:{0}".format(point))
        for i in range(10):
            kongzhi()
            bianxing()
            time.sleep(0.1)
        if list_panduan(xialuo_list,down_list):
            xialuo_list = xialuo_list
        else:
            xialuo_list = [i + 8 for i in xialuo_list]
        RGB_OFF()
        if list_panduan(xialuo_list,quanju_list):
            xialuo_list = [i - 8 for i in xialuo_list]
            go = False
            quanju_list = quanju_list + xialuo_list
            quanju_list = sorted(set(quanju_list),key=quanju_list.index)
            show(kong,0,0,0)
            print(quanju_list)
            list_win()
            break
        elif list_panduan(xialuo_list,down_list):
            go = False
            quanju_list = quanju_list + xialuo_list
            quanju_list = sorted(set(quanju_list),key=quanju_list.index)
            show(kong,0,0,0)
            print(quanju_list)
            list_win()
            break

def list_panduan_win(a,b):
    c = []
    c = [x for x in a if x in b]
    if len(c) == len(a):
        return True
    else:
        return False

def list_win():
    global win_list
    global quanju_list
    global point
    a = 0
    for i in range(15):
        if list_panduan_win(win_list[i],quanju_list):
            for q in range(2):
                # GPIO.output(shake_pin,GPIO.HIGH)
                shake.on()
                for j in win_list[i]:
                    rp.setPixelColor(j,Color(255,0,0))
                rp.show()
                time.sleep(0.2)
                for p in win_list[i]:
                    rp.setPixelColor(p,Color(255,255,255))
                rp.show()
                time.sleep(0.2)
            # GPIO.output(shake_pin,GPIO.LOW)
            shake.off()
#             quanju_list = (x for x in quanju_list if x not in win_list[i])
            quanju_list = list_win_list(quanju_list,win_list[i])
#             if len(quanju_list) == 0:
#                 RGB_OFF()
#             else:
            if i <=  6:
                for w in quanju_list:
                    if w < min(win_list[i]):
                        quanju_list[a] = w + 16
                    a += 1
                point += 2
            else:
                for w in quanju_list:
                    if w < min(win_list[i]):
                        quanju_list[a] = w + 8
                    a += 1
                point += 1
            RGB_OFF()
            for s in quanju_list:
                rp.setPixelColor(s,Color(255,255,255))
            rp.show()
            break

def list_win_list(a,b):
    for i in range(len(b)):
        a.remove(b[i])
    return a

def RGB_OFF():
    # list=[i for i in range(64)]
    # rp.sendPos2Show(list, 0, 0, 0)
    rp.fill()

def lose():
    global quanju_list
    global win_val
    lose_list = [2,3,4,5]
    if list_panduan(lose_list,quanju_list):
        time.sleep(1)
        for j in range(2):
            for i in quanju_list:
                rp.setPixelColor(i,Color(255,0,0))
            rp.show()
            time.sleep(0.2)
            RGB_OFF()
            time.sleep(0.2)
        win_val = False
        
lcd_screen = LCDModule()
        

rp = PixelStrip(64, 10)
rp.begin()

try:
    pygame.mixer.music.load("/usr/share/code/project/eluosi/1.wav")    #if NodeRed run this scripts, the path change to absolution path is better
    pygame.mixer.music.play()
    while win_val:
        xialuo()
        lose()

    pygame.mixer.music.stop()
    lcd_screen.write_lcd("Final score:{0}".format(point))
    pygame.mixer.music.load("/usr/share/code/project/eluosi/2.mp3")
    pygame.mixer.music.play()
    time.sleep(4)
    RGB_OFF()
    # GPIO.cleanup()
    shake.close()
    touch.close()
    lcd_screen.turn_off()
    pygame.mixer.music.stop()
    

except KeyboardInterrupt:
    RGB_OFF()
    # GPIO.cleanup()
    shake.close()
    touch.close()
    lcd_screen.turn_off()
    pygame.mixer.music.stop()