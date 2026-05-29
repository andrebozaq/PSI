import {
  ChangeEvent,
  FormEvent,
  useEffect,
  useMemo,
  useState,
  lazy,
  Suspense,
} from 'react';
import ComponentCard from '../../components/common/ComponentCard';
import PageBreadCrumb from '../../components/common/PageBreadCrumb';
import PageMeta from '../../components/common/PageMeta';
import PaginationWithTextAndIcon from '../../components/ui/pagination/PaginationWithTextAndIcon';
import GeometryCard from './components/GeometryCard';
import WindCard from './components/WindCard';
import SeismicCard from './components/SeismicCard';
import SupportCommon from './supports/SupportCommon';
import SummaryReport from './components/SummaryReport';
import {
  CalculationSnapshot,
  createEmptySnapshot,
  runBlockStage,
  runFinalStage,
  runLightweightStage,
} from './supports/DesignCalculations/DesignEngine';
import { DesignInputs } from './supports/DesignCalculations/Constants';
const Skirt = lazy(() => import('./supports/Skirt'));
const Legs = lazy(() => import('./supports/Legs'));
const Saddle = lazy(() => import('./supports/Saddle'));
const Lug = lazy(() => import('./supports/Lug'));
const RingSupport = lazy(() => import('./supports/RingSupport'));
const Anchoring = lazy(() => import('./supports/Anchoring'));

type UnitSystem = 'SI' | 'US';

type GeneralInfoForm = {
  projectName: string;
  service: string;
  designCode: string;
  designPressure: string;
  testPressure: string;
  designTemperature: string;
  corrosionAllowance: string;
  weldEfficiency: string;
  designLife: string;
  windPressure: string;
  seismicCoefficient: string;
  operatingWeight: string;
  testWeight: string;
  nozzleLoadNotes: string;
  notes: string;
  vesselType: string;
  orientation: string;
  supportType: string;
  // Geometry & weight
  outerDiameter?: string;
  length?: string;
  height?: string;
  vesselMaterial?: string;
  wallThickness?: string;
  insulationThickness?: string;
  liquidLevelPercent?: string;
  fluidSpecificGravity?: string;
  // Wind
  windAuto?: string;
  windValue?: string;
  exposureCategory?: string;
  windImportanceFactor?: string;
  // Seismic (ASME/ASCE)
  seismicSiteClass?: string;
  seismicSs?: string;
  seismicS1?: string;
  seismicR?: string;
  // Seismic (COVENIN)
  covenCity?: string;
  covenState?: string;
  covenSoilType?: string;
  covenImportanceGroup?: string;
  covenR?: string;
  // Saddle-specific
  saddleHeight?: string;
  saddleLocation?: string;
  saddleContactAngle?: string;
  saddleWebThickness?: string;
  saddleBasePlateWidth?: string;
  saddleBasePlateLength?: string;
  saddleFrictionType?: string;
  saddleRibCount?: string;
  saddleRibThickness?: string;
  wearPlateEnabled?: string;
  wearPlateThickness?: string;
  // Skirt-specific
  skirtHeight?: string;
  skirtThickness?: string;
  skirtBaseDiameter?: string;
  skirtTopDiameter?: string;
  skirtAccessHoleDiameter?: string;
  skirtRingID?: string;
  skirtRingOD?: string;
  skirtRingThickness?: string;
  skirtBoltCircleDiameter?: string;
  skirtAnchorChairs?: string;
  skirtChairHeight?: string;
  skirtChairTopPlateWidth?: string;
  skirtChairTopPlateThickness?: string;
  // Lug-specific
  lugQuantity?: string;
  lugElevation?: string;
  lugWidth?: string;
  lugLength?: string;
  lugThickness?: string;
  lugEccentricity?: string;
  lugHoleDiameter?: string;
  lugGusset?: string;
  lugGussetThickness?: string;
  lugPadPlate?: string;
  lugPadWidth?: string;
  lugPadLength?: string;
  lugPadThickness?: string;
  // Ring-specific
  ringProfile?: string;
  ringWebHeight?: string;
  ringWebThickness?: string;
  ringFlangeWidth?: string;
  ringFlangeThickness?: string;
  ringBasePlateWidth?: string;
  ringBasePlateLength?: string;
  ringGussets?: string;
  ringGussetQty?: string;
  ringGussetThickness?: string;
  ringGussetWidth?: string;
  // Leg-specific
  legProfileWidth?: string;
  legProfileThickness?: string;
  // Anchoring-specific
  boltQuantity?: string;
  boltDiameter?: string;
  boltMaterial?: string;
  embedmentDepth?: string;
  concreteStrength?: string;
  anchorType?: string;
  anchorEdgeDistance?: string;
  // Sincronización UI
  anchorBoltQuantity?: string;
  anchorBoltDiameter?: string;
  legBoltDiameter?: string;
  skirtAnchorBoltCount?: string;
  skirtAnchorBoltDiameter?: string;
};

