
# hundunnew 🧭⚙️

本项目旨在通过数值方法研究**受驱阻尼摆**的动力学行为，重点实现并对比了两种主流的数值积分方案：**Strang 算子分裂法**与**直接全方程积分法**。

## ✨ 项目简介

通过在相同的时间网格上求解受驱阻尼摆的运动方程，本项目提供了对两种数值方案的定量和定性比较。

-   **核心功能**:
    -   `strang/`：实现 **Strang 分裂法**。该方法将系统分解为保守部分和非保守部分，分别采用不同的积分器。具体为 `L(h/2) → N(h) → L(h/2)` 结构，其中：
        -   `N` (非线性保守部分) 采用 **Velocity-Verlet** 辛积分器。
        -   `L` (线性、耗散、驱动部分) 采用 `scipy.integrate.solve_ivp` (RK45)。
    -   `full/`：采用传统方法，对完整的动力学方程直接使用 `scipy.integrate.solve_ivp` (RK45) 或 `odeint` 进行求解。
    -   `compare/`：对比上述两种方案在相同设置下的结果，计算误差指标，并生成覆盖图、差异曲线和相图，以进行可视化分析。

## 🧠 数学模型

系统的动力学由以下一阶常微分方程组描述：

-   **状态变量**：`x = θ` (角度), `v = dθ/dt` (角速度)。
-   **运动方程**:
    $$
    \begin{cases}
    \frac{dx}{dt} = v \\
    \frac{dv}{dt} = \frac{mgr}{J} \sin(x) - 2bv - \frac{k}{J}x + \frac{k}{J}\theta_0 \cos(\omega t + \phi)
    \end{cases}
    $$
-   **默认参数**:
    -   `J = 0.0025` (转动惯量)
    -   `m = 0.044279` (质量)
    -   `g = 9.8` (重力加速度)
    -   `r = 0.1` (质心到轴距离)
    -   `b = 0.006062` (阻尼系数)
    -   `k = 0.0356` (扭转弹簧系数)
    -   `θ0 = 0.09` (驱动振幅)
    -   `ω = 1.1775` (驱动角频率)
    -   `φ = 0` (驱动初相位)

## 💻 代码实现与目录结构

```
.
├── strang/           # Strang 分裂法实现
│   ├── core.py       # 定义 L-step 和 N-step 算子
│   └── main.py       # 命令行入口，执行模拟与绘图
├── full/             # 全方程直接积分实现
│   ├── core.py       # 定义完整的 ODE 函数
│   └── main.py       # 命令行入口，执行模拟与绘图
├── compare/          # 对比模块
│   └── main.py       # 运行两种方案，计算误差并生成对比图
├── assets/           # 存放示例图像
├── REPORT.md         # 实验报告（可选）
├── README.md         # 本文档
├── LICENSE           # MIT 许可协议
└── .gitignore
```

-   **`strang/core.py`**: 实现了 Strang 分裂法的核心组件。`n_step` 函数使用 Velocity-Verlet 算法更新保守部分，`l_step` 函数调用 `solve_ivp` 更新非保守部分。
-   **`full/core.py`**: 定义了一个函数，该函数返回整个系统 `(dx/dt, dv/dt)` 的导数值，供 `solve_ivp` 或 `odeint` 直接调用。
-   **`main.py` 文件**: 均作为独立的命令行工具，负责解析参数、调用核心求解器、保存结果并生成可视化图像。
-   **`compare/main.py`**: 协调器，它会分别调用 `strang` 和 `full` 的核心求解函数，确保在完全相同的初始条件和时间网格下进行计算，然后进行后续的误差分析和绘图。

## 🚀 快速开始

**1. 创建虚拟环境并安装依赖**

```bash
# 创建并激活虚拟环境 (推荐)
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# 安装依赖库
pip install -U pip
pip install numpy scipy matplotlib
```

**2. 运行 Strang 分裂法**

```bash
python -m strang.main --tf 50 --h 1e-3 --plot --outdir figs
```

**3. 运行全方程积分法**

