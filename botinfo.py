def seperate(value):
    return value.split("=")[1].strip(" ")


file = open('botinfo.txt', 'w')
file.write("bought = True\nstockBought ="+str(0)+"\nbuyPrice =" +str(0)+"\nsellPrice ="+str(0)+"\nshares ="+str(0)+"\nmoney ="+str(0)+"\nvalue ="+"0"+'\n')
file.close()


