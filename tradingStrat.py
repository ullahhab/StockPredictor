def strat(money):
    ret = []
    while money>1:
        if money//10000:
            money -= 10000
            ret.append(10000)
        elif money//1000:
            money -= 1000
            ret.append(1000)
        elif money//100:
            money -= 100
            ret.append(100)
        elif money<100 and money>0:
            ret.append(money)
            money-=money
    return ret
