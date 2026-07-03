[← All tutorials](../README.md) · [Home](../../README.md) · **English** | [中文](../zh/06-cloud-gpu-autodl.md)

# 6. Cloud GPU — AutoDL Guide

If you do not have a local GPU, rent one from [AutoDL](https://www.autodl.com/) for approximately ¥1–3 per hour. The guide below uses the **browser-based JupyterLab** — no additional software needed on your local machine.

> ⚠️ **Download the dataset to your local machine first** (see [2. Dataset Preparation](02-datasets.md)) before creating a cloud instance.

---

### 🖥️ Step 1 — Create a GPU instance

1. Register and log in at [https://www.autodl.com/](https://www.autodl.com/).
2. Click **租用 → GPU 云服务器**.
3. Choose a GPU with **≥ 24 GB VRAM** for the full dataset (e.g., RTX 4090 24 GB).
   - For the lightweight 8 m / 10 min dataset, **≥ 8 GB VRAM** is sufficient.
4. Select the base image: **PyTorch 2.0 → Python 3.8 (ubuntu20.04) → CUDA 11.8**.
5. Click **立即创建** and wait for the instance to start.

---

### 🌐 Step 2 — Open JupyterLab

On the instance overview page, click the **JupyterLab** button. Use the **terminal** (Launcher → Terminal) to run shell commands.

---

### 💻 Step 3 — Clone the repository

```bash
cd /root/autodl-tmp/
git clone https://github.com/holmescao/U-RNN
```

---

### 📥 Step 4 — Upload the dataset via SCP

Find your **SSH login command** on the AutoDL instance overview page, e.g.:

```
ssh -p 12345 root@connect.westb.seetacloud.com
```

> ⚠️ The host, port, and password above are **examples** — use your own dashboard values.

#### Linux / macOS

```bash
# Upload the dataset zip
scp -P 12345 /local/path/urbanflood24.zip root@connect.westb.seetacloud.com:/root/autodl-tmp/
# Or rsync for large folders (resumes on failure):
rsync -avz --progress -e "ssh -p 12345" /local/path/urbanflood24/ \
    root@connect.westb.seetacloud.com:/root/autodl-tmp/U-RNN/data/urbanflood24/
```

#### Windows (PowerShell)

```powershell
scp -P 12345 C:\path\to\urbanflood24.zip root@connect.westb.seetacloud.com:/root/autodl-tmp/
```

Or use [WinSCP](https://winscp.net/) with Protocol = SCP.

#### Unzip on the cloud instance

```bash
cd /root/autodl-tmp/
unzip urbanflood24.zip
mv urbanflood24 U-RNN/data/
ls U-RNN/data/urbanflood24/train/flood/    # verify
```

---

### ⚙️ Step 5 — Install dependencies

```bash
cd /root/autodl-tmp/U-RNN/code
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### 📥 Step 6 — Upload pre-trained weights (required for Step 7; skip if going straight to Step 8)

```bash
# On your local machine:
scp -P 12345 /local/path/checkpoint_939_0.000205376.pth.tar \
    root@connect.westb.seetacloud.com:/root/autodl-tmp/U-RNN/exp/20240202_162801_962166/save_model/
```

---

### 🔍 Step 7 — Quick inference with pre-trained weights ([Scenario A](04-inference.md))

```bash
cd /root/autodl-tmp/U-RNN/code
python test.py \
    --exp_config configs/location1_scratch.yaml \
    --timestamp  20240202_162801_962166
```

Results appear in `exp/20240202_162801_962166/figs/`.

---

### 🏋️ Step 8 — Training

See [5. Training](05-training.md) for full details on each scenario.

**Scenario B — UrbanFlood24 lightweight dataset (128×128×36, ~3.5 h on one 4090):**

```bash
cd /root/autodl-tmp/U-RNN/code
python main.py --exp_config configs/lite.yaml
```

**Scenario C — Futian (Shenzhen, 400×560×72, ~25 h on one 4090):**

```bash
cd /root/autodl-tmp/U-RNN/code

# First convert the LarNO dataset (one-time):
python tools/convert_larfno_data.py --dataset futian \
    --larfno_root /root/autodl-tmp/data/larfno_futian \
    --dst_root    ../data/larfno_futian

# Train:
python main.py --exp_config configs/futian_scratch.yaml
```

**Scenario C — UKEA (UK, 52×120×36, ~2 h on one 4090):**

```bash
cd /root/autodl-tmp/U-RNN/code

# First convert the LarNO dataset (one-time):
python tools/convert_larfno_data.py --dataset ukea \
    --larfno_root /root/autodl-tmp/data/larfno_ukea \
    --dst_root    ../data/ukea_8m_5min

# Train:
python main.py --exp_config configs/ukea_scratch.yaml
```

**Scenario D — Full-resolution per-location (500×500×360, ~6–12 h per location on one 4090):**

```bash
python main.py --exp_config configs/location1_scratch.yaml
python main.py --exp_config configs/location2_scratch.yaml
python main.py --exp_config configs/location3_scratch.yaml
```

---

### 💾 Step 9 — Download results

```bash
# On your local machine:
scp -P 12345 -r root@connect.westb.seetacloud.com:/root/autodl-tmp/U-RNN/exp/ \
    /local/path/results/
```

---

Prev: [← 5. Training](05-training.md) · Next: [7. Reference →](07-reference.md)
