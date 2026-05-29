import React from 'react';

const Skirt: React.FC<{
  form: Record<string, string>;
  onFieldChange: (k: string, v: string) => void;
  unitSystem?: 'SI' | 'US';
  mode?: 'design' | 'analysis';
}> = ({ form, onFieldChange, unitSystem, mode = 'analysis' }) => {
  const lengthUnit = unitSystem === 'US' ? 'in' : 'mm';
  void mode;
  const boltCountValue = form.boltQuantity ?? form.skirtAnchorBoltCount ?? '';
  const boltDiameterValue =
    form.boltDiameter ?? form.skirtAnchorBoltDiameter ?? '';
  const useAnchorChairs = form.skirtAnchorChairs === 'true';

  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Altura del faldón ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.skirtHeight || ''}
          onChange={(e) => onFieldChange('skirtHeight', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Espesor del faldón ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.skirtThickness || ''}
          onChange={(e) => onFieldChange('skirtThickness', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Material del faldón
        <select
          value={form.skirtMaterial || ''}
          onChange={(e) => onFieldChange('skirtMaterial', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>Acero al carbono</option>
          <option>Acero inoxidable 304</option>
          <option>Acero inoxidable 316</option>
          <option>Acero aleado</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Diámetro del agujero de acceso (mm)
        <input
          type="number"
          min="0"
          step="any"
          value={form.skirtAccessHoleDiameter || ''}
          onChange={(e) =>
            onFieldChange('skirtAccessHoleDiameter', e.target.value)
          }
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Diámetro de la base ({lengthUnit})
        <input
          type="number"
          min="0"
          value={form.skirtBaseDiameter || ''}
          onChange={(e) => onFieldChange('skirtBaseDiameter', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Geometría del faldón
        <select
          value={form.skirtGeometry || ''}
          onChange={(e) => onFieldChange('skirtGeometry', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option value="cylindrical">Cilíndrico (Recto)</option>
          <option value="conical">Cónico (Cono)</option>
        </select>
      </label>

      {form.skirtGeometry === 'conical' && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Diámetro superior ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.skirtTopDiameter || ''}
            onChange={(e) => onFieldChange('skirtTopDiameter', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      )}

      <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Diámetro interior del anillo base ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.skirtRingID || ''}
            onChange={(e) => onFieldChange('skirtRingID', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Diámetro exterior del anillo base ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.skirtRingOD || ''}
            onChange={(e) => onFieldChange('skirtRingOD', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Espesor del anillo base ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.skirtRingThickness || ''}
            onChange={(e) =>
              onFieldChange('skirtRingThickness', e.target.value)
            }
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      </div>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Diámetro del círculo de pernos (Dbc) ({lengthUnit})
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
        Número de pernos de anclaje
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
        Diámetro del perno (Tamaño) ({lengthUnit})
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
        <div className="mb-1">¿Usar sillas de anclaje?</div>
        <div className="inline-flex items-center space-x-1 rounded-lg border border-gray-200 bg-white p-1 shadow-sm dark:border-gray-700 dark:bg-gray-900">
          <button
            type="button"
            onClick={() => onFieldChange('skirtAnchorChairs', 'false')}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              !useAnchorChairs
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            No
          </button>
          <button
            type="button"
            onClick={() => onFieldChange('skirtAnchorChairs', 'true')}
            className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
              useAnchorChairs
                ? 'bg-brand-500 text-white shadow-theme-sm'
                : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
            }`}
          >
            Sí
          </button>
        </div>
      </div>

      {useAnchorChairs && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Altura de la silla ({lengthUnit})
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
            Ancho de la placa superior ({lengthUnit})
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
            Espesor de la placa superior ({lengthUnit})
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
