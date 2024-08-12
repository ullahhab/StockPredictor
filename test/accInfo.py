import alpaca_trade_api as tradeapi
import time
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
APCA_API_KEY_ID = "PKN5KAP9WG3MS8OIDJM9"
APCA_API_SECRET_KEY = "TGvgTmfN6butL9pieJqDZyrCEulbF91YLScXZuF5"


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
        time.sleep(5)
        updated_order = api.get_order(order.id)
        print(updated_order.status)
        if updated_order.status == 'filled':
            return 200
        else:
            return 500

def ChangeOrderStatus(id):
    updated_order = api.get_order(id)
    return updated_order

def getAccInfo():
    account = api.get_account()

# Print account details
    print(f"Account ID: {account.id}")
    print(f"Status: {account.status}")
    print(f"Buying Power: {account.buying_power}")
    print(f"Equity: {account.equity}")
    print(f"Cash: {account.cash}")


#getAccInfo()
order = ChangeOrderStatus("1591df23-2996-4464-b2e2-219a6326a724")
print(order.limit_price, order.qty)