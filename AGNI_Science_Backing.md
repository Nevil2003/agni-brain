# AGNI Gut Bio-Tech: Complete Science Backing

## Core physics: How bowel sounds are made

There are TWO competing theories, both peer-reviewed:

### Theory 1: Spring-mass-damping model (the accurate one for your device)
**Paper:** Du et al., *JASA* 2018 — "A mathematical model of bowel sound generation"
- Bowel wall = mass-spring-damper system (same math as vocal cords)
- Peristalsis compresses intestinal contents → wall vibrates at 100-500 Hz
- FOUR parameters explain every bowel sound type:
  - **IWC** (Individual Wave Component) — gut segment dimensions (wall mass, stiffness)
  - **PI** (Pressure Index) — internal bowel pressure
  - **CQ** (Component Quantity) — number of contraction cycles
  - **CIT** (Component Interval Time) — contraction-relaxation timing

### Theory 2: Oscillating gas bubbles
**Paper:** Liu, Huang & Chen, *Chin J Physiol* 2010 — "Oscillating gas bubbles as the origin of bowel sounds"
- Gas bubbles in intestinal fluid oscillate at resonant frequencies
- Combined acoustic + ultrasound imaging proved bubbles generate measurable sounds
- Explains the "whistling" (Harmonic Sound) type

**For your device: Theory 1 is what drives AGNI's signal pipeline.** The spring-mass model predicts specific frequency bands and timing patterns that map to digestive states.

---

## The 4 bowel sound types (confirmed across 2+ papers)

| Type | Duration | Sounds like | What it means physiologically | % of events |
|------|----------|-------------|-------------------------------|-------------|
| **SB** — Single Burst | 18-58 ms | Short click | Single contraction, normal peristalsis | ~88% |
| **MB** — Multiple Bursts | 100-1030 ms | Click group, bubbling | Active fluid movement, multiple segments contracting | ~8% |
| **CRS** — Continuous Random | 119-1637 ms | Rumble, gurgle | Gas moving through variable-diameter lumen | ~3.5% |
| **HS** — Harmonic Sound | 73-763 ms | Whistle, tone | Rare — possible stenosis or resonant gas cavity | ~1% |

**Source:** Du et al. 2018 (JASA) + Baronetto et al. 2024 (JMIR AI) — both independently confirm these 4 types

---

## What bowel sounds tell you clinically (proven)

### Sound-to-sound interval = IBS diagnostic
**Craine et al. (1999/2002) — landmark study:**
- IBS patients: SSI = 452 ± 35 ms
- Healthy controls: SSI = 1,931 ± 365 ms
- Cut-off at 640 ms → **91% sensitivity, 100% specificity**
- This is THE most powerful single biomarker your device can track

### Postprandial response = digestive function
- Pre-meal: faster rate, higher variability (hunger contractions)
- Post-meal: slower rate, more SB events, CRS becomes more common
- **Your AGNI Score already has this as a weighted term (0.15)**

### IBD vs healthy classification
**MDPI Med Sci 2025 review (Mayo Clinic co-authors):**
- AI models achieve 88-96% accuracy, AUC ≥ 0.83, F1 = 0.71-0.85
- Transformer models (HuBERT, wav2vec 2.0) outperform CNNs
- Key acoustic biomarkers: spectral centroid, SSI, peak frequency

---

## The science stack your AGNI device maps to

```
Layer 1: PHYSICS — proven model (Du 2018)
  ├─ Bowel sounds = spring-mass oscillator at 100-500 Hz
  ├─ Event durations 10-4000 ms
  └─ Rate 5-34 events/min at rest

Layer 2: SENSING — validated hardware approaches
  ├─ MEMS microphone (INMP441): works at 16 kHz, $2 part
  ├─ PMUT array: -142.69 dB sensitivity, better but more complex (PMC9787765)
  ├─ GastroDigitalShirt: 8-mic array validated on 27 subjects (Baronetto 2024)
  └─ Stethoscope coupling: industry standard for 200+ years

Layer 3: SIGNAL PROCESSING — multiple proven methods
  ├─ Butterworth bandpass 80-1000 Hz (all papers agree)
  ├─ Short-time energy + adaptive threshold (standard since 1990s)
  ├─ Wavelet decomposition (Hadjileontiadis, 95% accuracy)
  └─ MFCC features (13 coefficients, standard for audio ML)

Layer 4: ML CLASSIFICATION — converging on winners
  ├─ EffUNet (EfficientNet-B2 + UNet): best for imbalanced data, 18.1M params
  ├─ Branchformer + self-supervised: best for data-limited scenarios
  └─ 1D-CNN (Edge Impulse): simplest, deployable on nRF52840

Layer 5: CLINICAL CORRELATION — established biomarkers
  ├─ SSI (sound-to-sound interval): 91% sens / 100% spec for IBS
  ├─ Rate change pre/post meal: digestive function proxy
  ├─ Spectral centroid shift: inflammation marker
  └─ CRS/MB ratio: gas vs fluid movement proxy

Layer 6: AYURVEDA FRAMING — emerging conceptual link
  ├─ Agni ↔ microbiome (IJAM 2026, BHU peer-reviewed)
  ├─ Prakriti types have distinct microbiomes (Medicina 2020, PMC7559905)
  └─ Mandagni = reduced microbial diversity, ↓ SCFAs
```

