import { Link } from 'react-router';
import PageMeta from '../components/common/PageMeta';
import PageBreadcrumb from '../components/common/PageBreadCrumb';
import { GiIBeam } from 'react-icons/gi';
import { MdPropaneTank } from 'react-icons/md';

export default function ProjectSelection() {
  return (
    <>
      <PageMeta
        title="Proyectos Guardados | Selección de módulo"
        description="Selecciona el tipo de proyecto que deseas ver."
      />
      
      <PageBreadcrumb pageTitle="Selección de Módulo" />
      <div className="mx-auto max-w-screen-md px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white sm:text-3xl">
            Proyectos Guardados
          </h1>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            ¿Qué tipo de proyectos deseas consultar?
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          {/* Elementos a presión */}
          <Link
            to="/proyectos/presion"
            className="group relative flex flex-col items-center justify-center overflow-hidden rounded-2xl border border-gray-200 bg-white p-8 shadow-sm transition hover:-translate-y-1 hover:shadow-md dark:border-gray-800 dark:bg-gray-900/60"
          >
            <div className="mb-4 rounded-full bg-amber-50 p-4 text-amber-500 transition group-hover:bg-amber-100 dark:bg-amber-500/10 dark:text-amber-400">
              <MdPropaneTank className="h-12 w-12" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
              Elementos a presión
            </h3>
            <p className="mt-2 text-center text-sm text-gray-500 dark:text-gray-400">
              Soportes y recipientes a presión.
            </p>
          </Link>

          {/* Elementos estructurales */}
          <Link
            to="/proximamente"
            className="group relative flex flex-col items-center justify-center overflow-hidden rounded-2xl border border-gray-200 bg-white p-8 shadow-sm transition hover:-translate-y-1 hover:shadow-md dark:border-gray-800 dark:bg-gray-900/60"
          >
            <div className="mb-4 rounded-full bg-emerald-50 p-4 text-emerald-500 transition group-hover:bg-emerald-100 dark:bg-emerald-500/10 dark:text-emerald-400">
              <GiIBeam className="h-12 w-12" />
            </div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
              Elementos estructurales
            </h3>
            <p className="mt-2 text-center text-sm text-gray-500 dark:text-gray-400">
              Vigas y análisis de soldadura.
            </p>
          </Link>
        </div>
      </div>
    </>
  );
}
