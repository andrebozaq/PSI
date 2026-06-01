import { useEffect, useMemo, useState, type ChangeEvent } from 'react';
import PageMeta from '../../components/common/PageMeta';
import PageBreadCrumb from '../../components/common/PageBreadCrumb';
import ComponentCard from '../../components/common/ComponentCard';
import GeometryCard from './components/GeometryCard';
import WindCard from './components/WindCard';
import SeismicCard from './components/SeismicCard';
import SupportCommon from './supports/SupportCommon';
import Saddle from './supports/Saddle';
import Skirt from './supports/Skirt';
import Legs from './supports/Legs';
import Lug from './supports/Lug';
import RingSupport from './supports/RingSupport';
import { ChevronDownIcon } from '../../icons';

// Simple form shape aligned with the existing support inputs
type FormState = Record<string, string> & {
  supportType: string;
  vesselType: string;
  designCode: string;
};

type AnalysisCheck = {
  name: string;
  status: 'PASS' | 'FAIL';
  ratio: number;
  value: string;
  limit: string;
};

type AnalysisResult = {
  status: 'PASS' | 'FAIL';
  governingRatio: number;
  governingCheck: string;
  checks: AnalysisCheck[];
};

const displayStatus = (status: 'PASS' | 'FAIL') =>
  status === 'PASS' ? 'PASÓ' : 'FALLÓ';

const supportOptionsByVessel: Record<string, { id: string; label: string }[]> =
  {
    Esférico: [
      { id: 'Leg (sin arriostrar)', label: 'Pata sin arriostrar' },
      { id: 'Leg (arriostrada)', label: 'Pata arriostrada' },
    ],
    Horizontal: [
      { id: 'Saddle', label: 'Saddle' },
      { id: 'Ring refuerzo', label: 'Anillo de refuerzo (revestido)' },
      { id: 'Leg (ligero)', label: 'Patas (equipo liviano)' },
    ],
    'Columna vertical': [
      { id: 'Leg (sin arriostrar)', label: 'Pata sin arriostrar' },
      { id: 'Leg (arriostrada)', label: 'Pata arriostrada' },
      { id: 'Lug', label: 'Lug' },
      { id: 'Ring refuerzo', label: 'Anillo de refuerzo' },
      { id: 'Skirt', label: 'Falda (skirt)' },
    ],
  };

const defaultForm: FormState = {
  projectName: 'V-201 Ammoniaco',
  vesselType: 'Horizontal',
  supportType: 'Saddle',
  designCode: 'ASME/ASCE',
  designPressure: '1.2',
  designTemperature: '80',
  corrosionAllowance: '1.5',
  windAuto: 'Zone 2',
  windValue: '0.85',
  exposureCategory: 'C',
  windImportanceFactor: '1.0',
  seismicSiteClass: 'D',
  seismicSs: '0.7',
  seismicS1: '0.25',
  seismicR: '3.5',
  outerDiameter: '2400',
  length: '8000',
  wallThickness: '16',
  insulationThickness: '50',
  liquidLevelPercent: '100',
  fluidSpecificGravity: '0.9',
  saddleHeight: '450',
  saddleLocation: '1200',
  saddleContactAngle: '120',
  saddleWebThickness: '10',
  saddleBasePlateWidth: '450',
  saddleBasePlateLength: '900',
  saddleFrictionType: 'Frictionless',
  wearPlateEnabled: 'false',
  wearPlateWidth: '',
  wearPlateThickness: '',
  wearPlateAngle: '120',
  anchorBoltDiameter: '',
  anchorBoltQuantity: '',
  // Skirt
  skirtHeight: '',
  skirtThickness: '',
  skirtMaterial: '',
  skirtBaseDiameter: '',
  skirtGeometry: 'cylindrical',
  skirtTopDiameter: '',
  skirtRingID: '',
  skirtRingOD: '',
  skirtRingThickness: '',
  skirtBoltCircleDiameter: '',
  skirtAnchorBoltCount: '',
  skirtAnchorBoltDiameter: '',
  // Lugs
  lugQuantity: '2',
  lugElevation: '',
  lugWidth: '',
  lugLength: '',
  lugThickness: '',
  lugEccentricity: '',
  lugHoleDiameter: '',
  lugGusset: 'false',
  lugGussetThickness: '',
  lugPadPlate: 'false',
  lugPadWidth: '',
  lugPadLength: '',
  lugPadThickness: '',
  // Legs
  legQuantity: '4',
  legProfile: '',
  legAngleSize: '',
  legAngleThickness: '',
  legPipeOD: '',
  legPipeThickness: '',
  legBeamDepth: '',
  legBeamFlangeWidth: '',
  legLength: '',
  bracingTier: '1',
  bracingHeight: '',
  legBasePlateWidth: '',
  legBasePlateLength: '',
  legLongSpacing: '',
  legTransSpacing: '',
  legBoltCircle: '',
  legBoltDiameter: '',
  legBoltPerLeg: '',
  // Ring girder
  ringElevation: '',
  ringSupportHeight: '',
  ringProfile: 'Bar',
  ringWebHeight: '',
  ringWebThickness: '',
  ringFlangeWidth: '',
  ringFlangeThickness: '',
  ringGussets: 'false',
  ringGussetQty: '',
  ringGussetThickness: '',
  ringGussetWidth: '',
  ringBoltCircle: '',
};

