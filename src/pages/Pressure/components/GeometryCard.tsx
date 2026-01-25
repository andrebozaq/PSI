import React from 'react';

const GeometryCard: React.FC<{
  form: any;
  handleInputChange: any;
  unitSystem: 'SI' | 'US';
}> = ({ form, handleInputChange, unitSystem }) => {
  const unit = unitSystem === 'SI' ? 'mm' : 'in';
  const lengthLabel =
    form && form.vesselType === 'Columna vertical' ? 'Altura' : 'Longitud';
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900">
      <h3 className="mb-3 text-sm font-semibold text-gray-800 dark:text-gray-100">
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
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>

        {!(form && form.vesselType === 'Esférico') && (
          <label className="text-sm text-gray-600 dark:text-gray-300">
            {lengthLabel} ({unit})
            <input
              type="number"
              step="any"
              value={form.length}
              onChange={handleInputChange('length')}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
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
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        )}

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Material del recipiente
          <select
            value={form.vesselMaterial}
            onChange={handleInputChange('vesselMaterial')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
          >
            <option>Carbon steel</option>
            <option>Stainless steel 304</option>
            <option>Stainless steel 316</option>
            <option>Alloy steel</option>
          </select>
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Espesor de pared ({unit})
          <input
            type="number"
            step="any"
            value={form.wallThickness}
            onChange={handleInputChange('wallThickness')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Espesor de aislamiento ({unit})
          <input
            type="number"
            step="any"
            value={form.insulationThickness}
            onChange={handleInputChange('insulationThickness')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
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
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>

        <label className="text-sm text-gray-600 dark:text-gray-300">
          Gravedad específica del fluido
          <input
            type="number"
            step="any"
            value={form.fluidSpecificGravity}
            onChange={handleInputChange('fluidSpecificGravity')}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      </div>
    </div>
  );
};

export default GeometryCard;
