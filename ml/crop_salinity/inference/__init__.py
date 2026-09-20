"""Production inference code for crop salinity screening."""

from .crop_prediction import is_model_trained, predict_multiple_crops, predict_yield

__all__ = ["is_model_trained", "predict_multiple_crops", "predict_yield"]
