# AGNI Research Pipeline — Live on Hermes

## Summary of fresh findings (June 2026)

### Pillar 1 — Acoustic sensing
| Paper | Key takeaway | Your pipeline connection |
|-------|-------------|-------------------------|
| **PMUT monitor** (Micromachines 2022) PMC9787765 | PMUT array achieves −142.69 dB sensitivity, 50 dB noise resolution at 100 Hz, better than condenser mics | Validates the 100–500 Hz bandpass and confirms MEMS approach works for bowel sounds |
| **EffUNet spotting** (JMIR AI 2024) PMC11269970 | 136h annotated wearable data, EffUNet (EfficientNet-B2 + U-Net), 25ms temporal resolution, 18.1M params | **Closest to your pipeline.** Use this architecture, not vanilla 1D-CNN. Public dataset. |
| **Branchformer** (PLOS ONE 2024) PMC11687808 | Self-supervised pre-training (HuBERT/wav2vec 2.0) + Branchformer architecture. Excels under data-limited conditions. | **Use this for your early-dataset problem.** Self-supervised means you don't need 10k+ labeled samples. |

**IMPORTANT: The EffUNet paper used a GastroDigitalShirt with 8x SPH0645LM4H-B mics at 16 kHz — the same sampling rate as your INMP441. Their GitHub is at github.com/AI4HealthUOL/bowel-sound-classification — you can use their model weights.**

### Pillar 2 — Ayurveda × microbiome
| Paper | Key takeaway |
|-------|-------------|
| **Agni ↔ Microbiome** (Vascular Endovasc Rev 2024) | Sama/Manda map directly to microbiome diversity. Not acoustic → Agni link proven, but the conceptual framework exists in peer-reviewed lit. |
| **Agni & Gut Microbiota** (IJAM 2026) Banaras Hindu Univ | Mandagni = reduced microbial diversity, ↓ SCFAs. Sama Agni = high diversity. **This paper is from March 2026 — very recent.** |
| **Microbiome from Modern Med & Ayurveda** (Medicina 2020) PMC7559905 | Prakriti types have distinct microbiomes. Agni ↔ digestive enzymes + microbiome metabolic activity. Ama ↔ LPS/leaky gut products. |

### New architectures to consider
| Architecture | Why better than 1D-CNN |
|-------------|------------------------|
| **EffUNet** (EfficientNet-B2 + UNet decoder) | 18.1M params, pretrained on AudioSet, handles extreme class imbalance (BS ratio = 0.0089) |
| **Branchformer + self-supervised** | Excels with limited labeled data — perfect for your early prototype |
| **BowelRCNN** (arXiv 2025) | CNN + region-based detection, latest architecture |

---

## Models to use (in your Hermes session)

### For literature research
```
/skill arxiv
Search: "bowel sound classification wearable" 
Search: "Agni Ayurveda microbiome gut dysbiosis"
```

### For code/ML pipeline
```
hermes skills install system-debugging
# Use Claude Sonnet 4 or GPT-4o for Python DSP coding
# Use Gemini 2.5 Pro for signal-processing math
```

### For content generation (patient-facing, investor docs)
- `nous/hermes-3-llama-3.1-405b` — you're already on Nous subscription, free to use
- `anthropic/claude-sonnet-4` — best for scientific writing
- `google/gemini-2.5-pro` — long context for reading full papers

---

## Immediate actions (this session)

1. Fork/use the EffUNet codebase: `github.com/AI4HealthUOL/bowel-sound-classification`
2. Download the public Kaggle bowel sound dataset (Ficek et al. 2021) used by Branchformer paper
3. Set up Python DSP pipeline: `pip install librosa scipy soundfile edge-impulse-linux`
4. Record ~2h of your own abdomen (INMP441 + XIAO → laptop) to build first test dataset
