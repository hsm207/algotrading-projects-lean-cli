from AlgorithmImports import *


class MarketOrders(QCAlgorithm):
    """
    This algorithm buys 100 shares of a stock using a market order.
    Then, it will sell all of its holdings using a market order at a predetermined time.
    """

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)  # Set Start Date
        self.SetEndDate(2015, 1, 1)  # Set End Date
        self.SetCash(10000)  # Set Strategy Cash
        self.stock = self.AddEquity("AAPL", Resolution.Daily)
        self.invest = True
        self.predetermined_time = datetime(2014, 1, 1)

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        Arguments:
            data: Slice object keyed by symbol containing the stock data
        """
        ticker = self.stock.Symbol.Value
        quantity = 100

        if not self.Portfolio.Invested and self.invest:
            self.MarketOrder(ticker, quantity)
            self.Debug(f"Purchased {ticker}")
            self.invest = False

        if self.Time >= self.predetermined_time and self.Portfolio.Invested:
            self.MarketOrder(ticker, -self.Portfolio[ticker].Quantity)
            self.invest = False
            self.Debug(f"Sold {ticker}")
