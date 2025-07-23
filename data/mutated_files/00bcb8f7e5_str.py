from typing import TypeAlias
__typ2 : TypeAlias = "Stock"
__typ3 : TypeAlias = "datetime"
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


__typ0 = namedtuple('Record', ['date', 'price', 'expected_rate', 'bps', 'fROE'])
__typ1 = namedtuple('YearStat', ['year', 'high_price', 'low_price', 'high_expected_rate', 'low_expected_rate', 'bps', 'fROE'])
Event = namedtuple('Event', ['date', 'record', 'buy'])
EventStat = namedtuple('EventStat', ['buy_count', 'sell_count', 'profit'])


def parse_date(date_str: <FILL>) :
    return __typ3.strptime(date_str.split('T')[0], '%Y-%m-%d')


def load_kakao_json(__tmp1, date: str=YESTERDAY) :
    url = KAKAO_DAY_CANDLES % (__tmp1, 90000, date)
    print(url)
    urlopen = urllib.request.urlopen(url)
    data = json.loads(urlopen.read().decode())
    if 'dayCandles' not in data:
        return

    return data['dayCandles']


def parse_day_candles(__tmp1, date: str=YESTERDAY):
    data = load_kakao_json(__tmp1, date)
    prices = [{'code': __tmp1, 'price': d['tradePrice'], 'date': parse_date(d['date'])} for d in data]

    first_date = prices[-1]['date']
    if first_date.month != 1 and first_date.day != 1:
        yesterday_of_first = first_date - timedelta(days=1)
        data = load_kakao_json(__tmp1, date=yesterday_of_first.strftime('%Y-%m-%d'))
        old = [{'code': __tmp1, 'price': d['tradePrice'], 'date': parse_date(d['date'])} for d in data]
        prices = old + prices

    latest = db.get_latest_price(__tmp1)
    if latest:
        prices = [p for p in prices if p['date'] > latest['date']]
    
    if prices:
        db.save_prices(prices)


def make_record(date, price, bps, __tmp2) :
    if not bps:
        return __typ0(date=date, price=price, expected_rate=0, bps=0, fROE=0) 
    year = date.year
    ROEs = [roe[1] for roe in __tmp2.four_years_roe(year)]
    if len(ROEs) < 1:
        return __typ0(date=date, price=price, expected_rate=0, bps=0, fROE=0) 

    future_roe = mean(ROEs)
    calc_future_bps = lambda future: int(bps * ((1 + (1 * future_roe / 100)) ** future))
    expected_rate = __tmp2.calc_expected_rate(calc_future_bps, 10, price)
    return __typ0(date=date, price=price, expected_rate=expected_rate, bps=bps, fROE=future_roe)    


def build_records(__tmp2) :
    prices = db.get_prices(__tmp2['code'])
    if not prices:
        parse_day_candles(__tmp2['code'])
        prices = db.get_prices(__tmp2['code'])
    else:
        last_date = prices[-1]['date']
        if last_date.strftime('%Y-%m-%d') != YESTERDAY:
            prices = db.get_prices(__tmp2['code'])
    
    if not prices:
        return
    
    BPSs = {b[0]: b[1] for b in __tmp2.year_stat('BPSs', exclude_future=True)}

    return [make_record(p['date'], p['price'], BPSs.get(p['date'].year-1), __tmp2) for p in prices]


def make_year_stat(year: int, records) :
    high_price = max(record.price for record in records)
    low_price = min(record.price for record in records)
    high_expected_rate = max(record.expected_rate for record in records)
    low_expected_rate = min(record.expected_rate for record in records)
    stat = __typ1(year=year, 
            high_price=high_price, low_price=low_price, 
            high_expected_rate=high_expected_rate, low_expected_rate=low_expected_rate,
            bps=records[0].bps, fROE=records[0].fROE)
    return stat


def __tmp0(__tmp2: __typ2) -> List[Tuple[__typ1, List[__typ0]]]:
    records = build_records(__tmp2)
    by_year = [(k, list(list(g))) for k, g in itertools.groupby(records, lambda r: r.date.year)]
    by_year = [(make_year_stat(year, records), records) for year, records in by_year]
    events = simulate(by_year)
    return [(year_stat, records, [e for e in events if e.date.year == year_stat.year]) for year_stat, records in by_year]


def simulate(by_year) :
    events = []
    last_buy_event = None
    for year_stat, records in by_year:
        mid_expected_rate = mean([year_stat.high_expected_rate, year_stat.low_expected_rate])
        if mid_expected_rate < 13.5:
            mid_expected_rate = 13.5
        for r in records:
            if not last_buy_event and r.expected_rate >= mid_expected_rate:
                last_buy_event = Event(date=r.date, record=r, buy=True)
                events.append(last_buy_event)
            if last_buy_event and ((last_buy_event.record.expected_rate - r.expected_rate) >= 1.2
                or (last_buy_event.record.price * 0.13 + last_buy_event.record.price) <= r.price):
                events.append(Event(date=r.date, record=r, buy=False))
                last_buy_event = None
    return events
