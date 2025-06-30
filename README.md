# 2025-Spring-Principles-of-Financial-Computing

This repo is about the assignments of NTU Principles of Financial Computing 113-2.

## Assignment 1
### Problem Description:
```
Write a program to analyze bond investment financing through a loan. Consider an n-year, V1-dollar loan charging an annual interest rate of r1 (the repayment schedule is by amortization), and an n-year level-coupon bond with a par value of V2 and paying an annual interest rate of r2, where r1 < r2. TA holds C dollars in cash, and intends to take out the loan to purchase the bond. The total sum of cash and loan proceeds will be fully invested in the bond (V1 + C = V2). In addition, TA aims to ensure that the payments for the loan (principal and interest) do not exceed the bond (interest) throughout the investment period. Note that V1 and V2 are integers, and payments and interests should be rounded to six decimal places. Inputs:
C: cash in TA's hand;
n: time to maturity of the loan and bond in years, an integer;
m: the number of payments per annum, an integer;
r1: annual interest rate of the loan, compounded m times per year;
r2: annual interest rate of the bond, compounded m times per year.
Outputs:
The maximum loan amount (V1, an integer) that TA can apply for balanced payments (the following outputs are with V1 of the maximum loan amount);
Total interest paid on the loan (rounded to six decimal places);
Total interest received from the bond (rounded to six decimal places);
Annualized internal rate of return of the investment (rounded to six decimal places).
For example, if C = 10000, n = 2, m = 12, r1 = 0.018, r2 = 0.045, the outputs are 968, 18.254282, 987.120000, and 0.046329. Input Format (for Python codes, replace the student ID with uppercase): "python3 F08922011_HW_1.py 10000 2 12 0.018 0.045". Output Format: "968, 18.254282, 987.120000, 0.046329". 
```
---

## Assignment 2
### Problem Description:
```
Write a binomial tree program to price Bermudan options, where early exercise is only allowed on specific dates. Inputs:
S: stock price;
X: strike price;
r: continuously compounded annual interest rate;
s: annual volatility;
T: time to maturity in days, which is an integer and also an exercise date;
m: number of periods per day for the tree, an integer;
E: early exercise dates from now, a list of integers.
Output: The prices of the Bermudan put option and the Bermudan call option. For example, if S = 100, X = 110, r = 0.03, s = 0.3, T = 60, m = 5, and E = 10, 20, 30, 40, 50, the example outputs are 11.248139 and 1.687963. Input Format (for Python codes, replace your student ID with uppercase): "python3 F08922011_HW_2.py 100 110 0.03 0.3 60 5 10 20 30 40 50". Output Format: "11.248139, 1.687963". 
```
---

## Assignment 3
### Problem Description:
```
Write a binomial tree program to price up-and-out and up-and-in barrier options. Note that the binomial tree may not align exactly with the barrier. Adjust the barrier by rounding it up to the nearest tree level. Inputs:
S: stock price;
X: strike price;
r: continuously compounded annual interest rate;
s: annual volatility;
T: time to maturity in days, which is an integer, and there are 365 days in a year;
H: up-and-out barrier, where H > S and H > X;
n: number of time steps in T, which is an integer.
Output:
The price of the up-and-out barrier call option.
The price of the up-and-out barrier put option.
The price of the up-and-in barrier call option.
The price of the up-and-in barrier put option.
For example, if S = 100, X = 110, r = 0.03, s = 0.3, T = 60, H = 120, and n = 100, the outputs are 0.311069, 11.083348, 1.370665, and 0.057256. Input Format (for Python codes, replace your student ID with uppercase): "python3 F08922011_HW_3.py 100 110 0.03 0.3 60 120 100". Output Format: "0.311069, 11.083348, 1.370665, 0.057256". 
```
---
## Assignment 4
### Problem Description:
```
Write a binomial-trinomial tree program to price double-barrier options. Note that the tree must match the barriers. Inputs:
S: stock price;
X: strike price;
r: continuously compounded annual interest rate;
s: annual volatility;
T: time to maturity in days, which is an integer, and there are 365 days in a year;
H: up-and-out barrier, where H > S and H > X;
L: down-and-out barrier, where L < S and L < X;
k: 2k represents the number of up steps from L to H, and is an integer as shown on page 776 of the course slides.
Output:
The price of the double-barrier barrier call option.
The delta of the double-barrier barrier call option (caluclated by S × 1.01 and S × 0.99).
The price of the double-barrier barrier put option.
The delta of the double-barrier barrier put option (caluclated by S × 1.01 and S × 0.99).
For example, if S = 95, X = 100, r = 0.10, s = 0.25, T = 365, H = 140, L = 90, and k = 50, the example outputs are 1.457183, 0.253302, 0.040884, and 0.007052. Input Format (for Python codes, replace your student ID with uppercase): "python3 F08922011_HW_4.py 95 100 0.10 0.25 365 140 90 50". Output Format: "1.457183, 0.253302, 0.040884, 0.007052". 
```
