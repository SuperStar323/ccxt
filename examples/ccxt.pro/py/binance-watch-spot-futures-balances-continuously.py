# -*- coding: utf-8 -*-

from asyncio import get_event_loop, gather
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxtpro  # noqa: E402


print('CCXT Pro Version:', ccxtpro.__version__)


async def print_balance_continuously(exchange):
    while True:
        try:
            print('-----------------------------------------------------------')
            await exchange.load_markets()
            balance = await exchange.watch_balance()
            print(exchange.iso8601(exchange.milliseconds()), exchange.id)
            for currency, value in balance['total'].items():
                print(value, currency)
        except Exception as e:
            print('-----------------------------------------------------------')
            print(exchange.iso8601(exchange.milliseconds()), exchange.id, type(e), e)
            await exchange.sleep (300000)  # sleep 5 minutes and retry


async def main():
    config = {
        'apiKey': 'YOUR_API_KEY',
        'secret': 'YOUR_SECRET',
    }
    exchange_ids = [
        'binance',
        'binanceusdm',
        'binancecoinm',
    ]
    exchanges = [getattr(ccxtpro, exchange_id)(config) for exchange_id in exchange_ids]
    loops = [print_balance_continuously(exchange) for exchange in exchanges]
    await gather(*loops)


loop = get_event_loop()
loop.run_until_complete(main())