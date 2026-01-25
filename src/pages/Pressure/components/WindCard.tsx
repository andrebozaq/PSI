import React from 'react';

const WindCard: React.FC<{
  form: any;
  handleInputChange: any;
  unitSystem: 'SI' | 'US';
}> = ({ form, handleInputChange, unitSystem }) => {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900">
      <h3 className="mb-3 text-sm font-semibold text-gray-800 dark:text-gray-100">
        Viento
      </h3>
      <div className="space-y-2">
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Zona de viento (auto)
        </label>
        <div className="flex items-center gap-2">
          <select
            value={form.windAuto}
            onChange={handleInputChange('windAuto')}
            className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
          >
            <option>Zone 1</option>
            <option>Zone 2</option>
            <option>Zone 3</option>
          </select>
        </div>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Valor de viento (opcional)
          <input
            type="number"
            step="any"
            value={form.windValue}
            onChange={handleInputChange('windValue')}
            placeholder={unitSystem === 'SI' ? 'm/s o kPa' : 'mph or psf'}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Categoría de exposición
          <select
            value={form.exposureCategory}
            onChange={handleInputChange('exposureCategory')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
          >
            <option>B</option>
            <option>C</option>
            <option>D</option>
          </select>
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Factor de importancia
          <input
            type="number"
            step="0.01"
            value={form.windImportanceFactor}
            onChange={handleInputChange('windImportanceFactor')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      </div>
    </div>
  );
};

export default WindCard;
