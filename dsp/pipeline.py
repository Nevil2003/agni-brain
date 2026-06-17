#!/usr/bin/env python3
"""
AGNI Health — Real-Time DSP Pipeline
=====================================
Takes raw 16 kHz audio from XIAO nRF52840 + INMP441,
runs bandpass filter → short-time energy → adaptive threshold,
outputs events/min, SSI, and daily trend data.

Usage:
    python dsp/pipeline.py              # Auto-detect serial port
    python dsp/pipeline.py --port COM3  # Specify port

Output:
    - Real-time stats to stdout
    - CSV log to agni_log.csv
"""

import argparse
import csv
import struct
import sys
import time

import numpy as np
import scipy.signal as signal

# ─── Configuration ──────────────────────────────────────────────────
SAMPLE_RATE = 16000
BANDPASS_LOW = 80       # Hz
BANDPASS_HIGH = 1000    # Hz
FILTER_ORDER = 4
FRAME_MS = 32           # Short-time energy window (ms)
STRIDE_MS = 16          # Overlap stride (ms)
THRESHOLD_STD = 2.0     # Adaptive threshold: mean + N * std
RATE_HISTORY = 100      # Samples for running average
MIN_EVENTS = 1          # Minimum events to report SSI
LOG_FILE = "agni_log.csv"
# ────────────────────────────────────────────────────────────────────

FRAME_SIZE = int(SAMPLE_RATE * FRAME_MS / 1000)   # 512
STRIDE_SIZE = int(SAMPLE_RATE * STRIDE_MS / 1000)  # 256
CHUNK_SIZE = 2048  # Process in ~128ms chunks


class AGNIPipeline:
    """Real-time bowel sound detection pipeline."""

    def __init__(self):
        # Bandpass filter
        nyquist = SAMPLE_RATE / 2
        self.b, self.a = signal.butter(
            FILTER_ORDER,
            [BANDPASS_LOW / nyquist, BANDPASS_HIGH / nyquist],
            btype='band'
        )

        self.buffer = []
        self.recent_rates = []
        self.total_events = 0
        self.total_minutes = 0
        self.log_data = []
        self.start_time = time.time()

        print(f"AGNI DSP Pipeline")
        print(f"  Bandpass: {BANDPASS_LOW}-{BANDPASS_HIGH} Hz")
        print(f"  Frame: {FRAME_MS}ms window, {STRIDE_MS}ms stride")
        print(f"  Threshold: mean + {THRESHOLD_STD}σ")
        print(f"  Logging to: {LOG_FILE}")
        print(f"{'─' * 55}")

    def process_chunk(self, chunk: np.ndarray) -> dict:
        """Process one audio chunk, return metrics."""
        # Bandpass filter
        filtered = signal.filtfilt(self.b, self.a, chunk)

        # Short-time energy
        energy = []
        for i in range(0, len(filtered) - FRAME_SIZE + 1, STRIDE_SIZE):
            frame = filtered[i:i + FRAME_SIZE]
            energy.append(float(np.mean(frame ** 2)))
        energy = np.array(energy)

        if len(energy) == 0:
            return {'rate': 0, 'ssi': 0, 'events': 0}

        # Adaptive threshold
        thresh = float(np.mean(energy) + THRESHOLD_STD * np.std(energy))
        events = energy > thresh
        n_events = int(np.sum(events))

        # Rate (events/min)
        window_seconds = len(energy) * STRIDE_MS / 1000
        rate = n_events / (window_seconds / 60) if window_seconds > 0 else 0

        # SSI (mean interval between events, ms)
        ssi = 0.0
        if n_events > MIN_EVENTS:
            idx = np.where(events)[0]
            intervals = np.diff(idx) * STRIDE_MS
            ssi = float(np.mean(intervals))

        # Running average rate
        self.recent_rates.append(rate)
        if len(self.recent_rates) > RATE_HISTORY:
            self.recent_rates.pop(0)

        return {
            'rate': round(rate, 1),
            'avg_rate': round(float(np.mean(self.recent_rates)), 1),
            'ssi': round(ssi),
            'events': n_events,
            'threshold': round(thresh, 6),
        }

    def log_csv(self, metrics: dict):
        """Append metrics to CSV log."""
        self.log_data.append({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'unix_time': time.time(),
            'rate': metrics['rate'],
            'avg_rate': metrics['avg_rate'],
            'ssi': metrics['ssi'],
            'events': metrics['events'],
        })

    def save_log(self):
        """Write accumulated log to CSV."""
        if not self.log_data:
            return
        with open(LOG_FILE, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=[
                'timestamp', 'unix_time', 'rate', 'avg_rate', 'ssi', 'events'
            ])
            w.writeheader()
            w.writerows(self.log_data)
        print(f"\nSaved {len(self.log_data)} records to {LOG_FILE}")

    def run(self, port: str):
        """Main loop: read from serial, process, display."""
        import serial
        ser = serial.Serial(port, 115200, timeout=2)
        print(f"Connected to {port}")

        # Wait for start marker
        while True:
            line = ser.readline().decode(errors='replace').strip()
            if "AGNI_RECORDING" in line:
                print("Recording... Press Ctrl+C to stop.\n")
                break

        try:
            while True:
                # Read one packet (512 ints, 1024 bytes)
                raw = ser.read(1024)
                if len(raw) < 1024:
                    continue

                samples = struct.unpack('<' + 'h' * 512, raw)
                self.buffer.extend(samples)

                # Process in chunks
                while len(self.buffer) >= CHUNK_SIZE:
                    chunk = np.array(self.buffer[:CHUNK_SIZE], dtype=np.float32)
                    self.buffer = self.buffer[CHUNK_SIZE:]

                    metrics = self.process_chunk(chunk)
                    self.log_csv(metrics)

                    # Display
                    elapsed = int(time.time() - self.start_time)
                    print(
                        f"[{elapsed:4d}s] "
                        f"Rate: {metrics['rate']:5.1f}/min "
                        f"(avg {metrics['avg_rate']:5.1f})  |  "
                        f"SSI: {metrics['ssi']:5.0f}ms  |  "
                        f"Events: {metrics['events']:3d}"
                    )

        except KeyboardInterrupt:
            print("\n\nStopping...")
        finally:
            self.save_log()
            ser.close()


def auto_detect_port():
    """Find the XIAO serial port."""
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if 'XIAO' in p.description.upper() or 'NRF52' in p.description.upper():
            return p.device
        if 'USB' in p.description and 'SERIAL' in p.description.upper():
            return p.device
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AGNI DSP Pipeline')
    parser.add_argument('--port', help='Serial port (auto-detect if omitted)')
    args = parser.parse_args()

    port = args.port or auto_detect_port()
    if not port:
        print("No serial port found. Specify with --port")
        print("Common: COM3 (Windows), /dev/ttyACM0 (Linux), /dev/cu.usbmodem* (Mac)")
        sys.exit(1)

    pipeline = AGNIPipeline()
    pipeline.run(port)
