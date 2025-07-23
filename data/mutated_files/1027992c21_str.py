from typing import TypeAlias
__typ3 : TypeAlias = "datetime"
__typ0 : TypeAlias = "Stock"
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


now = __typ3.now()
THIS_YEAR = now.year
TODAY = now.strftime('%Y-%m-%d')
YESTERDAY = (now - timedelta(days=1)).strftime('%Y-%m-%d')
TWO_YEARS_AGO = now.replace(year=now.year-2, month=1, day=1).strftime('%Y-%m-%d')


Record = namedtuple('Record', ['date', 'price', 'expected_rate', 'bps', 'fROE'])
__typ2 = namedtuple('YearStat', ['year', 'high_price', 'low_price', 'high_expected_rate', 'low_expected_rate', 'bps', 'fROE'])
Event = namedtuple('Event', ['date', 'record', 'buy'])
EventStat = namedtuple('EventStat', ['buy_count', 'sell_count', 'profit'])


def parse_date(__tmp5) :
    return __typ3.strptime(__tmp5.split('T')[0], '%Y-%m-%d')


def __tmp6(code, date: str=YESTERDAY) :
    url = KAKAO_DAY_CANDLES % (code, 90000, date)
    print(url)
    urlopen = urllib.request.urlopen(url)
    data = json.loads(urlopen.read().decode())
    if 'dayCandles' not in data:
        return

    return data['dayCandles']


def parse_day_candles(code: <FILL>, date: str=YESTERDAY):
    data = __tmp6(code, date)
    prices = [{'code': code, 'price': d['tradePrice'], 'date': parse_date(d['date'])} for d in data]

    first_date = prices[-1]['date']
    if first_date.month != 1 and first_date.day != 1:
        yesterday_of_first = first_date - timedelta(days=1)
        data = __tmp6(code, date=yesterday_of_first.strftime('%Y-%m-%d'))
        old = [{'code': code, 'price': d['tradePrice'], 'date': parse_date(d['date'])} for d in data]
        prices = old + prices

    latest = db.get_latest_price(code)
    if latest:
        prices = [p for p in prices if p['date'] > latest['date']]
    
    if prices:
        db.save_prices(prices)


def make_record(date, price, bps, __tmp7) :
    if not bps:
        return Record(date=date, price=price, expected_rate=0, bps=0, fROE=0) 
    year = date.year
    ROEs = [roe[1] for roe in __tmp7.four_years_roe(year)]
    if len(ROEs) < 1:
        return Record(date=date, price=price, expected_rate=0, bps=0, fROE=0) 

    future_roe = mean(ROEs)
    calc_future_bps = lambda future: __typ1(bps * ((1 + (1 * future_roe / 100)) ** future))
    expected_rate = __tmp7.calc_expected_rate(calc_future_bps, 10, price)
    return Record(date=date, price=price, expected_rate=expected_rate, bps=bps, fROE=future_roe)    


def __tmp1(__tmp7) :
    prices = db.get_prices(__tmp7['code'])
    if not prices:
        parse_day_candles(__tmp7['code'])
        prices = db.get_prices(__tmp7['code'])
    else:
        last_date = prices[-1]['date']
        if last_date.strftime('%Y-%m-%d') != YESTERDAY:
            prices = db.get_prices(__tmp7['code'])
    
    if not prices:
        return
    
    BPSs = {b[0]: b[1] for b in __tmp7.year_stat('BPSs', exclude_future=True)}

    return [make_record(p['date'], p['price'], BPSs.get(p['date'].year-1), __tmp7) for p in prices]


def __tmp3(year, __tmp4) -> __typ2:
    high_price = max(record.price for record in __tmp4)
    low_price = min(record.price for record in __tmp4)
    high_expected_rate = max(record.expected_rate for record in __tmp4)
    low_expected_rate = min(record.expected_rate for record in __tmp4)
    stat = __typ2(year=year, 
            high_price=high_price, low_price=low_price, 
            high_expected_rate=high_expected_rate, low_expected_rate=low_expected_rate,
            bps=__tmp4[0].bps, fROE=__tmp4[0].fROE)
    return stat


def records_by_year(__tmp7: __typ0) :
    __tmp4 = __tmp1(__tmp7)
    __tmp0 = [(k, list(list(g))) for k, g in itertools.groupby(__tmp4, lambda r: r.date.year)]
    __tmp0 = [(__tmp3(year, __tmp4), __tmp4) for year, __tmp4 in __tmp0]
    events = __tmp2(__tmp0)
    return [(year_stat, __tmp4, [e for e in events if e.date.year == year_stat.year]) for year_stat, __tmp4 in __tmp0]


def __tmp2(__tmp0) :
    events = []
    last_buy_event = None
    for year_stat, __tmp4 in __tmp0:
        mid_expected_rate = mean([year_stat.high_expected_rate, year_stat.low_expected_rate])
        if mid_expected_rate < 13.5:
            mid_expected_rate = 13.5
        for r in __tmp4:
            if not last_buy_event and r.expected_rate >= mid_expected_rate:
                last_buy_event = Event(date=r.date, record=r, buy=True)
                events.append(last_buy_event)
            if last_buy_event and ((last_buy_event.record.expected_rate - r.expected_rate) >= 1.2
                or (last_buy_event.record.price * 0.13 + last_buy_event.record.price) <= r.price):
                events.append(Event(date=r.date, record=r, buy=False))
                last_buy_event = None
    return events
