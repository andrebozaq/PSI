import React from 'react';

const WindCard: React.FC<{
  form: any;
  handleInputChange: any;
  unitSystem: 'SI' | 'US';
}> = ({ form, handleInputChange, unitSystem }) => {
  const windValueUnit = unitSystem === 'SI' ? 'kPa' : 'psi';

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900 print:border-none print:shadow-none print:p-0 print:bg-transparent">
      <h3 className="mb-3 text-sm font-semibold text-gray-800 dark:text-gray-100 border-b border-gray-200 pb-1 uppercase print:text-black print:border-black print:text-lg">
        Viento
      </h3>
      <div className="space-y-2">
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Zona de viento (auto)
        </label>
        <div className="flex items-center gap-2">
          <div className="relative w-full">
            <select
              value={form.windAuto}
              onChange={handleInputChange('windAuto')}
              className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:hidden"
            >
              <option>Zona 1</option>
              <option>Zona 2</option>
              <option>Zona 3</option>
            </select>
            <div className="hidden pt-1 font-bold text-black print:block">
              {form.windAuto || '—'}
            </div>
          </div>
        </div>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Valor de viento ({windValueUnit})
          <input
            type="number"
            min="0"
            step="any"
            value={form.windValue}
            onChange={handleInputChange('windValue')}
            placeholder={unitSystem === 'SI' ? 'm/s o kPa' : 'mph or psf'}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
          />
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Categoría de exposición
          <div className="relative">
            <select
              value={form.exposureCategory}
              onChange={handleInputChange('exposureCategory')}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:hidden"
            >
              <option>B</option>
              <option>C</option>
              <option>D</option>
            </select>
            <div className="hidden pt-1 font-bold text-black print:block">
              {form.exposureCategory || '—'}
            </div>
          </div>
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Factor de importancia
          <input
            type="number"
            min="0"
            step="0.01"
            value={form.windImportanceFactor}
            onChange={handleInputChange('windImportanceFactor')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
          />
        </label>
      </div>
    </div>
  );
};

export default WindCard;
