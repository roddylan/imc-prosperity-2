from datamodel import OrderDepth, UserId, TradingState, Order
import numpy as np
from typing import List
import string


class Trader:
    # def __init__(self):
    #     pass

    


    def reg(self, time):
        coef = np.array([
            np.float64('-2.39500559e-04'),
            np.float64('5.00390663e+03')
        ]).reshape(-1)


        return coef[0] * time + coef[1]

        

    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
        
        MAX_POS = {"STARFRUIT": 20, "AMETHYSTS": 20}

        time = state.timestamp
        mean_sf_price = self.reg(time)
        mean_am_price = 10000.090129

        pos = state.position

        result = {}


				# Orders to be placed on exchange matching engine
        
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            acceptable_price = 10  # Participant should calculate this value
            print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
    
            if len(order_depth.sell_orders) != 0:
                # best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                # if int(best_ask) < acceptable_price:
                #     print("BUY", str(-best_ask_amount) + "x", best_ask)
                #     orders.append(Order(product, best_ask, -best_ask_amount))

                for ask, amnt in order_depth.sell_orders.items():
                    if product == "AMETHYST" and ask <= mean_am_price:
                        orders.append(Order(product, ask, min(amnt, MAX_POS[product] - amnt)))

    
            if len(order_depth.buy_orders) != 0:
                for ask, amnt in order_depth.buy_orders.items():
                    if product == "AMETHYST" and ask >= mean_am_price:
                        orders.append(Order(product, ask, -min(np.abs(pos[product]), amnt)))
                
                
                # best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                # if int(best_bid) > acceptable_price:
                #     print("SELL", str(best_bid_amount) + "x", best_bid)
                #     orders.append(Order(product, best_bid, -best_bid_amount))
            
            result[product] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData
    
    # def run(self, state: TradingState):
    #     # all trading logic
        
    #     traderData = "" # TODO: finish
        
        
    #     print(state)
    #     # pass