# Changelog

All notable changes to U-RNN are documented here.

---

## [1.2.0] — 2026-05

### Added
- **Bilingual reproduction tutorials** under [`tutorials/`](tutorials/README.md): 8 intent-based guides (installation, datasets, weights, inference, training, cloud GPU, reference, FAQ) in both English (`tutorials/en/`) and 中文 (`tutorials/zh/`), with a language router at `tutorials/README.md`
- **`README_CN.md`**: Chinese landing page mirroring the slimmed README; language switcher between `README.md` ↔ `README_CN.md`
- **`code/tools/check_doc_links.py`**: dependency-free documentation link checker (relative links, image paths, heading anchors, stale-reference sweep)

### Changed
- **README slimmed from 972 → ~150 lines** — now a welcoming landing page (hero, one-line value proposition, collapsible News, architecture, Quick Start, performance highlights, an intent-based Documentation table, citation). All step-by-step depth moved verbatim into `tutorials/`
- Re-pointed cross-references that targeted README sections to the new tutorial files: `code/.github/ISSUE_TEMPLATE/bug_report.yml` (FAQ link + scenario dropdown), `code/notebooks/quickstart.ipynb`, `code/requirements_tensorrt.txt`, `code/configs/lite.yaml`, `CONTRIBUTING.md`

### Removed
- **Repository hygiene** — deleted internal development doc `code/docs/dataset_knowledge.md` (contained local-only paths) and 51 committed `__pycache__/*.pyc` bytecode files; tightened `.gitignore` (`__pycache__/`, `*.py[cod]`, `*.egg-info/`, `build/`, `dist/`, `.ipynb_checkpoints/`, `.DS_Store`)

### Fixed
- Pre-existing broken relative links that resolved to the repo root instead of `code/`: README `notebooks/`/`configs/` links, `CHANGELOG.md` Futian/UKEA config links, and `CONTRIBUTING.md` issue-template links now point under `code/`
- `CONTRIBUTING.md` developer-setup path corrected (`cd U-RNN/U-RNN` → `cd U-RNN/code`)

---

## [1.1.0] — 2026-03

### Added
- **Multi-dataset support**: train on [Futian](code/configs/futian_scratch.yaml) (Shenzhen, 20 m/5 min, 400×560) and [UKEA](code/configs/ukea_scratch.yaml) (UK, 8 m/5 min, 52×120) via LarFNO benchmark data
- **`configs/location2_scratch.yaml`**: ready-made config for UrbanFlood24 location2 lightweight training (125×125, 200 epochs)
- **`pyproject.toml`**: installable package (`pip install -e .`); adds `urnn-train` and `urnn-test` CLI entry points
- **Visualization upgrade**: `test.py` now produces a 3-row **Reference / U-RNN / Absolute Error** comparison figure with fixed colorbars (0–2 m depth, 0–0.3 m error)
- **Ablation results**: `prewarming=false` with 200 epochs achieves **R²=0.989** on the lightweight dataset (vs 0.943 for `prewarming=true` at 300 epochs)
- **Metrics comparison tool**: `tools/compare_metrics.py` — U-RNN vs LarFNO comparison with LaTeX table output
- **Dataset conversion tool**: `tools/convert_larfno_data.py` — converts LarFNO Futian/UKEA data to U-RNN format
- **GitHub infrastructure**: issue templates (bug report, feature request), CI workflow (import + config check across Python 3.8–3.10)
- **CONTRIBUTING.md**: contribution guidelines and new-dataset workflow
- `requirements_tensorrt.txt`: TensorRT-only dependencies split from core `requirements.txt`
- **Colab notebook**: `notebooks/quickstart.ipynb` — end-to-end demo in < 5 minutes, no local GPU required
- **🤗 Hugging Face Hub**: model page at `holmescao/U-RNN` (coming soon)

### Changed
- **`configs/lite.yaml`**: `epochs` corrected from 300 → **200** (200 epochs with `prewarming=false` achieves R²=0.989, outperforming 300-epoch baseline); added explicit `location: location1` and event list files for reproducibility
- **`configs/location2_scratch.yaml`**: `input_height`/`input_width` corrected from 128 → **125** (matches `downsample_dataset.py --spatial_factor 4` output: 500÷4=125)
- **`configs/`** root cleaned up: ablation / fine-tuning / transfer-learning experiment YAMLs moved to `configs/experiments/`
- **README**: restructured to 15 sections (removed duplicate Performance section and Scenario D); added Colab callout, HF Hub badge, `pip install -e .` note, and LarFNO dataset news
- `requirements.txt`: removed TensorRT and Apex deps (now in `requirements_tensorrt.txt`); pinned `openpyxl>=3.0.10`
- Default training recommendation: **200 epochs, `prewarming=false`** (previously 300 epochs)

### Fixed
- `main.py` `scheduler_update()`: added `WarmUpCosineAnneal_v2` to the step-update branch — the v2 scheduler was created but `.step()` was never called, causing the learning rate to remain constant at the initial value throughout training
- `Dynamic2DFlood._prepare_input`: spatial rainfall `(T,H,W)` now correctly handled (previously treated as scalar)
- `Dynamic2DFlood._prepare_target`: flood `(T,1,H,W)` → `(T,H,W)` squeeze
- `test.py compute_metrics`: added torch→numpy conversion guard
- `net_params.py`: decoder GRU input_channels formula corrected
- `model.py`: `reg_output_t` indexing fixed (`[:, :, 0]` not `[:, :, 0:1]`)
- `main.py` `WarmUpCosineAnneal`: fixed warmup/cosine formula (removed spurious `/0.1` division)

---

## [1.0.0] — 2025-04 (Paper Release)

### Added
- Initial public release accompanying the *Journal of Hydrology* 2025 paper
- U-RNN architecture: U-Net Encoder-Decoder with multi-scale ConvGRU
- SWP (Sliding Window Pre-warming) training paradigm
- UrbanFlood24 dataset support (4 locations, 500×500, 2 m/1 min)
- Pre-trained weights for location1 (1000 epochs)
- TensorRT inference support (`urnn_to_tensorrt.py`)
- AutoDL cloud GPU guide
