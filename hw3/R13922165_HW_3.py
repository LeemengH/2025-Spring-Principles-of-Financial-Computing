import sys
import math

def binomial_barrier_option(S, X, r, sigma, T_days, H, n):
    """Step1: Preprocessing & Tree Parameters"""
    T = T_days / 365.0
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt)) # Up factor
    d = 1 / u                           # Down factor (to maintain recombining tree)
    p = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)

    def build_tree(is_call, is_up_and_out):
        option_tree = [[0.0 for _ in range(i + 1)] for i in range(n + 1)]
        stock_tree = [[0.0 for _ in range(i + 1)] for i in range(n + 1)]

        """Step2: Build the Tree"""
        # Build stock price tree and option values at maturity
        for i in range(n + 1):
            for j in range(i + 1):
                stock_tree[i][j] = S * (u ** j) * (d ** (i - j))

        """Step3: Terminal Payoff (at maturity)"""
        for j in range(n + 1):
            stock_price = stock_tree[n][j]
            if stock_price >= H:
                option_tree[n][j] = 0.0 if is_up_and_out else max(0.0, (stock_price - X) if is_call else (X - stock_price))
            else:
                option_tree[n][j] = max(0.0, (stock_price - X) if is_call else (X - stock_price))

        """Step4: Backward Induction"""
        for i in range(n - 1, -1, -1):
            for j in range(i + 1):
                stock_price = stock_tree[i][j]
                if stock_price >= H:
                    option_tree[i][j] = 0.0 if is_up_and_out else disc * (p * option_tree[i + 1][j + 1] + (1 - p) * option_tree[i + 1][j])
                else:
                    option_tree[i][j] = disc * (p * option_tree[i + 1][j + 1] + (1 - p) * option_tree[i + 1][j])

        return option_tree[0][0]

    # Up-and-out
    up_out_call = build_tree(is_call=True, is_up_and_out=True)
    up_out_put = build_tree(is_call=False, is_up_and_out=True)

    # Vanilla options
    vanilla_call = build_tree(is_call=True, is_up_and_out=False)
    vanilla_put = build_tree(is_call=False, is_up_and_out=False)

    # Up-and-in = vanilla - up-and-out
    up_in_call = vanilla_call - up_out_call
    up_in_put = vanilla_put - up_out_put

    return up_out_call, up_out_put, up_in_call, up_in_put


if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python3 R13922165_HW_3.py S X r sigma T H n")
        sys.exit(1)

    S = float(sys.argv[1])
    X = float(sys.argv[2])
    r = float(sys.argv[3])
    sigma = float(sys.argv[4])
    T_days = int(sys.argv[5])
    H = float(sys.argv[6])
    n = int(sys.argv[7])

    result = binomial_barrier_option(S, X, r, sigma, T_days, H, n)
    print("{:.6f}, {:.6f}, {:.6f}, {:.6f}".format(*result))
