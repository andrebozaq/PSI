import { useRef } from 'react';
import ComponentCard from '../../../components/common/ComponentCard';
import Alert from '../../../components/ui/alert/Alert';
import {
  BlockResults,
  FinalDesignResults,
  LightweightResults,
} from '../supports/DesignCalculations/Constants';

type Props = {
  mode?: 'design' | 'analysis';
  form: any;
  unitSystem: 'SI' | 'US';
  lightweight: LightweightResults;
  block: BlockResults;
  final: FinalDesignResults;
  onSave?: () => void;
};

const unitLabels = {
  pressure: { SI: 'MPa', US: 'psi' },
  temperature: { SI: '°C', US: '°F' },
  length: { SI: 'mm', US: 'in' },
  force: { SI: 'kN', US: 'kips' },
  area: { SI: 'mm²', US: 'in²' },
  section: { SI: 'mm³', US: 'in³' },
  moment: { SI: 'kN·m', US: 'kip·ft' },
};

export default function SummaryReport({
  mode = 'design',
  form,
  unitSystem,
  lightweight,
  block,
  final,
  onSave,
}: Props) {
  /**
  * Objetivo: renderizar el reporte final del wizard de soporte.
  * Entradas: formulario, unidad activa y snapshot de resultados (`lightweight`, `block`, `final`).
  * Salida: vista consolidada con panel en vivo, tablas de diseño y observaciones imprimibles.
  * Norma/Criterio: representación visual de estados `Cumple/No cumple/Revisar/Pendiente`.
   */
  const printRef = useRef<HTMLDivElement | null>(null);
  const lengthUnit = unitLabels.length[unitSystem];
  const pressureUnit = unitLabels.pressure[unitSystem];
  const forceUnit = unitLabels.force[unitSystem];
  const areaUnit = unitLabels.area[unitSystem];
  const sectionUnit = unitLabels.section[unitSystem];
  const momentUnit = unitLabels.moment[unitSystem];
  const isSkirt = /^Skirt/i.test(form.supportType || '');
  const isLeg = /^Leg/i.test(form.supportType || '');
  const isLug = /^Lug/i.test(form.supportType || '');
  const isRing = /^Ring/i.test(form.supportType || '');
  const isSaddle = /Saddle/i.test(form.supportType || '');
  const hasAnchoring =
    Number(form.boltQuantity || form.anchorBoltQuantity || form.skirtAnchorBoltCount || 0) > 0 ||
    Number(
      form.boltDiameter ||
        form.anchorBoltDiameter ||
        form.legBoltDiameter ||
        form.skirtAnchorBoltDiameter ||
        0,
    ) > 0;
  const boltUnitText = unitSystem === 'US' ? '1 pulgada' : '25 mm';
  const derived = lightweight.derived;
  const blockValues = block.values;

  const formatDerived = (value: unknown) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return '-';
    return Number.isInteger(numeric) ? `${numeric}` : numeric.toFixed(2);
  };

  const formatLengthFromMm = (value: unknown) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return '-';
    const converted = unitSystem === 'US' ? numeric / 25.4 : numeric;
    return Number.isInteger(converted)
      ? `${converted}`
      : converted.toFixed(2);
  };

  const formatForceFromkN = (value: unknown) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return '-';
    const converted = unitSystem === 'US' ? numeric * 0.2248089431 : numeric;
    return Number.isInteger(converted) ? `${converted}` : converted.toFixed(2);
  };

  const formatStressFromMPa = (value: unknown) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return '-';
    const converted = unitSystem === 'US' ? numeric * 145.037738 : numeric;
    return Number.isInteger(converted) ? `${converted}` : converted.toFixed(2);
  };

  const formatAreaFromMm2 = (value: unknown) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return '-';
    const converted = unitSystem === 'US' ? numeric / 645.16 : numeric;
    return Number.isInteger(converted) ? `${converted}` : converted.toFixed(2);
  };

  const formatSectionFromMm3 = (value: unknown) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return '-';
    const converted = unitSystem === 'US' ? numeric / 16387.064 : numeric;
    return Number.isInteger(converted) ? `${converted}` : converted.toFixed(2);
  };

  const formatMomentFromkNm = (value: unknown) => {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return '-';
    const converted = unitSystem === 'US' ? numeric * 0.7375621493 : numeric;
    return Number.isInteger(converted) ? `${converted}` : converted.toFixed(2);
  };

  const getStatusClassName = (status: unknown) => {
    /**
     * Objetivo: convertir estado textual a estilo visual de cumplimiento.
     * Entradas: estado de verificación (`Cumple`, `No cumple`, `Revisar`, `Pendiente`).
     * Salida: clases CSS de color/peso para tabla y alertas.
     * Norma/Criterio: semáforo de estado (verde, rojo, ámbar, neutro).
     */
    const normalized = String(status ?? '').trim().toLowerCase();
    if (normalized === 'cumple') {
      return 'font-semibold text-green-700 dark:text-green-400';
    }
    if (normalized === 'no cumple' || normalized === 'error' || normalized === 'falló') {
      return 'font-semibold text-red-700 dark:text-red-400';
    }
    if (normalized === 'revisar' || normalized === 'pendiente') {
      return 'font-semibold text-amber-700 dark:text-amber-400';
    }
    return 'font-medium text-gray-700 dark:text-gray-300';
  };

  const recommendedDimensionsRows = final.recommendedDimensions.length
    ? final.recommendedDimensions
    : isSkirt
    ? [
        {
          parameter: 'Espesor Mínimo del Faldón (t)',
          value: `Pendiente de cálculo (ej.: 10.5 ${lengthUnit})`,
        },
        {
          parameter: 'Espesor Mínimo del Anillo Base',
          value: `Pendiente de cálculo (ej.: 25.0 ${lengthUnit})`,
        },
        {
          parameter: 'Ancho Mínimo del Anillo Base',
          value: `Pendiente de cálculo (ej.: 200 ${lengthUnit})`,
        },
        {
          parameter: 'Criterio Sísmico (Tensión)',
          value: 'Pendiente de cálculo (Pernos Requeridos / No Requeridos)',
        },
        {
          parameter: 'Anclaje',
          value: `Pendiente de cálculo (ej.: 12 pernos de ${boltUnitText})`,
        },
      ]
    : [
        {
          parameter: 'Dimensiones mínimas recomendadas del soporte',
          value: 'Pendiente de cálculo',
        },
        {
          parameter: 'Criterio sísmico (tensión)',
          value: 'Pendiente de cálculo (Pernos Requeridos / No Requeridos)',
        },
        {
          parameter: 'Anclaje recomendado',
          value: 'Pendiente de cálculo',
        },
      ];

  const calculationVerificationRows = (final.verificationRows.length
    ? final.verificationRows
    : [
        {
          check: 'Carga axial',
          actual: 'Pendiente de cálculo',
          allowable: 'Pendiente de cálculo',
          status: 'Pendiente',
        },
        {
          check: 'Momento por viento',
          actual: 'Pendiente de cálculo',
          allowable: 'Pendiente de cálculo',
          status: 'Pendiente',
        },
        {
          check: 'Momento por sismo',
          actual: 'Pendiente de cálculo',
          allowable: 'Pendiente de cálculo',
          status: 'Pendiente',
        },
        {
          check: 'Tracción en pernos',
          actual: 'Pendiente de cálculo',
          allowable: 'Pendiente de cálculo',
          status: 'Pendiente',
        },
      ]).map(row => {
        const actualStr = String(row.actual).trim().toLowerCase();
        const isInvalid = actualStr.includes('nan') || actualStr.includes('n/a') || actualStr.includes('infinity');
        if (isInvalid) {
          return { ...row, status: 'ERROR' };
        }
        return row;
      });





  const MAX_NOTES_VISIBLE = 8;
  const MAX_NOTE_CHARS = 180;
  const compactNote = (text: string) => {
    const normalized = String(text ?? '').replace(/\s+/g, ' ').trim();
    if (normalized.length <= MAX_NOTE_CHARS) return normalized;
    return `${normalized.slice(0, MAX_NOTE_CHARS - 1)}…`;
  };
  const displayedNotes = final.notes.slice(0, MAX_NOTES_VISIBLE).map(compactNote);
  const hiddenNotesCount = Math.max(0, final.notes.length - displayedNotes.length);

  const isSuccess = calculationVerificationRows.every(row => {
    const status = String(row.status ?? '').trim().toLowerCase();
    return status === 'pass' || status === 'cumple';
  });

  const summaryAlert: {
    variant: 'success' | 'error' | 'warning' | 'info';
    title: string;
    message: string;
  } = isSuccess
    ? {
        variant: 'success',
        title: 'Verificación de diseño',
        message: 'Tu diseño pasó exitosamente.',
      }
    : {
        variant: 'error',
        title: 'Verificación fallida',
        message:
          'El diseño no cumple con los criterios o contiene parámetros inválidos (N/A).',
      };

  const handlePrint = () => {
    /**
     * Objetivo: imprimir/exportar el resumen visible del reporte.
     * Entradas: referencia del contenedor de impresión (`printRef`).
     * Salida: ventana imprimible con HTML y estilos actuales.
     * Norma/Criterio: mantiene fidelidad visual para revisión documental.
     */
    const el = printRef.current;
    if (!el) return window.print();
    const printWindow = window.open('', '_blank', 'width=900,height=700');
    if (!printWindow) return window.print();

    const links = Array.from(
      document.querySelectorAll('link[rel="stylesheet"], style'),
    )
      .map((l) => l.outerHTML)
      .join('\n');

    const html = `<!doctype html><html><head><meta charset="utf-8"><title>${mode === 'analysis' ? 'Reporte de Verificación Estructural' : 'Reporte de Diseño Estructural'}</title>${links}<style>@media print{.no-print{display:none!important}.page-break{page-break-after:always}}</style></head><body>${el.innerHTML}</body></html>`;
    printWindow.document.open();
    printWindow.document.write(html);
    printWindow.document.close();
    printWindow.focus();
    setTimeout(() => {
      printWindow.print();
    }, 250);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-end gap-3 no-print">
        {onSave && (
          <button
            type="button"
            onClick={onSave}
            className="rounded-md bg-green-600 px-4 py-2 text-sm font-semibold text-white shadow-theme-sm transition hover:bg-green-700"
          >
            Guardar Proyecto
          </button>
        )}
        <button
          type="button"
          onClick={handlePrint}
          className="rounded-md bg-brand-500 px-4 py-2 text-sm font-semibold text-white shadow-theme-sm transition hover:bg-brand-600"
        >
          Imprimir / Exportar
        </button>
      </div>

      <div ref={printRef} id="summary-print-area">
        {/* Print Header */}
        <div className="mb-6 hidden border-b-2 border-gray-300 pb-4 print:block dark:border-gray-800">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-gray-100 text-xs font-bold text-gray-800 dark:bg-gray-800 dark:text-gray-100">
                LUZ
              </div>
              <div>
                <h1 className="text-xl font-bold uppercase text-gray-900 dark:text-white">
                  {mode === 'analysis' ? 'Reporte de Verificación Estructural' : 'Reporte de Diseño Estructural'}
                </h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Universidad del Zulia - Facultad de Ingeniería - Escuela de Mecánica
                </p>
              </div>
            </div>
            <div className="text-right text-xs text-gray-600 dark:text-gray-400">
              <p>
                <strong>Fecha:</strong> {new Date().toLocaleDateString('es-VE')}
              </p>
              <p>
                <strong>Código:</strong> {form.designCode || 'ASME VIII / COVENIN'}
              </p>
            </div>
          </div>
        </div>

        {/* Screen Dynamic Title */}
        <div className="mb-4 print:hidden">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">
            {mode === 'analysis' ? 'Reporte de Verificación Estructural' : 'Reporte de Diseño Estructural'}
          </h1>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Resumen del análisis y verificación de soportes del recipiente a presión.
          </p>
        </div>

        <Alert
          variant={summaryAlert.variant}
          title={summaryAlert.title}
          message={summaryAlert.message}
        />

        <div className="mt-4 space-y-4">
          <ComponentCard title="Resumen — Información general">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 text-sm text-gray-700 dark:text-gray-300">
              <div>
                <div className="font-medium">Proyecto</div>
                <div>{form.projectName || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Fluido de trabajo</div>
                <div>{form.service || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Código</div>
                <div>{form.designCode || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Presión de diseño</div>
                <div>
                  {form.designPressure
                    ? `${form.designPressure} ${unitLabels.pressure[unitSystem]}`
                    : '-'}
                </div>
              </div>
              <div>
                <div className="font-medium">Temperatura de diseño</div>
                <div>
                  {form.designTemperature
                    ? `${form.designTemperature} ${unitLabels.temperature[unitSystem]}`
                    : '-'}
                </div>
              </div>
              <div>{/* internal diameter removed */}</div>
            </div>
          </ComponentCard>

          <ComponentCard title="Geometría y peso">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 text-sm text-gray-700 dark:text-gray-300">
              <div>
                <div className="font-medium">Diámetro exterior</div>
                <div>{form.outerDiameter || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Longitud / Altura</div>
                <div>{form.length || form.height || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Material</div>
                <div>{form.vesselMaterial || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Espesor de pared</div>
                <div>{form.wallThickness || '-'}</div>
              </div>
            </div>
          </ComponentCard>

          <ComponentCard title="Viento y Sísmico">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 text-sm text-gray-700 dark:text-gray-300">
              <div>
                <div className="font-medium">Viento</div>
                <div>
                  {form.windAuto
                    ? `${form.windAuto} (${form.windValue || '-'})`
                    : '-'}
                </div>
              </div>
              <div>
                <div className="font-medium">Sísmico</div>
                <div>
                  {form.designCode === 'COVENIN'
                    ? `${form.covenCity || '-'}, ${form.covenState || '-'} (${form.covenSoilType || '-'})`
                    : `Clase de sitio: ${form.seismicSiteClass || '-'} Ss: ${form.seismicSs || '-'} S1: ${form.seismicS1 || '-'}`}
                </div>
              </div>
            </div>
          </ComponentCard>

          <ComponentCard
            title={
              isSaddle
                ? 'Resultados en vivo — Silletas'
                : isSkirt
                  ? 'Resultados en vivo — Faldón'
                  : isLug
                    ? 'Resultados en vivo — Ménsulas'
                    : isRing
                      ? 'Resultados en vivo — Anillo'
                  : 'Resultados en vivo — Cargas y patas'
            }
          >
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 text-sm text-gray-700 dark:text-gray-300">
              <div>
                <div className="font-medium">Carga gobernante ambiental</div>
                <div>{String(derived.cargaGobernante_Ambiental || '-')}</div>
              </div>
              <div>
                <div className="font-medium">Momento gobernante ({momentUnit})</div>
                <div>{formatMomentFromkNm(derived.momentoGobernante_kNm)}</div>
              </div>
              <div>
                <div className="font-medium">Coeficiente sísmico Cs</div>
                <div>{formatDerived(derived.coeficienteSismico_Cs)}</div>
              </div>
              {isSaddle ? (
                <>
                  <div>
                    <div className="font-medium">Esfuerzo cuerno S4 ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.saddle_esfuerzoCuerno_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Flexión en silleta S1 ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.saddle_esfuerzoFlexionSilleta_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Flexión en centro S2 ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.saddle_esfuerzoFlexionCentro_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Compresión en silleta ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.saddle_esfuerzoCompresionSilleta_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta de cuerno</div>
                    <div className={derived.saddle_alertaCuerno ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.saddle_alertaCuerno ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta de flexión</div>
                    <div className={derived.saddle_alertaFlexion ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.saddle_alertaFlexion ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta de compresión silleta</div>
                    <div className={derived.saddle_alertaSilleta ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.saddle_alertaSilleta ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                </>
              ) : isSkirt ? (
                <>
                  <div>
                    <div className="font-medium">Compresión en faldón ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.skirt_esfuerzoCompresionFaldon_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Tensión en faldón ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.skirt_esfuerzoTensionFaldon_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Presión en concreto ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.skirt_presionConcreto_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Tracción por perno ({forceUnit})</div>
                    <div>{formatForceFromkN(derived.skirt_tensionMaxPerno_kN)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Esfuerzo placa silla ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.skirt_esfuerzoPlacaSilla_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta pandeo faldón</div>
                    <div className={derived.skirt_alertaPandeoFaldon ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.skirt_alertaPandeoFaldon ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta levantamiento</div>
                    <div className={derived.skirt_alertaLevantamientoFaldon ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.skirt_alertaLevantamientoFaldon ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta agujero acceso</div>
                    <div className={derived.skirt_alertaAgujeroAcceso ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.skirt_alertaAgujeroAcceso ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta silla de anclaje</div>
                    <div className={derived.skirt_alertaSillaAnclaje ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.skirt_alertaSillaAnclaje ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                </>
              ) : isLug ? (
                <>
                  <div>
                    <div className="font-medium">Carga por ménsula ({forceUnit})</div>
                    <div>{formatForceFromkN(derived.lug_cargaMaxPorMensula_kN)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Flexión en ménsula ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.lug_esfuerzoFlexionMensula_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Corte en ménsula ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.lug_esfuerzoCorteMensula_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Presión en Pad Plate ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.lug_presionPlacaApoyo_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta flexión ménsula</div>
                    <div className={derived.lug_alertaFlexionMensula ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.lug_alertaFlexionMensula ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta falta Pad Plate</div>
                    <div className={derived.lug_alertaFaltaPlaca ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.lug_alertaFaltaPlaca ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                </>
              ) : isRing ? (
                <>
                  <div>
                    <div className="font-medium">Área de sección ({areaUnit})</div>
                    <div>{formatAreaFromMm2(derived.ring_areaSeccion_mm2)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Módulo de sección ({sectionUnit})</div>
                    <div>{formatSectionFromMm3(derived.ring_moduloSeccion_mm3)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Flexión en anillo ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.ring_esfuerzoFlexionAnillo_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Corte en anillo ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.ring_esfuerzoCorteAnillo_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Presión placa base ({pressureUnit})</div>
                    <div>{formatStressFromMPa(derived.ring_presionPlacaBase_MPa)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta flexión anillo</div>
                    <div className={derived.ring_alertaFlexion ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.ring_alertaFlexion ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta presión base</div>
                    <div className={derived.ring_alertaPresionBase ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.ring_alertaPresionBase ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                </>
              ) : (
                <>
                  <div>
                    <div className="font-medium">Compresión máxima por pata ({forceUnit})</div>
                    <div>{formatForceFromkN(derived.leg_compresionMaxima_kN)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Tensión máxima por pata ({forceUnit})</div>
                    <div>{formatForceFromkN(derived.leg_tensionMaxima_kN)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Corte por pata ({forceUnit})</div>
                    <div>{formatForceFromkN(derived.leg_cortePorPata_kN)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta de levantamiento</div>
                    <div
                      className={
                        derived.leg_alertaLevantamiento
                          ? 'font-semibold text-red-600 dark:text-red-400'
                          : 'font-medium text-green-600 dark:text-green-400'
                      }
                    >
                      {derived.leg_alertaLevantamiento ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  {isLeg && (
                    <>
                      <div>
                        <div className="font-medium">Pata arriostrada</div>
                        <div>{blockValues.isBraced ? 'SÍ' : 'NO'}</div>
                      </div>
                      <div>
                        <div className="font-medium">Niveles de refuerzo</div>
                        <div>{formatDerived(blockValues.braceLevels)}</div>
                      </div>
                      <div>
                        <div className="font-medium">
                          Longitud efectiva de pandeo ({lengthUnit})
                        </div>
                        <div>{formatLengthFromMm(blockValues.leg_longitudEfectiva_mm)}</div>
                      </div>
                      <div>
                        <div className="font-medium">Esbeltez KL/r</div>
                        <div>{formatDerived(blockValues.leg_esbeltez)}</div>
                      </div>
                    </>
                  )}
                </>
              )}
              {hasAnchoring && (
                <>
                  <div className="md:col-span-2 mt-2 border-t border-gray-200 pt-3 dark:border-gray-700">
                    <div className="font-semibold text-gray-800 dark:text-gray-100">Anclaje (AISC + ACI)</div>
                  </div>
                  <div>
                    <div className="font-medium">Ratio interacción acero (T+V)</div>
                    <div>{formatDerived(derived.anchor_ratioInteraccionAcero)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Ratio breakout concreto</div>
                    <div>{formatDerived(derived.anchor_ratioConcreto)}</div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta acero</div>
                    <div className={derived.anchor_alertaAcero ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.anchor_alertaAcero ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta concreto</div>
                    <div className={derived.anchor_alertaConcreto ? 'font-semibold text-red-600 dark:text-red-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.anchor_alertaConcreto ? 'ACTIVA' : 'NO'}
                    </div>
                  </div>
                  <div>
                    <div className="font-medium">Alerta borde</div>
                    <div className={derived.anchor_alertaBorde ? 'font-semibold text-amber-600 dark:text-amber-400' : 'font-medium text-green-600 dark:text-green-400'}>
                      {derived.anchor_alertaBorde ? 'PENALIZA' : 'NO'}
                    </div>
                  </div>
                </>
              )}
            </div>
          </ComponentCard>

          <ComponentCard title="Configuración del soporte">
            <div className="text-sm text-gray-700 dark:text-gray-300">
              <div>
                <div className="font-medium">Tipo de soporte</div>
                <div>{form.supportType || '-'}</div>
              </div>
              {isSaddle && (
                <div className="mt-2">
                  <div className="font-medium">Silleta (resumen)</div>
                  <div>
                    Altura: {form.saddleHeight || '-'} — Ubicación:{' '}
                    {form.saddleLocation || '-'}
                  </div>
                </div>
              )}
              {isLeg && (
                <div className="mt-2">
                  <div className="font-medium">Patas (resumen)</div>
                  <div>
                    Perfil: {String(blockValues.leg_perfilUsado || '-')} —
                    Esbeltez KL/r: {formatDerived(blockValues.leg_esbeltez)}
                  </div>
                </div>
              )}
              {isSkirt && (
                <div className="mt-2">
                  <div className="font-medium">Faldón (resumen)</div>
                  <div>
                    Altura: {form.skirtHeight || '-'} — Espesor:{' '}
                    {form.skirtThickness || '-'}
                  </div>
                  <div>
                    Anillo base ID/OD: {form.skirtRingID || '-'} /{' '}
                    {form.skirtRingOD || '-'}
                  </div>
                </div>
              )}
              {isLug && (
                <div className="mt-2">
                  <div className="font-medium">Ménsulas (resumen)</div>
                  <div>
                    Cantidad: {form.lugQuantity || '-'} — Espesor: {form.lugThickness || '-'}
                  </div>
                  <div>
                    Gusset: {String(form.lugGusset) === 'true' ? 'Sí' : 'No'} — Pad Plate: {String(form.lugPadPlate) === 'true' ? 'Sí' : 'No'}
                  </div>
                </div>
              )}
              {isRing && (
                <div className="mt-2">
                  <div className="font-medium">Anillo (resumen)</div>
                  <div>
                    Perfil: {form.ringProfile || '-'} — Alma: {form.ringWebHeight || '-'} x {form.ringWebThickness || '-'}
                  </div>
                  <div>
                    Brida: {form.ringFlangeWidth || '-'} x {form.ringFlangeThickness || '-'} — Placa base: {form.ringBasePlateWidth || '-'} x {form.ringBasePlateLength || '-'}
                  </div>
                </div>
              )}
              {hasAnchoring && (
                <div className="mt-2">
                  <div className="font-medium">Anclaje (resumen)</div>
                  <div>
                    Pernos: {form.boltQuantity || form.anchorBoltQuantity || form.skirtAnchorBoltCount || '-'} — Ø {form.boltDiameter || form.anchorBoltDiameter || form.legBoltDiameter || form.skirtAnchorBoltDiameter || '-'}
                  </div>
                  <div>
                    Material: {form.boltMaterial || 'Acero al carbono'} — hef: {form.embedmentDepth || '-'} — f'c: {form.concreteStrength || '-'} — borde: {form.anchorEdgeDistance || '-'}
                  </div>
                </div>
              )}
            </div>
          </ComponentCard>

          <ComponentCard title={mode === 'analysis' ? "RESULTADOS DE VERIFICACIÓN" : "RESULTADOS DE DISEÑO RECOMENDADOS"}>
            <div className="space-y-6 text-sm text-gray-700 dark:text-gray-300">
              {mode !== 'analysis' && (
                <div>
                  <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                    Tabla 1: Dimensiones recomendadas (Salida de diseño)
                  </div>
                  <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
                    <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                      <thead className="bg-gray-50 dark:bg-gray-800/60">
                        <tr>
                          <th className="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-300">
                            Parámetro
                          </th>
                          <th className="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-300">
                            Resultado recomendado
                          </th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-transparent">
                        {recommendedDimensionsRows.map((row) => (
                          <tr key={row.parameter}>
                            <td className="px-3 py-2 font-medium">{row.parameter}</td>
                            <td className="px-3 py-2">{row.value}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              <div>
                <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                  {mode === 'analysis' 
                    ? 'Tabla de Verificación de cálculo (Análisis estructural)' 
                    : 'Tabla 2: Verificación de cálculo (Prueba de diseño)'}
                </div>
                <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
                  <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead className="bg-gray-50 dark:bg-gray-800/60">
                      <tr>
                        <th className="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-300">
                          Verificación
                        </th>
                        <th className="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-300">
                          Carga real
                        </th>
                        <th className="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-300">
                          Carga permisible
                        </th>
                        <th className="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-300">
                          Estado
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 bg-white dark:divide-gray-700 dark:bg-transparent">
                      {calculationVerificationRows.map((row) => (
                        <tr key={row.check}>
                          <td className="px-3 py-2 font-medium">{row.check}</td>
                          <td className="px-3 py-2">{row.actual}</td>
                          <td className="px-3 py-2">{row.allowable}</td>
                          <td className={`px-3 py-2 ${getStatusClassName(row.status)}`}>
                            {row.status}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {!!final.notes.length && (
                <div>
                  <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                    Observaciones automáticas
                  </div>
                  <ul className="list-disc space-y-1 pl-5">
                    {displayedNotes.map((note, idx) => (
                      <li key={`${idx}-${note}`}>{note}</li>
                    ))}
                  </ul>
                  {hiddenNotesCount > 0 && (
                    <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                      +{hiddenNotesCount} observación(es) adicional(es) omitida(s) para resumir el reporte.
                    </div>
                  )}
                </div>
              )}
            </div>
          </ComponentCard>
        </div>
      </div>
    </div>
  );
}
