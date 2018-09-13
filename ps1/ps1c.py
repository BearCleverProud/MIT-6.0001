annual_salary=float(input("Enter the starting salary:"))
annual_salary_saved=annual_salary
total_cost=1000000.0
semi_annual_raise=0.07
portion_down_payment=0.25
current_savings=0.0
r=0.04
month=0
down_payment=total_cost*portion_down_payment
best_saving=6180
max_saving=10000
min_saving=0
best_saving_rate=float(best_saving)/10000

while month<36:
    current_savings+=annual_salary/12+current_savings*r/12
    month+=1
    if month%6==0:
        annual_salary+=annual_salary*semi_annual_raise
if current_savings<down_payment:
    print("It is not possible to pay the down payment in three years.")
else:
    step=0
    while abs(current_savings-down_payment)>100:
        annual_salary=annual_salary_saved
        current_savings=0
        step+=1
        month=0
        while month<36:
            current_savings+=annual_salary*best_saving_rate/12+current_savings*r/12
            month+=1
            if month%6==0:
                annual_salary+=annual_salary*semi_annual_raise
        if current_savings>down_payment:
            max_saving=best_saving
            best_saving=(best_saving+min_saving)//2
        else:
            min_saving=best_saving
            best_saving=(best_saving+max_saving)//2
        best_saving_rate=float(best_saving)/10000
    print("Best saving rate:"+str(float(best_saving)/10000))
    print("Steps in bisection search:"+str(step))