使用 `solve_ivp` (RK45):
```bash
python -m full.main --tf 50 --h 1e-3 --method solve_ivp --plot --outdir figs
```
使用 `odeint`:
```bash
python -m full.main --tf 50 --h 1e-3 --method odeint --plot --outdir figs
```

**4. 对比两种方案**

将 Strang 分裂法与 `solve_ivp` 的结果进行对比：
```bash
python -m compare.main --tf 50 --h 1e-3 --full-method solve_ivp --plot --outdir figs --export compare_solveivp.npz
```

## 📊 输出与图像

-   **控制台输出**: 比较时，会打印两种方法在 `x` 和 `v` 上的最大绝对误差和均方根误差。
    ```
    |dx|_max, |dv|_max, RMS(dx), RMS(dv)
    ```
-   **图像输出**: 生成 PNG 图像，直观展示结果。
    -   **时序图**: `x(t)` 和 `v(t)` 的轨迹覆盖图。
    -   **差异图**: `dx(t) = x_strang(t) - x_full(t)` 的误差演化。
    -   **相图**: `v` vs `x` 的相空间轨迹覆盖图。

### 🖼️ 示例图 (200s, h=5e-3, `solve_ivp` 对比)

| Strang 分裂法 (相图与时序) | 全方程积分 (相图与时序) | 对比与差异图 |
| :---: | :---: | :---: |
| ![Strang 相图与时序](assets/strang.png) | ![Full 相图与时序](assets/full_solve_ivp.png) | ![对比与差异图](assets/compare_solve_ivp.png) |

## 🔧 参数建议

-   **步长选择**: 为保证数值精度和稳定性，步长 `h` 应远小于系统驱动周期的特征时间，即 `h << 2π/ω` (在此项目中约为 5.34)。
-   **物理观察**: 由于系统包含驱动和阻尼，总能量不守恒。因此，相图（`x` vs `v`）是比能量图更直观地反映系统长期行为（如吸引子、混沌等）的工具。

## 📚 方法原理与证明

### 1) 数学原理说明

#### 问题设定

我们考虑一个常微分方程（ODE）的初值问题，其向量场可以被分解为两个部分：
$$
\frac{d\mathbf{y}}{dt} = F(\mathbf{y}, t) = (A + B)\,\mathbf{y}, \quad \mathbf{y}(t_0) = \mathbf{y}_0
$$
其中 $A$ 和 $B$ 是算子，可以代表系统的不同物理过程。在本项目中，受驱阻尼摆的方程被拆分为：

*   **算子 A (记为 L)**：对应“线性 + 耗散 + 外力驱动”部分。这部分不保守，但通常是线性或易于求解的。
    $$
    \dot{\mathbf{y}} = A \mathbf{y} \implies \begin{cases} \dot{x} = 0 \\ \dot{v} = -2bv - \frac{k}{J}x + \frac{k}{J}\theta_0 \cos(\omega t + \phi) \end{cases}
    $$
*   **算子 B (记为 N)**：对应“非线性保守（哈密顿）”部分。这部分描述了系统的内在几何结构。
    $$
    \dot{\mathbf{y}} = B \mathbf{y} \implies \begin{cases} \dot{x} = v \\ \dot{v} = \frac{mgr}{J}\sin x \end{cases}
    $$

#### 解算子 (Solution Operator)

从时间 $t$ 演化到 $t+h$ 的精确解可以通过一个解算子 $\Phi_h^{A+B}$ 来表示：
$$
\mathbf{y}(t+h) = \Phi_h^{A+B}(\mathbf{y}(t)) = e^{h(A+B)}\,\mathbf{y}(t)
$$
同理，对于子问题 $\dot{\mathbf{y}}=A\mathbf{y}$ 与 $\dot{\mathbf{y}}=B\mathbf{y}$，它们的解算子分别为 $\Phi_{h}^{A}=e^{hA}$ 和 $\Phi_{h}^{B}=e^{hB}$。

#### 算子分裂法的核心思想

由于直接计算 $e^{h(A+B)}$ 通常非常困难（当 $A$ 和 $B$ 不对易，即 $[A, B] = AB - BA \neq 0$ 时），算子分裂法通过组合子问题的精确解来近似它。

