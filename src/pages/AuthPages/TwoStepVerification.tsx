import PageMeta from '../../components/common/PageMeta';
import AuthLayout from './AuthPageLayout';

export default function TwoStepVerification() {
  return (
    <>
      <PageMeta
        title="PSI 2STEP | Software de ingeniería"
        description="This is React.js Two Step Verification Tables Dashboard page for TailAdmin - React.js Tailwind CSS Admin Dashboard Template"
      />
      <AuthLayout>
        <TwoStepVerification />
      </AuthLayout>
    </>
  );
}
