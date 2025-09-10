import argparse
import numpy as np
import os
from .core import integrate, J, m, g, r, b, k, theta0, omega, pha


def main():
    parser = argparse.ArgumentParser(description="Strang splitting integrator (L(h/2)->N(h)->L(h/2))")
    parser.add_argument("--t0", type=float, default=0.0)
    parser.add_argument("--tf", type=float, default=50.0)
    parser.add_argument("--h", type=float, default=1e-3)
    parser.add_argument("--x0", type=float, default=0.1)
    parser.add_argument("--v0", type=float, default=0.0)
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--save", type=str, default="")
    parser.add_argument("--outdir", type=str, default="")
    args = parser.parse_args()

    params = (J, m, g, r, b, k, theta0, omega, pha)
    T, X, V = integrate(args.t0, args.tf, args.h, args.x0, args.v0, params)

    print(f"Strang done: N={len(T)}, t in [{T[0]:.3f},{T[-1]:.3f}]")

    if args.save:
        np.savez(args.save, T=T, X=X, V=V)
        print(f"Saved: {args.save}")

    if args.plot or args.outdir:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(10, 4))
        ax[0].plot(T, X, lw=0.8)
        ax[0].set_xlabel('t'); ax[0].set_ylabel('x'); ax[0].set_title('x(t) - Strang')
        ax[1].plot(X, V, lw=0.6)
        ax[1].set_xlabel('x'); ax[1].set_ylabel('v'); ax[1].set_title('Phase portrait - Strang')
        fig.tight_layout()
        if args.outdir:
            os.makedirs(args.outdir, exist_ok=True)
            fpath = os.path.join(args.outdir, 'strang.png')
            fig.savefig(fpath, dpi=150)
            print(f"Figure saved: {fpath}")
        if args.plot:
            plt.show()


if __name__ == '__main__':
    main()