const initialForm: GeneralInfoForm = {
  projectName: '',
  service: '',
  designCode: 'ASME/ASCE',
  designPressure: '',
  testPressure: '',
  designTemperature: '',
  corrosionAllowance: '',
  weldEfficiency: '1.0',
  designLife: '20',
  windPressure: '',
  seismicCoefficient: '',
  operatingWeight: '',
  testWeight: '',
  nozzleLoadNotes: '',
  notes: '',
  vesselType: 'Horizontal',
  orientation: 'Horizontal',
  supportType: 'Saddle',
  outerDiameter: '',
  length: '',
  height: '',
  vesselMaterial: 'Carbon steel',
  wallThickness: '',
  insulationThickness: '',
  liquidLevelPercent: '100',
  fluidSpecificGravity: '1.0',
  windAuto: 'Zone 2',
  windValue: '',
  exposureCategory: 'C',
  windImportanceFactor: '1.0',
  seismicSiteClass: 'D',
  seismicSs: '',
  seismicS1: '',
  seismicR: '',
  covenCity: '',
  covenState: '',
  covenSoilType: 'S3',
  covenImportanceGroup: 'B2',
  covenR: '4',
  saddleHeight: '',
  saddleLocation: '',
  saddleContactAngle: '120',
  saddleWebThickness: '',
  saddleBasePlateWidth: '',
  saddleBasePlateLength: '',
  saddleFrictionType: 'Frictionless',
  saddleRibCount: '3',
  saddleRibThickness: '',
  wearPlateEnabled: 'false',
  wearPlateThickness: '',
  skirtHeight: '',
  skirtThickness: '',
  skirtBaseDiameter: '',
  skirtTopDiameter: '',
  skirtAccessHoleDiameter: '',
  skirtRingID: '',
  skirtRingOD: '',
  skirtRingThickness: '',
  skirtBoltCircleDiameter: '',
  skirtAnchorChairs: 'false',
  skirtChairHeight: '',
  skirtChairTopPlateWidth: '',
  skirtChairTopPlateThickness: '',
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
  ringProfile: 'Barra',
  ringWebHeight: '',
  ringWebThickness: '',
  ringFlangeWidth: '',
  ringFlangeThickness: '',
  ringBasePlateWidth: '',
  ringBasePlateLength: '',
  ringGussets: 'false',
  ringGussetQty: '4',
  ringGussetThickness: '',
  ringGussetWidth: '',
  legProfileWidth: '',
  legProfileThickness: '',
  boltQuantity: '4',
  boltDiameter: '',
  boltMaterial: 'Acero al carbono',
  embedmentDepth: '',
  concreteStrength: '',
  anchorType: '',
  anchorEdgeDistance: '',
  anchorBoltQuantity: '4',
  anchorBoltDiameter: '',
  legBoltDiameter: '',
  skirtAnchorBoltCount: '4',
  skirtAnchorBoltDiameter: '',
};

const unitLabels = {
  pressure: { SI: 'MPa', US: 'psi' },
  temperature: { SI: '°C', US: '°F' },
  length: { SI: 'mm', US: 'in' },
};

const formatNumber = (value: number) => {
  if (!Number.isFinite(value)) return '';
  return Number.isInteger(value) ? value.toString() : value.toFixed(3);
};

const convertPressure = (value: string, from: UnitSystem, to: UnitSystem) => {
  if (!value) return value;
  const numeric = Number(value);
  if (Number.isNaN(numeric) || from === to) return value;
  const converted = to === 'US' ? numeric * 145.037738 : numeric / 145.037738;
  return formatNumber(converted);
};

const convertLength = (value: string, from: UnitSystem, to: UnitSystem) => {
  if (!value) return value;
  const numeric = Number(value);
  if (Number.isNaN(numeric) || from === to) return value;
  const converted = to === 'US' ? numeric / 25.4 : numeric * 25.4;
  return formatNumber(converted);
};

