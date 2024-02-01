import alpaca_trade_api as tradeapi
import time
import datetime
import sys

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
APCA_API_KEY_ID = "PK7L6LK63UD41XRYVRQV"
APCA_API_SECRET_KEY = "FyMslIcTvjIYm8Mtzcw4NcLglTHbnOsnb3MK8AdF"

def getNeg(order):
    if (order.status!= "replaced") and (order.status!= "pending_replaced") and (order.status!= "pending_cancel") and (order.status!= "canceled") and (order.status!= "expired"):
        return True
    return False

def ChangeOrderStatus(id):
    updated_order = api.get_order(id)
    return updated_order

api = tradeapi.REST(key_id=APCA_API_KEY_ID, secret_key=APCA_API_SECRET_KEY, 
                    base_url=APCA_API_BASE_URL, api_version='v2')


new = {}

def orderDetails(orderId):
    limitPrice = api.get_order(orderId)
    return limitPrice

for stock in api.list_orders(status='all'):
    if getNeg(stock) and stock.status!='filled':
        print(stock.symbol, stock.status)
        if stock.symbol not in new:
            new[stock.symbol] = [stock.id]
        else:
            new[stock.symbol].append(stock.id)

print(new)
continuation = []
for stock in new:
    adder = {}
    flag = True
    for order in new[stock]:
        time.sleep(1)
        pOrder = orderDetails(order)
        if flag:
            continuation.append([pOrder.symbol, pOrder.qty])
            flag = False
        if getNeg(ChangeOrderStatus(order)) and ChangeOrderStatus(order).status!='filled':
            #print(orderDetails(order).symbol, orderDetails(order).qty, orderDetails(order).type, orderDetails(order).side, orderDetails(order).submitted_at, orderDetails(order).id)
            print("order details", orderDetails(order))
            if pOrder.type == 'limit' and pOrder.side == 'sell':
                adder['limit_sell'] = pOrder.id
            elif pOrder.side == "sell" and (pOrder.type == "stop_limit" or pOrder.type == "stop"):
                adder['stop_limit'] = pOrder.id
        elif pOrder.side == "buy" and pOrder.symbol == stock:
            adder['buy'] = pOrder.id
        continuation[-1].append(adder) 
                

print(continuation)


