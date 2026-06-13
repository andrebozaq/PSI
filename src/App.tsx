import { BrowserRouter as Router } from 'react-router';
import { ScrollToTop } from './components/common/ScrollToTop';
import AppRoutes from './routes/AppRoutes';
import { seedMaterialsDatabase } from './utils/seedMaterials';
import { useEffect } from 'react';

export default function App() {
  useEffect(() => {
    // Sube los materiales a Firestore en el primer render
    seedMaterialsDatabase();
  }, []);

  return (
    <>
      <Router>
        <ScrollToTop />
        <div className="flex min-h-screen flex-col">
          <div className="flex-1">
            <AppRoutes />
          </div>

          <footer className="border-t border-gray-200 px-4 py-4 text-center text-sm text-gray-500 dark:border-gray-800 dark:text-gray-400">
            © 2026 - Incsane, EIM, La Universidad del Zulia
          </footer>
        </div>
      </Router>
    </>
  );
}