*   **一阶 Lie–Trotter 分裂**：
    $$
    \Phi_h^{A+B} \approx \Phi_h^A\,\Phi_h^B
    $$
    其局部截断误差为 $O(h^2)$，全局误差为 $O(h)$。

*   **二阶 Strang 分裂**（或对称分裂）：
    $$
    \Psi_h^{\mathrm{Strang}} = \Phi_{h/2}^A\,\Phi_h^B\,\Phi_{h/2}^A
    $$
    这个过程可以描述为“$A$ 演化半步 → $B$ 演化整步 → $A$ 演化半步”。其对称的结构是获得更高精度的关键。

在您的项目中，所采用的方案是：
- **$B$ 部分 (N)** (非线性保守) 使用 Velocity-Verlet (一种辛积分器) 演化一个**整步** `h`。
- **$A$ 部分 (L)** (线性耗散+外驱) 使用 `solve_ivp` 中的 RK45 方法演化一个**半步** `h/2`。
- 最终组合成 Strang 分裂格式：`L(h/2) → N(h) → L(h/2)`。

### 2) 精度阶数证明（二阶）

**目标**：证明 Strang 分裂的局部截断误差为 $O(h^3)$，从而确保其全局误差为二阶 $O(h^2)$。

**关键工具**：Baker–Campbell–Hausdorff (BCH) 公式。对于两个非交换算子 $X$ 和 $Y$，有：
$$
e^X e^Y = e^Z, \quad \text{其中 } Z = X+Y + \frac{1}{2}[X,Y] + \frac{1}{12}[X,[X,Y]] - \frac{1}{12}[Y,[X,Y]] + \cdots
$$
当 $X, Y$ 都是 $O(h)$ 时，取对数可得一个非常有用的近似：
$$
\log(e^X e^Y) = X + Y + \frac{1}{2}[X,Y] + O(h^3)
$$

**证明思路**：
我们将 Strang 分裂算子 $\Psi_h^{\mathrm{Strang}}=e^{\frac{h}{2}A}e^{hB}e^{\frac{h}{2}A}$ 写成单一指数 $e^Z$ 的形式，然后将其与精确解的算子 $e^{h(A+B)}$ 进行比较。

1.  **首先合并后两项**
    令 $X = hB$, $Y = \frac{h}{2}A$。根据 BCH 公式：
    $$
    \begin{aligned}
    \log\left(e^{hB} e^{\frac{h}{2}A}\right) &= (hB) + \left(\frac{h}{2}A\right) + \frac{1}{2}\left[hB, \frac{h}{2}A\right] + O(h^3) \\
    &= hB + \frac{h}{2}A + \frac{h^2}{4}[B,A] + O(h^3)
    \end{aligned}
    $$
    我们记此结果为算子 $C$，即 $e^C = e^{hB} e^{\frac{h}{2}A}$。

2.  **再与第一项合并**
    现在我们计算 $\Psi_h^{\mathrm{Strang}}=e^{\frac{h}{2}A} e^C$。令 $X=\frac{h}{2}A$, $Y=C$：
    $$
    \log(\Psi_h^{\mathrm{Strang}}) = \left(\frac{h}{2}A\right) + C + \frac{1}{2}\left[\frac{h}{2}A, C\right] + O(h^3)
    $$

