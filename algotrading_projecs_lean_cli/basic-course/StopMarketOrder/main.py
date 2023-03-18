from AlgorithmImports import *


class StopMarketOrder(QCAlgorithm):
    """
    This algorithm shows how to place a stop market orders
    First, it wll buy some shares of a stock using a market order
    Then, it will place a stop market order to sell the stock at some price below the current price
    i.e. a stop loss order!
    """

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  # Set Start Date
        # self.SetEndDate(2013, 10, 11)  # Set End Date
        self.SetCash(100_000)  # Set Strategy Cash
        self.stock = self.AddEquity("BA", Resolution.Minute)
        self.invest = True
        self.sell_ticket = None  # to keep track of stop oder placed
        self.stop_loss_percent = 0.6

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        Arguments:
            data: Slice object keyed by symbol containing the stock data
        """
        if not self.Portfolio.Invested and self.invest:
            self.MarketOrder(self.stock.Symbol, 100)
            self.Debug(
                f"Purchased {self.Portfolio['BA'].Quantity} shares of f{self.stock.Symbol}"
            )
            self.invest = False

        if not self.sell_ticket and self.Portfolio.Invested:
            stop_price = self.stock.Close * (1 - self.stop_loss_percent)
            
            self.sell_ticket = self.StopMarketOrder(
                self.stock.Symbol,
                quantity=-self.Portfolio[self.stock.Symbol].Quantity,
                stopPrice=stop_price,
                tag=f"Stop Loss {self.stock.Symbol}"
            )
            self.Debug(
                f"Stop Market Order for {self.stock.Symbol} placed at {stop_price}"
            )
