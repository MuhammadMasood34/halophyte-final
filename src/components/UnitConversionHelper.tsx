import { useMemo, useState } from 'react';
import { Calculator } from 'lucide-react';
import { UNIT_CONVERSION_OPTIONS, type UnitConversionId } from '../utils/unitConversions';

export default function UnitConversionHelper() {
  const [inputValue, setInputValue] = useState('1');
  const [conversionType, setConversionType] = useState(UNIT_CONVERSION_OPTIONS[0].value);

  const selectedConversion = UNIT_CONVERSION_OPTIONS.find((option) => option.value === conversionType)
    ?? UNIT_CONVERSION_OPTIONS[0];
  const convertedValue = useMemo(() => {
    if (inputValue.trim() === '') {
      return null;
    }

    const numericValue = Number(inputValue);

    if (Number.isNaN(numericValue)) {
      return null;
    }

    return selectedConversion.convert(numericValue);
  }, [inputValue, selectedConversion]);

  return (
    <section className="conversion-section" aria-labelledby="unit-conversion-heading">
      <div className="conversion-header">
        <div>
          <p className="eyebrow">Study Helper</p>
          <h2 id="unit-conversion-heading">Unit Conversion</h2>
        </div>
        <Calculator aria-hidden="true" size={22} />
      </div>

      <div className="conversion-content">
        <div className="conversion-notes">
          <div>
            <h3>GR50 / Salinity</h3>
            <p>1 dS/m = 1 mS/cm</p>
            <p>1 dS/m = 1000 µS/cm</p>
          </div>
          <div>
            <h3>Ion concentration</h3>
            <p>The dataset uses mmol kg^-1 Tissue DW.</p>
            <p>Na+ mg/g DW = mmol kg^-1 x 22.99 / 1000</p>
            <p>Cl- mg/g DW = mmol kg^-1 x 35.45 / 1000</p>
            <p>K+ mg/g DW = mmol kg^-1 x 39.10 / 1000</p>
          </div>
        </div>

        <div className="converter-panel" aria-label="Mini unit converter">
          <label className="filter-field">
            <span>Value</span>
            <input
              type="number"
              value={inputValue}
              step="0.1"
              onChange={(event) => setInputValue(event.target.value)}
            />
          </label>

          <label className="filter-field">
            <span>Conversion</span>
            <select
              value={conversionType}
              onChange={(event) => setConversionType(event.target.value as UnitConversionId)}
            >
              {UNIT_CONVERSION_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </select>
          </label>

          <div className="conversion-result">
            <span>Result</span>
            <strong>
              {convertedValue == null ? 'Enter a number' : `${formatConversionResult(convertedValue)} ${selectedConversion.outputUnit}`}
            </strong>
          </div>
        </div>
      </div>
    </section>
  );
}

function formatConversionResult(value: number): string {
  return Number.isInteger(value) ? value.toString() : value.toFixed(4).replace(/\.?0+$/, '');
}
