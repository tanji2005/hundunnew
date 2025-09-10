# hundunnew 🧭⚙️

受驱阻尼摆的两种数值积分方案与对比分析。

## ✨ 项目简介
- 实现两种常用数值方法，并在相同时间网格上进行对比，支持图形化展示：
  - `strang/`：Strang 分裂（L(h/2) → N(h) → L(h/2)）。N 用 Velocity-Verlet（辛），L 用 `solve_ivp` 的 RK45。
  - `full/`：传统全方程数值解（`solve_ivp` 或 `odeint`）。
  - `compare/`：对比两方案，输出误差指标并绘制覆盖图、差异曲线和相图。

## 🧠 数学模型
- 变量：`x = θ`，`v = dθ/dt`。
- 方程：
  - `dx/dt = v`
  - `dv/dt = (m g r / J) sin x - 2 b v - (k/J) x + (k/J) θ0 cos(ω t + φ)`
- 默认参数：`J=0.0025, m=0.044279, g=9.8, r=0.1, b=0.006062, k=0.0356, θ0=0.09, ω=1.1775, φ=0`。

## 📦 目录结构
```
.
├── strang/           # Strang 分裂法（L 半步 + N 整步 + L 半步）
│   ├── core.py
│   └── main.py
├── full/             # 传统全方程求解（solve_ivp / odeint）
│   ├── core.py
│   └── main.py
├── compare/          # 对比两方案并绘图
│   └── main.py
├── REPORT.md         # 若干实验的指标与图像路径
├── README.md         # 本文档
├── LICENSE           # 许可协议（MIT）
└── .gitignore
```

## 🚀 快速开始
1) 激活虚拟环境并安装依赖：
- `source .venv/bin/activate`
- `pip install -U pip`
- `pip install numpy scipy matplotlib`

2) 运行 Strang 分裂并绘图：
- `python -m strang.main --tf 50 --h 1e-3 --plot --outdir figs`

3) 运行全方程（RK45 或 odeint）并绘图：
- `python -m full.main --tf 50 --h 1e-3 --method solve_ivp --plot --outdir figs`
- `python -m full.main --tf 50 --h 1e-3 --method odeint   --plot --outdir figs`

4) 对比两者（同一时间网格）：
- `python -m compare.main --tf 50 --h 1e-3 --full-method solve_ivp --plot --outdir figs --export compare_solveivp.npz`

## 📊 输出与图像
- 指标：在控制台输出 `|dx|_max, |dv|_max, RMS(dx), RMS(dv)`。
- 图像：生成 `x(t)` 覆盖图、`v(t)` 覆盖图、差值 `dx(t)`、相图覆盖，便于直观比较。

## 🔧 参数建议
- 选择 `h << 2π/ω`（约 5.34）以保证精度与稳定性。
- 系统含驱动与阻尼，总能量不守恒；相图（x-v）更直观地反映长期行为。

## 📝 许可
- 本项目使用 MIT License，详见 `LICENSE` 文件。

## 🤝 贡献
- 欢迎提交 Issue/PR，或提出新特性建议（如解析线性半步、Poincaré 截面、批量对比报告等）。
