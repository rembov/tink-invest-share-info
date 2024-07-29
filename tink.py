import os
import logging
from datetime import timedelta

import pandas as pd
from pandas import DataFrame
from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval, Client, SecurityTradingStatus, InstrumentIdType, PositionsResponse, \
    PositionsRequest, Instrument, LastPrice
from tinkoff.invest.services import InstrumentsService, MoneyValue, Quotation
from tinkoff.invest.utils import quotation_to_decimal
from config import TOKEN

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def tnk(ticker1):
    ticker = str(ticker1)

    with Client(TOKEN) as client:
        instruments: InstrumentsService = client.instruments
        tickers = []
        for method in ["shares"]:

            for item in getattr(instruments, method)().instruments:
                tickers.append(
                    {
                        "name": item.name,
                        "ticker": item.ticker,

                        "figi": item.figi,
                        "uid": item.uid,
                        "type": method,
                        "min_price_increment": quotation_to_decimal(
                            item.min_price_increment
                        ),
                        "scale": 9 - len(str(item.min_price_increment.nano)) + 1,
                        "lot": item.lot,
                        "trading_status": str(
                            SecurityTradingStatus(item.trading_status).name
                        ),
                        "api_trade_available_flag": item.api_trade_available_flag,
                        "currency": item.currency,
                        "exchange": item.exchange,
                        "buy_available_flag": item.buy_available_flag,
                        "sell_available_flag": item.sell_available_flag,
                        "short_enabled_flag": item.short_enabled_flag,
                        "nominal": quotation_to_decimal(item.nominal),
                        "klong": quotation_to_decimal(item.klong),
                        "kshort": quotation_to_decimal(item.kshort),

                    }
                )

        tickers_df = DataFrame(tickers)

        ticker_df = tickers_df[tickers_df["ticker"] == ticker]
        if ticker_df.empty:
            logger.error("There is no such ticker: %s", ticker)
            return

        figi = ticker_df["figi"].iloc[0]
        n = ticker_df.iloc[0][0]
        t = ticker_df.iloc[0][1]
        c = ticker_df.iloc[0][10]
        e = ticker_df.iloc[0][11]
        ka = ticker_df.iloc[0][7]
        mshc = ticker_df.iloc[0][5]
        dpd = ticker_df.iloc[0][12]
        dpd2 = ticker_df.iloc[0][13]

        f1 = ticker_df.iloc[0][2]

        u = client.market_data.get_last_prices(figi=[f1])
        uu = u.last_prices
        u2 = uu[0].price
        mon = cast_money(u2)
        llot = mon * ka

        k = f'Название компании: {n}\nТикер: {t}\nВалюта расчета: {c}\nБиржа: {e}\nДоступ к покупке: {ddd(dpd)}\nДоступ к продаже: {ddd2(dpd2)}\nКоличество акций в лоте: {ka}\nШаг цены: {mshc}\n' \
            f'Цена акции: {mon}\nЦена лота: {llot}\n'
        return k


def ddd(dpd):
    if dpd == True:
        return "Доступен к покупке"
    else:
        return "Недоступен к покупке"


def ddd2(dpd2):
    if dpd2 == True:
        return "Доступен к продаже"
    else:
        return "Недоступен к продаже"


def cast_money(v):
    return v.units + v.nano / 1e9 if isinstance(v, (Quotation, MoneyValue)) else v
