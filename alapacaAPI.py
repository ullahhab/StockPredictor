import alpaca_trade_api as tradeapi
import time
import datetime
import traceback

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"


api = ""


def limitTakeProfitStopLoss(symbol, qty, limit, stop_loss_price, take_profit_price):
    orderIds = {}
    try:
        order = api.submit_order(symbol=symbol,
                             qty=qty,
                             side='buy',
                             type='limit',
                             time_in_force='gtc',
                             limit_price=limit,
                             order_class='bracket',
                             stop_loss=dict(
                                 stop_price=stop_loss_price,
                                 # limit_price=round(stop_loss_price - 0.1,2)  # Optional: Set a limit price for the stop-loss
                             ),
                             take_profit=dict(
                                 limit_price=round((take_profit_price - (take_profit_price * 0.01)), 2),
                             )
                             )
        tries = 1
        #########################this will need some modification############################
        while True:
            time.sleep(10)
            updated_order = api.get_order(order.id)
            print("order status", updated_order.status)
            temp = order.id
            if updated_order.status != 'rejected' and updated_order.status != "canceled" and updated_order.status != 'denied':  # or updated_order.status == 'accepted':
                print("Order has been sent")
                print("Order status", updated_order.status)
                getOrderId(orderIds, order)
                return 200, orderIds
            elif updated_order.status == 'rejected' or updated_order.status == 'canceled' or updated_order.status == 'denied':
                print("updated order", updated_order)
                #print("Order has been ", updated_order.status, updated_order)
                return 500, orderIds
            if tries >= 5:
                print("issues putting the order", order.status)
                return 500, orderIds
            if updated_order.status != 'new' and updated_order.status != "accepted" and updated_order.status != "pending_new":
                tries += 1
    except Exception as e:
        tb = traceback.format_exc()
        print("trace", tb, "error", e)
        return 500, "timeout"
        


def ChangeOrderStatus(id):
    try:
        updated_order = api.get_order(id)
        return updated_order.status
    except:
        return "unknown"

def getOrderId(orderIds, orders):
    try:
        for order in orders.legs:
            if order.side == "sell" and order.type == "limit":
                orderIds["limitSell"] = order.id
            elif order.side == "sell" and (order.type == "stop_limit" or order.type == "stop"):
                orderIds["Stop_limit"] = order.id
        orderIds["buy"] = orders.id
    except Exception as e:
        tb = traceback.format_exc()
        print(e, tb)


def LookForOrderId(stock, lst):
    orderIds = {}
    try:
        while len(orderIds)<3:
            for order in api.list_orders(status='all'):
                if order.status != 'canceled' and order.status != 'rejected' and order.status!= 'filled' and order.status != 'replaced':
                    if order.side == "sell" and order.symbol == stock and order.type == "limit":
                        orderIds["limitSell"] = order.id
                    elif order.side == "sell" and order.symbol == stock and (order.type == "stop_limit" or order.type == "stop"):
                        orderIds["Stop_limit"] = order.id
                if order.side == "buy" and order.symbol == stock and order.type == 'limit':
                    orderIds["buy"] = order.id
        lst.append(orderIds)
    except Exception as e:
        pass


def getNeg(order):
    try:
        if (order.status != "replaced") and (order.status != "pending_replaced") and (order.status != "pending_cancel") and (order.status != "canceled") and (order.status != "expired"):
            return True
        return False
    except:
        return False
    



def orderLimitPriceDetails(orderId):
    try:
        limitPrice = api.get_order(orderId).limit_price
        return float(limitPrice)
    except:
        return 0

def accountValue():
    try:
        return api.get_account().equity
    except:
        return 0

def orderPrice(symbl):
    try:
        return float(api.get_latest_trade(symbl).price)
    except:
        return 0

def getBuyOrderPrice(orderId):
    try:
        return float(api.get_order(orderId).filled_avg_price)
    except:
        return 0

