import React, { useRef } from 'react';
import ComponentCard from '../../../components/common/ComponentCard';
import Alert from '../../../components/ui/alert/Alert';

type Props = {
  form: any;
  unitSystem: 'SI' | 'US';
};

const unitLabels = {
  pressure: { SI: 'MPa', US: 'psi' },
  temperature: { SI: '°C', US: '°F' },
  length: { SI: 'mm', US: 'in' },
};

export default function SummaryReport({ form, unitSystem }: Props) {
  const printRef = useRef<HTMLDivElement | null>(null);

  const handlePrint = () => {
    const el = printRef.current;
    if (!el) return window.print();
    const printWindow = window.open('', '_blank', 'width=900,height=700');
    if (!printWindow) return window.print();

    const links = Array.from(
      document.querySelectorAll('link[rel="stylesheet"], style'),
    )
      .map((l) => l.outerHTML)
      .join('\n');

    const html = `<!doctype html><html><head><meta charset="utf-8"><title>Resumen</title>${links}<style>@media print{.no-print{display:none!important}.page-break{page-break-after:always}}</style></head><body>${el.innerHTML}</body></html>`;
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
      <div className="flex justify-end no-print">
        <button
          type="button"
          onClick={handlePrint}
          className="rounded-md bg-brand-500 px-3 py-2 text-sm font-semibold text-white"
        >
          Imprimir / Exportar
        </button>
      </div>

      <div ref={printRef} id="summary-print-area">
        <Alert
          variant="success"
          title="Design check"
          message="Your design passed successfully."
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

          <ComponentCard title="Geometry & Weight">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 text-sm text-gray-700 dark:text-gray-300">
              <div>
                <div className="font-medium">Outer Diameter</div>
                <div>{form.outerDiameter || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Length / Height</div>
                <div>{form.length || form.height || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Material</div>
                <div>{form.vesselMaterial || '-'}</div>
              </div>
              <div>
                <div className="font-medium">Wall thickness</div>
                <div>{form.wallThickness || '-'}</div>
              </div>
            </div>
          </ComponentCard>

          <ComponentCard title="Wind & Seismic">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 text-sm text-gray-700 dark:text-gray-300">
              <div>
                <div className="font-medium">Wind</div>
                <div>
                  {form.windAuto
                    ? `${form.windAuto} (${form.windValue || '-'})`
                    : '-'}
                </div>
              </div>
              <div>
                <div className="font-medium">Seismic</div>
                <div>
                  {form.designCode === 'COVENIN'
                    ? `${form.covenCity || '-'}, ${form.covenState || '-'} (${form.covenSoilType || '-'})`
                    : `Site class: ${form.seismicSiteClass || '-'} Ss: ${form.seismicSs || '-'} S1: ${form.seismicS1 || '-'}`}
                </div>
              </div>
            </div>
          </ComponentCard>

          <ComponentCard title="Support configuration">
            <div className="text-sm text-gray-700 dark:text-gray-300">
              <div>
                <div className="font-medium">Support type</div>
                <div>{form.supportType || '-'}</div>
              </div>
              <div className="mt-2">
                <div className="font-medium">Saddle (summary)</div>
                <div>
                  Height: {form.saddleHeight || '-'} — Location:{' '}
                  {form.saddleLocation || '-'}
                </div>
              </div>
            </div>
          </ComponentCard>
        </div>
      </div>
    </div>
  );
}
