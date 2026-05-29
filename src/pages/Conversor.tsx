import PageBreadcrumb from '../components/common/PageBreadCrumb';
import ConversorTab from '../components/ui/conversor';
import PageMeta from '../components/common/PageMeta';

export default function Conversor() {
  return (
    <>
      <PageMeta
        title="PSI Conversor de unidades | Software de ingeniería"
        description="This is React.js Tabs page for TailAdmin - React.js Tailwind CSS Admin Dashboard Template"
      />
      <PageBreadcrumb pageTitle="Conversor" />
      <ConversorTab />
    </>
  );
}
