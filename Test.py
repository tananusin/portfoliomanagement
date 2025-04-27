from dataclasses import dataclass, field

@dataclass
class StockData:
	#Google Sheet Variables
    name: str
    ticker: str
    currency: str
    shares: float
    target: float
    type: str
	
    #Porfolio Variables
    Price: float
    fx: float
    value_local: float
    value_thb: float
    weight: float