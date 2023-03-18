from AlgorithmImports import *


class SellOnProfit(QCAlgorithm):
    """
    This algoritm buys AAPL and sells it when it reaches a 100% profit.
    """
    def Initialize(self):
        self.SetStartDate(2010, 1, 1)  # Set Start Date
        self.SetEndDate(2015, 1, 1)  # Set End Date
        self.SetCash(10000)  # Set Strategy Cash
        self.AddEquity("AAPL", Resolution.Daily)

        # Set to negative for target loss
        # e.g. -0.5 means 50% loss
        self.profit_percent_target = 1.0
        self.invest = True # avoids keep buying and selling

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        if not self.Portfolio.Invested and self.invest:
            self.SetHoldings("AAPL", 1)
            self.Debug("Purchased Stock")

        # UnrealizedProfitPercent is the percent of profit/loss ranges from -1 to infinity
        profit_percent = self.Portfolio["AAPL"].UnrealizedProfitPercent

        if profit_percent >= self.profit_percent_target:
            self.Liquidate("AAPL")
            self.invest = False
            self.Debug("Sold Stock")