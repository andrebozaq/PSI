import React from 'react';

const Lug: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
}> = ({ form, onFieldChange }) => {
  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Lug quantity
        <select
          value={form.lugQuantity || '2'}
          onChange={(e) => onFieldChange('lugQuantity', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>2</option>
          <option>4</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Lug elevation
        <input
          type="number"
          value={form.lugElevation || ''}
          onChange={(e) => onFieldChange('lugElevation', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Lug width
        <input
          type="number"
          value={form.lugWidth || ''}
          onChange={(e) => onFieldChange('lugWidth', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Lug length
        <input
          type="number"
          value={form.lugLength || ''}
          onChange={(e) => onFieldChange('lugLength', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Lug thickness
        <input
          type="number"
          value={form.lugThickness || ''}
          onChange={(e) => onFieldChange('lugThickness', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Eccentricity
        <input
          type="number"
          value={form.lugEccentricity || ''}
          onChange={(e) => onFieldChange('lugEccentricity', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Hole diameter
        <input
          type="number"
          value={form.lugHoleDiameter || ''}
          onChange={(e) => onFieldChange('lugHoleDiameter', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <div className="text-sm text-gray-600 dark:text-gray-300">
        <div className="mb-1">Stiffener gusset</div>
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
            Yes
          </button>
        </div>
      </div>

      {form.lugGusset && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Gusset thickness
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
        <div className="mb-1">Pad plate</div>
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
            Yes
          </button>
        </div>
      </div>

      {form.lugPadPlate && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Pad plate width
            <input
              type="number"
              value={form.lugPadWidth || ''}
              onChange={(e) => onFieldChange('lugPadWidth', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Pad plate length
            <input
              type="number"
              value={form.lugPadLength || ''}
              onChange={(e) => onFieldChange('lugPadLength', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Pad thickness
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
