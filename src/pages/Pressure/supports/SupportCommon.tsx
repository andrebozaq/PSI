import React from 'react';

const SupportCommon: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
  unitSystem?: 'SI' | 'US';
}> = ({ form, onFieldChange, unitSystem = 'SI' }) => {
  const temperatureUnit = unitSystem === 'SI' ? '°C' : '°F';

  return (
    <div className="space-y-3">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Material del soporte
        <select
          value={form.vesselMaterial}
          onChange={(e) => onFieldChange('vesselMaterial', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black print:appearance-none"
        >
          <option>Acero al carbono</option>
          <option>Acero inoxidable 304</option>
          <option>Acero inoxidable 316</option>
          <option>Acero aleado</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Temperatura de diseño ({temperatureUnit})
        <input
          type="number"
          step="any"
          min="0"
          value={form.designTemperature}
          onChange={(e) => onFieldChange('designTemperature', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
        />
      </label>
    </div>
  );
};

export default SupportCommon;
