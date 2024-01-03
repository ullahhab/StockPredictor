import alpaca_trade_api as tradeapi
import time
import datetime
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
APCA_API_KEY_ID = "PKD8V1TQWBUDC69ELWKM"
APCA_API_SECRET_KEY = "xE1m8nLhVrOPZK1aFmVpSyrouyhWh8iwb9D2XgX8"


api = tradeapi.REST(key_id=APCA_API_KEY_ID, secret_key=APCA_API_SECRET_KEY, 
                    base_url=APCA_API_BASE_URL, api_version='v2')


def limitTakeProfitStopLoss(symbol, qty, limit, stop_loss_price, take_profit_price):
    
    order = api.submit_order(symbol=symbol,
                            qty= qty,
                            side = 'buy',
                            type='limit',
                            time_in_force='gtc',
                            limit_price=limit,
                            order_class='bracket',
                            stop_loss=dict(
                                stop_price=stop_loss_price,
                                limit_price=round(stop_loss_price - 0.1,2)  # Optional: Set a limit price for the stop-loss
                            ),
                            take_profit=dict(
                                limit_price=round((take_profit_price - (take_profit_price *0.01)), 2),
                            )
                        )
    tries = 1
    #########################this will need some modification############################
    while True:
        time.sleep(10)
        updated_order = api.get_order(order.id)
        temp = order.id
        if updated_order.status != 'rejected' and updated_order.status != "canceled": #or updated_order.status == 'accepted':
            print("Order has been sent")
            print("Order status", updated_order.status)
            return 200, updated_order.id
        elif updated_order.status == 'rejected' or updated_order.status == 'canceled':
            print("Order has been ", updated_order.status)
            return 500, order.id
        if tries >=5:
            print("issues putting the order", order.status)
            return 500, order.id
        if updated_order.status != 'new' and updated_order.status != "accepted" and updated_order.status != "pending_new":
            tries+=1
        
def ChangeOrderStatus(id):
    updated_order = api.get_order(id)
    print(updated_order.status)
        #Change the files
    return updated_order.status


def getOrderId(stock, lst):
    orderIds = {}
    while len(orderIds)<2:
        print("looking for orders: Found =", len(orderIds))
        for order in api.list_orders(status='all'):
            if order.status != 'canceled' and order.status != 'rejected' and order.status!= 'filled' and order.status != 'replaced':
                if order.side == "sell" and order.symbol == stock and order.type == "limit":
                    orderIds["limitSell"] = order.id
                elif order.side == "sell" and order.symbol == stock and order.type == "stop_limit":
                    orderIds["Stop_limit"] = order.id
    
    lst.append(orderIds)
for order in api.list_orders(status='all'):
    if order.status != 'canceled' and order.status != 'rejected' and order.status!= 'filled' and order.status != 'replaced':
        print(f"Order ID: {order.id}")
        print(f"Symbol: {order.symbol}")
        print(f"Qty: {order.qty}")
        print(f"Side: {order.side}")
        print(f"Type: {order.type}")
        print(f"Status: {order.status}")
        print("------")


def getNeg(order):
    if (order.status!= "replaced") and (order.status!= "pending_replaced") and (order.status!= "pending_cancel") and (order.status!= "canceled") and (order.status!= "expired"):
        return True
    return False

def orderDetails(symbl, orderId):
    order = api.get_latest_trade(symbl)
    limitPrice = api.get_order(orderId).limit_price
    return order.price, limitPrice
