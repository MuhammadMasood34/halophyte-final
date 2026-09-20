# Crop salinity model

This package contains the crop-specific salinity response logic used by the Crop Salinity Screening module.

- `data/source/AuthenticHalophyteData.xlsx` is the verified 241-row source dataset.
- `config/crops.yaml` stores Maas–Hoffman thresholds, slopes, GR50 values, yield potentials, and citations.
- `inference/` contains production prediction and fallback logic.
- `training/train_surrogate.py` trains one surrogate per supported crop.
- `models/` contains metadata and any locally trained serialized artifacts.

Train only when intentionally updating model artifacts:

```powershell
python -m ml.crop_salinity.training.train_surrogate
```

Normal application startup does not retrain models.
