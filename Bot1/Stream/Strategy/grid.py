class Grid:
    def __init__(self, strategy, trade, grid):
        self.grid_data = []
        if trade.position_type=="long":
            for g in grid:
                print("l")
                size = trade.margin * g[1] / 100
                strategy.limit_order("sell", "long", size, strategy.price_with_percentage_delta(g[0]), trade=trade)
                self.grid_data.append([size, strategy.price_with_percentage_delta(g[0])])
        else:
            for g in grid:
                print("s")
                size = trade.margin * g[1] / 100
                strategy.limit_order("buy", "short", size, strategy.price_with_percentage_delta(-g[0]), trade=trade)
                self.grid_data.append([size, strategy.price_with_percentage_delta(-g[0])])
