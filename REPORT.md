**Results Summary**
- Configuration: `t0=0.0, tf=10.0, h=1e-3, x0=0.1, v0=0.0`
- Full solver: `solve_ivp (RK45)`

**Metrics (Strang − Full)**
- |dx|_max: 2.696e+00
- |dv|_max: 4.749e+00
- RMS(dx): 1.402e+00
- RMS(dv): 2.248e+00

**Figures**
- Comparison (time series, diffs, phase portraits): `figs/compare_solve_ivp.png`

Notes
- Driven–damped pendulum is sensitive; trajectories diverge over time. For closer agreement, reduce `tf` or step size `h`, or use a higher-accuracy linear half-step (analytic L) in the Strang scheme.

---

**Extended Run (200s)**
- Configuration: `t0=0.0, tf=200.0, h=5e-3, x0=0.1, v0=0.0`
- Full solver: `solve_ivp (RK45)`

**Metrics (Strang − Full)**
- |dx|_max: 3.732e+00
- |dv|_max: 5.519e+00
- RMS(dx): 1.247e+00
- RMS(dv): 1.867e+00

**Figures**
- Strang phase/time: `figs_200/strang.png`
- Full phase/time: `figs_200/full_solve_ivp.png`
- Comparison (overlays + diffs): `figs_200/compare_solve_ivp.png`

Notes
- Over long horizons (200s), the driven–damped system’s sensitivity amplifies discrepancies between schemes. Consider reducing `h` or using an analytic linear half-step in Strang for tighter agreement.
