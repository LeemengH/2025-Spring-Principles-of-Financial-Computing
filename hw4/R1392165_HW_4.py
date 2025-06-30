#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binomial-Trinomial tree with Brownian-Bridge adjustment
for DOUBLE-BARRIER (up-&-out / down-&-out) options.

執行方式：
    python3 R13922165_HW_4.py 95 100 0.10 0.25 365 140 90 50
輸出：
    call_price, call_delta, put_price, put_delta   (各保留 6 位小數)
"""

import sys, math
from typing import Tuple, List

def first_step_probs(r: float, sigma: float, dtp: float,
                     u0: float, d0: float) -> Tuple[float, float, float]:
    """三叉首步機率（二階動差配適）"""
    a  = math.exp(r * dtp)
    a2 = math.exp((2 * r + sigma ** 2) * dtp)
    A11, A12 = u0 - 1.0,           d0 - 1.0
    A21, A22 = u0 ** 2 - 1.0,      d0 ** 2 - 1.0
    B1,  B2  = a - 1.0,            a2 - 1.0
    det      = A11 * A22 - A12 * A21
    p_u      = (B1 * A22 - B2 * A12) / det
    p_d      = (A11 * B2 - A21 * B1) / det
    p_m      = 1.0 - p_u - p_d
    # 防止微小負值
    p_u = max(0.0, min(1.0, p_u))
    p_d = max(0.0, min(1.0, p_d))
    p_m = 1.0 - p_u - p_d
    return p_u, p_m, p_d


def hit_prob_up(S0: float, S1: float, H: float,
                sigma: float, dt: float) -> float:
    """Brownian-bridge 過程在 (t,t+dt] 內碰到上障礙的機率"""
    if S0 >= H or S1 >= H:
        return 1.0
    expo = -2.0 * math.log(H / S0) * math.log(H / S1) / (sigma ** 2 * dt)
    return math.exp(expo)


def hit_prob_down(S0: float, S1: float, L: float,
                  sigma: float, dt: float) -> float:
    """Brownian-bridge 過程在 (t,t+dt] 內碰到下障礙的機率"""
    if S0 <= L or S1 <= L:
        return 1.0
    expo = -2.0 * math.log(S0 / L) * math.log(S1 / L) / (sigma ** 2 * dt)
    return math.exp(expo)


def surv_prob(S0: float, S1: float, H: float, L: float,
              sigma: float, dt: float) -> float:
    """在 Δt 內同時維持 L<S<H 的存活率"""
    if (S0 >= H or S0 <= L or S1 >= H or S1 <= L):
        return 0.0
    q_up = hit_prob_up(S0, S1, H, sigma, dt)
    q_dn = hit_prob_down(S0, S1, L, sigma, dt)
    surv = 1.0 - q_up - q_dn
    return max(0.0, surv)


# ────────────────────────────────────────── Sub-tree  ──────────────────────────────────────────
def binomial_subtree_bridge(
    S0: float, X: float, r: float, sigma: float,
    u: float, d: float, p: float, dt: float, N: int,
    H: float, L: float, is_call: bool
) -> float:
    """含 Brownian-Bridge 修正的二叉子樹定價"""
    disc = math.exp(-r * dt)

    # 1. 終端層
    values: List[float] = []
    for j in range(N + 1):
        ST = S0 * (u ** j) * (d ** (N - j))
        payoff = 0.0
        if L < ST < H:
            payoff = max(ST - X, 0.0) if is_call else max(X - ST, 0.0)
        values.append(payoff)

    # 2. 反向折現並乘存活率
    for i in range(N - 1, -1, -1):
        new_layer: List[float] = []
        for j in range(i + 1):
            Sij = S0 * (u ** j) * (d ** (i - j))
            Sup = Sij * u
            Sdn = Sij * d
            surv_up = surv_prob(Sij, Sup, H, L, sigma, dt)
            surv_dn = surv_prob(Sij, Sdn, H, L, sigma, dt)

            val = disc * (p * surv_up * values[j + 1] +
                          (1.0 - p) * surv_dn * values[j])
            new_layer.append(val)
        values = new_layer

    return values[0]


# ────────────────────────────────────────── main ──────────────────────────────────────────
def double_barrier_price(
    S: float, X: float, r: float, sigma: float, T_days: int,
    H: float, L: float, k: int, is_call: bool
) -> float:
    """回傳 double-barrier call / put 價格"""
    T   = T_days / 365.0
    dt  = (math.log(H / L) / (2.0 * k * sigma)) ** 2
    N0  = max(1, math.floor(T / dt))        # 樹高
    dtp = T - (N0 - 1) * dt                 # 首層 Δt′

    # 二叉步長參數
    u   = math.exp(sigma * math.sqrt(dt))
    d   = 1.0 / u
    p   = (math.exp(r * dt) - d) / (u - d)
    p   = max(0.0, min(1.0, p))             # 安全限制

    # 首層三叉
    u0  = math.exp(sigma * math.sqrt(dtp))
    d0  = 1.0 / u0
    p_u0, p_m0, p_d0 = first_step_probs(r, sigma, dtp, u0, d0)

    N_sub = N0 - 1
    val_dn = binomial_subtree_bridge(S * d0, X, r, sigma,
                                     u, d, p, dt, N_sub, H, L, is_call)
    val_md = binomial_subtree_bridge(S,      X, r, sigma,
                                     u, d, p, dt, N_sub, H, L, is_call)
    val_up = binomial_subtree_bridge(S * u0, X, r, sigma,
                                     u, d, p, dt, N_sub, H, L, is_call)

    disc0 = math.exp(-r * dtp)
    price = disc0 * (p_d0 * val_dn + p_m0 * val_md + p_u0 * val_up)
    return price


# ────────────────────────────────────────── 價格與 Delta ─────────────────────────────────────
def price_and_delta(
    S: float, X: float, r: float, sigma: float, T_days: int,
    H: float, L: float, k: int
) -> Tuple[float, float, float, float]:

    call_price = double_barrier_price(S, X, r, sigma, T_days, H, L, k, True)
    put_price  = double_barrier_price(S, X, r, sigma, T_days, H, L, k, False)

    S_up, S_dn = S * 1.01, S * 0.99
    c_up = double_barrier_price(S_up, X, r, sigma, T_days, H, L, k, True)
    c_dn = double_barrier_price(S_dn, X, r, sigma, T_days, H, L, k, True)
    p_up = double_barrier_price(S_up, X, r, sigma, T_days, H, L, k, False)
    p_dn = double_barrier_price(S_dn, X, r, sigma, T_days, H, L, k, False)

    delta_call = (c_up - c_dn) / (S_up - S_dn)
    delta_put  = (p_up - p_dn) / (S_up - S_dn)

    return call_price, delta_call, put_price, delta_put


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage: python3 R13922165_HW_4.py S X r σ T_days H L k")
        sys.exit(1)

    S, X, r, sigma, T_days, H, L, k = map(float, sys.argv[1:])
    T_days = int(T_days)
    k      = int(k)

    c, dc, p, dp = price_and_delta(S, X, r, sigma, T_days, H, L, k)
    print(f"{c:.6f}, {dc:.6f}, {p:.6f}, {dp:.6f}")
