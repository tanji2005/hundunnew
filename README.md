**仓库简介**
- 本仓库实现了“受驱阻尼摆”的两种数值积分方案，并提供对比分析与绘图：
  - `strang/`：Strang 分裂（线性半步 L → 非线性整步 N → 线性半步 L）。其中 N 用 Velocity-Verlet（辛方法），L 用 `solve_ivp` 的 RK45。
  - `full/`：传统全方程数值解（`solve_ivp` 或 `odeint`）。
  - `compare/`：对比两方案在同一时间网格上的结果，输出误差指标与图像。

**数学模型**
- 变量：`x = θ`，`v = dθ/dt`。
- 方程：
  - `dx/dt = v`
  - `dv/dt = (m g r / J) sin x - 2 b v - (k/J) x + (k/J) θ0 cos(ω t + φ)`
- 缺省参数：`J=0.0025, m=0.044279, g=9.8, r=0.1, b=0.006062, k=0.0356, θ0=0.09, ω=1.1775, φ=0`。

**环境准备**
- 激活虚拟环境并安装依赖：
  - `source .venv/bin/activate`
  - `pip install -U pip`
  - `pip install numpy scipy matplotlib`

**运行：Strang 分裂**
- 绘制时序与相图，并保存图像：
  - `python -m strang.main --tf 50 --h 1e-3 --plot --outdir figs`
- 保存轨迹：
  - `python -m strang.main --tf 50 --h 1e-3 --save strang.npz`

**运行：全方程模拟**
- RK45：
  - `python -m full.main --tf 50 --h 1e-3 --method solve_ivp --plot --outdir figs`
- odeint：
  - `python -m full.main --tf 50 --h 1e-3 --method odeint   --plot --outdir figs`
- 保存轨迹：
  - `python -m full.main --tf 50 --h 1e-3 --save full_solveivp.npz`

**对比与绘图**
- 使用相同时间网格对比 Strang 与 Full，生成覆盖图与差异图，并导出误差：
  - `python -m compare.main --tf 50 --h 1e-3 --full-method solve_ivp --plot --outdir figs --export compare_solveivp.npz`
- 控制台会输出：`|dx|_max, |dv|_max, RMS(dx), RMS(dv)`。

**建议**
- 选择 `h << 2π/ω`（约 5.34）以保证精度。
- 系统含驱动与阻尼，总能量不守恒；相图更直观地反映动力学。
