"""
A basic example of controlling a motor via smbus
"""

import smbus2

BUS = smbus2.SMBus(1)
ADDRESS = 0x04

MODE_FLOAT = 0
MODE_BRAKE = 1
MODE_FWD = 2
MODE_BKW = 3

def set_motor(__tmp0, __tmp2: <FILL>) :
    """Sets a motor to spin. Any positive value is forwards, any negative one is
       backwards.
    """
    mode = MODE_FWD if __tmp2 >= 0 else MODE_BKW
    msg = smbus2.i2c_msg.write(ADDRESS, [__tmp0 << 5 | mode << 1 | 24, abs(__tmp2)])
    BUS.i2c_rdwr(msg)

def __tmp1(__tmp0) :
    """Stops the given motor"""
    # Mode 0 floats the motor.
    BUS.write_byte(ADDRESS, __tmp0 << 5 | MODE_BRAKE << 1)

def float_motors() :
    """Stops all motors and allows them to coast."""
    # The motor board stops all motors if bit 0 is high.
    BUS.write_byte(ADDRESS, 0x01)

def __tmp3() :
    """Stops all motors. Like, really hard."""
    for i in range(6):
        BUS.write_byte(ADDRESS, i << 5 | MODE_BRAKE << 1)
