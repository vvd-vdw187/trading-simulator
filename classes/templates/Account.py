from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Literal
from utils.logger import Logger
from Trade import Trade
from TradingPair import TradingPair

@dataclass
class Account:
    balance: int = 100
    logger: Logger = Logger()
    pairs: dict = {}

    def add_pair(self, pair_name: str, min_quote_size: float, min_base_size: float, pair_balance: float, trading_fee: float) -> None:
        self.pairs[pair_name] = TradingPair(pair_name, min_quote_size, min_base_size, pair_balance, trading_fee)

    def add_trade(self, pair_name: str, amount: float, buy_price: float, type: str) -> int:
        if pair_name not in self.pairs:
            self.pairs[pair_name] = TradingPair(pair_name)
        trade = Trade(self.trade_counter, amount, buy_price, type)
        self.pairs[pair_name].add_trade(trade)
        self.trade_counter += 1
    