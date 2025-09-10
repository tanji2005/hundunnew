import argparse
import numpy as np
import os
from strang.core import integrate as integrate_strang, J, m, g, r, b, k, theta0, omega, pha
from full.core import simulate_full_with_times


def main():
    parser = argparse.ArgumentParser(description="Compare Strang vs Full (solve_ivp/odeint)")
    parser.add_argument("--t0", type=float, default=0.0)
    parser.add_argument("--tf", type=float, default=50.0)
    parser.add_argument("--h", type=float, default=1e-3)
    parser.add_argument("--x0", type=float, default=0.1)
    parser.add_argument("--v0", type=float, default=0.0)
    parser.add_argument("--full-method", type=str, default="solve_ivp", choices=["solve_ivp", "odeint"])
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--outdir", type=str, default="")
    parser.add_argument("--export", type=str, default="", help="save npz of results & diffs")
    args = parser.parse_args()

    params = (J, m, g, r, b, k, theta0, omega, pha)

    # Strang on its own grid
    Ts, Xs, Vs = integrate_strang(args.t0, args.tf, args.h, args.x0, args.v0, params)
    # Full on the same grid
    Tf, Xf, Vf = simulate_full_with_times(Ts, args.x0, args.v0, params, method=args.full_method)

    dx = Xs - Xf
    dv = Vs - Vf
    metrics = {
        'dx_max': float(np.max(np.abs(dx))),
        'dv_max': float(np.max(np.abs(dv))),
        'dx_rms': float(np.sqrt(np.mean(dx * dx))),
        'dv_rms': float(np.sqrt(np.mean(dv * dv)))
    }
    print(f"Method(full)={args.full_method}; |dx|_max={metrics['dx_max']:.3e}, |dv|_max={metrics['dv_max']:.3e}, "
          f"RMS(dx)={metrics['dx_rms']:.3e}, RMS(dv)={metrics['dv_rms']:.3e}")

    if args.export:
        np.savez(args.export, Ts=Ts, Xs=Xs, Vs=Vs, Tf=Tf, Xf=Xf, Vf=Vf, dx=dx, dv=dv, **metrics)
        print(f"Saved: {args.export}")

    if args.plot or args.outdir:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 2, figsize=(12, 8))
        ax[0, 0].plot(Ts, Xs, label='Strang', lw=0.8)
        ax[0, 0].plot(Tf, Xf, '--', label=args.full_method, lw=0.8)
        ax[0, 0].set_xlabel('t'); ax[0, 0].set_ylabel('x'); ax[0, 0].set_title('x(t)')
        ax[0, 0].legend()

        ax[0, 1].plot(Ts, Vs, label='Strang', lw=0.8)
        ax[0, 1].plot(Tf, Vf, '--', label=args.full_method, lw=0.8)
        ax[0, 1].set_xlabel('t'); ax[0, 1].set_ylabel('v'); ax[0, 1].set_title('v(t)')
        ax[0, 1].legend()

        ax[1, 0].plot(Ts, dx, lw=0.8)
        ax[1, 0].set_xlabel('t'); ax[1, 0].set_ylabel('dx'); ax[1, 0].set_title('x diff (Strang - Full)')

        ax[1, 1].plot(Xs, Vs, label='Strang', lw=0.6)
        ax[1, 1].plot(Xf, Vf, '--', label=args.full_method, lw=0.6)
        ax[1, 1].set_xlabel('x'); ax[1, 1].set_ylabel('v'); ax[1, 1].set_title('Phase portrait')
        ax[1, 1].legend()

        fig.tight_layout()
        if args.outdir:
            os.makedirs(args.outdir, exist_ok=True)
            path = os.path.join(args.outdir, f'compare_{args.full_method}.png')
            fig.savefig(path, dpi=150)
            print(f"Figure saved: {path}")
        if args.plot:
            plt.show()


if __name__ == '__main__':
    main()

