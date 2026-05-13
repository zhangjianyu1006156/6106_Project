# AN6106 Food Delivery Optimization Project

This repository is organized by function:

| Folder | Purpose |
|---|---|
| `data/processed/` | Cleaned scenario datasets prepared for optimization |
| `src/` | Reusable Python functions for routing, evaluation, and plotting |
| `scripts/` | Runnable project scripts |
| `notebooks/` | Notebook version of the Member 3 computational workflow |
| `outputs/tables/` | Generated CSV validation, result, route, and sensitivity tables |
| `outputs/figures/` | Generated route and comparison figures |
| `docs/reports/` | Member reports and report PDF |
| `docs/guides/` | Start guides, follow-up checklist, and model confirmation notes |
| `docs/slides/` | Slide outlines for presentation preparation |

## Reproduce Member 3 Results

From the project root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/member3_run_experiment.py
```

The script writes updated tables to `outputs/tables/` and figures to `outputs/figures/`.

## Data Cleaning

If the raw `Zomato Dataset.csv` file is available in the project root, rerun Member 1 data preparation with:

```bash
.venv/bin/python scripts/member1_data_cleaning.py
```
