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


def __tmp1(date_str) -> __typ4:
    return __typ4.strptime(date_str.split('T')[0], '%Y-%m-%d')


def __tmp0(code, date: __typ3=YESTERDAY) -> List[dict]:
    url = KAKAO_DAY_CANDLES % (code, 90000, date)
    print(url)
    urlopen = urllib.request.urlopen(url)
    data = json.loads(urlopen.read().decode())
    if 'dayCandles' not in data:
        return

    return data['dayCandles']


def parse_day_candles(code: __typ3, date: __typ3=YESTERDAY):
    data = __tmp0(code, date)
    prices = [{'code': code, 'price': d['tradePrice'], 'date': __tmp1(d['date'])} for d in data]

    first_date = prices[-1]['date']
    if first_date.month != 1 and first_date.day != 1:
        yesterday_of_first = first_date - timedelta(days=1)
        data = __tmp0(code, date=yesterday_of_first.strftime('%Y-%m-%d'))
        old = [{'code': code, 'price': d['tradePrice'], 'date': __tmp1(d['date'])} for d in data]
        prices = old + prices

    latest = db.get_latest_price(code)
    if latest:
        prices = [p for p in prices if p['date'] > latest['date']]
    
    if prices:
        db.save_prices(prices)


def make_record(date, price, bps, stock) :
    if not bps:
        return __typ0(date=date, price=price, expected_rate=0, bps=0, fROE=0) 
    year = date.year
    ROEs = [roe[1] for roe in stock.four_years_roe(year)]
    if len(ROEs) < 1:
        return __typ0(date=date, price=price, expected_rate=0, bps=0, fROE=0) 

    future_roe = mean(ROEs)
    calc_future_bps = lambda future: __typ1(bps * ((1 + (1 * future_roe / 100)) ** future))
    expected_rate = stock.calc_expected_rate(calc_future_bps, 10, price)
    return __typ0(date=date, price=price, expected_rate=expected_rate, bps=bps, fROE=future_roe)    


def build_records(stock: <FILL>) :
    prices = db.get_prices(stock['code'])
    if not prices:
        parse_day_candles(stock['code'])
        prices = db.get_prices(stock['code'])
    else:
        last_date = prices[-1]['date']
        if last_date.strftime('%Y-%m-%d') != YESTERDAY:
            prices = db.get_prices(stock['code'])
    
    if not prices:
        return
    
    BPSs = {b[0]: b[1] for b in stock.year_stat('BPSs', exclude_future=True)}

    return [make_record(p['date'], p['price'], BPSs.get(p['date'].year-1), stock) for p in prices]


def make_year_stat(year, records: List[__typ0]) -> __typ2:
    high_price = max(record.price for record in records)
    low_price = min(record.price for record in records)
    high_expected_rate = max(record.expected_rate for record in records)
    low_expected_rate = min(record.expected_rate for record in records)
    stat = __typ2(year=year, 
            high_price=high_price, low_price=low_price, 
            high_expected_rate=high_expected_rate, low_expected_rate=low_expected_rate,
            bps=records[0].bps, fROE=records[0].fROE)
    return stat


def records_by_year(stock: Stock) -> List[Tuple[__typ2, List[__typ0]]]:
    records = build_records(stock)
    by_year = [(k, list(list(g))) for k, g in itertools.groupby(records, lambda r: r.date.year)]
    by_year = [(make_year_stat(year, records), records) for year, records in by_year]
    events = simulate(by_year)
    return [(year_stat, records, [e for e in events if e.date.year == year_stat.year]) for year_stat, records in by_year]


def simulate(by_year: List[Tuple[__typ2, List[__typ0]]]) :
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
