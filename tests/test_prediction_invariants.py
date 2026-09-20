from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"
for import_path in (PROJECT_ROOT, BACKEND_DIR):
    path_text = str(import_path)
    if path_text not in sys.path:
        sys.path.insert(0, path_text)

from biosaline_service import biosaline_predict, biosaline_status  # noqa: E402
from model_loader import NUMERIC_FIELDS, resources  # noqa: E402
from prediction_service import predict  # noqa: E402
from schemas import PredictionRequest  # noqa: E402


class GrassPredictionTests(unittest.TestCase):
    def test_dataset_and_model_bundle_load(self) -> None:
        self.assertEqual(len(resources.dataset), 30)
        self.assertTrue(resources.dataset_loaded)
        self.assertTrue(resources.model_loaded)

    def test_selected_species_is_preserved(self) -> None:
        species = str(resources.dataset.iloc[0]["species"])
        response = predict(
            PredictionRequest(
                mode="grass_based",
                species=species,
                known_field="na_shoot",
                known_value=100.0,
            )
        )
        self.assertEqual(response["species"], species)
        self.assertEqual(response["mode"], "grass_based")

    def test_ion_inputs_do_not_change_species_gr50(self) -> None:
        species_row = resources.dataset.iloc[0]
        expected_gr50 = round(float(species_row["gr50_avg"]), 3)

        for known_field in (field for field in NUMERIC_FIELDS if field != "gr50_avg"):
            with self.subTest(known_field=known_field):
                response = predict(
                    PredictionRequest(
                        mode="grass_based",
                        species=str(species_row["species"]),
                        known_field=known_field,
                        known_value=float(species_row[known_field]) + 250.0,
                    )
                )
                self.assertEqual(response["predictions"]["gr50_avg"], expected_gr50)

    def test_mechanism_prediction_uses_requested_group(self) -> None:
        response = predict(
            PredictionRequest(
                mode="mechanism_based",
                mechanism="Salt-Secreting",
                known_field="gr50_avg",
                known_value=20.0,
            )
        )
        self.assertEqual(response["mechanism"], "Salt-Secreting")
        self.assertTrue(response["similar_grasses"])


class CropSalinityTests(unittest.TestCase):
    def test_verified_dataset_is_available(self) -> None:
        status = biosaline_status()
        self.assertTrue(status["available"], status["setup_error"])
        self.assertEqual(status["dataset"]["rows"], 241)
        self.assertEqual(status["dataset"]["species_count"], 6)

    def test_crop_gr50_is_constant_across_environment_inputs(self) -> None:
        cool_wet = biosaline_predict(
            {"crop_id": "wheat", "ec_soil": 2, "temperature": 20, "rainfall_mm": 600}
        )
        hot_dry = biosaline_predict(
            {"crop_id": "wheat", "ec_soil": 20, "temperature": 44, "rainfall_mm": 60}
        )
        self.assertEqual(cool_wet["crop"]["gr50"], hot_dry["crop"]["gr50"])


if __name__ == "__main__":
    unittest.main()
