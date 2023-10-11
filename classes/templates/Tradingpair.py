from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Literal
from utils.logger import Logger
from Trade import Trade

@dataclass
class TradingPair(ABC):
    _pair_name: str
    _trading_fee: float
    _min_quote_size: float  = 0
    _min_base_size: float = 0

    trade_count:int = 0
    pair_balance: float = 100.0
    trades: dict = {}
    logger: Logger = Logger()

    @property
    def pair_name(self) -> str:
        return self._pair_name
    
    @property
    def trading_fee(self) -> float:
        return self.trading_fee
    
    @property
    def min_quote_size(self) -> float:
        return self._min_quote_size
    
    @property
    def min_base_size(self) -> float:
        return self._min_base_size
    
    def get_trades(self) -> dict:
        return self.trades
    
    def get_logger(self) -> Logger:
        return self.logger

    def get_balance(self) -> float:
        return self.pair_balance
    
    def deposit(self, amount: float) -> None:
        self.pair_balance += amount

    def withdraw(self, amount: float) -> None:
        assert self.pair_balance >= amount, f"Cannot withdraw {amount} from {self.pair_name}, current balance = {self.pair_balance}."
        self.pair_balance -= amount

    def open_trade(self, amount: float, entry_price: float, entry_date: int, trade_type: str) -> None:
        assert self.pair_balance >= amount, f"Not enought balance to open trade with amount {amount} on {self.pair_name}, current balance = {self.pair_balance}."
        
        try:
            if self.trades:
                assert all([trade.status=="closed" for trade in self.trades.values() if trade_type==trade.trade_type]), f"Cannot open trade on {self.pair_name} of type {trade_type}, there is already an open trade."
            trade =  Trade(self.trade_count, amount, entry_price, entry_date, trade_type)
            self.trades[trade.id] = trade
            self.trade_count += 1
        except AssertionError as e:
            print(e)
            #TODO implementing shorts
            print("Adding amount to current trade.")
            self.add_to_trade(amount, entry_price)
        finally:    
            self.pair_balance -= trade.amount

    def add_to_trade(self, amount: float, entry_price: float, entry_date: int, trade_type: str) -> None:
        assert self.pair_balance >= amount, f"Not enought balance to add to trade with amount {amount} on {self.pair_name}, current balance = {self.pair_balance}."
        assert not self.trades, f"Cannot add to trade on {self.pair_name} of type {trade_type}, there is no open trade."

        try:
            assert any([trade.status=="open" for trade in self.trades.values() if trade_type==trade.trade_type]), f"There is currently no open trades for type {trade_type}."
            for id, trade in self.trades.items():
                if trade.status=="open" and trade.trade_type==trade_type:
                    trade.add_to_trade(amount, entry_price)
                    break
            self.pair_balance -= amount
        except AssertionError as e:
            print(e)
            print("Opening new trade.")
            self.open_trade(amount, entry_price, trade_type, entry_date)

    def log_iteration(self, current_price: float) -> None:

        if self.trades and any([trade.status=="open" for trade in self.trades.values()]):
            total_trading_balance = sum([trade.amount for trade in self.trades.values() if trade.status == "open"])
            # E.g. total balance is 200 and trade.amount is 50 then formula is Σ_trades((50/200) * (trade_pnl - 1))
            total_trading_pnl = 1 + sum([(trade.amount/total_trading_balance) * (trade.get_pnl(current_price) - 1) for trade in self.trades.values() if trade.status == "open"]) 
            #Calculate the pnl of the pair proportional to the total balance of the pair
            pair_pnl = total_trading_pnl * (self.pair_balance / total_trading_balance)
            self.logger(pair_pnl)
        else:
            # No updates to the pnl
            old_pnl = self.logger.pnl_history[-1]
            self.logger(old_pnl)



