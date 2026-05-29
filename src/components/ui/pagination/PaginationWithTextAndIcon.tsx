type PaginationWithTextAndIconProps = {
  currentStep?: number;
  totalSteps?: number;
  prevLabel?: string;
  nextLabel?: string;
  className?: string;
  onPrev?: () => void;
  onNext?: () => void;
  onPageSelect?: (page: number) => void;
};

export default function PaginationWithTextAndIcon({
  currentStep = 1,
  totalSteps = 5,
  prevLabel = 'Previous',
  nextLabel = 'Next',
  className = '',
  onPrev,
  onNext,
  onPageSelect,
}: PaginationWithTextAndIconProps) {
  const prevDisabled = currentStep <= 1;
  const nextDisabled = currentStep >= totalSteps;

  const pages =
    totalSteps <= 7
      ? Array.from({ length: totalSteps }, (_, idx) => idx + 1)
      : [1, 2, '...', totalSteps - 1, totalSteps];

  return (
    <div
      className={`flex items-center justify-between gap-3 px-4 py-3 sm:justify-normal sm:gap-8 sm:px-6 sm:py-4 ${className}`.trim()}
    >
      <button
        // mobile: left arrow
        type="button"
        onClick={onPrev}
        disabled={prevDisabled}
        className={`order-1 flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200 sm:order-none sm:px-3.5 sm:py-2.5 ${
          prevDisabled ? 'cursor-not-allowed opacity-60' : ''
        }`.trim()}
        aria-label={prevLabel}
      >
        <svg
          className="fill-current"
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M2.58203 9.99868C2.58174 10.1909 2.6549 10.3833 2.80152 10.53L7.79818 15.5301C8.09097 15.8231 8.56584 15.8233 8.85883 15.5305C9.15183 15.2377 9.152 14.7629 8.85921 14.4699L5.13911 10.7472L16.6665 10.7472C17.0807 10.7472 17.4165 10.4114 17.4165 9.99715C17.4165 9.58294 17.0807 9.24715 16.6665 9.24715L5.14456 9.24715L8.85919 5.53016C9.15199 5.23717 9.15184 4.7623 8.85885 4.4695C8.56587 4.1767 8.09099 4.17685 7.79819 4.46984L2.84069 9.43049C2.68224 9.568 2.58203 9.77087 2.58203 9.99715C2.58203 9.99766 2.58203 9.99817 2.58203 9.99868Z"
            fill=""
          />
        </svg>

        <span className="hidden sm:inline"> {prevLabel} </span>
      </button>

      <span className="order-3 block w-full text-center text-sm font-medium text-gray-700 dark:text-gray-400 sm:hidden mt-2">
        Paso {currentStep} de {totalSteps}
      </span>

      <ul
        className="hidden items-center gap-0.5 sm:flex"
        aria-label="Step navigation"
      >
        {pages.map((page, index) => {
          if (page === '...') {
            return (
              <li
                key={`ellipsis-${index}`}
                className="px-2 text-sm text-gray-500 dark:text-gray-400"
              >
                ...
              </li>
            );
          }

          const isActive = page === currentStep;
          return (
            <li key={page}>
              <button
                type="button"
                onClick={() => onPageSelect?.(page as number)}
                className={`flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium transition hover:bg-brand-500 hover:text-white dark:text-gray-400 dark:hover:text-white ${
                  isActive
                    ? 'bg-brand-500 text-white'
                    : 'bg-transparent text-gray-700'
                }`}
                aria-current={isActive ? 'step' : undefined}
              >
                {page}
              </button>
            </li>
          );
        })}
      </ul>

      <button
        // mobile: right arrow
        type="button"
        onClick={onNext}
        disabled={nextDisabled}
        className={`order-2 flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-2 py-2 text-sm font-medium text-gray-700 shadow-theme-xs hover:bg-gray-50 hover:text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-white/[0.03] dark:hover:text-gray-200 sm:order-none sm:px-3.5 sm:py-2.5 ${
          nextDisabled ? 'cursor-not-allowed opacity-60' : ''
        }`.trim()}
        aria-label={nextLabel}
      >
        <span className="hidden sm:inline"> {nextLabel} </span>

        <svg
          className="fill-current"
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M17.4165 9.9986C17.4168 10.1909 17.3437 10.3832 17.197 10.53L12.2004 15.5301C11.9076 15.8231 11.4327 15.8233 11.1397 15.5305C10.8467 15.2377 10.8465 14.7629 11.1393 14.4699L14.8594 10.7472L3.33203 10.7472C2.91782 10.7472 2.58203 10.4114 2.58203 9.99715C2.58203 9.58294 2.91782 9.24715 3.33203 9.24715L14.854 9.24715L11.1393 5.53016C10.8465 5.23717 10.8467 4.7623 11.1397 4.4695C11.4327 4.1767 11.9075 4.17685 12.2003 4.46984L17.1578 9.43049C17.3163 9.568 17.4165 9.77087 17.4165 9.99715C17.4165 9.99763 17.4165 9.99812 17.4165 9.9986Z"
            fill=""
          />
        </svg>
      </button>
    </div>
  );
}
