[← All tutorials](../README.md) · [Home](../../README.md) · **English** | [中文](../zh/05-training.md)

# 5. Training

U-RNN supports three training scenarios, from a fast sanity check to full paper reproduction. Pick the one that matches your hardware and goal:

| Scenario | Dataset | Grid × Steps | Time (RTX 4090) | Use it to… |
|---|---|---|---|---|
| **B — Lightweight** | UrbanFlood24 Lite | 128×128 × 36 | ~3.5 h | verify the pipeline fast (recommended start) |
| **C — LarNO** | Futian / UKEA | 400×560 / 52×120 | 2–25 h | train on the LarNO benchmark catchments |
| **D — Full** | UrbanFlood24 | 500×500 × 360 | ~6–12 h / location | reproduce paper accuracy |

> All paths assume you run from the inner `code/` directory. Datasets are prepared in [2. Dataset Preparation](02-datasets.md).

---

## Scenario B — Lightweight Training (Fast Iteration)

> **Requirements:** UrbanFlood24 Lite dataset ([2. Dataset Preparation](02-datasets.md)) &nbsp;|&nbsp; ≥ 8 GB VRAM &nbsp;|&nbsp; ~3.5 h on RTX 4090 (1000 epochs)

This scenario trains on the **128×128 × 36 steps** lightweight dataset (~50× smaller than full resolution). It is the recommended starting point for verifying your setup before committing to full training.

Download the lite dataset ([2. Dataset Preparation](02-datasets.md)), then:

```bash
cd code   # the inner code directory
python main.py --exp_config configs/lite.yaml
```

### Multi-GPU (DDP via torchrun)

```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --nproc_per_node=2 main.py \
    --exp_config configs/lite.yaml
```

> DDP gradients are averaged automatically across GPUs; effective batch size = `batch_size × world_size`. Linux only (NCCL backend). On Windows use single-GPU.

### Outputs

The script creates `exp/<timestamp>/` with:

```
exp/<timestamp>/
├── save_model/     ← model checkpoints (.pth.tar)
├── save_train_loss/
├── save_res_data/
└── figs/           ← test visualizations (if test: true in config)
```

Note the generated `<timestamp>` — you will need it to run inference on your own trained model:

```bash
python test.py --exp_config configs/lite.yaml \
               --timestamp  <your_timestamp>
```

---

## Scenario C — LarNO Datasets Training (Futian & UKEA)

> **Requirements:** LarNO dataset ([2. Dataset Preparation](02-datasets.md)) &nbsp;|&nbsp; ≥ 8–16 GB VRAM &nbsp;|&nbsp; 2–25 h on RTX 4090

### Futian (Shenzhen, China)

> ~25 h on RTX 4090 (1000 epochs, 400×560 grid)

```bash
cd code   # the inner code directory

# First convert the LarNO dataset (one-time):
python tools/convert_larfno_data.py --dataset futian \
    --larfno_root /path/to/larfno/futian \
    --dst_root    ../data/larfno_futian

# Train:
python main.py --exp_config configs/futian_scratch.yaml
```

### UKEA (UK)

> ~2 h on RTX 4090 (1000 epochs, 52×120 grid)

```bash
# First convert the LarNO dataset (one-time):
python tools/convert_larfno_data.py --dataset ukea \
    --larfno_root /path/to/larfno/ukea \
    --dst_root    ../data/ukea_8m_5min

# Train:
python main.py --exp_config configs/ukea_scratch.yaml
```

### Multi-GPU (DDP via torchrun)

```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --nproc_per_node=2 main.py \
    --exp_config configs/futian_scratch.yaml
```

> DDP gradients are averaged automatically across GPUs; effective batch size = `batch_size × world_size`. Linux only (NCCL backend). On Windows use single-GPU.

---

## Scenario D — Full Training (Paper Results)

> **Requirements:** full UrbanFlood24 dataset ([2. Dataset Preparation](02-datasets.md)) &nbsp;|&nbsp; ≥ 16 GB VRAM per location &nbsp;|&nbsp; ~6–12 h per location on RTX 4090 (1000 epochs)

U-RNN trains on **one location at a time**. To reproduce paper results, train each location separately:

```bash
cd code   # the inner code directory

python main.py --exp_config configs/location1_scratch.yaml
python main.py --exp_config configs/location2_scratch.yaml
python main.py --exp_config configs/location3_scratch.yaml
```

### Multi-GPU (DDP via torchrun)

```bash
CUDA_VISIBLE_DEVICES=0,1 torchrun --nproc_per_node=2 main.py \
    --exp_config configs/location1_scratch.yaml
```

### Inference on your trained model

```bash
python test.py --exp_config configs/location1_scratch.yaml \
               --timestamp  <your_timestamp>
```

---

Prev: [← 4. Inference](04-inference.md) · Next: [6. Cloud GPU — AutoDL Guide →](06-cloud-gpu-autodl.md)
