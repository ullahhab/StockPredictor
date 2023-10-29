import random
import tkinter as tk


weeks = 158
Sum = 1690
estimator = 0
for i in range(1, weeks):
    rand = random.randint(1, 8)
    rand = rand/100
    rand = 0.08
    estimator += rand
    if i%2==0:
        Sum+=845
    Sum *= (1+rand)

print("total sum", Sum)
print("avg percentage", (estimator/(weeks-1)) *100 )

paidOptions = [
    'bi-weekly',
    'Montly',
    'weekly',
    'bi-monthly'
    ]


calculator = tk.Tk()

def calculate():
    weeks = 105
    Sum = 1690
    estimator = 0
    for i in range(1, weeks*2):
        rand = random.randint(1, 8)
        rand = rand/100
        estimator += rand
        if i%2==0:
            Sum+=845
        Sum *= (1+rand)
    if Sum//1000000:
        print((Sum/1000000), "M", "avg percentage= " ,(estimator/(((weeks*2)-1))*100))
    else:
        print(Sum, "avg percentage= " ,(estimator/(((weeks*2)-1))*100))
    #print(T1.get("1.0","end-1c"), T2.get("1.0","end-1c"), drop.get())
    popup = tk.Toplevel(calculator)
    popup.geometry("550x250")
    popup.title("Total sum in "+str(weeks*2)+" weeks")
    tk.Label(popup, text = str(Sum/1000000)+"Million avg perctage = "+str(estimator/(((weeks*2)-1))*100), font=('Helvetica 18 bold')).place(x=150,y=80)

        
calculator.geometry('250x125')
label = tk.Label(calculator, text="years").grid(row=1, column=0)
label = tk.Label(calculator, text="").grid(row=1, column=1)
label = tk.Label(calculator, text="").grid(row=1, column=2)
T1 = tk.Text(calculator, height=1, width = 8).grid(row=1, column=3)

clicked = tk.StringVar()
label = tk.Label(calculator, text="paid ").grid(row=2, column=0)
label = tk.Label(calculator, text="").grid(row=2, column=1)
label = tk.Label(calculator, text="").grid(row=2, column=2)
drop = tk.OptionMenu(calculator, clicked, *paidOptions).grid(row=2, column = 3)

label = tk.Label(calculator, text="Pay Period Amount").grid(row=3, column=0)
label = tk.Label(calculator, text="").grid(row=3, column=1)
label = tk.Label(calculator, text="").grid(row=3, column=2)
T2 = tk.Text(calculator, height=1, width = 8).grid(row=3, column=3)

label = tk.Label(calculator, text="weekly Percentage").grid(row=4, column=0)
label = tk.Label(calculator, text="").grid(row=4, column=1)
label = tk.Label(calculator, text="").grid(row=4, column=2)
T3 = tk.Text(calculator, height=1, width = 8).grid(row=4, column=3)


submit = tk.Button(calculator, text="submit", command=calculate).grid(row=6, column=0)



calculator.mainloop()