def orderDet(id):
    try:
        updated_order = api.get_order(id)
        return updated_order
    except Exception as e:
        print("something went wrong", e)

def cancelOrder(id):
    det = orderDet(id)
    try:
        api.cancel_order(id)
        det = orderDet(id)
        return det,(float(det.limit_price) * float(det.qty))
    except:
        return det 
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

def setSecret(key, secret, baseURL):
    global api
    APCA_API_BASE_URL = baseURL
    api = tradeapi.REST(key_id=key, secret_key=secret,
                    base_url=APCA_API_BASE_URL, api_version='v2')
#instead send the orders dictionay:
'''
TODO:
    1. update the time stamp here
    2. update to include time stamp in orderIds

def replaceSellOrder(ordersIds):
    det = cancelOrder(ordersIds['limitSell'])[0] #item 0 is detail of the order, 2 is the money it for cancelling it
    newLimitPrice = round(float(det.limit_price) -(float(det.limit_price) * 0.01), 2)
    stopOrderId = ordersIds['Stop_limit']
    stopOrder = orderDet(stopOrderId)
    if(stopOrder.status != 'cancelled'):
        api.cancel_order(stopOrderId)
    stopPrice = stopOrder.stop_price
    limitOrder = submitIndividualOrder(det.symbol,det.qty, 'sell', 'limit','gtc',newLimitPrice)
    if limitOrder.status != 'rejected' and limitOrder.status != "canceled" and limitOrder.status != 'denied':
        ordersIds['LimitSell'] = limitOrder.id
    else:
        return
    stopOrder = submitIndividualOrder(det.symbol, det.qty,'sell', 'stop_market', 'gtc', stopPrice)
    if stopOrder.status != 'rejected' and stopOrder.status != "canceled" and stopOrder.status != 'denied':
        ordersIds['Stop_limit'] = stopOrder.id
    else:
        return
    '''
def replaceOrder(orderId, qty, newLimitPrice, time_in_force='gtc'):
    order = api.replace_order(order_id = orderId, qty = qty, limit_price=newLimitPrice, time_in_force=time_in_force)
    return order

def replaceSellLimitOrder(ordersIds):
    det = orderDet(ordersIds['limitSell'])
    newLimitPrice = round(float(det.limit_price) -(float(det.limit_price) * 0.01), 2)
    order = replaceOrder(ordersIds['limitSell'], det.qty, newLimitPrice, time_in_force='gtc')
    ordersIds['limitSell'] = order.id
    time.sleep(1)


def getOrderPriceDetails(orderIds):
    buy = orderDet(orderIds['buy'])
    sell = orderDet(orderIds['limitSell'])
    stopLoss = orderDet(orderIds['Stop_limit'])

    if buy.status == 'filled':
        limitPrice = float(buy.filled_avg_price)
    else:
        limitPrice = float(buy.limit_price)
    symbol = buy.symbol
    share = float(buy.qty)
    sellPrice = float(sell.limit_price)
    stopLossPrice = float(stopLoss.stop_price)
    ordPrice = orderPrice(symbol)

    print(f'Stock={symbol} prices buy={limitPrice} sell price={sellPrice} current={ordPrice} stop loss={stopLossPrice} profit/loss={float(share)*(ordPrice-limitPrice)}')


def calculateMoney(orderId):
    det = orderDet(orderId)
    if 'cancel' in det.status:
        return float(det.limit_price)* float(det.qty), True
    return float(det.filled_avg_price) * float(det.filled_qty), det.filled_qty == det.qty

"""Exclude flag will maintain it's own existance. Exclude is the status that will result in any status that is not in the array otherwise true however if you provide 
that flag and do not provide list it will result in true or false for other logic"""
def orderStatus(orderId=None, 
                status="",
                exclude=False,
                stat=""
                ):
    if status.__class__ == list:
        if orderId:
            det = orderDet(orderId)
            stat = det.status
        if exclude:
            return stat not in status
        else:
            return stat in status
    else:
        #TODO: DO something with the data
        return det.status == status






    




