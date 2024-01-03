def strat(money):
    if money <= 0:
        return 0
    elif money < 100:
        return 1
    elif money > 10000 and money<100000:
        return int(money//10000)
    elif money > 1000 and money<=10000:
        return int(money//1000)
    elif money > 100 and money<=1000:
        return int(money//100)
    else:
        return money//1000
    
