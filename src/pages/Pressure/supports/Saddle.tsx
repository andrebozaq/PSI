import React from 'react';

const Saddle: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
  unitSystem?: 'SI' | 'US';
  mode?: 'design' | 'analysis';
}> = ({ form, onFieldChange, unitSystem = 'SI', mode: _mode = 'analysis' }) => {
  const lengthUnit = unitSystem === 'SI' ? 'mm' : 'in';

  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Altura de la silleta ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.saddleHeight || ''}
          onChange={(e) => onFieldChange('saddleHeight', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Locación (distancia desde la soldadura de cabeza) ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.saddleLocation || ''}
          onChange={(e) => onFieldChange('saddleLocation', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Ángulo de contacto (°)
        <select
          value={form.saddleContactAngle || '120'}
          onChange={(e) => onFieldChange('saddleContactAngle', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black print:appearance-none"
        >
          <option>120</option>
          <option>150</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Espesor del alma ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.saddleWebThickness || ''}
          onChange={(e) => onFieldChange('saddleWebThickness', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Ancho de la placa base ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.saddleBasePlateWidth || ''}
          onChange={(e) =>
            onFieldChange('saddleBasePlateWidth', e.target.value)
          }
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Largo de la placa base ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.saddleBasePlateLength || ''}
          onChange={(e) =>
            onFieldChange('saddleBasePlateLength', e.target.value)
          }
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
        />
      </label>

      {form && form.vesselType === 'Horizontal' && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Numero de costillas
            <select
              value={form.saddleRibCount || '3'}
              onChange={(e) => onFieldChange('saddleRibCount', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black print:appearance-none"
            >
              <option>3</option>
              <option>5</option>
              <option>7</option>
            </select>
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Espesor de la costilla ({lengthUnit})
            <input
              type="number"
              step="any"
              min="0"
              value={form.saddleRibThickness || ''}
              onChange={(e) =>
                onFieldChange('saddleRibThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
            />
          </label>
        </>
      )}

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Tipo de fricción
        <select
          value={form.saddleFrictionType || ''}
          onChange={(e) => onFieldChange('saddleFrictionType', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black print:appearance-none"
        >
          <option>Sin fricción</option>
          <option>Alta fricción</option>
        </select>
      </label>

      <div className="mt-3 rounded-lg border border-dashed border-gray-200 p-3 dark:border-gray-700 print:border-none print:p-0">
        <div className="mb-2 flex items-center justify-between text-sm font-semibold text-gray-800 dark:text-gray-100">
          <span>Usa placa</span>
          <label className="flex items-center gap-2 text-xs font-medium text-gray-600 dark:text-gray-300">
            <input
              type="checkbox"
              checked={form.wearPlateEnabled === 'true'}
              onChange={(e) =>
                onFieldChange(
                  'wearPlateEnabled',
                  e.target.checked ? 'true' : 'false',
                )
              }
              className="h-4 w-4 rounded border-gray-300 text-brand-500 focus:ring-brand-400 dark:border-gray-700 print:hidden"
            />
            <span className="print:hidden">Sí/No</span>
          </label>
        </div>

        {form.wearPlateEnabled === 'true' && (
          <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
            <label className="text-sm text-gray-600 dark:text-gray-300">
              Ancho (b) ({lengthUnit})
              <input
                type="number"
                min="0"
                value={form.wearPlateWidth || ''}
                onChange={(e) =>
                  onFieldChange('wearPlateWidth', e.target.value)
                }
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
              />
            </label>
            <label className="text-sm text-gray-600 dark:text-gray-300">
              Espesor (t) ({lengthUnit})
              <input
                type="number"
                min="0"
                value={form.wearPlateThickness || ''}
                onChange={(e) =>
                  onFieldChange('wearPlateThickness', e.target.value)
                }
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
              />
            </label>
            <label className="text-sm text-gray-600 dark:text-gray-300">
              Ángulo de extensión (°)
              <input
                type="number"
                min="0"
                value={form.wearPlateAngle || ''}
                onChange={(e) =>
                  onFieldChange('wearPlateAngle', e.target.value)
                }
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
              />
            </label>
          </div>
        )}
      </div>

      <div className="mt-2 rounded-lg border border-dashed border-gray-200 p-3 dark:border-gray-700 print:border-none print:p-0">
        <div className="mb-2 text-sm font-semibold text-gray-800 dark:text-gray-100">
          Anclaje
        </div>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Diámetro del perno ({lengthUnit})
            <input
              type="number"
              min="0"
              value={form.anchorBoltDiameter || ''}
              onChange={(e) =>
                onFieldChange('anchorBoltDiameter', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
            />
          </label>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Cantidad por silla
            <input
              type="number"
              min="0"
              value={form.anchorBoltQuantity || ''}
              onChange={(e) =>
                onFieldChange('anchorBoltQuantity', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black"
            />
          </label>
        </div>
      </div>
    </div>
  );
};

export default Saddle;
