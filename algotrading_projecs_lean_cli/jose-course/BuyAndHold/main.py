from AlgorithmImports import *


class BuyAndHold(QCAlgorithm):
    """
    This algo buys and holds one company
    """

    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 1, 1)  # Set End Date
        self.SetCash(10000)  # Set Strategy Cash
        self.AddEquity("AAPL", Resolution.Daily)

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        Arguments:
            data: Slice object keyed by symbol containing the stock data
        """
        if not self.Portfolio.Invested:
            self.SetHoldings("AAPL", 1)
            self.Debug("Purchased Stock")
