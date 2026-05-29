import PageBreadcrumb from '../components/common/PageBreadCrumb';
import ComponentCard from '../components/common/ComponentCard';
import FaqsOne from '../components/UiExample/FaqsExample/FaqsOne';
import PageMeta from '../components/common/PageMeta';

export default function Faqs() {
  return (
    <>
      <PageMeta
        title="PSI Preguntas frecuentes | Software de ingeniería"
        description="This is React.js Faqs Dashboard page for TailAdmin - React.js Tailwind CSS Admin Dashboard Template"
      />
      <PageBreadcrumb pageTitle="Preguntas frecuentes" />
      <div className="space-y-5 sm:space-y-6">
        <ComponentCard title="Alguna duda? Acá te la respondemos!">
          <FaqsOne />
        </ComponentCard>
        {/* <ComponentCard title="Alguna duda? Acá te la respondemos!">
          <FaqsTwo />
        </ComponentCard> */}
        {/* <ComponentCard title="Alguna duda? Acá te la respondemos!">
          <FaqsThree />
        </ComponentCard> */}
      </div>
    </>
  );
}
