[← All tutorials](../README.md) · [Home](../../README.md) · **English** | [中文](../zh/03-pretrained-weights.md)

# 3. Pre-trained Weights

We provide pre-trained checkpoints for all supported datasets.

| Checkpoint | Dataset | Grid | Epochs | R² | Size |
|---|---|---|---|---|---|
| **Location1 full-res** ⭐ | UrbanFlood24 location1 | 500×500 | 1000 | paper accuracy | ~300 MB |
| **Location1 lite** | UrbanFlood24 Lite location1 | 128×128 | 1000 | 0.989 | ~20 MB |
| **Futian** | Futian (Shenzhen) | 400×560 | 1000 | 0.888 | ~141 MB |
| **UKEA** | UKEA (UK) | 52×120 | 1000 | 0.896 | ~11 MB |

### Location1 full-res (500×500, paper accuracy)

| Mirror | Link |
|---|---|
| Google Drive | [Download (no password)](https://drive.google.com/file/d/1tfwRJ3gFFTa0kiziVeo9xXsz0DaaJrJU/view?usp=drive_link) |
| Baidu Cloud (code: `urnn`) | [Download](https://pan.baidu.com/s/1lIkKNMZy2GQqKmYCATtw1w) |
| 🤗 Hugging Face Hub | Not included (full-res weights are very large; use Google Drive above) |

### Location1 lite (128×128)

| Mirror | Link |
|---|---|
| Google Drive | [Download (no password)](https://drive.google.com/file/d/1ehvXWkLBMoa4Jvf4l_KtM734ZIaw_7DK/view?usp=sharing) |
| Baidu Cloud (code: `urnn`) | [Download](https://pan.baidu.com/s/1O2vRXe0HJ3iH3LaPBmzpPw?pwd=urnn) |
| 🤗 Hugging Face Hub | [Download](https://huggingface.co/holmescao/U-RNN/resolve/main/checkpoints/loc1_lite_weights.zip) |

### Futian — Shenzhen (400×560)

| Mirror | Link |
|---|---|
| Google Drive | [Download (no password)](https://drive.google.com/file/d/1jynGk6wbufjJpDV8sKhWu-sixKZ-ehDr/view?usp=sharing) |
| Baidu Cloud (code: `urnn`) | [Download](https://pan.baidu.com/s/1mV4RXSKyj7G3zmUQMHK5HQ?pwd=urnn) |
| 🤗 Hugging Face Hub | [Download](https://huggingface.co/holmescao/U-RNN/resolve/main/checkpoints/futian_weights.zip) |

### UKEA — UK (52×120)

| Mirror | Link |
|---|---|
| Google Drive | [Download (no password)](https://drive.google.com/file/d/1MuKPjLNvrE7_s_leO5uH4SVmQL4ebcA1/view?usp=sharing) |
| Baidu Cloud (code: `urnn`) | [Download](https://pan.baidu.com/s/1vuZLXU_a__6rYeq66YxN7Q?pwd=urnn) |
| 🤗 Hugging Face Hub | [Download](https://huggingface.co/holmescao/U-RNN/resolve/main/checkpoints/ukea_weights.zip) |

### Placement

Each archive follows the same `exp/<timestamp>/save_model/` structure. Extract and place as shown:

```
U-RNN/
└── exp/
    ├── 20240202_162801_962166/       ← location1 full-res
    │   └── save_model/
    │       └── checkpoint_939_0.000205376.pth.tar
    ├── 20260316_130418_443889/       ← location1 lite
    │   └── save_model/
    │       └── checkpoint_143_0.065581453.pth.tar
    ├── 20260316_134929_015563/       ← Futian
    │   └── save_model/
    │       └── checkpoint_198_0.112292888.pth.tar
    └── 20260316_153558_270657/       ← UKEA
        └── save_model/
            └── checkpoint_181_0.132711639.pth.tar
```

Pass the corresponding `--timestamp` when running inference:

```bash
# Location1 full-res
python test.py --exp_config configs/location1_scratch.yaml --timestamp 20240202_162801_962166

# Location1 lite
python test.py --exp_config configs/lite.yaml --timestamp 20260316_130418_443889

# Futian
python test.py --exp_config configs/futian_scratch.yaml --timestamp 20260316_134929_015563

# UKEA
python test.py --exp_config configs/ukea_scratch.yaml --timestamp 20260316_153558_270657
```

---

Prev: [← 2. Dataset Preparation](02-datasets.md) · Next: [4. Inference →](04-inference.md)
