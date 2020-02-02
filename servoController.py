#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import Adafruit_PCA9685
import time

#SG92Rをコントロールするためのクラス
class SG90_92R_Class:
    # mPin : GPIO Number (PWM)
    # mPwm : Pwmコントロール用のインスタンス
    # m_Zero_offset_duty :

    """コンストラクタ"""
    def __init__(self, Channel, ZeroOffset):
        self.mChannel = Channel
        self.m_ZeroOffset = ZeroOffset

        #Adafruit_PCA9685の初期化
        self.mPwm = Adafruit_PCA9685.PCA9685(address=0x40) #address:PCA9685のI2C Channel 0x40
        self.mPwm.set_pwm_freq(60)  #本当は50Hzだが60Hzの方がうまくいく

    """位置セット"""
    def SetPos(self,pos):
        #pulse = 150～650 : 0 ～ 180deg
        pulse = (650-150)*pos/180+150+self.m_ZeroOffset
        self.mPwm.set_pwm(self.mChannel, 0, pulse)

    """終了処理"""
    def Cleanup(self):
        #サーボを10degにセットしてから、インプットモードにしておく
        self.SetPos(90)
        time.sleep(1)

"""コントロール例"""
if __name__ == '__main__':
    Servo = SG90_92R_Class(Channel=0, ZeroOffset=-10)
    try:
        while True:
            Servo.SetPos(0)
            time.sleep(1)
            Servo.SetPos(90)
            time.sleep(1)
            Servo.SetPos(180)
            time.sleep(1)
            Servo.SetPos(90)
            time.sleep(1)
    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
    except Exception as e:
        print(str(e))
    finally:
        Servo.Cleanup()
        print("\nexit program")
