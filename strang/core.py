import numpy as np
from typing import Tuple
from scipy.integrate import solve_ivp


# 默认参数（可在主程序覆盖）
J = 0.0025
m = 0.044279
g = 9.8
r = 0.1
b = 0.006062
k = 0.0356
theta0 = 0.09
omega = 1.1775
pha = 0.0


def linear_rhs(t: float, y: np.ndarray,
               J_: float, b_: float, k_: float, theta0_: float, omega_: float, pha_: float):
    x, v = y
    dx = v
    dv = -2 * b_ * v - (k_ / J_) * x + (k_ / J_) * theta0_ * np.cos(omega_ * t + pha_)
    return [dx, dv]


def linear_halfstep(x: float, v: float, t: float, h: float,
                    J_: float, b_: float, k_: float, theta0_: float, omega_: float, pha_: float):
    hh = 0.5 * h
    sol = solve_ivp(
        lambda _t, y: linear_rhs(_t, y, J_, b_, k_, theta0_, omega_, pha_),
        (t, t + hh), y0=[x, v],
        method="RK45", rtol=1e-7, atol=1e-9, max_step=hh
    )
    x1, v1 = float(sol.y[0, -1]), float(sol.y[1, -1])
    return x1, v1, t + hh


def nonlinear_symplectic_step(x: float, v: float, h: float,
                              J_: float, m_: float, g_: float, r_: float):
    a = (m_ * g_ * r_ / J_) * np.sin(x)
    v_half = v + 0.5 * h * a
    x_new = x + h * v_half
    a_new = (m_ * g_ * r_ / J_) * np.sin(x_new)
    v_new = v_half + 0.5 * h * a_new
    return float(x_new), float(v_new)


def strang_step(x: float, v: float, t: float, h: float,
                J_: float, m_: float, g_: float, r_: float,
                b_: float, k_: float, theta0_: float, omega_: float, pha_: float):
    x, v, t = linear_halfstep(x, v, t, h, J_, b_, k_, theta0_, omega_, pha_)
    x, v = nonlinear_symplectic_step(x, v, h, J_, m_, g_, r_)
    x, v, t = linear_halfstep(x, v, t, h, J_, b_, k_, theta0_, omega_, pha_)
    return x, v, t


def integrate(t0: float, tf: float, h: float,
              x0: float, v0: float,
              params: Tuple[float, float, float, float, float, float, float, float, float]):
    J_, m_, g_, r_, b_, k_, theta0_, omega_, pha_ = params
    x, v, t = float(x0), float(v0), float(t0)
    T, X, V = [t], [x], [v]
    while t < tf - 1e-15:
        hh = min(h, tf - t)
        x, v, t = strang_step(x, v, t, hh, J_, m_, g_, r_, b_, k_, theta0_, omega_, pha_)
        T.append(t)
        X.append(x)
        V.append(v)
    return np.array(T), np.array(X), np.array(V)

