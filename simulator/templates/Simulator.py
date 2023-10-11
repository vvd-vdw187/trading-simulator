from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional, field
from classes.templates import Account
import pandas as pd
import inspect

@dataclass
class Simulator(ABC):
    data: pd.DataFrame 
    long_condition: Optional[Callable] = field(default=None)
    sell_long_condition: Optional[Callable] = field(default=None)
    short_condition: Optional[Callable] = field(default=None)
    sell_short_condition: Optional[Callable] = field(default=None)
    
    long_stop_loss: Optional[Callable] = field(default=None)
    long_take_profit: Optional[Callable] = field(default=None)
    short_stop_loss: Optional[Callable] = field(default=None)
    short_take_profit: Optional[Callable] = field(default=None)

    def __post__init__(self):
        #Check if even a long or short condition is set, and if so, check if the corresponding sell condition is set.
        assert any(self.long_condition, self.short_condition), "At least one of long_condition or short_condition must be set."
        assert not (self.long_condition is not None and self.sell_long_condition is None), "If long_condition is set, sell_long_condition must be set."
        assert not (self.short_condition is not None and self.sell_short_condition is None), "If short_condition is set, sell_short_condition must be set."

        #Test the defined buy and sell functions for returning boolean values 
        for func in (self.long_condition, self.short_condition, self.sell_long_condition, self.sell_short_condition):
            if func is not None:
                num_params = len(inspect.signature(func).parameters)
                mock_data = [None] * num_params
                result = func(*mock_data)
                if not isinstance(result, bool):
                    raise ValueError(f"The function {func.__name__} does not return a boolean value.")
                
        #Test the defined stop loss and take profit functions for returning float values 
        for func in (self.long_stop_loss, self.long_take_profit, self.short_stop_loss, self.short_take_profit):
            if func is not None:
                num_params = len(inspect.signature(func).parameters)
                mock_data = [None] * num_params
                result = func(*mock_data)
                if not isinstance(result, float):
                    raise ValueError(f"The function {func.__name__} does not return a float value.")
        
        #TODO Test if the columns used in the defined functions are present in the dataframe.

    @abstractmethod
    def simulate(self, account: Account) -> None:
        pass

                
    
        
    

        
        
