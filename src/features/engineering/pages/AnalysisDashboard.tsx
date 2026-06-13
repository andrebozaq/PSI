import { useEffect, useMemo, useState, type ChangeEvent } from 'react';
import PageMeta from '../../../components/common/PageMeta';
import PageBreadCrumb from '../../../components/common/PageBreadCrumb';
import ComponentCard from '../../../components/common/ComponentCard';
import GeometryCard from '../components/GeometryCard';
import WindCard from '../components/WindCard';
import SeismicCard from '../components/SeismicCard';
import SupportCommon from '../supports/SupportCommon';
import Saddle from '../supports/Saddle';
import Skirt from '../supports/Skirt';
import Legs from '../supports/Legs';
import Lug from '../supports/Lug';
import RingSupport from '../supports/RingSupport';
import { ChevronDownIcon } from '../../../icons';
import { runFinalStage } from '../supports/DesignCalculations/DesignEngine';
import { Modal } from '../../../components/ui/modal';
import { collection, query, where, getDocs, addDoc, updateDoc, doc, serverTimestamp } from 'firebase/firestore';
import { db } from '../../../config/firebase';
import { useAuth } from '../../auth/contexts/AuthContext';
import { useLocation } from 'react-router';

// Simple form shape aligned with the existing support inputs
type FormState = Record<string, string> & {
  supportType: string;
  vesselType: string;
  designCode: string;
};

type AnalysisCheck = {
  name: string;
  status: 'PASS' | 'FAIL' | 'PENDING' | 'REVIEW';
  ratio: number;
  value: string;
  limit: string;
};

type AnalysisResult = {
  status: 'PASS' | 'FAIL' | 'PENDING' | 'REVIEW';
  governingRatio: number;
  governingCheck: string;
  checks: AnalysisCheck[];
};

const displayStatus = (status: 'PASS' | 'FAIL' | 'PENDING' | 'REVIEW') => {
  if (status === 'PASS') return 'PASÓ';
  if (status === 'FAIL') return 'FALLÓ';
  if (status === 'REVIEW') return 'REVISAR';
  return 'PENDIENTE';
};

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
  projectName: '',
  vesselType: 'Horizontal',
  supportType: 'Saddle',
  designCode: 'ASME/ASCE',
  designPressure: '',
  designTemperature: '',
  corrosionAllowance: '',
  windAuto: 'Zone 2',
  windValue: '',
  exposureCategory: 'C',
  windImportanceFactor: '1.0',
  seismicSiteClass: 'D',
  seismicSs: '',
  seismicS1: '',
  seismicR: '3.5',
  outerDiameter: '',
  length: '',
  wallThickness: '',
  insulationThickness: '',
  liquidLevelPercent: '100',
  fluidSpecificGravity: '',
  saddleHeight: '',
  saddleLocation: '',
  saddleContactAngle: '120',
  saddleWebThickness: '',
  saddleBasePlateWidth: '',
  saddleBasePlateLength: '',
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


const formatNumber = (value: number) => {
  if (!Number.isFinite(value)) return '0.00';
  return value.toFixed(2);
};



const mapStatus = (statusStr: string): 'PASS' | 'FAIL' | 'PENDING' | 'REVIEW' => {
  if (statusStr === 'Cumple') return 'PASS';
  if (statusStr === 'No cumple') return 'FAIL';
  if (statusStr === 'Revisar') return 'REVIEW';
  return 'PENDING';
};

const mapRowToCheck = (row: any): AnalysisCheck => {
  const ratioMatch = row.actual.match(/[\d.]+/);
  const ratio = ratioMatch ? parseFloat(ratioMatch[0]) : 0;
  return {
    name: row.check,
    status: mapStatus(row.status),
    ratio: ratio,
    value: row.actual,
    limit: row.allowable,
  };
};

const runRealAnalysis = (form: FormState): AnalysisResult => {
  const snapshot = runFinalStage(form as any);
  const rows = snapshot.final?.verificationRows || [];
  
  if (rows.length === 0) {
    return {
      status: 'PENDING',
      governingRatio: 0,
      governingCheck: 'Sin chequeos',
      checks: [],
    };
  }

  const checks = rows.map(mapRowToCheck);
  
  const governing = checks.reduce(
    (max, c) => (c.ratio > max.ratio ? c : max),
    checks[0],
  );

  let overallStatus: 'PASS' | 'FAIL' | 'PENDING' | 'REVIEW' = 'PASS';
  if (checks.some(c => c.status === 'FAIL')) overallStatus = 'FAIL';
  else if (checks.some(c => c.status === 'REVIEW')) overallStatus = 'REVIEW';
  else if (checks.some(c => c.status === 'PENDING')) overallStatus = 'PENDING';

  return {
    status: overallStatus,
    governingRatio: governing.ratio,
    governingCheck: governing.name,
    checks,
  };
};

