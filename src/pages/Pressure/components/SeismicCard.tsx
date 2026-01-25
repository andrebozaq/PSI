import React from 'react';

const SeismicCard: React.FC<{
  form: any;
  handleInputChange: any;
}> = ({ form, handleInputChange }) => {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900">
      <h3 className="mb-3 text-sm font-semibold text-gray-800 dark:text-gray-100">
        Sismo
      </h3>
      <div className="space-y-2">
        {form.designCode === 'ASME/ASCE' ? (
          <>
            <label className="text-sm text-gray-600 dark:text-gray-300">
              Clase del sitio
              <select
                value={form.seismicSiteClass}
                onChange={handleInputChange('seismicSiteClass')}
                className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
              >
                <option>A</option>
                <option>B</option>
                <option>C</option>
                <option>D</option>
                <option>E</option>
                <option>F</option>
              </select>
            </label>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              Ss (short period)
              <input
                type="number"
                step="any"
                value={form.seismicSs}
                onChange={handleInputChange('seismicSs')}
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
              />
            </label>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              S1 (1-sec period)
              <input
                type="number"
                step="any"
                value={form.seismicS1}
                onChange={handleInputChange('seismicS1')}
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
              />
            </label>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              Factor de respuesta R
              <input
                type="text"
                value={form.seismicR}
                onChange={handleInputChange('seismicR')}
                placeholder="(configurable según soporte)"
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
              />
            </label>
          </>
        ) : (
          <>
            <label className="text-sm text-gray-600 dark:text-gray-300">
              Ciudad
              <input
                type="text"
                value={form.covenCity}
                onChange={handleInputChange('covenCity')}
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
              />
            </label>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              Estado
              <select
                value={form.covenState}
                onChange={handleInputChange('covenState')}
                className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
              >
                <option value="">Seleccione un estado</option>
                <option>Amazonas</option>
                <option>Anzoátegui</option>
                <option>Apure</option>
                <option>Aragua</option>
                <option>Barinas</option>
                <option>Bolívar</option>
                <option>Carabobo</option>
                <option>Cojedes</option>
                <option>Delta Amacuro</option>
                <option>Falcón</option>
                <option>Guárico</option>
                <option>Lara</option>
                <option>Mérida</option>
                <option>Miranda</option>
                <option>Monagas</option>
                <option>Nueva Esparta</option>
                <option>Portuguesa</option>
                <option>Sucre</option>
                <option>Táchira</option>
                <option>Trujillo</option>
                <option>La Guaira</option>
                <option>Yaracuy</option>
                <option>Zulia</option>
                <option>Distrito Capital</option>
                <option>Dependencias Federales</option>
              </select>
            </label>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              Tipo de suelo
              <select
                value={form.covenSoilType}
                onChange={handleInputChange('covenSoilType')}
                className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
              >
                <option>S1 (rock)</option>
                <option>S2</option>
                <option>S3</option>
                <option>S4 (soft)</option>
              </select>
            </label>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              Grupo de importancia
              <select
                value={form.covenImportanceGroup}
                onChange={handleInputChange('covenImportanceGroup')}
                className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
              >
                <option>A (critical)</option>
                <option>B1</option>
                <option>B2</option>
              </select>
            </label>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              Factor de respuesta R
              <input
                type="text"
                value={form.covenR}
                onChange={handleInputChange('covenR')}
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
              />
            </label>
          </>
        )}
      </div>
    </div>
  );
};

export default SeismicCard;