---

## Key papers to cite (by pillar)

### Pillar 1: Physics & Physiology
| Paper | Why cite | DOI |
|-------|----------|-----|
| **Du et al. 2018** — Mathematical model of bowel sound generation | The first-principles physics backbone of your entire device | 10.1121/1.5080528 |
| **Liu et al. 2010** — Oscillating gas bubbles as origin of bowel sounds | Alternative mechanism, combined acoustic + ultrasound | Chin J Physiol 53(4) |
| **Craine et al. 2002** — IBS vs healthy SSI cutoff | The 91%/100% sensitivity/specificity biomarker paper | — |

### Pillar 2: Hardware
| Paper | Why cite | DOI/PMCID |
|-------|----------|-----------|
| **Baronetto et al. 2024** — EffUNet on GastroDigitalShirt | Your closest technical reference. 16 kHz, 136h data | PMC11269970 |
| **PMUT monitor 2022** — High-sensitivity bowel sound monitor | Alternative sensor approach, -142.69 dB | PMC9787765 |
| **Zauli et al. 2023** — Microphone technologies for digital auscultation | Validates MEMS approach | PMC10673215 |

### Pillar 3: ML
| Paper | Why cite | DOI/PMCID |
|-------|----------|-----------|
| **Nowak et al. 2021** — Automated BS analysis: an overview | THE comprehensive review. 50+ years of research summarized | 10.3390/s21165294 |
| **Yu et al. 2024** — Branchformer + self-supervised | Best for limited data (your early stage) | PMC11687808 |
| **Sood et al. 2025** — AI-powered BS for IBD (Mayo Clinic review) | 88-96% accuracy, latest evidence | 10.3390/medsci13040230 |

### Pillar 4: Ayurveda × Microbiome
| Paper | Why cite | DOI/PMCID |
|-------|----------|-----------|
| **Singh & Rao 2026** — Agni and Gut Microbiota (BHU) | Sama/Manda ↔ microbiome diversity. March 2026, very fresh | 10.47552/ijam.v17i1.6388 |
| **Wallace 2020** — Microbiome from Modern Med & Ayurveda | Prakriti types have distinct microbiomes | PMC7559905 |
| **Mishra et al. 2024** — Gut Microbiota and Agni review | Conceptual framework for your Ayurvedic framing | VER 7(2) |

---

## What models/approaches to follow

### Follow: Du 2018 mathematical model
Your pipeline should be designed around the spring-mass-damping framework. This gives physical meaning to your 4 acoustic classes.

### Follow: EffUNet architecture (Baronetto 2024)
Don't build from scratch. Their GitHub has pretrained weights. Use their 16 kHz / 25ms frame / 128 Mel bins as YOUR starting spec.

### Follow: Self-supervised pre-training (Yu 2024)
For your limited Indian-gut dataset, use HuBERT/wav2vec 2.0 pre-training. You don't need 10k labels.

### Avoid: Pure 1D-CNN as final model
It works but EffUNet or Branchformer will outperform. Use 1D-CNN only for Edge Impulse deployment (nRF52840 can't run 18M params).

### Follow: Craine SSI biomarker
Your AGNI Score's "Bowel-sound rate vs baseline" (weight 0.40) is essentially tracking SSI. This is your strongest clinical signal.

---

## The honest science gap (be transparent about this)

**What IS proven:**
- Bowel sounds are real, measurable, and ML-classifiable ✓
- Sound-to-sound interval distinguishes IBS from healthy (91% sens) ✓
- Postprandial vs fasting patterns are distinguishable ✓
- Hardware exists (AbStats FDA-cleared, multiple academic prototypes) ✓
- Agni states correlate with microbiome composition ✓

**What is NOT yet proven:**
- That bowel sound features map onto the 4 Ayurvedic Agni states ✗
- That a consumer patch with a single MEMS mic matches research-grade arrays ✗
- That daily score / WhatsApp delivery changes health outcomes ✗

**Your pitch should say:**
> "The acoustics are proven. The Ayurvedic framing is a hypothesis we're validating. The device tells you your gut trend — not a diagnosis."

This makes you honest AND defensible.
