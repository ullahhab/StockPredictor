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
                                limit_price=stop_loss_price - 0.1,  # Optional: Set a limit price for the stop-loss
                            ),
                            take_profit=dict(
                                limit_price=take_profit_price,
                            )
                        )
    while True:
        time.sleep(1)
        updated_order = api.get_order(order.id)
        print(updated_order.status)
        if updated_order.status == 'filled' or updated_order.status == 'accepted':
            return 200
        else:
            return 500
def ChangeOrderStatus(id):
    updated_order = api.get_order(id)
    print(updated_order.status)
    if updated_order.status == 'filled':
        #Change the files
        pass


