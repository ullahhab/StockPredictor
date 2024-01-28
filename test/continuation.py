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
            array = [pOrder.symbol, pOrder.qty]
            flag = False
        if getNeg(ChangeOrderStatus(order)) and ChangeOrderStatus(order).status!='filled':
            print(orderDetails(order).symbol, orderDetails(order).qty, orderDetails(order).type, orderDetails(order).side, orderDetails(order).submitted_at, orderDetails(order).id)
            if pOrder.type == 'limit' and pOrder.side == 'sell':
                adder['limit_sell'] = pOrder.id
            elif pOrder.side == "sell" and (pOrder.type == "stop_limit" or pOrder.type == "stop"):
                adder['stop_limit'] = pOrder.id
    array.append(adder)
    continuation.append(array)
for stock in continuation:
            for order in api.list_orders(status='all'):
                if order.symbol == stock[0] and order.qty == stock[1] and order.type == 'limit' and order.side == 'buy':
                    stock[2]['buy'] = order.id 
#final processing
                    #Problem adding multiple orders with same array
pArray = []
for stock in range(len(continuation)):
    while len(continuation[stock])>3:
        #pArray.append([stock[0], stock[1], stock.pop()])
        continuation[stock].pop()

print(continuation)