3.  **代入 C 并按 h 的幂次收集项**
    将算子 $C$ 的表达式代入上式：
    $$
    \log(\Psi_h^{\mathrm{Strang}}) = \frac{h}{2}A + \left( hB + \frac{h}{2}A + \frac{h^2}{4}[B,A] \right) + \frac{1}{2}\left[\frac{h}{2}A, hB + \frac{h}{2}A + \dots\right] + O(h^3)
    $$
    现在，我们按 $h$ 的幂次来整理和分析各项。

    *   **$O(h)$ 阶项**:
        只看与 $h$ 成正比的项：
        $$
        \frac{h}{2}A + hB + \frac{h}{2}A = h(A+B)
        $$
        这与精确解算子 $e^{h(A+B)}$ 的指数中的一阶项完全一致。

    *   **$O(h^2)$ 阶项**:
        接下来，我们收集所有与 $h^2$ 成正比的项。这些项来自两个地方：
        1.  来自 $C$ 表达式中的项：$\frac{h^2}{4}[B,A]$
        2.  来自对易子 $\frac{1}{2}\left[\frac{h}{2}A, C\right]$。我们只需考虑 $C$ 中的最低阶项（$hB$），因为其他项会产生更高阶的贡献（$O(h^3)$ 或更高）。所以，这一部分的主要贡献是：
            $$
            \frac{1}{2}\left[\frac{h}{2}A, hB\right] = \frac{h^2}{4}[A,B]
            $$
        将这两个 $O(h^2)$ 的项相加：
        $$
        \frac{h^2}{4}[B,A] + \frac{h^2}{4}[A,B]
        $$
        利用对易子的反对称性质 $[A,B] = -[B,A]$，上式变为：
        $$
        -\frac{h^2}{4}[A,B] + \frac{h^2}{4}[A,B] = 0
        $$
        可见，由于 Strang 分裂的对称性，$O(h^2)$ 阶的误差项被完全抵消了。

**结论**

由于 $O(h^2)$ 项为零，$\log(\Psi_h^{\mathrm{Strang}})$ 的展开式与 $h(A+B)$ 的差异从 $O(h^3)$ 阶才开始出现：
$$
\log(\Psi_h^{\mathrm{Strang}}) = h(A+B) + O(h^3)
$$
这意味着 Strang 分裂算子与精确解算子之差为 $O(h^3)$：
$$
\Psi_h^{\mathrm{Strang}} = e^{h(A+B) + O(h^3)} = e^{h(A+B)} + O(h^3)
$$
因此，该方法的**局部截断误差**为 $O(h^3)$，经过 $T/h$ 步积分后，**全局误差**为 $O(h^2)$。

**证毕。**

### 3) 稳定性与可行性分析

#### 可行性（Feasibility）
分裂法是否实用的关键在于“子问题是否比原问题更容易求解”。

1.  **$B$ 部分（非线性保守）**：这是一个哈密顿子系统，其物理性质（如能量、相空间体积）有特殊的几何结构。使用**辛积分器**（如本项目中的 Velocity-Verlet）来求解，可以高效、稳定地进行整步更新，并很好地保持系统的长期几何特性。
2.  **$A$ 部分（线性耗散+外驱）**：这是一个线性系统（如果忽略 $x$ 对它的影响，则是时变线性系统），可以使用标准的高精度数值方法（如 RK45）高效求解，或者在某些情况下甚至可以求得解析解。用它来演化半步，计算成本低且精度有保障。

#### 稳定性（Stability）

*   **继承子方法的稳定性**：Strang 分裂的稳定性通常继承自其构成部分的数值方法。
    *   用于 $B$ 部分的 Velocity-Verlet 在线性测试方程下是无条件稳定的，并且其辛结构能够有效抑制能量的虚假漂移，对长期模拟至关重要。
    *   用于 $A$ 部分的 RK45 在合理的步长下是稳定的，且 $A$ 本身包含阻尼项，具有内在的稳定化作用。
*   **结构保持优势**：虽然整个系统因为驱动和阻尼而是非保守的，但通过对系统的保守“骨架”（$B$ 部分）使用辛积分器，该方法能够更好地“记住”系统的哈密顿几何结构。相比于用单一的、非几何的积分器（如 RK45）直接求解整个方程，这种分裂方案在弱耗散/弱驱动的情况下，往往能提供更稳健、物理意义更真实的长期模拟结果。

综上所述，Strang 分裂方案通过“对保守骨架用辛法，对耗散驱动用标准法”的巧妙搭配，在精度、效率和长期稳定性之间取得了出色的平衡，是计算物理与化学领域中广泛应用的强大工具。

## 📝 许可

本项目采用 **MIT License**。详情请参阅 `LICENSE` 文件。

## 🤝 贡献

欢迎通过提交 **Issue** 或 **Pull Request** 来为项目做出贡献。如果您有新的特性建议（例如：
-   实现 $L$ 部分的解析解以提高效率。
-   增加 Poincaré 截面图的生成功能。
-   开发批量运行和生成对比报告的脚本。
），也请随时提出！
