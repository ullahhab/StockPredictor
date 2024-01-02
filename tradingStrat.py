def strat(money):
    if money > 100 and money<=1000:
        return money//100
    elif money < 100:
        return 1
    elif money > 1000 and money<=10000:
        return money//1000
    elif money > 10000 and money<100000:
        return money//10000
    else:
        return money//1000
    
