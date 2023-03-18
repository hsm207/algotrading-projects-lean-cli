from AlgorithmImports import *


class SellAtPrice(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 1, 1)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        # self.AddEquity("SPY", Resolution.Daily)
        # another way to add a stock:
        self.apple = self.AddEquity("AAPL", Resolution.Daily)

        self.limit_price = 50
        # decide whether to invest or not
        self.invest = True

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        Arguments:
            data: Slice object keyed by symbol containing the stock data
        """
        if not self.Portfolio.Invested and self.invest:
            self.SetHoldings("AAPL", 1)
            self.Debug("Purchased Stock")

        # get apple's closing price and check if it's greater than the limit price
        closing_price = self.Portfolio["AAPL"].Price

        # make sure you hold apple stock before selling
        if closing_price > self.limit_price and self.Portfolio.Invested:
            self.Liquidate("AAPL")
            self.Debug("Sold Stock")
            self.invest = False
