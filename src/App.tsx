import { useEffect, useState } from 'react';
import { BarChart3, Database, GitBranch, Map, Microscope, Sprout } from 'lucide-react';
import GrassLibrary from './pages/GrassLibrary';
import Prediction from './pages/Prediction';
import CropSalinityScreening from './pages/CropSalinityScreening';
import SoilSalinityMapper from './pages/SoilSalinityMapper';

type AppPage =
  | 'library'
  | 'prediction'
  | 'cropSalinityScreening'
  | 'knowledgeGraph'
  | 'fieldMatch'
  | 'halophyteSurveyMap';

const ROUTES: Record<AppPage, string> = {
  library: '/',
  prediction: '/prediction',
  cropSalinityScreening: '/crop-salinity-screening',
  knowledgeGraph: '/knowledge-graph',
  fieldMatch: '/field-match',
  halophyteSurveyMap: '/halophyte-survey-map',
};

function pageFromPath(pathname: string): AppPage {
  if (pathname === '/prediction') {
    return 'prediction';
  }
  if (
    pathname === '/crop-salinity-screening' ||
    pathname === '/biosaline-crop-screening' ||
    pathname === '/salinity-risk-model'
  ) {
    return 'cropSalinityScreening';
  }
  if (pathname === '/knowledge-graph') {
    return 'knowledgeGraph';
  }
  if (pathname === '/field-match' || pathname === '/halophyte-field-match') {
    return 'fieldMatch';
  }
  if (
    pathname === '/halophyte-survey-map' ||
    pathname === '/soil-salinity-mapping' ||
    pathname === '/salinity-map'
  ) {
    return 'halophyteSurveyMap';
  }
  return 'library';
}

const NAV_ITEMS: Array<{ page: AppPage; label: string; icon: typeof Database }> = [
  { page: 'library', label: 'Grass Library', icon: Database },
  { page: 'prediction', label: 'Prediction Model', icon: BarChart3 },
  { page: 'halophyteSurveyMap', label: 'Halophyte Survey Map', icon: Map },
  { page: 'cropSalinityScreening', label: 'Crop Salinity Screening', icon: Sprout },
  { page: 'knowledgeGraph', label: 'Knowledge Graph', icon: GitBranch },
  { page: 'fieldMatch', label: 'Field Match', icon: Microscope },
];

function StaticModulePage({ title, src }: { title: string; src: string }) {
  return (
    <main className="module-page">
      <iframe className="module-frame" title={title} src={src} />
    </main>
  );
}

export default function App() {
  const [activePage, setActivePage] = useState<AppPage>(() => pageFromPath(window.location.pathname));

  useEffect(() => {
    if (window.location.pathname === '/soil-salinity-mapping' || window.location.pathname === '/salinity-map') {
      window.history.replaceState({}, '', ROUTES.halophyteSurveyMap);
    }
    const handlePopState = () => setActivePage(pageFromPath(window.location.pathname));
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigate = (page: AppPage) => {
    const path = ROUTES[page];
    if (window.location.pathname !== path) {
      window.history.pushState({}, '', path);
    }
    setActivePage(page);
  };

  const renderNavButton = ({ page, label, icon: Icon }: { page: AppPage; label: string; icon: typeof Database }) => (
    <button
      className={activePage === page ? 'nav-button nav-button-active' : 'nav-button'}
      type="button"
      onClick={() => navigate(page)}
    >
      <Icon aria-hidden="true" size={15} />
      {label}
    </button>
  );

  return (
    <>
      <nav className="app-navigation" aria-label="Main navigation">
        <div className="app-brand">
          <span className="brand-mark" aria-hidden="true">H</span>
          <div>
            <strong>Biosaline Halophyte Intelligence Platform</strong>
            <span>Decision support for halophyte, salinity, and crop screening workflows</span>
          </div>
        </div>
        <div className="app-navigation-actions">
          {NAV_ITEMS.map((item) => renderNavButton(item))}
        </div>
      </nav>
      {activePage === 'library' ? (
        <GrassLibrary />
      ) : activePage === 'prediction' ? (
        <Prediction />
      ) : activePage === 'cropSalinityScreening' ? (
        <CropSalinityScreening />
      ) : activePage === 'knowledgeGraph' ? (
        <StaticModulePage title="Halophyte Knowledge Graph" src="/modules/knowledge-graph/index.html" />
      ) : activePage === 'fieldMatch' ? (
        <StaticModulePage title="Halophyte Field Match" src="/modules/field-match/index.html" />
      ) : (
        <SoilSalinityMapper />
      )}
    </>
  );
}
