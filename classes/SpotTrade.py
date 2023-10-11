from templates import Trade

class SpotTrade(Trade):
    def get_pnl(self, current_price: float) -> float:
        if self.status == "open":
            if self.trade_type == "long":
                return (current_price - self.entry_price) / self.entry_price
            return (self.entry_price - current_price) / self.entry_price