#!/bin/python
import serial
import time
import sys
from struct import *

debug = 0


# work for pms3003
# support to Python3
# use the Raspberry Pi3 and connect to by TX/RX (GPIO 14 & GPIO 15) => /dev/ttyS0
# data structure: https://github.com/avaldebe/AQmon/blob/master/Documents/PMS3003_LOGOELE.pdf

class g3_sensor:
    def __init__(self):
        self.device = "/dev/ttyS0"
        self.serial = serial.Serial(self.device, baudrate=9600)

        if debug:
            print("init")
        self.endian = sys.byteorder
        self.data = None

    def conn_serial_port(self):
        if debug:
            print(self.device)
        if debug:
            print("conn ok")

    def check_keyword(self):
        if debug: print("check_keyword")
        while True:
            token2_hex = None
            token = self.serial.read()
            token_hex = token.hex()
            if debug:
                print(token_hex)
            if token_hex == '42':
                if debug:
                    print("get 42")
                token2 = self.serial.read()
                token2_hex = token2.hex()
                if debug:
                    print(token2_hex)
                if token2_hex == '4d':
                    if debug:
                        print("get 4d")
                    return True
            # fix me
            elif token2_hex == '00':
                if debug:
                    print("get 00")
                token3 = self.serial.read()
                token3_hex = token3.hex()
                if token3_hex == '4d':
                    if debug:
                        print("get 4d")
                    return True

    def vertify_data(self):
        if debug:
            print(self.data)
        n = 2
        pre_sum = int('42', 16) + int('4d', 16)
        for i in range(0, len(self.data) - 4, n):
            # print data[i:i+n]
            pre_sum = pre_sum + int(self.data[i:i + n], 16)
        ver_sum = int(self.data[40] + self.data[41] + self.data[42] + self.data[43], 16)
        if debug:
            print(pre_sum)
            if debug:
                print(ver_sum)
        if pre_sum == ver_sum:
            print("data correct")

    def read_data(self):
        self.data = self.serial.read(22)
        #data_hex = self.data.encode('hex')
        data_hex = self.data.hex()
        if debug:
            self.vertify_data(data_hex)

        pm1_cf = int(data_hex[4] + data_hex[5] + data_hex[6] + data_hex[7], 16)
        pm25_cf = int(data_hex[8] + data_hex[9] + data_hex[10] + data_hex[11], 16)
        pm10_cf = int(data_hex[12] + data_hex[13] + data_hex[14] + data_hex[15], 16)
        pm1 = int(data_hex[16] + data_hex[17] + data_hex[18] + data_hex[19], 16)
        pm25 = int(data_hex[20] + data_hex[21] + data_hex[22] + data_hex[23], 16)
        pm10 = int(data_hex[24] + data_hex[25] + data_hex[26] + data_hex[27], 16)
        if debug: print("pm1_cf: " + str(pm1_cf))
        if debug: print("pm25_cf: " + str(pm25_cf))
        if debug: print("pm10_cf: " + str(pm10_cf))
        if debug: print("pm1: " + str(pm1))
        if debug: print("pm25: " + str(pm25))
        if debug: print("pm10: " + str(pm10))
        data = [pm1_cf, pm10_cf, pm25_cf, pm1, pm10, pm25]
        self.serial.close()
        return data

    def read(self):
        self.conn_serial_port()
        if self.check_keyword():
            self.data = self.read_data()
            if debug:
                print(self.data)
            return self.data



# use this method can get the data => [pm1 , pm10 ,pm2.5]
def readAir():
    air = g3_sensor()
    try:
        pm_data = air.read()
    except:
        prnit("Error")

    if pm_data:
        return pm_data


# main
if __name__ == '__main__':
    while True:
        
        print(readAir())

