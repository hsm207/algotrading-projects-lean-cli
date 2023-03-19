from AlgorithmImports import *


class ScheduleEvent(QCAlgorithm):
    """
    This algoritm will schedule a function to buy a stock once a month for
    a fixed dollar amount.
    If the fixed dollar amount is not enough to buy a full share, the algoritm
    will transfer bring forward the fixed dollar amount to the next month and
    add it to the fixed dollar amount for the next month.
    We repeat this process until we run out of cash.
    """

    def Initialize(self):
        self.SetStartDate(2019, 1, 1)  # Set Start Date
        # self.SetEndDate(2021, 1, 1)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.stock = self.AddEquity("TSLA", Resolution.Daily)

        # schedule the Buy function to run once a month at 9:30am
        self.Schedule.On(
            self.DateRules.MonthStart(), self.TimeRules.At(9, 30), self.Buy
        )

        # set the fixed dollar amount to buy a stock
        self.monthly_purchase_target = 200
        # set the current monthly allowance to the fixed dollar amount
        self.current_monthly_allowance = self.monthly_purchase_target

    # You don't need OnData() if you don't want to use it.
    # def OnData(self, data):
    #     """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
    #         Arguments:
    #             data: Slice object keyed by symbol containing the stock data
    #     """
    #     if not self.Portfolio.Invested:
    #         self.SetHoldings("SPY", 1)
    #         self.Debug("Purchased Stock")

    def Buy(self):
        # check if our portfolio has enough cash to buy a stock
        self.Debug(f"{self.stock.Symbol} opened at ${self.stock.Open} today.")

        if self.Portfolio.Cash < self.stock.Open:
            self.Debug(f"Not enough cash to buy {self.stock.Symbol} anymore :(")
            return

        # check if the current monthly allowance is enough to buy a stock
        if self.current_monthly_allowance < self.stock.Open:
            # if not, bring forward the current monthly allowance to the next month
            self.current_monthly_allowance += self.monthly_purchase_target
            self.Debug(
                f"Not enough cash to buy {self.stock.Symbol} this month. Bringing forward ${self.monthly_purchase_target} to the next month."
            )
            
        else:
            # figure out the number of shares we can buy
            shares_to_buy = self.current_monthly_allowance // self.stock.Open
            # buy the stock with a market order
            self.MarketOrder(self.stock.Symbol, shares_to_buy)
            # log the purchase
            self.Debug(
                f"Bought {shares_to_buy} shares of {self.stock.Symbol} with the ${self.current_monthly_allowance} allowance"
            )
            # reset the current monthly allowance to the fixed dollar amount
            self.current_monthly_allowance = self.monthly_purchase_target
    
    def OnOrderEvent(self, orderEvent):
        # log the cash balance after each order is filled
        if orderEvent.Status == OrderStatus.Filled:
            self.Debug(f"Current cash balance: ${self.Portfolio.Cash}")