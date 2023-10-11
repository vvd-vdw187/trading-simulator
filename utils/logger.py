from dataclasses import dataclass

@dataclass
class Logger:
    # The logger class is entended to be run as the very first thing in an iteration.
    pnl_history: list[float] = [1.0]
    drawdown_history: list[float] = [0.0]
    peak_pnl: float = 1

    def log_iteration(self, current_pnl: float) -> None:
        if current_pnl > self.peak_pnl:
            self.peak_pnl = current_pnl
            self.drawdown_history.append(0.0)
        else:
            self.drawdown_history.append((self.peak_pnl - current_pnl) / self.peak_pnl)
        self.pnl_history.append(current_pnl)

    def get_pnl_history(self) -> list[float]:
        return self.pnl_history
    
    def get_drawdown_history(self) -> list[float]:
        return self.drawdown_history
    
    def get_peak_pnl(self) -> float:
        return self.peak_pnl