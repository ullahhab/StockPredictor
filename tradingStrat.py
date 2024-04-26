def strat(money):
    ret = []
    while money>0:
        if money//10000:
            money -= 10000
            ret.append(10000)
        if money//1000:
            money -= 1000
            ret.append(1000)
        if money//100:
            money -= 100
            ret.append(100)
        if money<100 and money>0:
            ret.append(money)
            money-=money
    test=0
    return ret
