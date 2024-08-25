import alpaca_trade_api as tradeapi
import time
import datetime
import sys
import traceback

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"

file = open(".env", 'r')
file = file.read().split("\n")
for value in file:
    value = value.split("=")
    print(value)
    if value[0] == "APCA_API_KEY_ID":
        APCA_API_KEY_ID = value[1]
    elif value[0] == 'APCA_API_BASE_URL':
        APCA_API_BASE_URL = value[1]
    elif value[0] == 'APCA_API_SECRET_KEY':
        APCA_API_SECRET_KEY = value[1]
print(APCA_API_BASE_URL, APCA_API_KEY_ID, APCA_API_SECRET_KEY)
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

def orderDet(id):
    try:
        updated_order = api.get_order(id)
        return updated_order
    except Exception as e:
        print("something went wrong", e)

def orderDetails(orderId):
    limitPrice = api.get_order(orderId)
    return limitPrice

def checkExcecution(order1, order2):
    return (order1.filled_at==None) and (order2.filled_at==None)
"""
for stock in api.list_orders(status='all', side='buy'):
    if getNeg(stock):
        if stock.symbol not in new:
            new[stock.symbol] = [stock.id]
        else:
            new[stock.symbol].append(stock.id)
continuation = []
tracker = []
for stock in new:
    flag = True
    for order in new[stock]:
        time.sleep(0.2)
        adder = {}
        pOrder = orderDet(order)
        if pOrder.legs:
            if pOrder.symbol in tracker:
                print(pOrder.symbol, pOrder.qty,"is available more than once")
            else:
                tracker.append(pOrder.symbol)
            print("obj0",pOrder.legs[0].side, pOrder.legs[0].type)
            print("obj1",pOrder.legs[1].side, pOrder.legs[1].type)
           # print(checkExcecution(pOrder.legs[0], pOrder.legs[1]))
            if getNeg(pOrder.legs[0]) and getNeg(pOrder.legs[1]) and checkExcecution(pOrder.legs[0], pOrder.legs[1]):
                #print("Order has not been excecuted", pOrder.legs[0].symbol)
                adder['buy'] = pOrder.id
                if pOrder.legs[0].side == 'sell' and pOrder.legs[0].type == 'limit':
                    adder['limit_sell'] = pOrder.legs[0].id
                if pOrder.legs[0].side == "sell" and (pOrder.legs[0].type == "stop_limit" or pOrder.legs[0].type == "stop"):
                    adder['stop_limit'] = pOrder.legs[0].id
                if pOrder.legs[1].side == 'sell' and pOrder.legs[1].type == 'limit':
                    adder['limit_sell'] = pOrder.legs[1].id
                if pOrder.legs[1].side == "sell" and (pOrder.legs[1].type == "stop_limit" or pOrder.legs[1].type == "stop"):
                    adder['stop_limit'] = pOrder.legs[1].id
                continuation.append([pOrder.symbol, pOrder.qty, adder])
            #else: print("order has been excecuted", pOrder.symbol)
            #for leg in pOrder.legs:\
print("leg 1",pOrder.legs[1])
print("leg 0", pOrder.legs[0])
'''
        if flag:
            continuation.append([pOrder.symbol, pOrder.qty])
            flag = False
        if getNeg(ChangeOrderStatus(order)) and ChangeOrderStatus(order).status!='filled':
            #print(orderDetails(order).symbol, orderDetails(order).qty, orderDetails(order).type, orderDetails(order).side, orderDetails(order).submitted_at, orderDetails(order).id)
            #print("order details", orderDetails(order))
            if pOrder.type == 'limit' and pOrder.side == 'sell':
                adder['limit_sell'] = pOrder.id
            if pOrder.side == "sell" and (pOrder.type == "stop_limit" or pOrder.type == "stop"):
                adder['stop_limit'] = pOrder.id
        if pOrder.side == "buy" and pOrder.symbol == stock and pOrder.type == 'limit':
            adder['buy'] = pOrder.id
            #print(pOrder)
    continuation[-1].append(adder)
'''
 

print(continuation)
print(len(continuation))
"""


def sellOrder(shares=4, symbol='AAPL', side='sell',type='stop_limit', limitPrice=250, stopPrice=210):
    order = api.submit_order(
        symbol=symbol,
        side=side,
        qty=shares,
        type=type,
        stop_price=stopPrice,
        limit_price=limitPrice,
        time_in_force='gtc'
    )
