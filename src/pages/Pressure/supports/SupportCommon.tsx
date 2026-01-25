import React from 'react';

const SupportCommon: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
}> = ({ form, onFieldChange }) => {
  return (
    <div className="space-y-3">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Material del soporte
        <select
          value={form.vesselMaterial}
          onChange={(e) => onFieldChange('vesselMaterial', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>Carbon steel</option>
          <option>Stainless steel 304</option>
          <option>Stainless steel 316</option>
          <option>Alloy steel</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Temperatura de diseño
        <input
          type="number"
          step="any"
          value={form.designTemperature}
          onChange={(e) => onFieldChange('designTemperature', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>
    </div>
  );
};

export default SupportCommon;
