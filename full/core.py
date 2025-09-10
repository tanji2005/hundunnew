import numpy as np
from typing import Tuple
from scipy.integrate import solve_ivp, odeint


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


def full_rhs_solve_ivp(t: float, y: np.ndarray,
                       J_: float, m_: float, g_: float, r_: float,
                       b_: float, k_: float, theta0_: float, omega_: float, pha_: float):
    x, v = y
    dxdt = v
    dvdt = (m_ * g_ * r_ * np.sin(x) - (2 * b_ * J_) * v - k_ * x + k_ * theta0_ * np.cos(omega_ * t + pha_)) / J_
    return [dxdt, dvdt]


def full_rhs_odeint(y: np.ndarray, t: float,
                    J_: float, m_: float, g_: float, r_: float,
                    b_: float, k_: float, theta0_: float, omega_: float, pha_: float):
    x, v = y
    dxdt = v
    dvdt = (m_ * g_ * r_ * np.sin(x) - (2 * b_ * J_) * v - k_ * x + k_ * theta0_ * np.cos(omega_ * t + pha_)) / J_
    return [dxdt, dvdt]


def simulate_full_with_times(T_eval: np.ndarray, x0: float, v0: float,
                             params: Tuple[float, float, float, float, float, float, float, float, float],
                             method: str = "solve_ivp") -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    J_, m_, g_, r_, b_, k_, theta0_, omega_, pha_ = params
    y0 = [x0, v0]
    if method == "solve_ivp":
        sol = solve_ivp(
            lambda t, y: full_rhs_solve_ivp(t, y, J_, m_, g_, r_, b_, k_, theta0_, omega_, pha_),
            (float(T_eval[0]), float(T_eval[-1])), y0=y0,
            t_eval=T_eval, method="RK45", rtol=1e-9, atol=1e-11
        )
        return sol.t, sol.y[0], sol.y[1]
    elif method == "odeint":
        Y = odeint(full_rhs_odeint, y0, T_eval, args=(J_, m_, g_, r_, b_, k_, theta0_, omega_, pha_), atol=1e-11, rtol=1e-9)
        return T_eval, Y[:, 0], Y[:, 1]
    else:
        raise ValueError("method 必须是 'solve_ivp' 或 'odeint'")

