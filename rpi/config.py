#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import serial
import RPi.GPIO as GPIO
from typing import Optional

Temp = '0123456789ABCDEF*'

class Config:
    FORCE = 17
    STANDBY = 4

    def __init__(self, baudrate: int = 9600):
        self.serial: Optional[serial.Serial] = serial.Serial("/dev/ttyS0", baudrate)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.FORCE, GPIO.IN)
        GPIO.setup(self.STANDBY, GPIO.OUT)
        GPIO.output(self.STANDBY, GPIO.HIGH)

    def uart_send_byte(self, value: bytes) -> None:
        if self.serial:
            self.serial.write(value)

    def uart_send_string(self, value: str) -> None:
        if self.serial:
            self.serial.write(value.encode())

    def uart_receive_byte(self) -> bytes:
        if self.serial:
            return self.serial.read(1)
        return b''

    def uart_receive_string(self, length: int) -> str:
        if self.serial:
            return self.serial.read(length).decode(errors='ignore')
        return ""

    def uart_set_baudrate(self, baudrate: int) -> None:
        if self.serial:
            self.serial.baudrate = baudrate