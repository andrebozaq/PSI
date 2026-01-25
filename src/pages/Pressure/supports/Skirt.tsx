import React from 'react';

const Skirt: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
  unitSystem: 'SI' | 'US';
}> = ({ form, onFieldChange, unitSystem }) => {
  const boltCountValue = form.boltQuantity ?? form.skirtAnchorBoltCount ?? '';
  const boltDiameterValue =
    form.boltDiameter ?? form.skirtAnchorBoltDiameter ?? '';

  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Skirt height
        <input
          type="number"
          value={form.skirtHeight || ''}
          onChange={(e) => onFieldChange('skirtHeight', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Skirt thickness
        <input
          type="number"
          value={form.skirtThickness || ''}
          onChange={(e) => onFieldChange('skirtThickness', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Base diameter
        <input
          type="number"
          value={form.skirtBaseDiameter || ''}
          onChange={(e) => onFieldChange('skirtBaseDiameter', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Skirt Geometry
        <select
          value={form.skirtGeometry || ''}
          onChange={(e) => onFieldChange('skirtGeometry', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option value="cylindrical">Cylindrical (Straight)</option>
          <option value="conical">Conical (Tapered)</option>
        </select>
      </label>

      {form.skirtGeometry === 'conical' && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Top diameter
          <input
            type="number"
            value={form.skirtTopDiameter || ''}
            onChange={(e) => onFieldChange('skirtTopDiameter', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      )}

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Bolt Circle Diameter (Dbc)
        <input
          type="number"
          value={form.skirtBoltCircleDiameter || ''}
          onChange={(e) =>
            onFieldChange('skirtBoltCircleDiameter', e.target.value)
          }
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Number of Anchor Bolts
        <input
          type="number"
          value={boltCountValue}
          onChange={(e) => {
            onFieldChange('boltQuantity', e.target.value);
            onFieldChange('skirtAnchorBoltCount', e.target.value);
          }}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Bolt Diameter (Size)
        <input
          type="number"
          value={boltDiameterValue}
          onChange={(e) => {
            onFieldChange('boltDiameter', e.target.value);
            onFieldChange('skirtAnchorBoltDiameter', e.target.value);
          }}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <div className="text-sm text-gray-600 dark:text-gray-300">
        <div className="mb-1">Use Anchor Chairs?</div>
        <div className="inline-flex items-center space-x-1 rounded-lg border border-gray-200 bg-white p-1 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <button
            type="button"
            onClick={() => onFieldChange('skirtAnchorChairs', false)}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              !form.skirtAnchorChairs
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            No
          </button>
          <button
            type="button"
            onClick={() => onFieldChange('skirtAnchorChairs', true)}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              form.skirtAnchorChairs
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            Yes
          </button>
        </div>
      </div>

      {form.skirtAnchorChairs && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Chair Height
            <input
              type="number"
              value={form.skirtChairHeight || ''}
              onChange={(e) =>
                onFieldChange('skirtChairHeight', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Top Plate Width
            <input
              type="number"
              value={form.skirtChairTopPlateWidth || ''}
              onChange={(e) =>
                onFieldChange('skirtChairTopPlateWidth', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Top Plate Thickness
            <input
              type="number"
              value={form.skirtChairTopPlateThickness || ''}
              onChange={(e) =>
                onFieldChange('skirtChairTopPlateThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </>
      )}
    </div>
  );
};

export default Skirt;
