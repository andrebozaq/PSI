import React from 'react';

const Lug: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
  unitSystem?: 'SI' | 'US';
  mode?: 'design' | 'analysis';
}> = ({ form, onFieldChange, unitSystem = 'SI', mode = 'analysis' }) => {
  void mode;
  const lengthUnit = unitSystem === 'SI' ? 'mm' : 'in';
  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Cantidad de ménsulas
        <select
          value={form.lugQuantity || '2'}
          onChange={(e) => onFieldChange('lugQuantity', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>2</option>
          <option>4</option>
          <option>8</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Elevación de la ménsula ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.lugElevation || ''}
          onChange={(e) => onFieldChange('lugElevation', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Ancho de la ménsula ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.lugWidth || ''}
          onChange={(e) => onFieldChange('lugWidth', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Longitud de la ménsula ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.lugLength || ''}
          onChange={(e) => onFieldChange('lugLength', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Espesor de la ménsula ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.lugThickness || ''}
          onChange={(e) => onFieldChange('lugThickness', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Excentricidad ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.lugEccentricity || ''}
          onChange={(e) => onFieldChange('lugEccentricity', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Diámetro del agujero ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.lugHoleDiameter || ''}
          onChange={(e) => onFieldChange('lugHoleDiameter', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <div className="text-sm text-gray-600 dark:text-gray-300">
        <div className="mb-1">Refuerzo de ménsula</div>
        <div className="inline-flex items-center space-x-1 rounded-lg border border-gray-200 bg-white p-1 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <button
            type="button"
            onClick={() => onFieldChange('lugGusset', false)}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              !form.lugGusset
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            No
          </button>
          <button
            type="button"
            onClick={() => onFieldChange('lugGusset', true)}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              form.lugGusset
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            Sí
          </button>
        </div>
      </div>

      {form.lugGusset && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Espesor del refuerzo ({lengthUnit})
          <input
            type="number"
            value={form.lugGussetThickness || ''}
            onChange={(e) =>
              onFieldChange('lugGussetThickness', e.target.value)
            }
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      )}

      <div className="text-sm text-gray-600 dark:text-gray-300">
        <div className="mb-1">Placa de apoyo</div>
        <div className="inline-flex items-center space-x-1 rounded-lg border border-gray-200 bg-white p-1 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <button
            type="button"
            onClick={() => onFieldChange('lugPadPlate', false)}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              !form.lugPadPlate
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            No
          </button>
          <button
            type="button"
            onClick={() => onFieldChange('lugPadPlate', true)}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              form.lugPadPlate
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            Sí
          </button>
        </div>
      </div>

      {form.lugPadPlate && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Ancho de la placa de apoyo ({lengthUnit})
            <input
              type="number"
              value={form.lugPadWidth || ''}
              onChange={(e) => onFieldChange('lugPadWidth', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Longitud de la placa de apoyo ({lengthUnit})
            <input
              type="number"
              value={form.lugPadLength || ''}
              onChange={(e) => onFieldChange('lugPadLength', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Espesor de la placa de apoyo ({lengthUnit})
            <input
              type="number"
              value={form.lugPadThickness || ''}
              onChange={(e) => onFieldChange('lugPadThickness', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </>
      )}
    </div>
  );
};

export default Lug;
