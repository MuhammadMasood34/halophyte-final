# Machine-learning assets

`data/`, `models/`, and `notebooks/` support the 30-record grass prediction workflow. `crop_salinity/` is a separate species-specific crop yield workflow built from the verified 241-row crop salinity dataset.

- `data/halophyte_grass_library.csv` — production grass dataset.
- `models/best_model_bundle.joblib` — production grass prediction bundle.
- `models/model_comparison_results.csv` and `model_metrics_summary.json` — evaluation results.
- `notebooks/grass_prediction_model_training.ipynb` — grass model comparison and training notebook.
- `crop_salinity/inference/` — production crop screening code.
- `crop_salinity/training/` — offline dataset reconstruction and surrogate training.

Production services load saved artifacts directly and never execute notebooks.
