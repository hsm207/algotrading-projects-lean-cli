from AlgorithmImports import *


class LimitOrders(QCAlgorithm):
    """
    This algo buys one stock using a limit order and then immediately sets another
    limit order to sell the stock at a higher price
    """

    def Initialize(self):
        self.SetStartDate(2011, 1, 1)  # Set Start Date
        # no end date means the algo will run forever
        # self.SetEndDate(2013, 10, 11)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.stock = self.AddEquity("TSLA", Resolution.Daily)
        self.invest = True

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        Arguments:
            data: Slice object keyed by symbol containing the stock data
        """
        ticker = self.stock.Symbol.Value

        if not self.Portfolio.Invested and self.invest:
            self.LimitOrder(ticker, quantity=100, limitPrice=2.00)

            self.LimitOrder(ticker, quantity=-100, limitPrice=300.00)

            self.invest = False
