[← All tutorials](../README.md) · [Home](../../README.md) · **English** | [中文](../zh/08-faq.md)

# 8. FAQ

**Q: Which scenario should I start with?**

A: Follow this order:
1. **[Scenario A — Inference](04-inference.md)** — run inference with the pre-trained weights to verify your setup (requires full dataset, ~5 min).
2. **[Scenario B — Lightweight training](05-training.md)** — train on the lightweight dataset (~3.5 h) to confirm the training pipeline works end-to-end.
3. **[Scenario C — LarNO training](05-training.md)** — train on LarNO datasets (Futian or UKEA) with pre-converted data.
4. **[Scenario D — Full training](05-training.md)** — full training to reproduce paper accuracy (~40 hours).

---

**Q: Training is very slow. How can I speed it up?**

A: Three main levers:
1. **Reduce spatiotemporal resolution** — use `tools/downsample_dataset.py` to create a downsampled dataset. A 4× spatial + 10× temporal reduction gives ~50× speedup ([Scenario B](05-training.md)).
2. **Reduce epochs** — 1000 epochs is the default for all configs. You may try fewer epochs for preliminary experiments, but the model requires sufficient training to converge properly.
3. **Enable gradient checkpointing** — add `--use_checkpoint` to reduce GPU memory and allow larger `--seq_num`.

---

**Q: I get CUDA out-of-memory during training. What can I do?**

A: Try any of the following:
- Add `--use_checkpoint` (gradient checkpointing; already enabled in experiment YAMLs).
- Reduce `--seq_num` (e.g., from 28 to 14) to shorten each backward pass.
- Use the lightweight dataset ([Scenario B](05-training.md)) to reduce input size.
- Reduce `--batch_size` (default is already 1).

---

**Q: What do I need to change when using my own dataset?**

A: You need to:
1. Prepare data files: `flood.npy` (T, H, W), `rainfall.npy` (T,) or (T, H, W), and geodata files.
2. Put them under `data/<your_dataset>/train/flood/<location>/` and `geodata/<location>/`.
3. Create event list files `src/lib/dataset/<your>_train.txt` and `<your>_test.txt`.
4. Copy an existing config (e.g., `configs/lite.yaml`) to `configs/custom.yaml` and update `data_root`, `input_height`, `input_width`, `window_size`, `duration`, and normalization constants.

---

**Q: How do I evaluate on a new location?**

A: Train the model from scratch for that location (providing matching `train.txt` / `test.txt`). The architecture parameters (filter sizes, number of stages) do not depend on location and can be reused. Only normalization constants may need tuning for significantly different rainfall regimes.

---

**Q: How do I run single-GPU vs multi-GPU training?**

A: The same `main.py` entry point supports both modes automatically:
- **Single GPU**: `python main.py --exp_config ...` — no launcher needed.
- **Multi-GPU (DDP)**: `torchrun --nproc_per_node=N main.py --exp_config ...` — `torchrun` sets `LOCAL_RANK`/`RANK`/`WORLD_SIZE` automatically.

**Important — `batch_size` scaling rule:** `batch_size` in the config is the per-GPU batch size.
The effective batch size = `batch_size × N` (number of GPUs).
**Set `batch_size` equal to the number of GPUs you are using** so that the effective batch
size scales proportionally with GPU count (e.g. 2 GPUs → `batch_size: 2`, 4 GPUs → `batch_size: 4`).

Note: `python -m torch.distributed.launch` (deprecated since PyTorch 1.9) also still works.

---

**Q: Multi-GPU training doesn't work on Windows.**

A: The NCCL backend requires Linux. On Windows, use single-GPU (`python main.py ...`) or WSL2 for multi-GPU.

---

**Q: test.py says it can't find the checkpoint.**

A: The `--timestamp` must match exactly the directory name under `exp/`. Check that `exp/<timestamp>/save_model/` contains at least one `checkpoint_*.pth.tar` file.

---

**Q: How do I change the visualization time points?**

A: Pass `--viz_time_points 0 60 120 180` (space-separated integers, zero-indexed). Make sure all indices are within `[0, window_size - 1]`. For the lightweight dataset (36 steps), use `--viz_time_points 0 11 23 35`.

---

**Q: How do I use spatial (heterogeneous) rainfall?**

A: Store `rainfall.npy` as shape `(T, H, W)` instead of `(T,)`. The dataset loader detects the shape automatically — no config change needed. Futian and UKEA configs already use spatial rainfall.

---

**Q: Does the code require exactly torch==2.0.0?**

A: No. PyTorch 2.0.0 is the version tested on the development machine, but the code is compatible with PyTorch 2.1.x and later. If your environment already has a newer PyTorch version, you do not need to downgrade.

---

**Q: I only have a subset of the test events (e.g., 1 event). Can I still run inference?**

A: Yes. Create a custom test list file with just the event names you have:

```bash
echo 'r100y_p0.5_d3h' > code/src/lib/dataset/demo_test.txt
```

Then pass it to `test.py`:

```bash
python test.py --exp_config configs/lite.yaml \
               --timestamp 20260316_130418_443889 \
               --test_list_file ./src/lib/dataset/demo_test.txt
```

---

Prev: [← 7. Reference](07-reference.md) · [Back to all tutorials](../README.md)
