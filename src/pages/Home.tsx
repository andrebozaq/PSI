import PageMeta from '../components/common/PageMeta';

export default function Home() {
  return (
    <>
      <PageMeta
        title="PSI Inicio| Software for structural analysis"
        description="This is React.js Ecommerce Dashboard page for TailAdmin - React.js Tailwind CSS Admin Dashboard Template"
      />

      <div className="min-h-screen rounded-2xl border border-gray-200 bg-white px-5 py-7 dark:border-gray-800 dark:bg-white/[0.03] xl:px-10 xl:py-12">
        <div className="mx-auto w-full max-w-[630px] text-center">
          <h3 className="mb-4 font-semibold text-gray-800 text-theme-xl dark:text-white/90 sm:text-2xl">
            Inicio
          </h3>

          <p className="text-sm text-gray-500 dark:text-gray-400 sm:text-base">
            Página principal, quizá con una animación o algo llamativo.
          </p>
        </div>
        <img
          src="./images/logo/processing.svg"
          alt="imgaa"
          className="dark:hidden"
        />
        <img
          src="./images/logo/problem-solving.svg"
          alt="imgaa"
          className="hidden dark:block"
        />
      </div>
    </>
  );
}
