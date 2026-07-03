[← All tutorials](../README.md) · [Home](../../README.md) · **English** | [中文](../zh/01-installation.md)

# 1. Installation

💻 **Step 1 — Clone the repository**

```bash
git clone https://github.com/holmescao/U-RNN
cd U-RNN
```

💻 **Step 2 — Create a conda environment**

```bash
conda create -n urnn python=3.8
conda activate urnn
```

💻 **Step 3 — Install PyTorch**

Install **PyTorch 2.0.0 with CUDA 11.8** (tested on NVIDIA RTX 4090):

```bash
pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 \
    --index-url https://download.pytorch.org/whl/cu118
```

> 🇨🇳 China users — add the Tsinghua mirror for faster pip downloads (PyTorch must still be installed from the official wheel URL above):
> ```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

💻 **Step 4 — Install project dependencies**

```bash
cd code   # the inner code directory
pip install -r requirements.txt
```

> 📦 **Alternative — install as a package:**
> ```bash
> pip install -e .   # editable install from pyproject.toml
> ```
> This makes `urnn-train` and `urnn-test` available as CLI commands.

> **TensorRT inference (optional):** also run `pip install -r requirements_tensorrt.txt` — only needed for the TensorRT section of [04-inference.md](04-inference.md).

✅ **Step 5 — Verify the installation**

```bash
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
# Expected: 2.0.0+cu118 True
```

> **Other CUDA versions** — other PyTorch + CUDA combinations will also work; check [pytorch.org](https://pytorch.org/get-started/locally/) for the matching install command.

---

Next: [2. Dataset Preparation →](02-datasets.md)
