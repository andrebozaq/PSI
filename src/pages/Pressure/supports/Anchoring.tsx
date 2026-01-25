import React from 'react';

const Anchoring: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
}> = ({ form, onFieldChange }) => {
  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Bolt quantity
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
        Bolt diameter
        <input
          type="number"
          step="any"
          value={form.boltDiameter || ''}
          onChange={(e) => onFieldChange('boltDiameter', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Bolt material
        <select
          value={form.boltMaterial || 'Carbon steel'}
          onChange={(e) => onFieldChange('boltMaterial', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>Carbon steel</option>
          <option>Stainless steel</option>
          <option>A325</option>
          <option>A490</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Embedment depth
        <input
          type="number"
          step="any"
          value={form.embedmentDepth || ''}
          onChange={(e) => onFieldChange('embedmentDepth', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Concrete strength (MPa)
        <input
          type="number"
          step="any"
          value={form.concreteStrength || ''}
          onChange={(e) => onFieldChange('concreteStrength', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Anchor Type
        <select
          value={form.anchorType || ''}
          onChange={(e) => onFieldChange('anchorType', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option value="">Select an anchor</option>
          <option>Hex Head Bolt</option>
          <option>L-Hook Bolt</option>
          <option>J-Hook Bolt</option>
          <option>Epoxy Anchor</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Edge Distance (Distancia al borde) (mm)
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
