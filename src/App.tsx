import { BrowserRouter as Router, Routes, Route } from 'react-router';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import DesignSupports from './pages/Pressure/DesignSupport';
import AnalysisSupport from './pages/AnalysisSupport';
import AnalyticsBeams from './pages/Structural/AnalyticsBeams';
import DesignWeld from './pages/Structural/DesignWeld';
import AnalyticsWeld from './pages/Structural/AnalyticsWeld';
import AnalyticsSupports from './pages/Pressure/AnalyticsSupports';
import AnalysisDashboard from './pages/Pressure/AnalysisDashboard';
import SignIn from './pages/AuthPages/SignIn';
import SignUp from './pages/AuthPages/SignUp';
import NotFound from './pages/OtherPage/NotFound';
import UserProfiles from './pages/UserProfiles';
import BasicTables from './pages/Tables/BasicTables';
import DataTables from './pages/Tables/DataTables';
import Faqs from './pages/Faqs';
import FormElements from './pages/Forms/FormElements';
import FormLayout from './pages/Forms/FormLayout';
import Maintenance from './pages/OtherPage/Maintenance';
import FiveZeroZero from './pages/OtherPage/FiveZeroZero';
import FiveZeroThree from './pages/OtherPage/FiveZeroThree';
import ComingSoon from './pages/OtherPage/ComingSoon';
import Vessels from './pages/Pressure/Vessels';
import ResetPassword from './pages/AuthPages/ResetPassword';
import TwoStepVerification from './pages/AuthPages/TwoStepVerification';
import Success from './pages/OtherPage/Success';
import AppLayout from './layout/AppLayout';
import { ScrollToTop } from './components/common/ScrollToTop';
// import Saas from './pages/Pressure/Saas';
import Home from './pages/Home';
import Conversor from './pages/Conversor';
import SavedProjects from './pages/SavedProjects';
import ProjectSelection from './pages/ProjectSelection';
import ForumDashboard from './pages/ForumDashboard';
import PostDetail from './pages/PostDetail';
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
            <Routes>
          {/* Dashboard Layout (Protected) */}
          <Route element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          }>
            <Route index path="/inicio" element={<Home />} />
            <Route path="/proyectos" element={<ProjectSelection />} />
            <Route path="/proyectos/presion" element={<SavedProjects />} />
            <Route path="/soporte-analisis" element={<AnalyticsSupports />} />
            <Route
              path="/soporte-analisis-editor"
              element={<AnalysisDashboard />}
            />
            <Route path="/soporte-diseno" element={<DesignSupports />} />
            <Route path="/analisis" element={<AnalysisSupport />} />
            <Route path="/recipientes-analisis" element={<Vessels />} />
            <Route path="/vigas-analisis" element={<AnalyticsBeams />} />
            <Route path="/soldadura-diseno" element={<DesignWeld />} />
            <Route path="/soldadura-analisis" element={<AnalyticsWeld />} />

            {/* Others Page */}
            <Route path="/perfil" element={<UserProfiles />} />
            <Route path="/conversor" element={<Conversor />} />
            <Route path="/" element={<Home />} />
            <Route path="/faq" element={<Faqs />} />
            <Route path="/foro" element={<ForumDashboard />} />
            <Route path="/foro/:postId" element={<PostDetail />} />

            {/* Forms */}
            <Route path="/form-elements" element={<FormElements />} />
            <Route path="/form-layout" element={<FormLayout />} />

            {/* Tables */}
            <Route path="/basic-tables" element={<BasicTables />} />
            <Route path="/data-tables" element={<DataTables />} />
          </Route>

          {/* Auth Layout */}
          <Route path="/login" element={<SignIn />} />
          <Route path="/registro" element={<SignUp />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route
            path="/two-step-verification"
            element={<TwoStepVerification />}
          />

          {/* Fallback Route */}
          <Route path="*" element={<NotFound />} />
          <Route path="/maintenance" element={<Maintenance />} />
          <Route path="/success" element={<Success />} />
          <Route path="/five-zero-zero" element={<FiveZeroZero />} />
          <Route path="/four-zero-three" element={<FiveZeroThree />} />
          <Route path="/proximamente" element={<ComingSoon />} />
            </Routes>
          </div>

          <footer className="border-t border-gray-200 px-4 py-4 text-center text-sm text-gray-500 dark:border-gray-800 dark:text-gray-400">
            © 2026 - Incsane, EIM, La Universidad del Zulia
          </footer>
        </div>
      </Router>
    </>
  );
}
