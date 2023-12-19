import alpaca_trade_api as tradeapi
import time
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
APCA_API_KEY_ID = "PK4OKCEX7MBY9ZQ1XGGE"
APCA_API_SECRET_KEY = "HUcCIfdfRh7IOaWcyKA9GBwu4irO6umTvDzhHnU2"


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
                                limit_price=take_profit_price,
                            )
                        )
    tries = 1
    while True:
        time.sleep(10)
        updated_order = api.get_order(order.id)
        if updated_order.status == 'filled' or updated_order.status == 'accepted':
            print("Order has been excecuted")
            print("Making sure the sell order has been put", "before =", order.id)

            while True:
                for order in api.list_orders():
                    print(f"Order ID: {order.id}")
                    print(f"Symbol: {order.symbol}")
                    print(f"Quantity: {order.qty}")
                    print(f"Side: {order.side}")
                    print(f"Type: {order.type}")
                    print(f"Status: {order.status}")
                    print(f"Limit Price: {order.limit_price}")
                    print(f"Stop Price: {order.stop_price}")
                    print(f"Filled Qty: {order.filled_qty}")
                    print(f"Submitted At: {order.submitted_at}")
                    if order.side == "sell" and order.symbol == symbol and order.type == "limit":
                        break
                if order.side == "sell" and order.symbol == symbol and order.type == "limit":
                    break
            print("sell has been put with ID", "after =", order.id)
            return 200, order.id
        elif updated_order.status == 'rejected' or updated_order.status == 'canceled':
            print("Order has been rejected")
            return 500, order.id
        if tries >=5:
            print("issues putting the order")
            return 500, order.id
        if updated_order.status != 'new':
            tries+=1
        
def ChangeOrderStatus(id):
    updated_order = api.get_order(id)
    print(updated_order.status)
    if updated_order.status == 'filled':
        #Change the files
        return True
    return False