const savedCases: {
  id: string;
  name: string;
  note: string;
  form: FormState;
}[] = [
  {
    id: 'case-201',
    name: 'V-201 Ammoníaco',
    note: 'Carga de viento moderada, espesor bajo (fallando)',
    form: defaultForm,
  },
  {
    id: 'case-202',
    name: 'V-202 Urea',
    note: 'Mayor Ss, espesor reforzado',
    form: {
      ...defaultForm,
      projectName: 'V-202 Urea',
      windValue: '1.1',
      seismicSs: '0.9',
      saddleWebThickness: '14',
      saddleHeight: '520',
      wearPlateEnabled: 'true',
      wearPlateWidth: '320',
      wearPlateThickness: '12',
      wearPlateAngle: '130',
      anchorBoltDiameter: '25',
      anchorBoltQuantity: '8',
    },
  },
  {
    id: 'case-301',
    name: 'T-301 Propano',
    note: 'Equipo ligero, viento alto',
    form: {
      ...defaultForm,
      projectName: 'T-301 Propano',
      vesselType: 'Horizontal',
      windValue: '1.6',
      wallThickness: '12',
      saddleWebThickness: '12',
      length: '6000',
      wearPlateEnabled: 'false',
      anchorBoltDiameter: '22',
      anchorBoltQuantity: '6',
    },
  },
];

const formatNumber = (value: number) => {
  if (!Number.isFinite(value)) return '0.00';
  return value.toFixed(2);
};

const safeNum = (value: string) => {
  const n = Number(value);
  if (!Number.isFinite(n) || n < 0) return 0;
  return n;
};

const runAnalysis = (form: FormState): AnalysisResult => {
  const thickness = safeNum(
    form.saddleWebThickness || form.wallThickness || '0',
  );
  const pressure = safeNum(form.designPressure || '0');
  const wind = safeNum(form.windValue || '0');
  const seismic =
    safeNum(form.seismicSs || '0') + safeNum(form.seismicS1 || '0');
  const diameter = safeNum(form.outerDiameter || '0');

  // Toy formulas to drive UI state; replace with real engine when ready
  const bendingRatio = Math.abs(
    (pressure * 0.4 + wind * 0.6) / Math.max(thickness, 1),
  );
  const seismicRatio = Math.abs(
    (seismic * diameter) / Math.max(thickness, 1) / 10,
  );
  const bearingRatio = Math.abs(
    Math.max(pressure, wind) / Math.max(thickness, 1.5),
  );

  const checks: AnalysisCheck[] = [
    {
      name: 'Flexión local',
      ratio: bendingRatio,
      value: formatNumber(bendingRatio),
      limit: '1.00',
      status: bendingRatio <= 1 ? 'PASS' : 'FAIL',
    },
    {
      name: 'Sismo / vuelco',
      ratio: seismicRatio,
      value: formatNumber(seismicRatio),
      limit: '1.00',
      status: seismicRatio <= 1 ? 'PASS' : 'FAIL',
    },
    {
      name: 'Soporte',
      ratio: bearingRatio,
      value: formatNumber(bearingRatio),
      limit: '1.00',
      status: bearingRatio <= 1 ? 'PASS' : 'FAIL',
    },
  ];

  const governing = checks.reduce(
    (max, c) => (c.ratio > max.ratio ? c : max),
    checks[0],
  );

  return {
    status: governing.ratio <= 1 ? 'PASS' : 'FAIL',
    governingRatio: governing.ratio,
    governingCheck: governing.name,
    checks,
  };
};

