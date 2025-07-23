from typing import TypeAlias
__typ4 : TypeAlias = "datetime"
__typ3 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from collections import namedtuple
from statistics import mean
import itertools

import urllib.request
import json

from db import Stock
import db


KAKAO_DAY_CANDLES = "http://stock.kakao.com/api/securities/KOREA-A%s/day_candles.json?limit=%d&to=%s"


now = __typ4.now()
THIS_YEAR = now.year
TODAY = now.strftime('%Y-%m-%d')
YESTERDAY = (now - timedelta(days=1)).strftime('%Y-%m-%d')
TWO_YEARS_AGO = now.replace(year=now.year-2, month=1, day=1).strftime('%Y-%m-%d')


__typ0 = namedtuple('Record', ['date', 'price', 'expected_rate', 'bps', 'fROE'])
__typ2 = namedtuple('YearStat', ['year', 'high_price', 'low_price', 'high_expected_rate', 'low_expected_rate', 'bps', 'fROE'])
Event = namedtuple('Event', ['date', 'record', 'buy'])
EventStat = namedtuple('EventStat', ['buy_count', 'sell_count', 'profit'])


def __tmp6(__tmp7) :
    return __typ4.strptime(__tmp7.split('T')[0], '%Y-%m-%d')


def __tmp11(__tmp10, date: __typ3=YESTERDAY) -> List[dict]:
    url = KAKAO_DAY_CANDLES % (__tmp10, 90000, date)
    print(url)
    urlopen = urllib.request.urlopen(url)
    data = json.loads(urlopen.read().decode())
    if 'dayCandles' not in data:
        return

    return data['dayCandles']


def __tmp8(__tmp10, date: __typ3=YESTERDAY):
    data = __tmp11(__tmp10, date)
    prices = [{'code': __tmp10, 'price': d['tradePrice'], 'date': __tmp6(d['date'])} for d in data]

    first_date = prices[-1]['date']
    if first_date.month != 1 and first_date.day != 1:
        yesterday_of_first = first_date - timedelta(days=1)
        data = __tmp11(__tmp10, date=yesterday_of_first.strftime('%Y-%m-%d'))
        old = [{'code': __tmp10, 'price': d['tradePrice'], 'date': __tmp6(d['date'])} for d in data]
        prices = old + prices

    latest = db.get_latest_price(__tmp10)
    if latest:
        prices = [p for p in prices if p['date'] > latest['date']]
    
    if prices:
        db.save_prices(prices)


def __tmp4(date, price, bps, __tmp12) -> __typ0:
    if not bps:
        return __typ0(date=date, price=price, expected_rate=0, bps=0, fROE=0) 
    year = date.year
    ROEs = [roe[1] for roe in __tmp12.four_years_roe(year)]
    if len(ROEs) < 1:
        return __typ0(date=date, price=price, expected_rate=0, bps=0, fROE=0) 

    future_roe = mean(ROEs)
    calc_future_bps = lambda future: __typ1(bps * ((1 + (1 * future_roe / 100)) ** future))
    expected_rate = __tmp12.calc_expected_rate(calc_future_bps, 10, price)
    return __typ0(date=date, price=price, expected_rate=expected_rate, bps=bps, fROE=future_roe)    


def __tmp3(__tmp12: Stock) -> List[__typ0]:
    prices = db.get_prices(__tmp12['code'])
    if not prices:
        __tmp8(__tmp12['code'])
        prices = db.get_prices(__tmp12['code'])
    else:
        last_date = prices[-1]['date']
        if last_date.strftime('%Y-%m-%d') != YESTERDAY:
            prices = db.get_prices(__tmp12['code'])
    
    if not prices:
        return
    
    BPSs = {b[0]: b[1] for b in __tmp12.year_stat('BPSs', exclude_future=True)}

    return [__tmp4(p['date'], p['price'], BPSs.get(p['date'].year-1), __tmp12) for p in prices]


def __tmp5(year, __tmp9) -> __typ2:
    high_price = max(record.price for record in __tmp9)
    low_price = min(record.price for record in __tmp9)
    high_expected_rate = max(record.expected_rate for record in __tmp9)
    low_expected_rate = min(record.expected_rate for record in __tmp9)
    stat = __typ2(year=year, 
            high_price=high_price, low_price=low_price, 
            high_expected_rate=high_expected_rate, low_expected_rate=low_expected_rate,
            bps=__tmp9[0].bps, fROE=__tmp9[0].fROE)
    return stat


def __tmp0(__tmp12: <FILL>) :
    __tmp9 = __tmp3(__tmp12)
    __tmp1 = [(k, list(list(g))) for k, g in itertools.groupby(__tmp9, lambda r: r.date.year)]
    __tmp1 = [(__tmp5(year, __tmp9), __tmp9) for year, __tmp9 in __tmp1]
    events = __tmp2(__tmp1)
    return [(year_stat, __tmp9, [e for e in events if e.date.year == year_stat.year]) for year_stat, __tmp9 in __tmp1]


def __tmp2(__tmp1) -> List[Event]:
    events = []
    last_buy_event = None
    for year_stat, __tmp9 in __tmp1:
        mid_expected_rate = mean([year_stat.high_expected_rate, year_stat.low_expected_rate])
        if mid_expected_rate < 13.5:
            mid_expected_rate = 13.5
        for r in __tmp9:
            if not last_buy_event and r.expected_rate >= mid_expected_rate:
                last_buy_event = Event(date=r.date, record=r, buy=True)
                events.append(last_buy_event)
            if last_buy_event and ((last_buy_event.record.expected_rate - r.expected_rate) >= 1.2
                or (last_buy_event.record.price * 0.13 + last_buy_event.record.price) <= r.price):
                events.append(Event(date=r.date, record=r, buy=False))
                last_buy_event = None
    return events
