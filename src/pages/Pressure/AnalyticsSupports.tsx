import GridShape from '../../components/common/GridShape';
import { Link } from 'react-router';
import CountdownTimer from '../../components/common/CountdownTimer';
import PageMeta from '../../components/common/PageMeta';

export default function AnalyticsSupports() {
  const targetDate = new Date();
  targetDate.setDate(targetDate.getDate() + 29);
  return (
    <>
      <PageMeta
        title="PSI Análisis de soportes | Software de ingeniería"
        description="Página de análisis de soportes (Próximamente)"
      />
      <div className="relative flex flex-col items-center justify-center w-full min-h-screen p-6 overflow-hidden z-1">
        <GridShape />

        <div>
          <div className="mx-auto w-full max-w-[460px] text-center">
            <Link to="/" className="inline-block mb-6">
              <img
                className="dark:hidden"
                src="./images/logo/ball-triangle.svg"
                alt="Logo"
              />
              <img
                className="hidden dark:block"
                src="./images/logo/ball-triangle.svg"
                alt="Logo"
              />
            </Link>

            <h1 className="mb-3 font-bold text-gray-800 text-title-md dark:text-white/90 xl:text-title-xl">
              Próximamente
            </h1>

            <p className="text-base text-gray-500 mb-9 dark:text-gray-400">
              Esta página está en construcción, ingresa tu email para obtener
              las actualizaciones y notificaciones más recientes sobre la web.
            </p>

            <CountdownTimer targetDate={targetDate} />

            <p className="mb-5 text-sm text-gray-700 dark:text-gray-400">
              No quieres perderte de nada? Subscribete ahora mismo!
            </p>

            <form>
              <div className="flex flex-col gap-2 sm:flex-row sm:gap-3">
                <div className="w-full sm:w-[320px]">
                  <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    className="w-full px-4 py-3 text-sm text-gray-800 bg-transparent border border-gray-300 rounded-lg h-11 shadow-theme-xs placeholder:text-gray-400 focus:border-brand-300 focus:shadow-focus-ring focus:outline-hidden dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:placeholder:text-gray-400 dark:focus:border-brand-300"
                  />
                </div>

                <button
                  type="submit"
                  className="flex items-center justify-center w-full gap-2 px-4 py-3 text-sm font-medium text-white bg-gray-800 rounded-lg hover:bg-brand-600 dark:bg-brand-500 dark:hover:bg-brand-600 sm:w-auto"
                >
                  <svg
                    className="fill-current"
                    width="20"
                    height="20"
                    viewBox="0 0 20 20"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      fillRule="evenodd"
                      clipRule="evenodd"
                      d="M10.7497 2.29248C10.7497 1.87827 10.4139 1.54248 9.99967 1.54248C9.58546 1.54248 9.24967 1.87827 9.24967 2.29248V2.83613C6.0823 3.20733 3.62467 5.9004 3.62467 9.16748V14.4591H3.33301C2.91879 14.4591 2.58301 14.7949 2.58301 15.2091C2.58301 15.6234 2.91879 15.9591 3.33301 15.9591H4.37467H15.6247H16.6663C17.0806 15.9591 17.4163 15.6234 17.4163 15.2091C17.4163 14.7949 17.0806 14.4591 16.6663 14.4591H16.3747V9.16748C16.3747 5.9004 13.9171 3.20733 10.7497 2.83613V2.29248ZM14.8747 14.4591V9.16748C14.8747 6.47509 12.6921 4.29248 9.99967 4.29248C7.30729 4.29248 5.12467 6.47509 5.12467 9.16748V14.4591H14.8747ZM7.99967 17.7085C7.99967 18.1228 8.33546 18.4585 8.74967 18.4585H11.2497C11.6639 18.4585 11.9997 18.1228 11.9997 17.7085C11.9997 17.2943 11.6639 16.9585 11.2497 16.9585H8.74967C8.33546 16.9585 7.99967 17.2943 7.99967 17.7085Z"
                      fill=""
                    />
                  </svg>
                  Notificame
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}
