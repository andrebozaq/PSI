import { BrowserRouter as Router, Routes, Route } from 'react-router';
import DesignSupports from './pages/Pressure/DesignSupport';
import AnalyticsBeams from './pages/Structural/AnalyticsBeams';
import DesignWeld from './pages/Structural/DesignWeld';
import AnalyticsWeld from './pages/Structural/AnalyticsWeld';
import AnalyticsSupports from './pages/Pressure/AnalyticsSupports';
import AnalysisDashboard from './pages/Pressure/AnalysisDashboard';
import SignIn from './pages/AuthPages/SignIn';
import SignUp from './pages/AuthPages/SignUp';
import NotFound from './pages/OtherPage/NotFound';
import UserProfiles from './pages/UserProfiles';
import Carousel from './pages/UiElements/Carousel';
import Maintenance from './pages/OtherPage/Maintenance';
import FiveZeroZero from './pages/OtherPage/FiveZeroZero';
import FiveZeroThree from './pages/OtherPage/FiveZeroThree';
import Videos from './pages/UiElements/Videos';
import Images from './pages/UiElements/Images';
import Alerts from './pages/UiElements/Alerts';
import Badges from './pages/UiElements/Badges';
import Pagination from './pages/UiElements/Pagination';
import Avatars from './pages/UiElements/Avatars';
import Buttons from './pages/UiElements/Buttons';
import ButtonsGroup from './pages/UiElements/ButtonsGroup';
import Notifications from './pages/UiElements/Notifications';
import LineChart from './pages/Charts/LineChart';
import BarChart from './pages/Charts/BarChart';
import PieChart from './pages/Charts/PieChart';
import Invoices from './pages/Invoices';
import ComingSoon from './pages/OtherPage/ComingSoon';
import FileManager from './pages/FileManager';
import Calendar from './pages/Calendar';
import BasicTables from './pages/Tables/BasicTables';
import DataTables from './pages/Tables/DataTables';
import PricingTables from './pages/PricingTables';
import Faqs from './pages/Faqs';
import Chats from './pages/Chat/Chats';
import FormElements from './pages/Forms/FormElements';
import FormLayout from './pages/Forms/FormLayout';
import Blank from './pages/Blank';
import EmailInbox from './pages/Email/EmailInbox';
import EmailDetails from './pages/Email/EmailDetails';
import Vessels from './pages/Pressure/Vessels';

import TaskKanban from './pages/Task/TaskKanban';
import BreadCrumb from './pages/UiElements/BreadCrumb';
import Cards from './pages/UiElements/Cards';
import Dropdowns from './pages/UiElements/Dropdowns';
import Links from './pages/UiElements/Links';
import Lists from './pages/UiElements/Lists';
import Popovers from './pages/UiElements/Popovers';
import Progressbar from './pages/UiElements/Progressbar';
import Ribbons from './pages/UiElements/Ribbons';
import Spinners from './pages/UiElements/Spinners';
import Tabs from './pages/UiElements/Tabs';
import Tooltips from './pages/UiElements/Tooltips';
import Modals from './pages/UiElements/Modals';
import ResetPassword from './pages/AuthPages/ResetPassword';
import TwoStepVerification from './pages/AuthPages/TwoStepVerification';
import Success from './pages/OtherPage/Success';
import AppLayout from './layout/AppLayout';
import { ScrollToTop } from './components/common/ScrollToTop';
import TaskList from './pages/Task/TaskList';
// import Saas from './pages/Pressure/Saas';
import Home from './pages/Home';
import Conversor from './pages/Conversor';

export default function App() {
  return (
    <>
      <Router>
        <ScrollToTop />
        <div className="flex min-h-screen flex-col">
          <div className="flex-1">
            <Routes>
          {/* Dashboard Layout */}
          <Route element={<AppLayout />}>
            <Route index path="/inicio" element={<Home />} />
            <Route path="/soporte-analisis" element={<AnalyticsSupports />} />
            <Route
              path="/soporte-analisis-editor"
              element={<AnalysisDashboard />}
            />
            <Route path="/soporte-diseno" element={<DesignSupports />} />
            <Route path="/recipientes-analisis" element={<Vessels />} />
            <Route path="/vigas-analisis" element={<AnalyticsBeams />} />
            <Route path="/soldadura-diseno" element={<DesignWeld />} />
            <Route path="/soldadura-analisis" element={<AnalyticsWeld />} />

            {/* Others Page */}
            <Route path="/perfil" element={<UserProfiles />} />
            <Route path="/calendario" element={<Calendar />} />
            <Route path="/conversor" element={<Conversor />} />
            <Route path="/" element={<Home />} />
            <Route path="/documentacion" element={<Invoices />} />
            <Route path="/faq" element={<Faqs />} />
            <Route path="/pricing-tables" element={<PricingTables />} />
            <Route path="/blank" element={<Blank />} />

            {/* Forms */}
            <Route path="/form-elements" element={<FormElements />} />
            <Route path="/form-layout" element={<FormLayout />} />

            {/* Applications */}
            <Route path="/chat" element={<Chats />} />

            <Route path="/task-list" element={<TaskList />} />
            <Route path="/task-kanban" element={<TaskKanban />} />
            <Route path="/file-manager" element={<FileManager />} />

            {/* Email */}

            <Route path="/inbox" element={<EmailInbox />} />
            <Route path="/inbox-details" element={<EmailDetails />} />

            {/* Tables */}
            <Route path="/basic-tables" element={<BasicTables />} />
            <Route path="/data-tables" element={<DataTables />} />

            {/* Ui Elements */}
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/avatars" element={<Avatars />} />
            <Route path="/badge" element={<Badges />} />
            <Route path="/breadcrumb" element={<BreadCrumb />} />
            <Route path="/buttons" element={<Buttons />} />
            <Route path="/buttons-group" element={<ButtonsGroup />} />
            <Route path="/cards" element={<Cards />} />
            <Route path="/carousel" element={<Carousel />} />
            <Route path="/dropdowns" element={<Dropdowns />} />
            <Route path="/images" element={<Images />} />
            <Route path="/links" element={<Links />} />
            <Route path="/list" element={<Lists />} />
            <Route path="/modals" element={<Modals />} />
            <Route path="/notifications" element={<Notifications />} />
            <Route path="/pagination" element={<Pagination />} />
            <Route path="/popovers" element={<Popovers />} />
            <Route path="/progress-bar" element={<Progressbar />} />
            <Route path="/ribbons" element={<Ribbons />} />
            <Route path="/spinners" element={<Spinners />} />
            <Route path="/tabs" element={<Tabs />} />
            <Route path="/tooltips" element={<Tooltips />} />
            <Route path="/videos" element={<Videos />} />

            {/* Charts */}
            <Route path="/line-chart" element={<LineChart />} />
            <Route path="/bar-chart" element={<BarChart />} />
            <Route path="/pie-chart" element={<PieChart />} />
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