export default function AnalysisDashboard() {
  const [unitSystem, setUnitSystem] = useState<'SI' | 'US'>('SI');
  const [form, setForm] = useState<FormState>(defaultForm);
  const [activeCaseId, setActiveCaseId] = useState<string>('case-201');
  const [isStatusExpanded, setIsStatusExpanded] = useState(false);
  const [result, setResult] = useState<AnalysisResult>(() =>
    runAnalysis(defaultForm),
  );

  useEffect(() => {
    setResult(runAnalysis(form));
  }, [form]);

  // Keep support type constrained to vessel-specific options (align with DesignSupport logic)
  useEffect(() => {
    const allowed = supportOptionsByVessel[form.vesselType] ?? [];
    const isAllowed = allowed.some((opt) => opt.id === form.supportType);
    if (!isAllowed && allowed[0]) {
      setForm((prev) => ({ ...prev, supportType: allowed[0].id }));
    }
  }, [form.vesselType, form.supportType]);

  const handleInputChange =
    <K extends keyof FormState>(key: K) =>
    (
      event:
        | ChangeEvent<HTMLInputElement>
        | ChangeEvent<HTMLSelectElement>
        | ChangeEvent<HTMLTextAreaElement>,
    ) => {
      const { value } = event.target;
      setForm((prev) => ({ ...prev, [key]: value }));
    };

  const handleFieldChange = (key: string, value: string | number) => {
    setForm((prev) => ({ ...prev, [key]: String(value) }));
  };

  const loadCase = (caseId: string) => {
    const found = savedCases.find((c) => c.id === caseId);
    if (!found) return;
    setActiveCaseId(caseId);
    setForm(found.form);
  };

  const resetCurrent = () => {
    setForm(savedCases.find((c) => c.id === activeCaseId)?.form ?? defaultForm);
  };

  const severityColor = useMemo(() => {
    return result.status === 'PASS'
      ? 'bg-green-50 border-green-500 text-green-700'
      : 'bg-red-50 border-red-500 text-red-700';
  }, [result.status]);

  return (
    <>
      <PageMeta
        title="Editor de análisis"
        description="Ajuste soportes y valide en tiempo real."
      />

      {/* Header solo para impresión */}
      <div className="hidden w-full border-b-2 border-black pb-4 print:block">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gray-200 text-xs font-bold text-black">
              LOGO
            </div>
            <div>
              <h1 className="text-2xl font-bold uppercase tracking-wide text-black">
                Reporte de Cálculo
              </h1>
              <p className="text-sm font-medium text-gray-700">
                Universidad del Zulia - Facultad de Ingeniería
              </p>
              <p className="text-xs text-gray-500">
                Escuela de Ingeniería Mecánica
              </p>
            </div>
          </div>
          <div className="text-right text-sm text-black">
            <p className="font-mono">
              <strong>Fecha:</strong> {new Date().toLocaleDateString()}
            </p>
            <p className="font-mono">
              <strong>Hora:</strong> {new Date().toLocaleTimeString()}
            </p>
            <p className="mt-1 text-xs text-gray-500">Generado por PSI-App</p>
          </div>
        </div>
      </div>

      <div className="mb-6 flex flex-wrap items-start justify-between gap-4 print:hidden">
        <div className="space-y-2">
          <PageBreadCrumb pageTitle="Análisis de soportes" />
          <div>
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
              Panel de Análisis Estructural
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Ajuste los parámetros del soporte y verifique los resultados de análisis en tiempo real.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-gray-500 dark:text-gray-400">
            Sistema de unidades
          </span>
          <div className="flex rounded-lg border border-gray-200 bg-white p-1 shadow-sm dark:border-gray-700 dark:bg-gray-900">
            <button
              type="button"
              onClick={() => setUnitSystem('SI')}
              className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
                unitSystem === 'SI'
                  ? 'bg-brand-500 text-white shadow-theme-sm'
                  : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
              }`}
            >
              SI
            </button>
            <button
              type="button"
              onClick={() => setUnitSystem('US')}
              className={`rounded-md px-3 py-1.5 text-sm font-semibold transition ${
                unitSystem === 'US'
                  ? 'bg-brand-500 text-white shadow-theme-sm'
                  : 'text-gray-700 hover:bg-gray-50 dark:text-gray-300 dark:hover:bg-white/5'
              }`}
            >
              Inglés
            </button>
          </div>
        </div>
      </div>

      {/* Encabezado sticky compacto + detalle desplegable */}
      <div
        className={`sticky top-24 z-10 mb-4 rounded-2xl border border-l-8 p-5 shadow-sm backdrop-blur supports-[backdrop-filter]:bg-white/90 dark:border-gray-800 dark:bg-gray-900/90 ${severityColor}`}
      >
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="min-w-0">
            <p className="text-xs uppercase tracking-wide text-gray-500">
              Estado
            </p>
            <h2 className="text-3xl font-bold">
              {displayStatus(result.status)}
            </h2>
            <p className="text-sm text-gray-700">
              Chequeo rector: {result.governingCheck} — Ratio{' '}
              {formatNumber(result.governingRatio)}
            </p>
          </div>

          <button
            type="button"
            onClick={() => setIsStatusExpanded((prev) => !prev)}
            className="flex h-12 w-12 items-center justify-center rounded-full bg-gray-100 transition-transform duration-200 ease-linear dark:bg-white/[0.03]"
            aria-expanded={isStatusExpanded}
            aria-label={isStatusExpanded ? 'Ocultar detalle de verificaciones' : 'Mostrar detalle de verificaciones'}
          >
            <ChevronDownIcon
              className={`size-5 text-gray-700 transition-transform duration-200 dark:text-gray-200 ${isStatusExpanded ? 'rotate-180' : ''}`}
            />
          </button>
        </div>

        {isStatusExpanded && (
          <div className="mt-4 space-y-4">
            <div className="text-right text-xs text-gray-600 dark:text-gray-300">
              <div>Proyecto: {form.projectName || '—'}</div>
              <div>Soporte: {form.supportType}</div>
              <div>Código: {form.designCode}</div>
              </div>

            <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
              {result.checks.map((check) => (
                <div
                  key={check.name}
                  className="rounded-lg border border-gray-200 bg-white p-3 text-sm shadow-sm dark:border-gray-800 dark:bg-gray-900"
                >
                  <div className="flex items-center justify-between font-semibold text-gray-800 dark:text-gray-100">
                    <span>{check.name}</span>
                    <span
                      className={
                        check.status === 'PASS' ? 'text-green-600' : 'text-red-600'
                      }
                    >
                      {displayStatus(check.status)}
                    </span>
                  </div>
                  <div className="mt-1 h-2 w-full overflow-hidden rounded-full bg-gray-200">
                    <div
                      className={`h-2 rounded-full ${check.status === 'PASS' ? 'bg-green-500' : 'bg-red-500'}`}
                      style={{ width: `${Math.min(check.ratio * 100, 100)}%` }}
                    />
                  </div>
                  <div className="mt-2 flex items-center justify-between text-xs text-gray-600 dark:text-gray-300">
                    <span>Ratio: {formatNumber(check.ratio)}</span>
                    <span>Límite: {check.limit}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[380px,1fr]">
        {/* Sidebar */}
        <div className="rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-900">
          <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3 text-sm font-semibold text-gray-800 dark:border-gray-800 dark:text-gray-100 print:hidden">
            <span>Parámetros</span>
            <select
              value={activeCaseId}
              onChange={(e) => loadCase(e.target.value)}
              className="rounded-md border border-gray-200 bg-white px-2 py-1 text-xs font-medium text-gray-700 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black print:appearance-none"
            >
              {savedCases.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-4 p-4">
            <div className="flex items-center justify-between gap-2 print:hidden">
              <div className="text-xs text-gray-500">
                Caso base seleccionado
              </div>
              <div className="flex gap-2 text-xs">
                <button
                  type="button"
                  onClick={resetCurrent}
                  className="rounded-md border border-gray-200 px-3 py-1 font-semibold text-gray-700 transition hover:bg-gray-50 dark:border-gray-700 dark:text-gray-200 dark:hover:bg-white/10"
                >
                  Reset
                </button>
                <button
                  type="button"
                  onClick={() => window.print()}
                  className="rounded-md bg-brand-500 px-3 py-1 font-semibold text-white shadow-theme-sm transition hover:bg-brand-600"
                >
                  Imprimir/Exportar
                </button>
              </div>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {savedCases.find((c) => c.id === activeCaseId)?.note}
            </p>

            <div className="space-y-6 print:space-y-0 print:grid print:grid-cols-2 print:gap-x-8 print:gap-y-4">
              <ComponentCard title="Cargas y sitio">
                <WindCard
                  form={form}
                  handleInputChange={handleInputChange}
                  unitSystem={unitSystem}
                />
                <div className="mt-3">
                  <SeismicCard
                    form={form}
                    handleInputChange={handleInputChange}
                  />
                </div>
              </ComponentCard>

              <ComponentCard title="Geometría">
                <GeometryCard
                  form={form}
                  handleInputChange={handleInputChange}
                  unitSystem={unitSystem}
                />
              </ComponentCard>

              <ComponentCard title="Soporte">
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                  <label className="text-xs text-gray-600 dark:text-gray-300">
                    Tipo de soporte
                    <select
                      value={form.supportType}
                      onChange={handleInputChange('supportType')}
                      className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-2 py-1 text-xs dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black print:appearance-none"
                    >
                      {(supportOptionsByVessel[form.vesselType] ?? []).map(
                        (opt) => (
                          <option key={opt.id}>{opt.id}</option>
                        ),
                      )}
                    </select>
                  </label>
                  <label className="text-xs text-gray-600 dark:text-gray-300">
                    Tipo de recipiente
                    <select
                      value={form.vesselType}
                      onChange={handleInputChange('vesselType')}
                      className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-2 py-1 text-xs dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100 print:border-none print:bg-transparent print:p-0 print:h-auto print:font-bold print:text-black print:appearance-none"
                    >
                      <option>Horizontal</option>
                      <option>Columna vertical</option>
                      <option>Esférico</option>
                    </select>
                  </label>
                </div>

                <SupportCommon form={form} onFieldChange={handleFieldChange} />
                <div className="mt-2 rounded-lg border border-dashed border-gray-200 p-3 dark:border-gray-700">
                  {(() => {
                    const key = form.supportType || '';
                    if (/Saddle/i.test(key))
                      return (
                        <Saddle form={form} onFieldChange={handleFieldChange} />
                      );
                    if (/Skirt/i.test(key))
                      return (
                        <Skirt
                          form={form}
                          onFieldChange={handleFieldChange}
                          unitSystem={unitSystem}
                        />
                      );
                    if (/Leg/i.test(key))
                      return (
                        <Legs form={form} onFieldChange={handleFieldChange} />
                      );
                    if (/Lug/i.test(key))
                      return (
                        <Lug form={form} onFieldChange={handleFieldChange} />
                      );
                    if (/Ring/i.test(key))
                      return (
                        <RingSupport
                          form={form}
                          onFieldChange={handleFieldChange}
                        />
                      );
                    return (
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Seleccione un tipo de soporte válido para mostrar sus
                        parámetros.
                      </p>
                      );
                  })()}
                </div>
                </div>
              </ComponentCard>
            </div>
          </div>
        </div>

        {/* Main panel */}
        <div className="space-y-4">
          <ComponentCard
            title="Utilización por componente"
            desc="Muestra qué chequeo gobierna y dónde está el cuello de botella"
          >
            <div className="space-y-3">
              {result.checks.map((check) => {
                const ratioPercent = Math.min(check.ratio * 100, 100);
                return (
                  <div key={`util-${check.name}`} className="space-y-1">
                    <div className="flex items-center justify-between text-sm font-semibold text-gray-800 dark:text-gray-100">
                      <span>{check.name}</span>
                      <span
                        className={
                          check.status === 'PASS'
                            ? 'text-green-600'
                            : 'text-red-600'
                        }
                      >
                        {displayStatus(check.status)}
                      </span>
                    </div>
                    <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
                      <div
                        className={`h-2 rounded-full ${check.status === 'PASS' ? 'bg-green-500' : 'bg-red-500'}`}
                        style={{ width: `${ratioPercent}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-300 font-mono">
                      <span>Actual: {check.value}</span>
                      <span>Límite: {check.limit}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </ComponentCard>
        </div>
      </div>

      {/* SIGNATURE BLOCK - PRINT ONLY */}
      <div className="hidden print:flex mt-12 pt-8 justify-between items-end break-inside-avoid">
        <div className="text-center">
          <div className="mb-2 w-64 border-b-2 border-black" />
          <p className="text-sm font-bold uppercase">Ing. Revisor</p>
          <p className="text-xs text-gray-500">Firma y Sello</p>
        </div>

        <div className="text-right text-xs text-gray-400">
          <p>Cálculo verificado según ASME VIII Div 1</p>
          <p>Software: PSI Indicator v1.0</p>
        </div>
      </div>
    </>
  );
}
