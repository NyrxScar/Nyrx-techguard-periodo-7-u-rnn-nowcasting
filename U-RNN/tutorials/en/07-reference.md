[← All tutorials](../README.md) · [Home](../../README.md) · **English** | [中文](../zh/07-reference.md)

# 7. Reference — Project Structure & Outputs

## Project Structure

```
U-RNN/
├── data/                               ← populate after downloading
│   └── urbanflood24/
│       ├── train/
│       │   ├── flood/<location>/<event>/
│       │   │   ├── flood.npy           (T, H, W) metres
│       │   │   └── rainfall.npy        (T,) or (T, H, W) mm/step
│       │   └── geodata/<location>/
│       │       ├── absolute_DEM.npy    (H, W) metres
│       │       ├── impervious.npy      (H, W) fraction
│       │       └── manhole.npy         (H, W) binary
│       └── test/                       ← same structure
│
├── exp/                                ← auto-created during training
│   └── <timestamp>/
│       ├── save_model/                 ← checkpoints (.pth.tar)
│       ├── save_train_loss/
│       ├── save_res_data/
│       └── figs/epoch@<N>/            ← inference visualizations (PNG)
│
└── code/                               ← run all scripts from here
    ├── main.py                         ← training entry point
    ├── test.py                         ← inference entry point
    ├── config.py                       ← all hyperparameters (argparse + YAML)
    ├── pyproject.toml                  ← package definition (pip install -e .)
    ├── urnn_to_tensorrt.py             ← PyTorch → TensorRT conversion
    ├── requirements.txt
    ├── notebooks/
    │   └── quickstart.ipynb            ← Colab quickstart notebook
    ├── configs/
    │   ├── lite.yaml               ← lightweight UrbanFlood24 (recommended start) ⭐
    │   ├── location1_scratch.yaml  ← UrbanFlood24 location1 from scratch
    │   ├── location2_scratch.yaml  ← UrbanFlood24 location2 from scratch
    │   ├── location3_scratch.yaml  ← UrbanFlood24 location3 from scratch
    │   ├── futian_scratch.yaml     ← Futian (Shenzhen) from scratch
    │   ├── ukea_scratch.yaml       ← UKEA (UK) from scratch
    │   ├── network.yaml            ← model architecture shapes (rarely changed)
    │   ├── defaults/               ← internal defaults (do not edit)
    │   │   ├── training.yaml
    │   │   └── data.yaml
    │   └── experiments/            ← ablation / research configs (not for general use)
    ├── tools/
    │   ├── downsample_dataset.py       ← lightweight dataset generator
    │   ├── convert_larfno_data.py      ← LarNO → U-RNN format converter
    │   └── compare_metrics.py          ← U-RNN vs baseline metrics comparison
    │
    └── src/lib/
        ├── dataset/
        │   ├── Dynamic2DFlood.py       ← data loading (supports scalar + spatial rain)
        │   ├── train.txt               ← UrbanFlood24 training event list (all locations)
        │   ├── test.txt                ← UrbanFlood24 test event list (all locations)
        │   ├── location1_train.txt / location1_test.txt
        │   ├── location2_train.txt / location2_test.txt
        │   ├── location3_train.txt / location3_test.txt
        │   ├── futian_train.txt / futian_test.txt
        │   └── ukea_train.txt / ukea_test.txt
        ├── model/
        │   ├── networks/
        │   │   ├── model.py            ← ED (Encoder-Decoder) architecture
        │   │   ├── encoder.py          ← multi-scale encoder with ConvGRU
        │   │   ├── decoder.py          ← multi-scale decoder with ConvGRU
        │   │   ├── ConvRNN.py          ← ConvLSTM / ConvGRU cell
        │   │   ├── net_params.py       ← architecture configuration
        │   │   ├── losses.py           ← FocalBCE_and_WMSE loss
        │   │   └── head/flood_head.py  ← dual-output head (reg + cls)
        │   └── earlystopping.py
        └── utils/
            ├── distributed_utils.py    ← multi-GPU DDP utilities
            └── general.py
```

---

## Outputs

### Training Logs

Training prints per-epoch loss and saves checkpoints to `exp/<timestamp>/save_model/`.

Example log line:
```
[ 939/1000] loss:0.000205376 | loss_reg:... | loss_cls:... | time:42.31 sec
```

### Inference Visualizations

For each test event, `test.py` saves a 3-row PNG to:

```
exp/<timestamp>/figs/epoch@<N>/
└── <event_name>/
    └── water_depth_spatial_temporal.png
```

**Figure layout:** Row 1 = Reference (ground truth), Row 2 = U-RNN prediction, Row 3 = Absolute error. Rows 1–2 share a fixed 0–2 m colorbar; Row 3 uses 0–0.3 m.

### Metrics

Per-event metrics (R², RMSE, MAE, CSI) are saved to `exp/<timestamp>/metrics/metrics_epoch<N>.xlsx`.

---

Prev: [← 6. Cloud GPU — AutoDL Guide](06-cloud-gpu-autodl.md) · Next: [8. FAQ →](08-faq.md)
