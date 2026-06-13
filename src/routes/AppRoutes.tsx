import { Routes, Route } from 'react-router';
import { ProtectedRoute } from '../components/auth/ProtectedRoute';
import DesignSupports from '../features/engineering/pages/DesignSupport';
import AnalysisSupport from '../pages/AnalysisSupport';
import AnalyticsBeams from '../pages/Structural/AnalyticsBeams';
import DesignWeld from '../pages/Structural/DesignWeld';
import AnalyticsWeld from '../pages/Structural/AnalyticsWeld';
import AnalyticsSupports from '../pages/Pressure/AnalyticsSupports';
import AnalysisDashboard from '../features/engineering/pages/AnalysisDashboard';
import SignIn from '../features/auth/pages/SignIn';
import SignUp from '../features/auth/pages/SignUp';
import NotFound from '../pages/OtherPage/NotFound';
import UserProfiles from '../features/profile/pages/UserProfiles';
import BasicTables from '../pages/Tables/BasicTables';
import DataTables from '../pages/Tables/DataTables';
import Faqs from '../pages/Faqs';
import FormElements from '../pages/Forms/FormElements';
import FormLayout from '../pages/Forms/FormLayout';
import Maintenance from '../pages/OtherPage/Maintenance';
import FiveZeroZero from '../pages/OtherPage/FiveZeroZero';
import FiveZeroThree from '../pages/OtherPage/FiveZeroThree';
import ComingSoon from '../pages/OtherPage/ComingSoon';
import Vessels from '../pages/Pressure/Vessels';
import ResetPassword from '../features/auth/pages/ResetPassword';
import TwoStepVerification from '../features/auth/pages/TwoStepVerification';
import Success from '../pages/OtherPage/Success';
import AppLayout from '../layout/AppLayout';
import Home from '../pages/Home';
import Conversor from '../pages/Conversor';
import SavedProjects from '../features/engineering/pages/SavedProjects';
import ProjectSelection from '../pages/ProjectSelection';
import ForumDashboard from '../features/forum/pages/ForumDashboard';
import PostDetail from '../features/forum/pages/PostDetail';

export default function AppRoutes() {
  return (
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
  );
}