const convertTemperature = (
  value: string,
  from: UnitSystem,
  to: UnitSystem,
) => {
  if (!value) return value;
  const numeric = Number(value);
  if (Number.isNaN(numeric) || from === to) return value;
  const converted =
    to === 'US' ? numeric * (9 / 5) + 32 : (numeric - 32) * (5 / 9);
  return formatNumber(converted);
};

export default function DesignSupport() {
  /**
  * Objetivo: orquestar el wizard completo de diseño estructural de soportes.
  * Entradas: interacciones del usuario sobre formulario, selección de soporte y unidades.
  * Salida: snapshot de cálculo actualizado por etapas y vista final de reporte.
  * Norma/Criterio: flujo por etapas (lightweight → block → final) con sincronía de campos.
   */
  const [unitSystem, setUnitSystem] = useState<UnitSystem>('SI');
  const [form, setForm] = useState<GeneralInfoForm>(initialForm);
  const [step, setStep] = useState(1);
  const [calculationSnapshot, setCalculationSnapshot] =
    useState<CalculationSnapshot>(createEmptySnapshot);
  const totalSteps = 7;
  const [previewVesselType, setPreviewVesselType] = useState<string | null>(
    null,
  );
  const [previewSupportType, setPreviewSupportType] = useState<string | null>(
    null,
  );
  const [animDir, setAnimDir] = useState<'left' | 'right'>('right');
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  useEffect(() => {
    const timer = window.setTimeout(() => {
      console.log('[DesignSupport][live-form-input]', form);
      setCalculationSnapshot((prev) =>
        runLightweightStage(
          { ...(form as unknown as DesignInputs), unitSystem } as DesignInputs,
          prev,
        ),
      );
    }, 350);

    return () => window.clearTimeout(timer);
  }, [form]);

  useEffect(() => {
    if (step !== 7) return;

    console.log('[DesignSupport][final-stage-trigger]', {
      step,
      supportType: form.supportType,
      vesselType: form.vesselType,
    });

    setCalculationSnapshot((prev) =>
      runFinalStage(
        { ...(form as unknown as DesignInputs), unitSystem } as DesignInputs,
        prev,
      ),
    );
  }, [step, form]);

  // Orientation step removed per request; orientation can be inferred from vessel type later.

  const vesselOptions = [
    {
      id: 'Horizontal',
      label: 'Horizontal ',
      image: '/images/vessels/horizontal.jpg',
    },
    {
      id: 'Columna vertical',
      label: 'Columna vertical',
      image: '/images/vessels/vertical.png',
    },
    {
      id: 'Esférico',
      label: 'Esférico',
      image: '/images/vessels/sphere.png',
    },
  ];

  const supportOptionsByVessel: Record<
    string,
    { id: string; label: string; image: string }[]
  > = {
    Esférico: [
      {
        id: 'Leg (sin arriostrar)',
        label: 'Pata sin arriostrar',
        image: '/images/supports/leg.jpg',
      },
      {
        id: 'Leg (arriostrada)',
        label: 'Pata arriostrada',
        image: '/images/supports/leg.jpg',
      },
    ],
    Horizontal: [
      { id: 'Saddle', label: 'Silleta', image: '/images/supports/saddle.jpg' },
      {
        id: 'Ring refuerzo',
        label: 'Anillo de refuerzo',
        image: '/images/supports/ring.jpg',
      },
      {
        id: 'Leg (ligero)',
        label: 'Patas (equipo liviano)',
        image: '/images/supports/leg.jpg',
      },
    ],
    'Columna vertical': [
      {
        id: 'Leg (sin arriostrar)',
        label: 'Pata sin arriostrar',
        image: '/images/supports/leg.jpg',
      },
      {
        id: 'Leg (arriostrada)',
        label: 'Pata arriostrada',
        image: '/images/supports/leg.jpg',
      },
      { id: 'Lug', label: 'Ménsulas', image: '/images/supports/lug.jpg' },
      {
        id: 'Ring refuerzo',
        label: 'Anillo de refuerzo',
        image: '/images/supports/ring.jpg',
      },
      {
        id: 'Skirt',
        label: 'Faldón',
        image: '/images/supports/skirt.jpg',
      },
    ],
  };

  const stepTitles = useMemo(
    () => [
      'Información general',
      'Tipo de recipiente',
      'Cargas y criterio',
      'Tipo de soporte',
      'Materiales y corrosión',
      'Anclaje',
      'Reporte final',
    ],
    [],
  );

  const handleInputChange =
    <K extends keyof GeneralInfoForm>(key: K) =>
    (
      event: ChangeEvent<
        HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
      >,
    ) => {
      const { value } = event.target;
      setForm((prev) => ({ ...prev, [key]: value }));
    };

  const handleFocus = (key: string) => {
    setTouched((prev) => ({ ...prev, [key]: true }));
  };

  const handleBlur = (key: string) => {
    // Warning will be shown based on touched and empty value
  };

  const handleSupportFieldChange = (key: string, value: any) => {
    /**
     * Objetivo: mantener consistencia entre aliases de campos compartidos.
     * Entradas: clave/valor editados en submódulos de soporte.
     * Salida: estado `form` sincronizado (ej. diámetro/cantidad de pernos en anchor-leg-skirt).
     * Norma/Criterio: mapeo bidireccional de campos equivalentes para evitar desalineaciones.
     */
    setForm((prev) => {
      const next = { ...prev, [key]: value } as GeneralInfoForm &
        Record<string, any>;

      if (key === 'boltDiameter') {
        next.anchorBoltDiameter = value;
        next.legBoltDiameter = value;
        next.skirtAnchorBoltDiameter = value;
      }

      if (
        key === 'anchorBoltDiameter' ||
        key === 'legBoltDiameter' ||
        key === 'skirtAnchorBoltDiameter'
      ) {
        next.boltDiameter = value;
        next.anchorBoltDiameter = value;
        next.legBoltDiameter = value;
        next.skirtAnchorBoltDiameter = value;
      }

      if (key === 'boltQuantity') {
        next.anchorBoltQuantity = value;
        next.skirtAnchorBoltCount = value;
      }

      if (key === 'anchorBoltQuantity' || key === 'skirtAnchorBoltCount') {
        next.boltQuantity = value;
        next.anchorBoltQuantity = value;
        next.skirtAnchorBoltCount = value;
      }

      return next;
    });
  };

  const handleUnitChange = (nextUnit: UnitSystem) => {
    if (nextUnit === unitSystem) return;
    setForm((prev) => ({
      ...prev,
      designPressure: convertPressure(
        prev.designPressure,
        unitSystem,
        nextUnit,
      ),
      testPressure: convertPressure(prev.testPressure, unitSystem, nextUnit),
      designTemperature: convertTemperature(
        prev.designTemperature,
        unitSystem,
        nextUnit,
      ),
      corrosionAllowance: convertLength(
        prev.corrosionAllowance,
        unitSystem,
        nextUnit,
      ),
    }));
    setUnitSystem(nextUnit);
  };

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const nextSnapshot = runBlockStage(
      { ...(form as unknown as DesignInputs), unitSystem } as DesignInputs,
      calculationSnapshot,
    );
    setCalculationSnapshot(nextSnapshot);
    console.info('General design basis saved', {
      form,
      unitSystem,
      calculationSnapshot: nextSnapshot,
    });
  };

  const moveToStep = (targetStep: number) => {
    /**
     * Objetivo: gestionar navegación de pasos y disparo de cálculos por fase.
     * Entradas: paso objetivo solicitado por el usuario.
     * Salida: actualización de `step` y `calculationSnapshot` según etapa requerida.
     * Norma/Criterio: al avanzar, usa `runBlockStage`; en último paso, usa `runFinalStage`.
     */
    const boundedStep = Math.max(1, Math.min(totalSteps, targetStep));

    if (boundedStep > step) {
      if (boundedStep === totalSteps) {
        console.log('[DesignSupport][navigation][runFinalStage]', {
          from: step,
          to: boundedStep,
          supportType: form.supportType,
        });
        setCalculationSnapshot((prev) =>
          runFinalStage(
            { ...(form as unknown as DesignInputs), unitSystem } as DesignInputs,
            prev,
          ),
        );
      } else {
        console.log('[DesignSupport][navigation][runBlockStage]', {
          from: step,
          to: boundedStep,
          supportType: form.supportType,
        });
        setCalculationSnapshot((prev) =>
          runBlockStage(
            { ...(form as unknown as DesignInputs), unitSystem } as DesignInputs,
            prev,
          ),
        );
      }
    }

    setStep(boundedStep);
  };

  const renderGeneralInfoForm = () => (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <label className="space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          Proyecto / nombre del equipo
          <input
            type="text"
            value={form.projectName}
            onChange={handleInputChange('projectName')}
            placeholder="e.j., Contenedor de amoníaco V-201"
            className="w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:text-gray-100"
          />
        </label>

        <label className="space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          Fluído de trabajo
          <input
            type="text"
            value={form.service}
            onChange={handleInputChange('service')}
            placeholder="e.j., Aire seco, ammoníaco, nitrógeno"
            className="w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:text-gray-100"
          />
        </label>

        <label className="space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          Código de diseño / estandar
          <select
            value={form.designCode}
            onChange={handleInputChange('designCode')}
            className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
          >
            <option>ASME/ASCE</option>
            <option>COVENIN</option>
          </select>
        </label>

        <label className="space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          Eficiencia de soldadura
          <select
            value={form.weldEfficiency}
            onChange={handleInputChange('weldEfficiency')}
            className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
          >
            <option value="1.00">1.00 (Radiografía completa - RT-1)</option>
            <option value="0.85">0.85 (Radiografía parcial - RT-3)</option>
            <option value="0.70">0.70 (Sin radiografía)</option>
          </select>
        </label>

        <label className="space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          Presión de diseño ({unitLabels.pressure[unitSystem]})
          <input
            type="number"
            min="0"
            step="any"
            value={form.designPressure}
            onChange={handleInputChange('designPressure')}
            onFocus={() => handleFocus('designPressure')}
            onBlur={() => handleBlur('designPressure')}
            placeholder={`e.j., ${unitSystem === 'SI' ? '1.0' : '150'}`}
            className="w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:text-gray-100"
          />
          {touched.designPressure && !form.designPressure && (
            <p className="text-xs text-red-500 mt-1">Este campo es obligatorio para realizar los cálculos.</p>
          )}
        </label>

        <label className="space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          Temperatura de dseño ({unitLabels.temperature[unitSystem]})
          <input
            type="number"
            step="any"
            value={form.designTemperature}
            onChange={handleInputChange('designTemperature')}
            onFocus={() => handleFocus('designTemperature')}
            onBlur={() => handleBlur('designTemperature')}
            className="w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:text-gray-100"
          />
          {touched.designTemperature && !form.designTemperature && (
            <p className="text-xs text-red-500 mt-1">Este campo es obligatorio para realizar los cálculos.</p>
          )}
        </label>

        <label className="space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          Corrosión permitida ({unitLabels.length[unitSystem]})
          <input
            type="number"
            min="0"
            step="any"
            value={form.corrosionAllowance}
            onChange={handleInputChange('corrosionAllowance')}
            onFocus={() => handleFocus('corrosionAllowance')}
            onBlur={() => handleBlur('corrosionAllowance')}
            className="w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:text-gray-100"
          />
          {touched.corrosionAllowance && !form.corrosionAllowance && (
            <p className="text-xs text-red-500 mt-1">Este campo es obligatorio para realizar los cálculos.</p>
          )}
        </label>

        {/* internalDiameter removed per request */}

        <label className="space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
          Vida útil (años)
          <input
            type="number"
            min="0"
            step="1"
            value={form.designLife}
            onChange={handleInputChange('designLife')}
            className="w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      </div>

      <label className="block space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
        Notas / asunciones
        <textarea
          rows={3}
          value={form.notes}
          onChange={handleInputChange('notes')}
          placeholder="Condiciones de diseño, asunciones de corrosión, simportancia sismica y del viento, etc."
          className="w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <div className="flex flex-wrap items-center justify-end gap-3 print:hidden">
        <button
          type="button"
          onClick={() => setForm(initialForm)}
          className="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-white/5"
        >
          Limpiar
        </button>

        <button
          type="submit"
          className="rounded-lg bg-brand-500 px-4 py-2 text-sm font-semibold text-white shadow-theme-sm transition hover:bg-brand-600 focus:outline-none focus:ring-2 focus:ring-brand-400"
        >
          Guardar info general
        </button>
      </div>
    </form>
  );

  const renderLoadsForm = () => (
    <div className="space-y-6">
      <div className="text-sm font-semibold text-gray-700 dark:text-gray-200">
        Tipo de recipiente seleccionado: {form.vesselType || '-'}
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <GeometryCard
          form={form}
          handleInputChange={handleInputChange}
          unitSystem={unitSystem}
          handleFocus={handleFocus}
          handleBlur={handleBlur}
          touched={touched}
        />
        <WindCard
          form={form}
          handleInputChange={handleInputChange}
          unitSystem={unitSystem}
        />
        <SeismicCard form={form} handleInputChange={handleInputChange} />
      </div>

      <label className="block space-y-1 text-sm font-medium text-gray-700 dark:text-gray-300">
        Notas de cargas locales / toberas
        <textarea
          rows={3}
          value={form.nozzleLoadNotes}
          onChange={handleInputChange('nozzleLoadNotes')}
          placeholder="Cargas en boquillas, soportes de plataforma, transporte, etc."
          className="w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 focus:ring-0 dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      <p className="text-sm text-gray-600 dark:text-gray-400">
        Use unidades consistentes con el código de diseño seleccionado. Estas
        cargas se aplicarán antes de dimensionar el tipo de recipiente y su
        soporte.
      </p>
    </div>
  );

  const renderStepContent = () => {
    if (step === 1) return renderGeneralInfoForm();

    if (step === 2) {
      return (
        <div
          className="grid grid-cols-1 gap-6 md:grid-cols-2"
          onMouseLeave={() => setPreviewVesselType(null)}
        >
          <div className="space-y-3">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Tipos de recipiente
            </p>
            <div className="w-full overflow-hidden rounded-lg border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
              <ul className="flex flex-col">
                {vesselOptions.map((opt) => {
                  const isActive = form.vesselType === opt.id;
                  return (
                    <li
                      key={opt.id}
                      className="border-b border-gray-200 last:border-b-0 dark:border-gray-800"
                    >
                      <button
                        type="button"
                        className={`flex w-full items-center justify-between gap-3 px-3 py-2.5 text-sm font-medium transition ${
                          isActive
                            ? 'text-brand-600 bg-brand-50 dark:bg-brand-500/[0.12] dark:text-brand-400'
                            : 'text-gray-600 hover:bg-brand-50 hover:text-brand-600 dark:text-gray-400 dark:hover:bg-brand-500/[0.12] dark:hover:text-brand-400'
                        }`}
                        onMouseEnter={() => setPreviewVesselType(opt.id)}
                        onFocus={() => setPreviewVesselType(opt.id)}
                        onClick={() => {
                          const nextSupport =
                            supportOptionsByVessel[opt.id]?.[0]?.id ??
                            form.supportType;
                          setForm((prev) => ({
                            ...prev,
                            vesselType: opt.id,
                            supportType: nextSupport,
                            orientation:
                              opt.id === 'Horizontal'
                                ? 'Horizontal'
                                : 'Vertical',
                          }));
                          setPreviewVesselType(opt.id);
                          setPreviewSupportType(null);
                        }}
                      >
                        <span className="flex items-center gap-3">
                          <span className="inline-block h-2 w-2 rounded-full bg-gray-300" />
                          {opt.label}
                        </span>
                        <span className="text-xs text-gray-400">
                          {isActive ? 'Seleccionado' : 'Seleccionar'}
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
          </div>

          <div className="flex items-center justify-center">
            <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-900">
              <div className="relative flex h-64 w-full items-center justify-center bg-gray-50 p-4 dark:bg-gray-800">
                <img
                  src={
                    vesselOptions.find(
                      (opt) =>
                        opt.id === (previewVesselType ?? form.vesselType),
                    )?.image ?? vesselOptions[0].image
                  }
                  alt={previewVesselType ?? form.vesselType}
                  className="h-full w-full max-w-md rounded-xl object-cover transition-transform duration-300 group-hover:scale-105"
                />
              </div>
              <div className="border-t border-gray-200 px-4 py-3 text-center text-sm font-medium text-gray-800 dark:border-gray-700 dark:text-gray-200">
                {previewVesselType ?? form.vesselType}
              </div>
            </div>
          </div>
        </div>
      );
    }

    if (step === 3) return renderLoadsForm();

    if (step === 4) {
      const supportOptions = supportOptionsByVessel[form.vesselType] ?? [];
      const effectiveSupport =
        supportOptions.find((s) => s.id === form.supportType)?.id ??
        supportOptions[0]?.id ??
        '';
      return (
        <div
          className="grid grid-cols-1 gap-6 md:grid-cols-2"
          onMouseLeave={() => setPreviewSupportType(null)}
        >
          <div className="space-y-3">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Tipos de soporte
            </p>
            <div className="w-full overflow-hidden rounded-lg border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03]">
              <ul className="flex flex-col">
                {supportOptions.map((opt) => {
                  const isActive = form.supportType === opt.id;
                  return (
                    <li
                      key={opt.id}
                      className="border-b border-gray-200 last:border-b-0 dark:border-gray-800"
                    >
                      <button
                        type="button"
                        className={`flex w-full items-center justify-between gap-3 px-3 py-2.5 text-sm font-medium transition ${
                          isActive
                            ? 'text-brand-600 bg-brand-50 dark:bg-brand-500/[0.12] dark:text-brand-400'
                            : 'text-gray-600 hover:bg-brand-50 hover:text-brand-600 dark:text-gray-400 dark:hover:bg-brand-500/[0.12] dark:hover:text-brand-400'
                        }`}
                        onMouseEnter={() => setPreviewSupportType(opt.id)}
                        onFocus={() => setPreviewSupportType(opt.id)}
                        onClick={() => {
                          setForm((prev) => ({ ...prev, supportType: opt.id }));
                          setPreviewSupportType(opt.id);
                        }}
                      >
                        <span className="flex items-center gap-3">
                          <span className="inline-block h-2 w-2 rounded-full bg-gray-300" />
                          {opt.label}
                        </span>
                        <span className="text-xs text-gray-400">
                          {isActive ? 'Seleccionado' : 'Seleccionar'}
                        </span>
                      </button>
                    </li>
                  );
                })}
              </ul>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Los soportes se filtran según el tipo de recipiente seleccionado.
            </p>
          </div>

          <div className="flex items-center justify-center">
            <div className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-900">
              <div className="relative flex h-64 w-full items-center justify-center bg-gray-50 p-4 dark:bg-gray-800">
                <img
                  src={
                    supportOptions.find(
                      (opt) =>
                        opt.id ===
                        (previewSupportType ??
                          form.supportType ??
                          effectiveSupport),
                    )?.image ??
                    supportOptions[0]?.image ??
                    '/images/supports/saddle.jpg'
                  }
                  alt={
                    previewSupportType ?? form.supportType ?? effectiveSupport
                  }
                  className="h-full w-full max-w-md rounded-xl object-cover transition-transform duration-300 group-hover:scale-105"
                />
              </div>
              <div className="border-t border-gray-200 px-4 py-3 text-center text-sm font-medium text-gray-800 dark:border-gray-700 dark:text-gray-200">
                {previewSupportType ??
                  form.supportType ??
                  effectiveSupport ??
                  'Seleccione un soporte'}
              </div>
            </div>
          </div>
        </div>
      );
    }

    if (step === 5) {
      const supportTypeKey = form.supportType ?? '';
      const supportTypeDisplay =
        (
          supportOptionsByVessel[form.vesselType] ?? []
        ).find((option) => option.id === supportTypeKey)?.label ??
        ({
          Saddle: 'Silleta',
          Skirt: 'Faldón',
          Lug: 'Ménsulas',
          'Ring refuerzo': 'Anillo de refuerzo',
          'Leg (ligero)': 'Patas (equipo liviano)',
          'Leg (sin arriostrar)': 'Pata sin arriostrar',
          'Leg (arriostrada)': 'Pata arriostrada',
        }[supportTypeKey] ??
          supportTypeKey);
      const renderSupportFields = () => {
        if (/^Skirt/i.test(supportTypeKey))
          return (
            <Skirt
              form={form}
              onFieldChange={handleSupportFieldChange}
              unitSystem={unitSystem}
            />
          );
        if (/^Leg/i.test(supportTypeKey))
          return (
            <Legs
              form={form}
              onFieldChange={handleSupportFieldChange}
              unitSystem={unitSystem}
            />
          );
        if (/Saddle/i.test(supportTypeKey))
          return (
            <Saddle
              form={form}
              onFieldChange={handleSupportFieldChange}
              unitSystem={unitSystem}
            />
          );
        if (/Lug/i.test(supportTypeKey))
          return (
            <Lug
              form={form}
              onFieldChange={handleSupportFieldChange}
              unitSystem={unitSystem}
            />
          );
        if (
          /Ring/i.test(supportTypeKey) ||
          /Ring refuerzo/i.test(supportTypeKey)
        )
          return (
            <RingSupport
              form={form}
              onFieldChange={handleSupportFieldChange}
              unitSystem={unitSystem}
            />
          );
        return (
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Seleccione un tipo de soporte en la etapa anterior para editar sus
            parámetros.
          </div>
        );
      };

      return (
        <>
          <div className="-mt-1 mb-1 text-sm font-semibold text-gray-700 dark:text-gray-200">
            Soporte: {supportTypeDisplay || '-'}
          </div>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div className="space-y-3">
              <h2 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Configuración general del soporte
              </h2>
              <div className="w-full overflow-hidden rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]">
                <SupportCommon
                  form={form}
                  onFieldChange={handleSupportFieldChange}
                  unitSystem={unitSystem}
                />
              </div>
            </div>

            <div>
              <h3 className="mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                Parametros por tipo de soporte
              </h3>
              <div className="w-full overflow-hidden rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-800 dark:bg-white/[0.03]">
                <Suspense
                  fallback={
                    <div className="p-4 text-sm text-gray-500">Cargando...</div>
                  }
                >
                  {renderSupportFields()}
                </Suspense>
              </div>
            </div>
          </div>
        </>
      );
    }

    if (step === 6) {
      return (
        <Suspense
          fallback={
            <div className="p-4 text-sm text-gray-500">
              Cargando anclajes...
            </div>
          }
        >
          <Anchoring
            form={form}
            onFieldChange={handleSupportFieldChange}
            unitSystem={unitSystem}
          />
        </Suspense>
      );
    }

    if (step === 7) {
      console.log('[DesignSupport][summary-snapshot]', calculationSnapshot);
      return (
        <SummaryReport
          form={form}
          unitSystem={unitSystem}
          lightweight={calculationSnapshot.lightweight}
          block={calculationSnapshot.block}
          final={calculationSnapshot.final}
        />
      );
    }

    return (
      <div className="rounded-lg border border-dashed border-gray-200 bg-white p-4 text-sm text-gray-600 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-300">
        Esta etapa se reservará para materiales, corrosión y detalles de
        fijación del soporte. Use la navegación para revisar o adelantar pasos.
      </div>
    );
  };

  return (
    <>
      <PageMeta
        title="Pressure Vessel Design | General Information"
        description="Capture design basis and unit system before configuring vessel-specific details."
      />

      {/* Header visible only when printing */}
      <div className="mb-6 hidden border-b-2 border-black pb-4 print:block">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gray-200 text-xs font-bold text-black">
              LUZ
            </div>
            <div>
              <h1 className="text-2xl font-bold uppercase text-black">
                Reporte de Cálculo
              </h1>
              <p className="text-sm text-gray-700">
                Universidad del Zulia - Facultad de Ingeniería
              </p>
            </div>
          </div>
          <div className="text-right text-sm text-black">
            <p>
              <strong>Fecha:</strong> {new Date().toLocaleDateString()}
            </p>
            <p>
              <strong>Código:</strong> ASME VIII / COVENIN
            </p>
          </div>
        </div>
      </div>

      <div className="mb-6 flex flex-wrap items-start justify-between gap-4 print:hidden">
        <div className="space-y-2">
          <PageBreadCrumb pageTitle="Diseño de soportes" />
          <div>
            <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
              {step}. {stepTitles[step - 1]}
            </h1>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Ingrese las bases de diseño e información globales. Luego proceda a escoger el tipo
              de recipiente y su soporte.
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
              onClick={() => handleUnitChange('SI')}
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
              onClick={() => handleUnitChange('US')}
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

      <div className="space-y-6">
        <ComponentCard title="Datos de diseño">
          <div
            key={step}
            className={
              animDir === 'right'
                ? 'animate-fade-slide-right'
                : 'animate-fade-slide-left'
            }
          >
            {renderStepContent()}
          </div>
        </ComponentCard>

        <ComponentCard title="" className="print:hidden">
          <div
            key={`nav-${step}`}
            className={
              animDir === 'right'
                ? 'animate-fade-slide-right'
                : 'animate-fade-slide-left'
            }
          >
            <PaginationWithTextAndIcon
              currentStep={step}
              totalSteps={totalSteps}
              prevLabel="Atrás"
              nextLabel={step === totalSteps ? 'Terminado' : 'Siguiente'}
              onPrev={() => {
                setAnimDir('left');
                moveToStep(step - 1);
              }}
              onNext={() => {
                setAnimDir('right');
                moveToStep(step + 1);
              }}
              onPageSelect={(page) => {
                setAnimDir(page > step ? 'right' : 'left');
                moveToStep(page);
              }}
              className="px-0"
            />
          </div>
        </ComponentCard>
      </div>
    </>
  );
}
