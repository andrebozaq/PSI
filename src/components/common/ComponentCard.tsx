interface ComponentCardProps {
  title: string;
  children: React.ReactNode;
  className?: string; // Additional custom classes for styling
  desc?: string; // Description text
}

const ComponentCard: React.FC<ComponentCardProps> = ({
  title,
  children,
  className = '',
  desc = '',
}) => {
  return (
    <div
      className={`rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03] print:border-none print:shadow-none print:p-0 print:bg-transparent ${className}`}
    >
      {/* Card Header */}
      <div className="px-6 py-5 print:px-0 print:py-2 print:border-none">
        <h3 className="text-base font-medium text-gray-800 dark:text-white/90 print:text-lg print:font-bold print:text-black">
          {title}
        </h3>
        {desc && (
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {desc}
          </p>
        )}
      </div>

      {/* Card Body */}
      <div className="p-4 border-t border-gray-100 dark:border-gray-800 sm:p-6 print:border-none print:p-0">
        <div className="space-y-6 print:space-y-3">{children}</div>
      </div>
    </div>
  );
};

export default ComponentCard;
