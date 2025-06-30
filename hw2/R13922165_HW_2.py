import sys
import math

def bermudan_option_price(S, X, r, sigma, T_days, m, E):

    # T denote the time to expiration of the option measured in years
    T = T_days / 365.0
    # Total time steps
    N = T_days * m 
    # It means each period is delta t years long
    dt = T / N

    # u*d = 1 (To make nodes at the same horizontal level of the tree hvae identical price)
    # By page 299, Let u = e^(sigma*((delta t)^(1/2)))
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    
    # The period gross return R is e^(r*dt)
    # The pseudo probability p = (R - d) / (u - d)
    p = (math.exp(r * dt) - d) / (u - d)
    discount = math.exp(-r * dt)

    # Convert early exercise days to step indices
    early_exercise_steps = set(e * m for e in E)

    # Initialize asset prices at maturity
    asset_prices = [S * (u ** i) * (d ** (N - i)) for i in range(N + 1)]

    # Initialize option values at maturity
    call_values = [max(0, asset_prices[i] - X) for i in range(N + 1)]
    put_values = [max(0, X - asset_prices[i]) for i in range(N + 1)]

    # Backward Induction
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            asset_price = S * (u ** j) * (d ** (i - j))
            call_hold = discount * (p * call_values[j+1] + (1 - p) * call_values[j])
            put_hold = discount * (p * put_values[j+1] + (1 - p) * put_values[j])
            
            if i in early_exercise_steps:
                call_values[j] = max(call_hold, asset_price - X)
                put_values[j] = max(put_hold, X - asset_price)
            else:
                call_values[j] = call_hold
                put_values[j] = put_hold

    return round(put_values[0], 6), round(call_values[0], 6)

if __name__ == '__main__':
    args = sys.argv[1:]
    S = float(args[0])
    X = float(args[1])
    r = float(args[2])
    sigma = float(args[3])
    T_days = int(args[4])
    m = int(args[5])
    E = list(map(int, args[6:]))

    put, call = bermudan_option_price(S, X, r, sigma, T_days, m, E)
    print(f"{put}, {call}")
