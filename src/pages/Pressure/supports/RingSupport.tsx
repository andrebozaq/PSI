import React from 'react';

const RingSupport: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
  unitSystem?: 'SI' | 'US';
  mode?: 'design' | 'analysis';
}> = ({ form, onFieldChange, unitSystem = 'SI', mode = 'analysis' }) => {
  void mode;
  const lengthUnit = unitSystem === 'SI' ? 'mm' : 'in';
  const elevationLabel =
    form && form.vesselType === 'Horizontal' && /Ring/i.test(form.supportType)
      ? 'Distancia desde la soldadura del cabezal'
      : 'Elevación del anillo';

  const boltLabel =
    form && form.vesselType === 'Horizontal' && /Ring/i.test(form.supportType)
      ? 'Tramo de anclaje (transversal)'
      : 'Círculo de pernos';

  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        {elevationLabel} ({lengthUnit})
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
            Altura del soporte ({lengthUnit})
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
        Tipo de perfil del anillo
        <select
          value={form.ringProfile || ''}
          onChange={(e) => onFieldChange('ringProfile', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>Barra</option>
          <option>Viga I</option>
          <option>Sección T</option>
        </select>
      </label>

      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Ancho de la placa base ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.ringBasePlateWidth || ''}
            onChange={(e) =>
              onFieldChange('ringBasePlateWidth', e.target.value)
            }
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Largo de la placa base ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.ringBasePlateLength || ''}
            onChange={(e) =>
              onFieldChange('ringBasePlateLength', e.target.value)
            }
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      </div>

      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Altura del alma ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.ringWebHeight || ''}
            onChange={(e) => onFieldChange('ringWebHeight', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Espesor del alma ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.ringWebThickness || ''}
            onChange={(e) => onFieldChange('ringWebThickness', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Ancho de la brida ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.ringFlangeWidth || ''}
            onChange={(e) => onFieldChange('ringFlangeWidth', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Espesor de la brida ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.ringFlangeThickness || ''}
            onChange={(e) =>
              onFieldChange('ringFlangeThickness', e.target.value)
            }
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      </div>

      <div className="text-sm text-gray-600 dark:text-gray-300">
        <div className="mb-1">Refuerzos</div>
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
            Sí
          </button>
        </div>
      </div>

      {form.ringGussets && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Cantidad de refuerzos
            <input
              type="number"
              value={form.ringGussetQty || ''}
              onChange={(e) => onFieldChange('ringGussetQty', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Espesor del refuerzo ({lengthUnit})
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
            Ancho del refuerzo ({lengthUnit})
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
        {boltLabel} ({lengthUnit})
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
