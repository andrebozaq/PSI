import React from 'react';
import GridShape from '../../components/common/GridShape';
import { Link } from 'react-router';
import ThemeTogglerTwo from '../../components/common/ThemeTogglerTwo';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="relative p-6 bg-white z-1 dark:bg-gray-900 sm:p-0">
      <div className="relative flex flex-col justify-center w-full h-screen lg:flex-row dark:bg-gray-900 sm:p-0">
        <div className="flex flex-col flex-1 w-full overflow-y-auto no-scrollbar lg:w-1/2">
          {children}

          {/* Mobile Logos (Visible only on small screens) */}
          <div className="flex justify-center items-center gap-5 pt-4 pb-8 lg:hidden">
              <Link to="/" className="inline-block">
                  <img width={55} src="/images/logo/PSI-logo.png" alt="PSI Logo" />
              </Link>
              <div className="inline-block">
                  <img width={65} className="dark:hidden" src="/images/logo/LUZ.png" alt="LUZ Logo" />
                  <img width={65} className="hidden dark:block" src="/images/logo/LUZ-dark.png" alt="LUZ Logo" />
              </div>
              <a href="https://www.instagram.com/fingluz?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==" target="_blank" rel="noopener noreferrer" className="inline-block">
                  <img width={65} className="dark:hidden" src="/images/logo/EIM.png" alt="EIM Logo" />
                  <img width={65} className="hidden dark:block" src="/images/logo/EIM-dark.png" alt="EIM Logo" />
              </a>
          </div>
        </div>

        <div className="items-center hidden w-full h-full lg:w-1/2 bg-brand-00 dark:bg-white/5 lg:grid">
          <div className="relative flex items-center justify-center z-1">
            {/* <!-- ===== Common Grid Shape Start ===== --> */}
            <GridShape />
            <div className="flex flex-col items-center max-w-lg px-8">
              <div className="flex items-center justify-center gap-6 mb-6">
                <Link to="/" className="inline-block">
                  <img width={180} src="/images/logo/PSI.png" alt="PSI Logo" />
                </Link>
                <div className="inline-block">
                  <img width={110} className="dark:hidden" src="/images/logo/LUZ.png" alt="LUZ Logo" />
                  <img width={110} className="hidden dark:block" src="/images/logo/LUZ-dark.png" alt="LUZ Logo" />
                </div>
                <a
                  href="https://www.instagram.com/fingluz?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block"
                >
                  <img
                    width={110}
                    className="dark:hidden"
                    src="/images/logo/EIM.png"
                    alt="EIM Logo"
                  />
                  <img
                    width={110}
                    className="hidden dark:block"
                    src="/images/logo/EIM-dark.png"
                    alt="EIM Logo"
                  />
                </a>
              </div>
              <p className="text-center text-gray-400 dark:text-white/60">
                Software gratis para soportes de recipientes a presión
              </p>
            </div>
          </div>
        </div>

        <div className="fixed z-50 hidden bottom-6 right-6 sm:block">
          <ThemeTogglerTwo />
        </div>
      </div>
    </div>
  );
}
