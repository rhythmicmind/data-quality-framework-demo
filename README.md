# Data Quality Framework Demo

A small structured-data quality pipeline with validation rules, robust amount outliers, remediation recommendations, and population stability index drift.

## Project status

New portfolio implementation prepared in October 2026 with coding-assistant support.
This is not a historical project submission, employer deliverable, or deployed system.
The bundled data is synthetic. See [DATA_CARD.md](DATA_CARD.md) before interpreting outputs.

## Run locally

Python 3.11 is recommended. From this repository folder:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python quality.py
python -m pytest -q
python -m streamlit run app.py
```

Commands use paths relative to the repository root. Outputs are written to `results/`.
The Streamlit app reads local sample data until a CSV is uploaded (where supported).
CSV exports can contain source text; review sensitive content before sharing them.

## Design

The core module is usable without Streamlit. The CLI exports machine-readable results;
the dashboard provides an interactive view. Tests exercise failure cases and invariants,
including duplicate handling, invalid inputs, and distribution checks where applicable.
The original inputs are preserved. There is no automatic overwrite of source data.

## Results and limitations

Example outputs in `results/` were generated from the bundled synthetic data.
They demonstrate execution, not real-world accuracy. Dependency lower/upper bounds
support installation; `results/environment.txt` records the actual validation environment.
Run the commands yourself before presenting or extending this project.

## Next steps

Read the code, explain each decision, and replace fixtures with appropriately licensed
data. Keep a record of your experiments, review failures, and add results from a real
held-out dataset where relevant. Document changes and remaining limitations.

## License

Code: MIT. External datasets retain their own licenses and attribution requirements.
