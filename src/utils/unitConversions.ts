export type UnitConversionId = 'ds-to-ms' | 'ds-to-us' | 'na-to-mg-g' | 'cl-to-mg-g' | 'k-to-mg-g';

export type UnitConversionOption = {
  value: UnitConversionId;
  label: string;
  outputUnit: string;
  convert: (value: number) => number;
};

export const UNIT_CONVERSION_OPTIONS: UnitConversionOption[] = [
  {
    value: 'ds-to-ms',
    label: 'GR50 dS/m to mS/cm',
    outputUnit: 'mS/cm',
    convert: (value) => value,
  },
  {
    value: 'ds-to-us',
    label: 'GR50 dS/m to µS/cm',
    outputUnit: 'µS/cm',
    convert: (value) => value * 1000,
  },
  {
    value: 'na-to-mg-g',
    label: 'Na+ mmol kg^-1 to mg/g DW',
    outputUnit: 'mg/g DW',
    convert: (value) => (value * 22.99) / 1000,
  },
  {
    value: 'cl-to-mg-g',
    label: 'Cl- mmol kg^-1 to mg/g DW',
    outputUnit: 'mg/g DW',
    convert: (value) => (value * 35.45) / 1000,
  },
  {
    value: 'k-to-mg-g',
    label: 'K+ mmol kg^-1 to mg/g DW',
    outputUnit: 'mg/g DW',
    convert: (value) => (value * 39.1) / 1000,
  },
];
