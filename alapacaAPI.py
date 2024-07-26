import alpaca_trade_api as tradeapi
import time
import datetime

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
#APCA_API_KEY_ID = ""  # "PK7L6LK63UD41XRYVRQV"
#APCA_API_SECRET_KEY = ""  # "FyMslIcTvjIYm8Mtzcw4NcLglTHbnOsnb3MK8AdF"

api = ""


def limitTakeProfitStopLoss(symbol, qty, limit, stop_loss_price, take_profit_price):
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
                return 200, updated_order.id
            elif updated_order.status == 'rejected' or updated_order.status == 'canceled' or updated_order.status == 'denied':
                print("updated order", updated_order)
                #print("Order has been ", updated_order.status, updated_order)
                return 500, order.id
            if tries >= 5:
                print("issues putting the order", order.status)
                return 500, order.id
            if updated_order.status != 'new' and updated_order.status != "accepted" and updated_order.status != "pending_new":
                tries += 1
    except Exception as e: 
        print("Something bad happened\n reason:", e)
        return 500, "timeout"
        


def ChangeOrderStatus(id):
    try:
        updated_order = api.get_order(id)
        return updated_order.status
    except:
        return "unknown"


def getOrderId(stock, lst):
    orderIds = {}
    try:
        while len(orderIds)<3:
            print("looking for orders: Found =", len(orderIds))
            for order in api.list_orders(status='all'):
                if order.status != 'canceled' and order.status != 'rejected' and order.status!= 'filled' and order.status != 'replaced':
                    if order.side == "sell" and order.symbol == stock and order.type == "limit":
                        orderIds["limitSell"] = order.id
                    elif order.side == "sell" and order.symbol == stock and (order.type == "stop_limit" or order.type == "stop"):
                        orderIds["Stop_limit"] = order.id
                if order.side == "buy" and order.symbol == stock and order.type == 'limit':
                    orderIds["buy"] = order.id
        print("found ", len(orderIds), "debug", orderIds)
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
    



def orderDetails(symbl, orderId):
    try:
        order = api.get_latest_trade(symbl)
        limitPrice = api.get_order(orderId).limit_price
        return order.price, limitPrice
    except:
        return 0, 0

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

def getBuyOrder(orderId):
    try:
        return float(api.get_order(orderId).limit_price)
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
    api.cancel_order(id)
    return det.limit_price * det.shares
     

def setSecret(key, secret, baseURL):
    global api
    APCA_API_BASE_URL = baseURL
    api = tradeapi.REST(key_id=key, secret_key=secret,
                    base_url=APCA_API_BASE_URL, api_version='v2')
