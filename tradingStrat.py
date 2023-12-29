def strat(money):
    if money > 100 and money<=1000:
        return money//100
    elif money > 1000 and money<=10000:
        return money//1000
    else:
        money//10000
