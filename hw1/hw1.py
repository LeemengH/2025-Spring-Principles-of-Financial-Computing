import sys

input_list = sys.argv

# Parameter definition
C = float(input_list[1])
n = int(input_list[2])
m = int(input_list[3])
r1 = float(input_list[4])
r2 = float(input_list[5])

compounded_r1 = r1 / m
compounded_r2 = r2 / m
compounded_times = n*m


# Step1
a1 = compounded_r1/(1 - (1 + compounded_r1)**(-1*compounded_times))
V1 = int(compounded_r2*C / (a1 - compounded_r2))

# Step2
Total_interest_paid = V1*(a1*compounded_times - 1)
Total_interest_received = (C + V1)*(r2*n)

# Step3
fv = C + Total_interest_received - Total_interest_paid
pv = C
Annualized_IRR = ((fv / pv)**(1/compounded_times) - 1)*m

# Step4
print(str(V1)+", "+str(format(round(Total_interest_paid, 6), '.6f'))+", "
	+str(format(round(Total_interest_received, 6), '.6f'))+", "+
	str(format(round(Annualized_IRR, 6), '.6f')))