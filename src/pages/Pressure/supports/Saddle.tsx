import React from 'react';

const Saddle: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
}> = ({ form, onFieldChange }) => {
  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Saddle height
        <input
          type="number"
          value={form.saddleHeight || ''}
          onChange={(e) => onFieldChange('saddleHeight', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Location (distance from head weld)
        <input
          type="number"
          value={form.saddleLocation || ''}
          onChange={(e) => onFieldChange('saddleLocation', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Contact angle
        <select
          value={form.saddleContactAngle || '120'}
          onChange={(e) => onFieldChange('saddleContactAngle', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>120</option>
          <option>150</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Web thickness
        <input
          type="number"
          value={form.saddleWebThickness || ''}
          onChange={(e) => onFieldChange('saddleWebThickness', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Base plate width
        <input
          type="number"
          value={form.saddleBasePlateWidth || ''}
          onChange={(e) =>
            onFieldChange('saddleBasePlateWidth', e.target.value)
          }
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Base plate length
        <input
          type="number"
          value={form.saddleBasePlateLength || ''}
          onChange={(e) =>
            onFieldChange('saddleBasePlateLength', e.target.value)
          }
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      {form && form.vesselType === 'Horizontal' && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Number of Ribs
            <select
              value={form.saddleRibCount || '3'}
              onChange={(e) => onFieldChange('saddleRibCount', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
            >
              <option>3</option>
              <option>5</option>
              <option>7</option>
            </select>
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Rib thickness (mm)
            <input
              type="number"
              step="any"
              value={form.saddleRibThickness || ''}
              onChange={(e) =>
                onFieldChange('saddleRibThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </>
      )}

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Friction type
        <select
          value={form.saddleFrictionType || ''}
          onChange={(e) => onFieldChange('saddleFrictionType', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>Frictionless</option>
          <option>High friction</option>
        </select>
      </label>
    </div>
  );
};

export default Saddle;
