import React from 'react';

const RingSupport: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
}> = ({ form, onFieldChange }) => {
  const elevationLabel =
    form && form.vesselType === 'Horizontal' && /Ring/i.test(form.supportType)
      ? 'Distance from Head Weld'
      : 'Ring elevation';

  const boltLabel =
    form && form.vesselType === 'Horizontal' && /Ring/i.test(form.supportType)
      ? 'Anchor span (transverse)'
      : 'Bolt circle';

  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        {elevationLabel}
        <input
          type="number"
          value={form.ringElevation || ''}
          onChange={(e) => onFieldChange('ringElevation', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      {form &&
        form.vesselType === 'Horizontal' &&
        /Ring/i.test(form.supportType) && (
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Support Height
            <input
              type="number"
              value={form.ringSupportHeight || ''}
              onChange={(e) =>
                onFieldChange('ringSupportHeight', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        )}

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Ring profile type
        <select
          value={form.ringProfile || ''}
          onChange={(e) => onFieldChange('ringProfile', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>Type A</option>
          <option>Type B</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Ring OD
        <input
          type="number"
          value={form.ringOD || ''}
          onChange={(e) => onFieldChange('ringOD', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Ring ID
        <input
          type="number"
          value={form.ringID || ''}
          onChange={(e) => onFieldChange('ringID', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Hole type
        <input
          type="text"
          value={form.ringHoleType || ''}
          onChange={(e) => onFieldChange('ringHoleType', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Web height
        <input
          type="number"
          value={form.ringWebHeight || ''}
          onChange={(e) => onFieldChange('ringWebHeight', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Web thickness
        <input
          type="number"
          value={form.ringWebThickness || ''}
          onChange={(e) => onFieldChange('ringWebThickness', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Flange width
        <input
          type="number"
          value={form.ringFlangeWidth || ''}
          onChange={(e) => onFieldChange('ringFlangeWidth', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Flange thickness
        <input
          type="number"
          value={form.ringFlangeThickness || ''}
          onChange={(e) => onFieldChange('ringFlangeThickness', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <div className="text-sm text-gray-600 dark:text-gray-300">
        <div className="mb-1">Gussets</div>
        <div className="inline-flex items-center space-x-1 rounded-lg border border-gray-200 bg-white p-1 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <button
            type="button"
            onClick={() => onFieldChange('ringGussets', false)}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              !form.ringGussets
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            No
          </button>
          <button
            type="button"
            onClick={() => onFieldChange('ringGussets', true)}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              form.ringGussets
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            Yes
          </button>
        </div>
      </div>

      {form.ringGussets && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Quantity of gussets
            <input
              type="number"
              value={form.ringGussetQty || ''}
              onChange={(e) => onFieldChange('ringGussetQty', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Gusset thickness
            <input
              type="number"
              value={form.ringGussetThickness || ''}
              onChange={(e) =>
                onFieldChange('ringGussetThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Gusset width
            <input
              type="number"
              value={form.ringGussetWidth || ''}
              onChange={(e) => onFieldChange('ringGussetWidth', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </>
      )}

      <label className="text-sm text-gray-600 dark:text-gray-300">
        {boltLabel}
        <input
          type="number"
          value={form.ringBoltCircle || ''}
          onChange={(e) => onFieldChange('ringBoltCircle', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>
    </div>
  );
};

export default RingSupport;
