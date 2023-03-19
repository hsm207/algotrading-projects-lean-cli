from AlgorithmImports import *


class OrderEvent(QCAlgorithm):
    """
    This algorithm shows how to work with the OnOrderEvent method

    The algorithm itself is about buying a stock and selling it for x% profit
    """
    def Initialize(self):
        self.SetStartDate(2015, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 1, 1)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.stock = self.AddEquity("TSLA", Resolution.Daily)

        self.buy_toggle = True
        self.sell_toggle = True

        self.profit_target_percent = 0.1

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        """
        
        # don't do anything if your data feed has no data about the stock
        if not data[self.stock.Symbol]:
            return
        
        if not self.Portfolio.Invested and self.buy_toggle:
            purchase_quantity = self.Portfolio.Cash // data[self.stock.Symbol].Open
            self.MarketOrder(self.stock.Symbol, purchase_quantity)
            self.Debug(f"Bought {purchase_quantity} shares of {self.stock.Symbol}")
            self.buy_toggle = False
            return
        
        unrealized_profit = self.Portfolio[self.stock.Symbol].UnrealizedProfitPercent

        if unrealized_profit > self.profit_target_percent and self.sell_toggle:
            self.MarketOrder(self.stock.Symbol, -self.Portfolio[self.stock.Symbol].Quantity)
            # log the unrealized profit in 2 decimal places
            self.Debug(f"Sold {self.stock.Symbol} for a {unrealized_profit * 100:.2f}% profit")
            self.sell_toggle = False
        
    def OnOrderEvent(self, orderEvent):
        # this event is triggered when an order is filled
        # it's a good place to log the order event
        self.Debug(f"Order Event: {orderEvent}")
        # you can also access the order object
        order = self.Transactions.GetOrderById(orderEvent.OrderId)
        self.Debug(f"Order: {order}")
        
