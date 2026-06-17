# AGNI Health — Gut-Acoustic Monitoring Patch

India's first continuous gut-acoustic monitoring patch. Listens to bowel sounds, tracks your digestion rate, and delivers one daily trend over WhatsApp.

**Status:** Research & prototype stage — not for sale.

## The Science

The FDA-cleared **AbStats system (K150782)** proves that counting bowel sound events per minute provides clinically valuable gut health tracking — 100% sensitivity, 97% specificity for gastrointestinal motility assessment (Spiegel 2014). AGNI brings the same technology to consumers at 1/100th the cost.

**Key papers:**
- Spiegel 2014 — 100% sens, 97% spec for GI monitoring
- Craine 2002 — SSI (sound-to-sound interval) at 640ms cutoff gives 91% sens, 100% spec for IBS
- Cohen 2021 — AbStats tracks meal size (360 vs 1,110 kcal)
- Du 2018 — Mathematical model of bowel sound generation

## Hardware

| Component | Cost (₹) | Source |
|-----------|----------|--------|
| XIAO nRF52840 Sense | 1,719 | Robocraze |
| INMP441 I2S MEMS mic | 200-326 | Robokits/Amazon |
| Stethoscope diaphragm | 300-800 | Local pharmacy |
| Tegaderm film | 95/pc | Healthklin |
| LiPo + connectors | 250-500 | Robu.in |
| **Total PoC** | **≈₹4,000** | |

## Pipeline

```
INMP441 mic → XIAO nRF52840 → 80-1000 Hz bandpass → Short-time energy
→ Adaptive threshold → Events/min + SSI → JSON over BLE → WhatsApp
```

No ML required for the core metric. The nRF52840 can run the full DSP on-device.

## Repo Structure

```
agni-brain/
├── firmware/          # Arduino code for XIAO nRF52840
│   └── agni_i2s/      # I2S audio capture @ 16 kHz
├── dsp/               # Python DSP pipeline
│   ├── pipeline.py    # Real-time bandpass → event detection
│   └── analysis.py    # Offline analysis + visualization
├── docs/
│   ├── AGNI_Complete_Workflow.html  # Full build guide
│   ├── AGNI_Science_Backing.md      # Science analysis
│   └── AGNI_Easiest_Path.md         # Simplified approach
├── LICENSE
└── README.md
```

## Quick Start

```bash
# Clone
git clone https://github.com/nevilparekh/agni-brain
cd agni-brain

# Upload firmware
Open firmware/agni_i2s/agni_i2s.ino in Arduino IDE
Board: Seeed XIAO nRF52840 Sense
Upload via USB

# Run DSP (on laptop)
pip install pyserial numpy scipy
python dsp/pipeline.py
```

## License

MIT
