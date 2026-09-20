import { BookOpen, MapPinned, Table2 } from 'lucide-react';

const GENERATED_MAP_URL = '/modules/soil-salinity-mapping/generated-map.html';

const VEGETATION_CONTEXT = [
  { year: 1989, vegetativeArea: '12.58', nonVegetativeArea: '121.20', totalArea: '133.78' },
  { year: 1994, vegetativeArea: '21.70', nonVegetativeArea: '114.50', totalArea: '136.20' },
  { year: 1999, vegetativeArea: '13.80', nonVegetativeArea: '124.00', totalArea: '137.80' },
  { year: 2004, vegetativeArea: '13.90', nonVegetativeArea: '124.80', totalArea: '138.70' },
  { year: 2009, vegetativeArea: '18.60', nonVegetativeArea: '120.60', totalArea: '139.20' },
  { year: 2014, vegetativeArea: '14.50', nonVegetativeArea: '126.90', totalArea: '141.40' },
  { year: 2018, vegetativeArea: '15.40', nonVegetativeArea: '127.80', totalArea: '143.20' },
];

export default function SoilSalinityMapper() {
  return (
    <main className="library-page soil-page survey-map-page">
      <header className="page-hero soil-hero">
        <div>
          <p className="eyebrow">Survey Layer</p>
          <h1>Karachi Halophyte Survey Map</h1>
          <p className="page-subtitle">
            Observed halophyte species locations from the Karachi Coast, based on GPS-geotagged survey records in
            Niaz et al., 2021, Table 2.
          </p>
        </div>
      </header>

      <section className="soil-layout soil-layout-single survey-overview" aria-labelledby="survey-area-heading">
        <div className="soil-control-panel survey-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Survey Layer</p>
              <h2 id="survey-area-heading">Survey Area</h2>
            </div>
            <MapPinned aria-hidden="true" size={22} />
          </div>

          <div className="survey-panel-grid">
            <label className="filter-field survey-area-field">
              <span>Study Area</span>
              <select defaultValue="Karachi Coast" aria-label="Study area" disabled>
                <option value="Karachi Coast">Karachi Coast</option>
              </select>
            </label>

            <dl className="survey-fact-list">
              <div>
                <dt>Records</dt>
                <dd>30 observed halophyte records</dd>
              </div>
              <div>
                <dt>Survey Data</dt>
                <dd>GPS-Geotagged Species Locations</dd>
              </div>
              <div>
                <dt>Source</dt>
                <dd>Niaz et al., 2021, Table 2</dd>
              </div>
              <div>
                <dt>NDVI Context</dt>
                <dd>Vegetation Coverage, 1989-2018</dd>
              </div>
            </dl>
          </div>
        </div>
      </section>

      <section className="soil-map-section survey-map-section" aria-labelledby="survey-map-heading">
        <div className="results-header">
          <div>
            <p className="eyebrow">Observed Point Layer</p>
            <h2 id="survey-map-heading">Observed Halophyte Locations</h2>
          </div>
          <span className="result-count">Karachi Coast</span>
        </div>

        <iframe
          className="soil-map-frame"
          title="Karachi Halophyte Survey Map"
          src={`${GENERATED_MAP_URL}?v=karachi-halophyte-survey`}
        />
      </section>

      <section className="survey-context-section" aria-labelledby="vegetation-context-heading">
        <div className="section-heading">
          <div>
            <p className="eyebrow">NDVI Context</p>
            <h2 id="vegetation-context-heading">Vegetation Coverage, 1989-2018</h2>
          </div>
          <Table2 aria-hidden="true" size={21} />
        </div>

        <div className="survey-context-copy">
          <BookOpen aria-hidden="true" size={18} />
          <p>
            Table 3 provides vegetation coverage context for the same coastal study area. It is shown as supporting
            landscape context for the observed point layer.
          </p>
        </div>

        <div className="survey-table-shell">
          <table className="survey-context-table">
            <thead>
              <tr>
                <th>Year</th>
                <th>Vegetative Area km2</th>
                <th>Non-Vegetative Area km2</th>
                <th>Total Area km2</th>
              </tr>
            </thead>
            <tbody>
              {VEGETATION_CONTEXT.map((row) => (
                <tr key={row.year}>
                  <td>{row.year}</td>
                  <td>{row.vegetativeArea}</td>
                  <td>{row.nonVegetativeArea}</td>
                  <td>{row.totalArea}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
