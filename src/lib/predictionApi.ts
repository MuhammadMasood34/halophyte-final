export type PredictionMode = 'grass_based' | 'mechanism_based';

export interface GrassOption {
  species: string;
  common_name: string;
  mechanism: string;
}

export interface PredictionMetadata {
  numeric_fields: string[];
  mechanism_options: string[];
  prediction_modes: PredictionMode[];
  available_species: GrassOption[];
}

export interface PredictionRequest {
  mode: PredictionMode;
  species: string | null;
  mechanism: string | null;
  known_field: string;
  known_value: number;
}

export interface SimilarGrass {
  species: string;
  common_name: string;
  mechanism: string;
  similarity_note: string;
}

export interface PredictionResponse {
  mode: PredictionMode;
  species: string | null;
  mechanism: string;
  known_field: string;
  known_value: number;
  dataset_known_value: number | null;
  difference: number | null;
  difference_percent: number | null;
  known_value_comparison: {
    dataset_known_value: number;
    user_known_value: number;
    difference: number;
    difference_percent: number | null;
  } | null;
  calculation_basis: {
    base_species_profile: boolean;
    regression_scope: string;
    method: string;
  } | null;
  predictions: Record<string, number>;
  similar_grasses: SimilarGrass[];
  model_used: string;
  note: string;
}

export function getPredictionMetadata() {
  return requestJson<PredictionMetadata>('/metadata');
}

export function getGrassOptions() {
  return requestJson<GrassOption[]>('/grasses');
}

export function predictValues(payload: PredictionRequest) {
  return requestJson<PredictionResponse>('/predict', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
import { requestJson } from './apiClient';
