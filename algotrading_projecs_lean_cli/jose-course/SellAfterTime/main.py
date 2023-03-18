from AlgorithmImports import *


class SellAfterTime(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 1, 1)  # Set End Date
        self.SetCash(10000)  # Set Strategy Cash
        self.AddEquity("SPY", Resolution.Daily)
        self.invest = True

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        # buy SPY if not invested and want to invest
        if not self.Portfolio.Invested and self.invest:
            self.SetHoldings("SPY", 1)
            self.Debug("Purchased SPY")
            # record the invested time
            self.invested_time = self.Time
        
        # calculate the time difference between now and the invested time in days
        time_diff = (self.Time - self.invested_time).days
        # log it's been ... since you invested
        if self.Portfolio.Invested:
            self.Debug(f"It's been {time_diff} days since you bought SPY")

        # if the time difference is greater than 100 days, sell the stock
        # and log it
        if time_diff > 100 and self.Portfolio.Invested:
            self.Liquidate("SPY")
            self.Debug("Sold SPY after 100 days")
            self.invest = False
