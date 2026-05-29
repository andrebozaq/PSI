import React from 'react';

const GeometryCard: React.FC<{
  form: any;
  handleInputChange: any;
  unitSystem: 'SI' | 'US';
  handleFocus?: (key: string) => void;
  handleBlur?: (key: string) => void;
  touched?: Record<string, boolean>;
}> = ({ form, handleInputChange, unitSystem, handleFocus, handleBlur, touched }) => {
  const unit = unitSystem === 'SI' ? 'mm' : 'in';
  const lengthLabel =
    form && form.vesselType === 'Columna vertical' ? 'Altura' : 'Longitud';
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900 print:border-none print:shadow-none print:p-0 print:bg-transparent">
      <h3 className="mb-3 text-sm font-semibold text-gray-800 dark:text-gray-100 border-b border-gray-200 pb-1 uppercase print:text-black print:border-black print:text-lg">
        Geometría y Peso
      </h3>
      <div className="space-y-2">
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Diámetro exterior ({unit})
          <input
            type="number"
            step="any"
            value={form.outerDiameter}
            onChange={handleInputChange('outerDiameter')}
            onFocus={handleFocus ? () => handleFocus('outerDiameter') : undefined}
            onBlur={handleBlur ? () => handleBlur('outerDiameter') : undefined}
            min="0"
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
          />
          {touched?.outerDiameter && !form.outerDiameter && (
            <p className="text-xs text-red-500 mt-1">Este campo es obligatorio para realizar los cálculos.</p>
          )}
        </label>

        {!(form && form.vesselType === 'Esférico') && (
          <label className="text-sm text-gray-600 dark:text-gray-300">
            {lengthLabel} ({unit})
            <input
              type="number"
              step="any"
              value={form.length}
              onChange={handleInputChange('length')}
              min="0"
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
            />
          </label>
        )}

        {!(
          form &&
          (form.vesselType === 'Columna vertical' ||
            form.vesselType === 'Esférico' ||
            form.vesselType === 'Horizontal')
        ) && (
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Altura ({unit})
            <input
              type="number"
              step="any"
              value={form.height}
              onChange={handleInputChange('height')}
              min="0"
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
            />
          </label>
        )}

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Material del recipiente
          <select
            value={form.vesselMaterial}
            onChange={handleInputChange('vesselMaterial')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black print:appearance-none"
          >
            <option>Acero al carbono</option>
            <option>Acero inoxidable 304</option>
            <option>Acero inoxidable 316</option>
            <option>Acero aleado</option>
          </select>
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Espesor de pared ({unit})
          <input
            type="number"
            step="any"
            value={form.wallThickness}
            onChange={handleInputChange('wallThickness')}
            onFocus={handleFocus ? () => handleFocus('wallThickness') : undefined}
            onBlur={handleBlur ? () => handleBlur('wallThickness') : undefined}
            min="0"
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
          />
          {touched?.wallThickness && !form.wallThickness && (
            <p className="text-xs text-red-500 mt-1">Este campo es obligatorio para realizar los cálculos.</p>
          )}
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Espesor de aislamiento ({unit})
          <input
            type="number"
            step="any"
            value={form.insulationThickness}
            onChange={handleInputChange('insulationThickness')}
            min="0"
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
          />
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Nivel líquido (%)
          <input
            type="number"
            min="0"
            max="100"
            step="0.1"
            value={form.liquidLevelPercent}
            onChange={handleInputChange('liquidLevelPercent')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
          />
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Gravedad específica del fluido
          <input
            type="number"
            step="any"
            value={form.fluidSpecificGravity}
            onChange={handleInputChange('fluidSpecificGravity')}
            min="0"
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
          />
        </label>
      </div>
    </div>
  );
};

export default GeometryCard;
