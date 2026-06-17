#!/usr/bin/env python3
"""
AGNI Health — Offline Analysis & Visualization
===============================================
Analyze recorded CSV data: plot rate trends, SSI patterns,
meal response curves, and compare against reference values.

Usage:
    python dsp/analysis.py agni_log.csv          # Basic analysis
    python dsp/analysis.py agni_log.csv --plot   # With plots (requires matplotlib)
"""

import argparse
import csv
import sys

import numpy as np

try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# Reference values from literature
REF_NORMAL_RATE_LOW = 5
REF_NORMAL_RATE_HIGH = 34
REF_HEALTHY_SSI = 1900  # ms (Craine 2002)
REF_IBS_SSI_CUTOFF = 640  # ms (Craine 2002 — 91% sens, 100% spec)
REF_POSTMEAL_PEAK_MIN = 80  # minutes (Cohen 2021)
REF_POSTMEAL_PEAK_MAX = 100


def load_csv(path: str) -> list[dict]:
    """Load AGNI log CSV."""
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'timestamp': row['timestamp'],
                'unix_time': float(row['unix_time']),
                'rate': float(row['rate']),
                'avg_rate': float(row.get('avg_rate', row['rate'])),
                'ssi': float(row['ssi']),
                'events': int(row['events']),
            })
    return data


def analyze(data: list[dict]):
    """Print analysis summary."""
    rates = np.array([d['rate'] for d in data])
    ssis = np.array([d['ssi'] for d in data])

    print("=" * 55)
    print("AGNI — Recording Analysis")
    print("=" * 55)
    print(f"Duration: {len(data) * 0.128:.1f}s ({len(data) * 0.128 / 60:.1f} min)")
    print(f"Samples: {len(data)}")
    print()

    # Rate analysis
    print("─" * 55)
    print("BOWEL SOUND RATE")
    print(f"  Mean:      {rates.mean():.1f} events/min")
    print(f"  Median:    {np.median(rates):.1f} events/min")
    print(f"  Std Dev:   {rates.std():.1f}")
    print(f"  Min:       {rates.min():.1f} events/min")
    print(f"  Max:       {rates.max():.1f} events/min")
    print(f"  Normal range (5-34): ", end="")
    if np.median(rates) >= REF_NORMAL_RATE_LOW and np.median(rates) <= REF_NORMAL_RATE_HIGH:
        print("✅ WITHIN range")
    elif np.median(rates) < REF_NORMAL_RATE_LOW:
        print("⬇ BELOW normal (hypoactive)")
    else:
        print("⬆ ABOVE normal (hyperactive)")

    # SSI analysis
    valid_ssi = ssis[ssis > 0]
    print()
    print("SOUND-TO-SOUND INTERVAL (SSI)")
    if len(valid_ssi) > 0:
        print(f"  Mean:      {valid_ssi.mean():.0f} ms")
        print(f"  Median:    {np.median(valid_ssi):.0f} ms")
        print(f"  Healthy:   ~{REF_HEALTHY_SSI} ms (Craine 2002)")
        print(f"  IBS cutoff: {REF_IBS_SSI_CUTOFF} ms (91% sens, 100% spec)")
        print(f"  Assessment: ", end="")
        mean_ssi = valid_ssi.mean()
        if mean_ssi > REF_HEALTHY_SSI * 0.6:
            print(f"✅ Healthy range ({mean_ssi:.0f}ms)")
        elif mean_ssi < REF_IBS_SSI_CUTOFF:
            print(f"⚠ Below IBS cutoff ({mean_ssi:.0f}ms)")
        else:
            print(f"Intermediate range ({mean_ssi:.0f}ms)")
    else:
        print("  No events detected")

    # Stability analysis
    print()
    print("STABILITY")
    # Coefficient of variation
    cv = rates.std() / rates.mean() if rates.mean() > 0 else 0
    print(f"  Rate CV:   {cv:.2f} (lower = more stable)")
    if cv < 0.5:
        print(f"  ✅ Stable pattern")
    elif cv < 1.0:
        print(f"  ⚠ Moderately variable")
    else:
        print(f"  ⬆ Highly variable")

    print("=" * 55)
    print()


def plot_analysis(data: list[dict], output_path: str = None):
    """Generate analysis plots."""
    if not HAS_MPL:
        print("Install matplotlib for plots: pip install matplotlib")
        return

    times = np.array([(d['unix_time'] - data[0]['unix_time']) / 60 for d in data])
    rates = np.array([d['rate'] for d in data])
    ssis = np.array([d['ssi'] for d in data])
    valid_ssi = np.where(ssis > 0, ssis, np.nan)

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    fig.suptitle('AGNI — Gut Acoustic Monitoring Session', fontsize=14)

    # Rate
    ax = axes[0]
    ax.plot(times, rates, color='#e85d04', alpha=0.6, linewidth=0.8)
    ax.axhline(REF_NORMAL_RATE_LOW, color='green', linestyle='--', alpha=0.5, label=f'Normal low ({REF_NORMAL_RATE_LOW}/min)')
    ax.axhline(REF_NORMAL_RATE_HIGH, color='green', linestyle='--', alpha=0.5, label=f'Normal high ({REF_NORMAL_RATE_HIGH}/min)')
    ax.fill_between(times, REF_NORMAL_RATE_LOW, REF_NORMAL_RATE_HIGH, alpha=0.05, color='green')
    ax.set_ylabel('Rate (events/min)')
    ax.set_title('Bowel Sound Rate')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # SSI
    ax = axes[1]
    ax.plot(times, valid_ssi / 1000, color='#2563eb', alpha=0.6, linewidth=0.8)
    ax.axhline(REF_HEALTHY_SSI / 1000, color='green', linestyle='--', alpha=0.5, label=f'Healthy (~{REF_HEALTHY_SSI}ms)')
    ax.axhline(REF_IBS_SSI_CUTOFF / 1000, color='red', linestyle='--', alpha=0.5, label=f'IBS cutoff ({REF_IBS_SSI_CUTOFF}ms)')
    ax.set_ylabel('SSI (seconds)')
    ax.set_title('Sound-to-Sound Interval')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Histogram of rates
    ax = axes[2]
    ax.hist(rates, bins=30, color='#e85d04', alpha=0.7, edgecolor='white')
    ax.axvline(REF_NORMAL_RATE_LOW, color='green', linestyle='--', alpha=0.5)
    ax.axvline(REF_NORMAL_RATE_HIGH, color='green', linestyle='--', alpha=0.5)
    ax.set_xlabel('Rate (events/min)')
    ax.set_ylabel('Count')
    ax.set_title('Rate Distribution')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {output_path}")

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AGNI Offline Analysis')
    parser.add_argument('csv', help='Path to AGNI log CSV')
    parser.add_argument('--plot', action='store_true', help='Generate plots')
    parser.add_argument('--output', '-o', help='Save plot to file')
    args = parser.parse_args()

    data = load_csv(args.csv)
    if not data:
        print("No data found in CSV")
        sys.exit(1)

    analyze(data)

    if args.plot or args.output:
        plot_analysis(data, args.output)