def putOrder():
    new = {}
    try:
        order = api.submit_order(symbol='MNTS',
                             qty=4,
                             side='buy',
                             type='limit',
                             time_in_force='gtc',
                             limit_price=250,
                             order_class='bracket',
                             stop_loss=dict(
                                 stop_price=150,
                                 # limit_price=round(stop_loss_price - 0.1,2)  # Optional: Set a limit price for the stop-loss
                             ),
                             take_profit=dict(
                                 limit_price=round((280 - (280 * 0.01)), 2),
                             )
                             )
        tries = 1
        for legs in order.legs:
            print(legs.id, legs.side, legs.order_type)
        #########################this will need some modification############################
        while True:
            time.sleep(1)
            updated_order = api.get_order(order.id)
            print("order status", updated_order.status)
            temp = order.id
            if updated_order.status != 'rejected' and updated_order.status != "canceled" and updated_order.status != 'denied':  # or updated_order.status == 'accepted':
                print("Order has been sent")
                print("Order status", updated_order.status)
                getOrderId(new, order)
                print("orderDetail for stop order",orderDet(new['Stop_limit']))
                print("new before",new)
                return 200, updated_order.id, new
            elif updated_order.status == 'rejected' or updated_order.status == 'canceled' or updated_order.status == 'denied':
                print("updated order", updated_order)
                #print("Order has been ", updated_order.status, updated_order)
                return 500, order.id, new
            if tries >= 5:
                print("issues putting the order", order.status)
                return 500, order.id, new
            if updated_order.status != 'new' and updated_order.status != "accepted" and updated_order.status != "pending_new":
                tries += 1
    except Exception as e:
        #tb = traceback.format_exc()
        return 500, "timeout"

def submitIndividualOrder(symbol, qty, side, type, time_in_force, limitPrice):
    if type == 'limit':
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type,
            limit_price=limitPrice,
            time_in_force=time_in_force
        )
    elif type == 'stop_market':
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type,
            stop_price=limitPrice,
            time_in_force=time_in_force
        )
    return order
def cancelOrder(id):
    api.cancel_order(id)
    det = orderDet(id)
    print("cancelled order details", det.status, det.limit_price, det.qty)
    return det,(float(det.limit_price) * float(det.qty))

def orderPrice(symbl):
    try:
        return api.get_latest_trade(symbl)
    except:
        return 0

def replaceOrder(orderId, qty, newLimitPrice, time_in_force='gtc'):
    order = api.replace_order(order_id = orderId, qty = qty, limit_price=newLimitPrice, time_in_force=time_in_force)
    return order

def replaceSellLimitOrder(ordersIds):
    det = orderDet(ordersIds['limitSell'])
    print(det)
    newLimitPrice = round(float(det.limit_price) -(float(det.limit_price) * 0.01), 2)
    order = replaceOrder(ordersIds['limitSell'], det.qty, newLimitPrice, time_in_force='gtc')
    #ordersIds['limitSell'] = order.id
    print(order)
    print(f"old id={det.id}\n new id={order.id}")



def getOrderId(orderIds, orders):
    try:
        for order in orders.legs:
            #print("*****************New Order deatils**********************")
            #print("orders", order)
            if order.side == "sell" and order.type == "limit":
                orderIds["limitSell"] = order.id
            elif order.side == "sell" and (order.type == "stop_limit" or order.type == "stop"):
                orderIds["Stop_limit"] = order.id
        orderIds["buy"] = orders.id
        print("found ", len(orderIds), "debug", orderIds)
    except Exception as e:
        tb = traceback.format_exc()
        print(e, tb)

#status, order, new = putOrder()

#sellOrder()


def getPrice(id, symbl):
    det = orderDet(id)
    print(det)
    priceDet = orderPrice(symbl)
    print((priceDet.price - float(det.filled_avg_price)) * float(det.filled_qty))


#getPrice('e316f8cb-cde7-4604-9b51-6d16c1577a0f', 'TSE')


stock_symbol = 'AAPL'

# Get quote for the specified stock

active_assets = api.list_assets(status='active')


print(len(active_assets))
borrow = {}
for stock in active_assets:
    if stock.easy_to_borrow:
        borrow[stock] = True
        print(stock)
        print(f"stock {stock.symbol} is easy to borrow: {stock.easy_to_borrow}")
print(len(borrow))
#for stock in active_assets:
    #print(stock.symbol)
# Check if the stock is easy to borrow
#is_easy_to_borrow = quote.easy_to_borrow

#if is_easy_to_borrow:
 #   print(f"{stock_symbol} is easy to borrow.")
#else:
 #   print(f"{stock_symbol} is not easy to borrow.")