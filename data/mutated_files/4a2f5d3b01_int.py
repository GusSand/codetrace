"""Helper code for polling I2C touch sensors"""

from threading import Thread
import time

import smbus2

from data import SensorData

class __typ0(Thread):
    """Polls the rotary encoder and updates the relevant sensors."""
    def __init__(__tmp0, __tmp1, address: <FILL>, data) :
        __tmp0.address = address
        __tmp0.bus = smbus2.SMBus(__tmp1)
        __tmp0.data = data

        super().__init__()

    def run(__tmp0):
        while True:
            msg = smbus2.i2c_msg.read(5, 2)
            __tmp0.bus.i2c_rdwr(msg)
            for i, val in enumerate(msg):
                if val >= 128:
                    val = -256 + val

                if i == 1:
                    __tmp0.data.front_lifting_rot.change(val)
                elif i == 0:
                    __tmp0.data.back_lifting_rot.change(val)

            time.sleep(0.05)
