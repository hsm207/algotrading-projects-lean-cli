from AlgorithmImports import *


class TrailingStop(QCAlgorithm):
    """ "
    This algorithm demonstrates how to use the TrailingStop function to set a trailing stop loss on a long position.
    We set the initial stop loss to x% below the entry price and then use the TrailingStop function to move the stop loss
    up by y% each time the price closed at a new high
    """

    def Initialize(self):
        self.SetStartDate(2010, 1, 1)  # Set Start Date
        # self.SetEndDate(2023, 1, 1)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.stock = self.AddEquity("SPY", Resolution.Daily)
        self.sell_ticket = None
        self.invest = True
        self.buy_quantity = None
        self.buy_portfolio_percent = 0.1

        self.last_high_price = None
        self.initial_stop_percent = 0.90
        self.trailing_stop_increase_percent = 0.05

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        Arguments:
            data: Slice object keyed by symbol containing the stock data
        """

        # buy the stock with a market order if not invested and want to invest
        if not self.Portfolio.Invested and self.invest:
            # self.MarketOrder(self.stock.Symbol, self.buy_quantity)
            self.SetHoldings(self.stock.Symbol, self.buy_portfolio_percent)
            self.invest = False

        # when invested, create the sell stop market order
        if self.Portfolio.Invested and not self.sell_ticket:
            current_price = self.Securities[self.stock.Symbol].Close
            self.last_high_price = current_price
            # calculate stop price and round to 2 decimal places
            stop_price = round(current_price * (1 - self.initial_stop_percent), 2)

            self.sell_ticket = self.StopMarketOrder(
                self.stock.Symbol, -self.buy_quantity, stop_price
            )
            self.Debug(
                f"Created stop market order to sell {self.buy_quantity} shares of {self.stock.Symbol} at {stop_price}"
            )

        # when the sell stop market order is in place, check if need to update the stop price
        if self.sell_ticket:
            current_close_price = self.Securities[self.stock.Symbol].Close
            if current_close_price > self.last_high_price:
                self.last_high_price = current_close_price
                old_stop_price = self.sell_ticket.Get(OrderField.StopPrice)
                new_stop_price = round(
                    old_stop_price * (1 + self.trailing_stop_increase_percent), 2
                )

                self.Debug(
                    f"Updating stop price to {new_stop_price} from {old_stop_price}"
                )

                updateFields = UpdateOrderFields()
                updateFields.StopPrice = new_stop_price

                self.sell_ticket.Update(updateFields)

                response = self.sell_ticket.Update(updateFields)

                if response.IsSuccess:
                    self.Debug(f"Successfully updated stop price to {new_stop_price}")

    def OnOrderEvent(self, orderEvent):
        # log when the trailing stop order is filled
        if (
            orderEvent.Status == OrderStatus.Filled
            and self.sell_ticket
            and self.sell_ticket.OrderId == orderEvent.OrderId
        ):
            self.Debug(f"Trailing stop order filled at {orderEvent.FillPrice:.2f}")
            self.sell_ticket = None

        # log when the buy order is filled
        if orderEvent.Status == OrderStatus.Filled and orderEvent.FillQuantity > 0:
            self.buy_quantity = orderEvent.FillQuantity
            self.Debug(
                f"Purchased {orderEvent.FillQuantity} shares of {orderEvent.Symbol} at {orderEvent.FillPrice:.2f}"
            )
