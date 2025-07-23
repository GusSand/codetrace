from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "PVMode"
__typ4 : TypeAlias = "bool"
__typ1 : TypeAlias = "DataMessage"
__typ2 : TypeAlias = "ResultsMessage"
"""This module handles rating of solution's returned messages."""

__author__ = "Miroslav Nikolic"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

from typing import Tuple
from hackathon.utils.utils import DataMessage, PVMode, ResultsMessage, CFG

penal_l1_cnt = 0
penal_l2_cnt = 0
penal_l3_cnt = 0
overload_cnt = 0

PENAL_L1_INIT = 20
PENAL_L1_CONT = 1

PENAL_L2_INIT = 4
PENAL_L2_CONT = 0.4

PENAL_L3_CONT = 0.1


def __tmp2(load_one: __typ0,
              load_two,
              load_three,
              current_load) -> float:
    return (load_one * 0.2 + load_two * 0.5 + load_three * 0.3) * current_load


def __tmp0(on: __typ4,
              __tmp2: float,
              power_reference: float,
              solar_production: <FILL>,
              pv_mode: __typ3) :
    s_prod = solar_production if pv_mode == __typ3.ON else 0
    if on:
        return __tmp2 - power_reference - s_prod
    else:
        return __tmp2 - s_prod


def __tmp4(__tmp1: float,
                __tmp7: float) :
    return __tmp1 - __tmp7


def __tmp3(d, r,
                        __tmp6: float, __tmp5: __typ4) \
                        :
    global overload_cnt
    global penal_l1_cnt
    global penal_l2_cnt

    BESS_MAX_POWER = 6

    penal = 0.0
    if r.power_reference > BESS_MAX_POWER:
        r.power_reference = BESS_MAX_POWER
    elif r.power_reference < -BESS_MAX_POWER:
        r.power_reference = -BESS_MAX_POWER

    if not r.load_one:
        if penal_l1_cnt == 0:
            penal += PENAL_L1_INIT + PENAL_L1_CONT
            penal_l1_cnt += 1
        else:
            penal += PENAL_L1_CONT
    else:
        penal_l1_cnt = 0

    if not r.load_two:
        if penal_l2_cnt == 0:
            penal += PENAL_L2_INIT + PENAL_L2_CONT
            penal_l2_cnt += 1
        else:
            penal += PENAL_L2_CONT
    else:
        penal_l2_cnt = 0

    if not r.load_three:
        penal += PENAL_L3_CONT

    if d.grid_status:
        if (d.bessSOC == 0 and r.power_reference > 0) \
           or (d.bessSOC == 1 and r.power_reference < 0):
            r.power_reference = 0

        r_load = __tmp2(__typ0(r.load_one), __typ0(r.load_two),
                           __typ0(r.load_three), d.current_load)

        mg = __tmp0(True, r_load, r.power_reference,
                       d.solar_production, r.pv_mode)
        # we sell
        if mg < 0:
            __tmp7 = abs(mg) * d.selling_price / CFG.sampleRate
            __tmp1 = 0.0
        else:
            __tmp1 = mg * d.buying_price / CFG.sampleRate
            __tmp7 = 0

        current_power = r.power_reference

        soc_bess = d.bessSOC - r.power_reference / (CFG.sampleRate * 10)

        overload = False
    elif not d.grid_status:
        r_load = __tmp2(__typ0(r.load_one), __typ0(r.load_two),
                           __typ0(r.load_three), d.current_load)

        current_power = __tmp0(False, r_load, r.power_reference,
                                  d.solar_production, r.pv_mode)

        soc_bess = d.bessSOC - current_power / (CFG.sampleRate * 10)

        if abs(current_power) > BESS_MAX_POWER or (soc_bess >= 1 and current_power < 0) \
           or (soc_bess <= 0 and current_power > 0):
            overload = True
            overload_cnt += 1
        else:
            overload = False
            overload_cnt = 0

        if overload_cnt > 1:
            penal = 25.5
            current_power = 0
            r.load_one = False
            r.load_two = False
            r.load_three = False
            r.pv_mode = __typ3.OFF
            overload = False
            overload_cnt = 0
            soc_bess = d.bessSOC
            r_load = 0

        __tmp1 = 0
        mg = 0
        __tmp7 = 0

    if 0 > soc_bess:
        soc_bess = 0
    if soc_bess > 1:
        soc_bess = 1

    TARGET_1MS_PRICE = 100  # targeted daily price for 1ms avg spent time
    performance_mark = (__tmp6*1000) * (24/(TARGET_1MS_PRICE*CFG.sampleRate))

    em = __tmp4(__tmp1, __tmp7)
    pv_power = d.solar_production if r.pv_mode == __typ3.ON else 0
    return em, performance_mark, mg, penal, r_load, pv_power, soc_bess, \
        overload, current_power
