#!/usr/bin/env python3
"""
Analyze vertical ascent from FPV OSD CSV.

Expected columns (case-insensitive; spaces allowed):
- GForce (load factor n)
- Wattage (W)
- Frame (frame index at N fps, default 30)
- Amperage (A)
Aliases accepted:
  GForce: g, g_load, loadfactor
  Wattage: power
  Frame: frameindex
  Amperage: current, aperage

What it computes:
- t [s] from frames, dt [s] from frame gaps
- a_z = 9.81 * (G - 1) [m/s^2] (straight-up assumption)
- Rolling-smoothed a_z
- Δv_z and Δh by trapezoid integration
- Voltage = Wattage / Amperage
- Optional thrust estimate: T ≈ n * m * g (needs --mass kg)

Outputs:
- Console stats (including values near 1.0 s)
- out/analyzed.csv with derived columns
- out/plots.png with 4 panels
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy.integrate import cumtrapz
except Exception:
    print("scipy is required. Please install with: pip install scipy", file=sys.stderr)
    raise

G0 = 9.81

def find_col(df, keys):
    keys = [k.lower() for k in keys]
    for c in df.columns:
        lc = c.lower()
        if any(k in lc for k in keys):
            return c
    return None

def load_and_prepare(csv_path, fps, start_at_zero):
    df = pd.read_csv(csv_path)
    # Strip/normalize column names but keep originals for display
    df.columns = [c.strip() for c in df.columns]

    gcol = find_col(df, ["gforce", "g_load", "loadfactor", "g"])
    wcol = find_col(df, ["wattage", "power"])
    fcol = find_col(df, ["frame", "frameindex"])
    acol = find_col(df, ["amperage", "current", "aperage", "amps"])

    missing = [name for name, col in [
        ("GForce", gcol), ("Wattage", wcol), ("Frame", fcol), ("Amperage", acol)
    ] if col is None]
    if missing:
        raise ValueError(f"Missing required columns (or aliases): {', '.join(missing)}.\n"
                         f"Found columns: {list(df.columns)}")

    # Time from frame index
    frames = df[fcol].to_numpy()
    if start_at_zero:
        t = (frames - frames[0]) / float(fps)
    else:
        t = frames / float(fps)
    df["t_s"] = t
    # dt from frame gaps
    df["dt_s"] = np.r_[0.0, np.diff(frames) / float(fps)]

    # Acceleration (straight up): a_z = g * (n - 1)
    df["a_z"] = G0 * (df[gcol].astype(float) - 1.0)

    # Voltage = W / A (avoid divide by zero)
    df["voltage_V"] = df[wcol].astype(float) / df[acol].replace(0, np.nan).astype(float)

    return df, gcol, wcol, fcol, acol

def smooth_series(s, window):
    window = int(max(1, window))
    if window % 2 == 0:
        window += 1
    return s.rolling(window, center=True, min_periods=1).mean()

def integrate_series(t, y):
    # Trapezoidal cumulative integral with nonuniform t
    return cumtrapz(y, t, initial=0.0)

def main():
    # Hardkodet CSV-sti for testing
    csv_path = "/Users/husby/Downloads/Drone Data.csv"
    fps = 30.0
    mass = 0.24
    smooth = 5
    start_at_zero = False
    out_csv = "out/analyzed.csv"
    no_gui = False

    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    out_png = os.path.join(os.path.dirname(out_csv), "plots.png")

    df, gcol, wcol, fcol, acol = load_and_prepare(csv_path, fps, start_at_zero)

    # Smooth acceleration
    df["a_z_smooth"] = smooth_series(df["a_z"], smooth)

    # Integrate to Δv and Δh
    t = df["t_s"].to_numpy()
    az = df["a_z_smooth"].to_numpy()
    df["delta_v"] = integrate_series(t, az)
    df["delta_h"] = integrate_series(t, df["delta_v"].to_numpy())

    # Optional thrust estimate (straight up): T ≈ n * m * g
    if mass is not None:
        df["thrust_N"] = mass * G0 * df[gcol].astype(float)
        # Thrust per Watt (instantaneous)
        df["thrust_per_W"] = df["thrust_N"] / df[wcol].replace(0, np.nan).astype(float)

    # Save output
    df.to_csv(out_csv, index=False)

    # Console summary
    tspan = df["t_s"].iloc[-1] - df["t_s"].iloc[0]
    print("\nQuick stats")
    print(f"- Time span: {tspan:.3f} s, FPS={fps}")
    print(f"- G range: {df[gcol].min():.2f} – {df[gcol].max():.2f}")
    print(f"- Peak a_z: {df['a_z'].max():.2f} m/s^2; Mean a_z: {df['a_z'].mean():.2f} m/s^2")
    print(f"- End Δv_z: {df['delta_v'].iloc[-1]:.2f} m/s; End Δh: {df['delta_h'].iloc[-1]:.2f} m")
    print(f"- Voltage range: {df['voltage_V'].min():.2f} – {df['voltage_V'].max():.2f} V")
    if mass is not None:
        print(f"- Thrust range: {df['thrust_N'].min():.2f} – {df['thrust_N'].max():.2f} N")
    # Report at ~1.0 s (frame ~30)
    one_sec_idx = np.searchsorted(t, (t[0] + 1.0) if start_at_zero else 1.0, side="right") - 1
    one_sec_idx = max(0, min(one_sec_idx, len(df)-1))
    print("\nAt ~1.0 s:")
    print(df.loc[df.index[one_sec_idx], [fcol, "t_s", gcol, "a_z", "delta_v", "delta_h", wcol, acol, "voltage_V"]])

    # Akselerasjon uten gravitasjon (bare nettoakselerasjon oppover)
    df["a_net"] = df["a_z_smooth"] - G0  # Fjern 1g
    
    # Beregn kraft (F = m * a) for hver tidspoint
    df["force_N"] = mass * df["a_net"]
    
    # Plots - Vindu 1: Kraft og akselerasjon
    fig1, axes1 = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    ax = axes1[0]
    ax.plot(df["t_s"], df[gcol] - 1, marker="o", label="G - 1 (netto load factor)", linewidth=2)
    ax.set_ylabel("G - 1"); ax.grid(True); ax.legend()
    ax.set_title("Netto G-kraft (uten gravitasjon)")

    ax = axes1[1]
    ax.plot(df["t_s"], df["a_z"], alpha=0.35, label="a_z raw (total)")
    ax.plot(df["t_s"], df["a_z_smooth"], label="a_z smooth (total)", linewidth=2)
    ax.plot(df["t_s"], df["a_net"], label="a_net (uten 1g)", linewidth=2, linestyle="--", color="red")
    ax.set_ylabel("Akselerasjon [m/s²]"); ax.grid(True); ax.legend()
    ax.set_title("Akselerasjon - Total vs Netto")

    ax = axes1[2]
    ax.plot(df["t_s"], df["force_N"], label="Kraft [N]", linewidth=2, color="red")
    ax.set_ylabel("Kraft [N]")
    ax.set_xlabel("Tid [s]")
    ax.grid(True); ax.legend()
    ax.set_title(f"Nettkraft på drone (masse = {mass} kg)")

    fig1.tight_layout()
    fig1.savefig("out/plots_kraft_akselerasjon.png", dpi=150)
    
    # Plots - Vindu 2: Hastighet, høyde og elektrisitet
    fig2, axes2 = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    ax = axes2[0]
    ax.plot(df["t_s"], df["delta_v"], label="Hastighet [m/s]", linewidth=2, color="green")
    ax.set_ylabel("Hastighet [m/s]")
    ax.grid(True); ax.legend()
    ax.set_title("Vertikal hastighet")

    ax = axes2[1]
    ax.plot(df["t_s"], df["delta_h"], label="Høyde [m]", linewidth=2, color="orange")
    ax.set_ylabel("Høyde [m]")
    ax.grid(True); ax.legend()
    ax.set_title("Vertikal høyde")

    ax = axes2[2]
    ax.plot(df["t_s"], df[wcol], label="Power [W]", linewidth=1.5)
    ax.plot(df["t_s"], df[acol], label="Current [A]", linewidth=1.5)
    ax.plot(df["t_s"], df["voltage_V"], label="Voltage [V]", linewidth=1.5)
    ax.set_ylabel("W / A / V")
    ax.set_xlabel("Tid [s]")
    ax.grid(True); ax.legend()
    ax.set_title("Elektrisk data")
    
    fig2.tight_layout()
    fig2.savefig("out/plots_hastighet_hoyde.png", dpi=150)
    
    print(f"\nSaved: {out_csv}")
    print(f"Saved: out/plots_kraft_akselerasjon.png")
    print(f"Saved: out/plots_hastighet_hoyde.png")
    print(f"\n--- Kraft statistikk ---")
    print(f"Min kraft: {df['force_N'].min():.2f} N")
    print(f"Max kraft: {df['force_N'].max():.2f} N")
    print(f"Gjennomsnittlig kraft: {df['force_N'].mean():.2f} N")

    if not no_gui:
        plt.show()

if __name__ == "__main__":
    main()