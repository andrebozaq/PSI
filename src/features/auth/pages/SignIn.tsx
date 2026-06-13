import PageMeta from '../../../components/common/PageMeta';
import AuthLayout from '../../../pages/AuthPages/AuthPageLayout';
import SignInForm from '../components/SignInForm';

export default function SignIn() {
  return (
    <>
      <PageMeta
        title="PSI Login | Software de ingeniería"
        description="This is React.js SignIn Tables Dashboard page for TailAdmin - React.js Tailwind CSS Admin Dashboard Template"
      />
      <AuthLayout>
        <SignInForm />
      </AuthLayout>
    </>
  );
}