export default function AnalysisDashboard() {
  const { currentUser } = useAuth();
  const location = useLocation();
  const [unitSystem, setUnitSystem] = useState<'SI' | 'US'>('SI');
  const [form, setForm] = useState<FormState>(defaultForm);
  const [activeCaseId, setActiveCaseId] = useState<string>('new');
  const [isStatusExpanded, setIsStatusExpanded] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [projectSearch, setProjectSearch] = useState('');
  const [result, setResult] = useState<AnalysisResult>(() =>
    runRealAnalysis(defaultForm),
  );

  const [savedProjects, setSavedProjects] = useState<any[]>([]);
  const [materials, setMaterials] = useState<any[]>([]);
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [isSaveModalOpen, setIsSaveModalOpen] = useState(false);
  const [saveModalMessage, setSaveModalMessage] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      if (!currentUser) {
        setIsLoadingData(false);
        return;
      }
      try {
        const [matsSnap, projsSnap] = await Promise.all([
          getDocs(collection(db, 'materials')),
          getDocs(query(collection(db, 'studies'), where('userId', '==', currentUser.uid)))
        ]);
        const loadedMaterials = matsSnap.docs.map(d => ({ id: d.id, ...d.data() }));
        setMaterials(loadedMaterials);

        const loadedProjects = projsSnap.docs.map(d => ({ id: d.id, ...d.data() })).filter((p: any) => p.mode === 'analysis');
        setSavedProjects(loadedProjects);
        
        const projectFromState = location.state?.project;
        if (projectFromState) {
          const found: any = loadedProjects.find((p: any) => p.id === projectFromState.id);
          if (found) {
            setActiveCaseId(found.id);
            if (found.inputs) setForm(found.inputs);
          }
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setIsLoadingData(false);
      }
    };
    fetchData();
  }, [currentUser]);


  useEffect(() => {
    setResult(runRealAnalysis(form));
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
    setActiveCaseId(caseId);
    if (caseId === 'new') {
      setForm(defaultForm);
      return;
    }
    const found = savedProjects.find((c) => c.id === caseId);
    if (found && found.inputs) {
      setForm(found.inputs);
    }
  };

  const resetCurrent = () => {
    if (activeCaseId === 'new') setForm(defaultForm);
    else setForm(savedProjects.find((c) => c.id === activeCaseId)?.inputs ?? defaultForm);
  };

  const handleSave = async () => {
    if (!currentUser) return;
    if (!form.projectName?.trim()) {
      setSaveModalMessage('Por favor, asigne un nombre al proyecto antes de guardar');
      setIsSaveModalOpen(true);
      return;
    }
    try {
      const projectData = {
        userId: currentUser.uid,
        projectName: form.projectName || 'Análisis sin título',
        supportType: form.supportType,
        vesselType: form.vesselType,
        mode: 'analysis',
        unitSystem,
        inputs: form,
        results: { final: result },
        calculationStatus: result.status,
      };

      if (activeCaseId && activeCaseId !== 'new') {
        await updateDoc(doc(db, 'studies', activeCaseId), {
          ...projectData,
          updatedAt: serverTimestamp(),
        });
        setSaveModalMessage('¡Análisis actualizado con éxito!');
        setIsSaveModalOpen(true);
      } else {
        const docRef = await addDoc(collection(db, 'studies'), {
          ...projectData,
          createdAt: serverTimestamp(),
          updatedAt: serverTimestamp(),
        });
        setActiveCaseId(docRef.id);
        setSaveModalMessage('¡Análisis guardado con éxito!');
        setIsSaveModalOpen(true);
      }

      const projsSnap = await getDocs(query(collection(db, 'studies'), where('userId', '==', currentUser.uid)));
      setSavedProjects(projsSnap.docs.map(d => ({ id: d.id, ...d.data() })).filter((p: any) => p.mode === 'analysis'));
    } catch (error) {
      console.error('Error al guardar:', error);
      setSaveModalMessage('Hubo un error al guardar el análisis.');
      setIsSaveModalOpen(true);
    }
  };

  const severityColor = useMemo(() => {
    if (result.status === 'PASS') return 'bg-green-50 border-green-500 text-green-700';
    if (result.status === 'FAIL') return 'bg-red-50 border-red-500 text-red-700';
    if (result.status === 'REVIEW') return 'bg-amber-50 border-amber-500 text-amber-700';
    return 'bg-gray-50 border-gray-500 text-gray-700';
  }, [result.status]);

  const filteredDropdownProjects = useMemo(() => {
    return savedProjects.filter(p => 
      (p.projectName || p.name || 'Análisis sin título')
      .toLowerCase()
      .includes(projectSearch.toLowerCase())
    );
  }, [savedProjects, projectSearch]);

  const activeProjectName = useMemo(() => {
    if (activeCaseId === 'new') return 'Nuevo Análisis';
    const proj = savedProjects.find(p => p.id === activeCaseId);
    return proj ? (proj.projectName || proj.name || 'Análisis sin título') : 'Seleccionar...';
  }, [activeCaseId, savedProjects]);

  if (isLoadingData) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-brand-500 border-t-transparent"></div>
        <span className="ml-3 text-sm text-gray-500">Cargando datos...</span>
      </div>
    );
  }

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
                        check.status === 'PASS' ? 'text-green-600' : 
                        check.status === 'FAIL' ? 'text-red-600' :
                        check.status === 'REVIEW' ? 'text-amber-600' : 'text-gray-600'
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
                    <span>Valor actual: {check.value}</span>
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
            <div className="relative w-64 print:hidden">
              <div
                className="flex cursor-pointer items-center justify-between rounded-md border border-gray-200 bg-white px-3 py-1.5 text-xs font-medium text-gray-700 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              >
                <span className="truncate">{activeProjectName}</span>
                <ChevronDownIcon className={`size-4 transition-transform ${isDropdownOpen ? 'rotate-180' : ''}`} />
              </div>
              
              {isDropdownOpen && (
                <div className="absolute right-0 top-full mt-1 z-50 max-h-60 w-full overflow-y-auto rounded-lg border border-gray-200 bg-white shadow-lg dark:border-gray-700 dark:bg-gray-800">
                  <div className="sticky top-0 bg-white p-2 dark:bg-gray-800">
                    <input
                      type="text"
                      className="w-full rounded-md border border-gray-300 bg-white px-2 py-1.5 text-xs outline-none focus:border-brand-500 dark:border-gray-600 dark:bg-gray-900 dark:text-white"
                      placeholder="Buscar proyecto..."
                      value={projectSearch}
                      onChange={(e) => setProjectSearch(e.target.value)}
                      onClick={(e) => e.stopPropagation()}
                    />
                  </div>
                  <div 
                    className="cursor-pointer px-3 py-2 text-xs hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700"
                    onClick={() => {
                      loadCase('new');
                      setIsDropdownOpen(false);
                      setProjectSearch('');
                    }}
                  >
                    Nuevo Análisis
                  </div>
                  {filteredDropdownProjects.map((c) => (
                    <div
                      key={c.id}
                      className={`cursor-pointer px-3 py-2 text-xs hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-700 ${activeCaseId === c.id ? 'bg-brand-50 text-brand-600 dark:bg-brand-900/20' : ''}`}
                      onClick={() => {
                        loadCase(c.id);
                        setIsDropdownOpen(false);
                        setProjectSearch('');
                      }}
                    >
                      {c.projectName || c.name || 'Análisis sin título'}
                    </div>
                  ))}
                  {filteredDropdownProjects.length === 0 && (
                    <div className="px-3 py-2 text-xs text-gray-500">No se encontraron proyectos</div>
                  )}
                </div>
              )}
            </div>
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
                  onClick={handleSave}
                  className="rounded-md bg-blue-600 px-3 py-1 font-semibold text-white shadow-theme-sm transition hover:bg-blue-700"
                >
                  Guardar Análisis
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
              {savedProjects.find((c) => c.id === activeCaseId)?.note}
            </p>

            <div className="space-y-2 pb-2">
              <label className="block text-xs font-semibold text-gray-700 dark:text-gray-300">
                Nombre del Proyecto / Equipo
                <input
                  type="text"
                  value={form.projectName || ''}
                  onChange={handleInputChange('projectName')}
                  placeholder="Ej. V-201 Ammoníaco"
                  className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm transition focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
                />
              </label>
            </div>

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
                  dbMaterials={materials}
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

                <SupportCommon form={form} onFieldChange={handleFieldChange} dbMaterials={materials} />
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
                          dbMaterials={materials}
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
                          check.status === 'PASS' ? 'text-green-600' : 
                          check.status === 'FAIL' ? 'text-red-600' :
                          check.status === 'REVIEW' ? 'text-amber-600' : 'text-gray-600'
                        }
                      >
                        {displayStatus(check.status)}
                      </span>
                    </div>
                    <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
                      <div
                        className={`h-2 rounded-full ${
                          check.status === 'PASS' ? 'bg-green-500' : 
                          check.status === 'FAIL' ? 'bg-red-500' :
                          check.status === 'REVIEW' ? 'bg-amber-500' : 'bg-gray-500'
                        }`}
                        style={{ width: `${ratioPercent}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-300 font-mono">
                      <span>Valor actual: {check.value}</span>
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

      <Modal
        isOpen={isSaveModalOpen}
        onClose={() => setIsSaveModalOpen(false)}
        className="max-w-[400px] p-6 text-center"
        showCloseButton={false}
      >
        <div className="mb-4 flex justify-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600 dark:bg-green-500/20 dark:text-green-400">
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
        <h3 className="mb-2 text-lg font-bold text-gray-900 dark:text-white">Operación Exitosa</h3>
        <p className="mb-6 text-sm text-gray-600 dark:text-gray-400">
          {saveModalMessage}
        </p>
        <button
          onClick={() => setIsSaveModalOpen(false)}
          className="w-full rounded-lg bg-brand-500 px-4 py-2.5 text-sm font-semibold text-white shadow-theme-sm transition hover:bg-brand-600"
        >
          Aceptar
        </button>
      </Modal>
    </>
  );
}
