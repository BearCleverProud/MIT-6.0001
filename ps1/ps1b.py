annual_salary=float(input("Enter your annual_salary:"))
portion_saved=float(input("Enter the percent of your salary to save, as a decimal:"))
total_cost=float(input("Enter the cost of your dream home:"))
semi_annual_raise=float(input("Enter the semi-annual raise, as a decimal:"))
portion_down_payment=0.25
current_savings=0.0
r=0.04
month=0
down_payment=total_cost*portion_down_payment

while current_savings<down_payment:
    current_savings+=annual_salary*portion_saved/12+current_savings*r/12
    month+=1
    if month%6==0:
        annual_salary+=annual_salary*semi_annual_raise

print("Number of months:"+str(month))
