import threading
import traceback
from enum import Enum
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from _bleio.exceptions import BluetoothError
from bleak.exc import BleakError
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure


class VibrotactorArray:
    class VibrotactorArraySide(Enum):
        LEFT = b'\x01'
        RIGHT = b'\x00'

    class VibrotactorArrayReturn(Enum):
        PASS = b'\x00'
        FAIL = b'\x01'
        ERROR = -1

    class VibrotactorArrayData(Enum):
        AX = 0
        AY = 1
        AZ = 2
        GX = 3
        GY = 4
        GZ = 5
        MX = 6
        MY = 7
        MZ = 8
        HEADING = 9
        PITCH = 10
        ROLL = 11

    def __init__(self, ble, motor_count=12, max_vib=255):
        self.motor_count = motor_count
        self.max_vib = max_vib
        self.uart_connection = None
        self.uart_service = None
        self.ble = ble
        self.streaming = False
        self.data = [[] for i in range(12)]
        self.imu_thread = None

    def connect(self):
        self.uart_connection = None
        for tries in range(0, 10):
            if not self.uart_connection:
                try:
                    for adv in self.ble.start_scan(ProvideServicesAdvertisement):
                        if UARTService in adv.services:
                            self.uart_connection = self.ble.connect(adv)
                            break
                    self.ble.stop_scan()
                except BluetoothError:
                    print("Retrying...")
                    print(traceback.print_exc())
                except BleakError:
                    print("Retrying...")
                    print(traceback.print_exc())
        if self.uart_connection and self.uart_connection.connected:
            self.uart_service = self.uart_connection[UARTService]
            return True
        else:
            return False

    def write_motor(self, motor_index, vib_strength):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            if 0 <= motor_index < self.motor_count:
                if 0 <= vib_strength <= self.max_vib:
                    write_motor_command = bytearray([0x01, motor_index, vib_strength])
                    self.uart_service.write(write_motor_command)
                else:
                    return False
            else:
                return False
        else:
            return False

    def write_vib_level(self, motor_index, vib_strength):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            if 0 <= motor_index < self.motor_count:
                if 0 <= vib_strength <= self.max_vib:
                    write_motor_command = bytearray([0x02, motor_index, vib_strength])
                    self.uart_service.write(write_motor_command)
                else:
                    return False
            else:
                return False
        else:
            return False

    def trigger_vib(self):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            write_motor_command = bytearray([0x03, 0, 0])
            self.uart_service.write(write_motor_command)
        else:
            return False

    def start_imu(self):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            write_motor_command = bytearray([0x04, 0, 0])
            self.uart_service.write(write_motor_command)
            return_bytes = self.uart_service.read(1)
            try:
                return_code = self.VibrotactorArrayReturn(return_bytes)
                if return_code == self.VibrotactorArrayReturn.FAIL:
                    return return_code
                self.streaming = True
                # self.imu_thread = threading.Thread(target=self._imu_thread_cycle)
                # self.imu_thread.start()
                return return_code
            except ValueError:
                return self.VibrotactorArrayReturn.ERROR
        else:
            return False

    def stop_imu(self):
        self.streaming = False

    def get_side(self):
        if self.uart_connection and self.uart_connection.connected and self.uart_service:
            write_motor_command = bytearray([0x05, 0, 0])
            self.uart_service.write(write_motor_command)
            return_bytes = self.uart_service.read(1)
            try:
                return self.VibrotactorArraySide(return_bytes)
            except ValueError as ve:
                return self.VibrotactorArrayReturn.ERROR
        else:
            return False

    @staticmethod
    def get_ble_instance():
        return BLERadio()

    @staticmethod
    def parse_data_files():
        pass