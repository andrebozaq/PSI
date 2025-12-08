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
        {children}
        <div className="items-center hidden w-full h-full lg:w-1/2 bg-brand-00 dark:bg-white/5 lg:grid">
          <div className="relative flex items-center justify-center z-1">
            {/* <!-- ===== Common Grid Shape Start ===== --> */}
            <GridShape />
            <div className="flex flex-col items-center max-w-xs">
              <div className="flex items-center gap-10 mb-4">
                <Link to="/" className="inline-block">
                  <img width={300} src="/images/logo/PSI.png" alt="Logo" />
                </Link>
                <a
                  href="https://www.instagram.com/fingluz?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block"
                >
                  <img
                    width={140}
                    height={48}
                    className="dark:hidden"
                    src="/images/logo/EIM.png"
                    alt="EIM Logo"
                  />
                  <img
                    width={140}
                    height={48}
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
