from templates.Account import Account
from Spotpair import SpotPair

class SpotAccount(Account):
    def add_pair(self, pair_name: str, min_quote_size: float, min_base_size: float, pair_balance: float, trading_fee: float) -> None:
        self.pairs[pair_name] = SpotPair(pair_name, min_quote_size, min_base_size, pair_balance, trading_fee)