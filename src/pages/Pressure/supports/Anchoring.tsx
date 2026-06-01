import React from 'react';

const Anchoring: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
  unitSystem?: 'SI' | 'US';
  dbMaterials?: any[];
}> = ({ form, onFieldChange, unitSystem = 'SI', dbMaterials }) => {
  const lengthUnit = unitSystem === 'SI' ? 'mm' : 'in';
  const pressureUnit = unitSystem === 'SI' ? 'MPa' : 'psi';

  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Cantidad de pernos
        <select
          value={form.boltQuantity || '4'}
          onChange={(e) => onFieldChange('boltQuantity', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>2</option>
          <option>4</option>
          <option>6</option>
          <option>8</option>
          <option>12</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Diámetro del perno ({lengthUnit})
        <input
          type="number"
          step="any"
          value={form.boltDiameter || ''}
          onChange={(e) => onFieldChange('boltDiameter', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Material del perno
        <select
          value={form.boltMaterial || 'Carbon steel'}
          onChange={(e) => onFieldChange('boltMaterial', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option value="">Seleccione un material...</option>
          {dbMaterials && dbMaterials.map((mat: any) => (
            <option key={mat.id} value={mat.name}>
              {mat.name} ({mat.standard})
            </option>
          ))}
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Profundidad de anclaje ({lengthUnit})
        <input
          type="number"
          step="any"
          value={form.embedmentDepth || ''}
          onChange={(e) => onFieldChange('embedmentDepth', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Resistencia del concreto ({pressureUnit})
        <input
          type="number"
          step="any"
          value={form.concreteStrength || ''}
          onChange={(e) => onFieldChange('concreteStrength', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Tipo de anclaje
        <select
          value={form.anchorType || ''}
          onChange={(e) => onFieldChange('anchorType', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option value="">Selecciona un anclaje</option>
          <option>Perno de cabeza hexagonal</option>
          <option>Perno en L</option>
          <option>Perno en J</option>
          <option>Anclaje epóxico</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Distancia al borde ({lengthUnit})
        <input
          type="number"
          step="any"
          value={form.anchorEdgeDistance || ''}
          onChange={(e) => onFieldChange('anchorEdgeDistance', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>
    </div>
  );
};

export default Anchoring;
