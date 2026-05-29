import React, { useRef, useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import Alert from '../../../components/ui/alert/Alert';

const Legs: React.FC<{
  form: Record<string, string>;
  onFieldChange: (k: string, v: string) => void;
  unitSystem?: 'SI' | 'US';
  mode?: 'design' | 'analysis';
}> = ({ form, onFieldChange, unitSystem = 'SI', mode = 'analysis' }) => {
  void mode;
  const lengthUnit = unitSystem === 'SI' ? 'mm' : 'in';
  const boltRef = useRef<HTMLInputElement | null>(null);
  const [alertPos, setAlertPos] = useState<{
    left: number;
    top: number;
  } | null>(null);
  const [shouldShowAlert, setShouldShowAlert] = useState(false);
  const tipRef = useRef<HTMLSpanElement | null>(null);
  const [tipVisible, setTipVisible] = useState(false);
  const [tipPos, setTipPos] = useState<{ left: number; top: number } | null>(
    null,
  );

  const isLeg = !!(form && form.supportType && /Leg/i.test(form.supportType));
  const isHorizontalLeg = !!(isLeg && form && form.vesselType === 'Horizontal');
  const isBracedLeg = !!(
    form &&
    form.supportType &&
    /arriostrada/i.test(form.supportType)
  );
  const isSphere = form && form.vesselType === 'Esférico';
  const isVertical = form && form.vesselType === 'Columna vertical';
  const legProfile = form?.legProfile || '';
  const isAngleProfile = /Angle|Ángulo|\(L\)/i.test(legProfile);
  const isBeamProfile = /Beam|W\/I|Viga/i.test(legProfile);
  const isHssProfile = /HSS|cuadrado/i.test(legProfile);
  const isPipeProfile = /Pipe|Tube|Tubo|Sch 40\/80/i.test(legProfile) && !isHssProfile;

  useEffect(() => {
    const update = () => {
      const boltCircle = Number(form?.legBoltCircle);
      const sphereDia = Number(form?.outerDiameter);
      const isUnderSlung = !!form?.underSlung;
      const show =
        form &&
        form.vesselType === 'Esférico' &&
        Number.isFinite(boltCircle) &&
        Number.isFinite(sphereDia) &&
        boltCircle < sphereDia &&
        !isUnderSlung;
      setShouldShowAlert(!!show);
      if (show && boltRef.current) {
        const r = boltRef.current.getBoundingClientRect();
        setAlertPos({
          left: r.left + r.width / 2 + window.scrollX,
          top: r.bottom + 8 + window.scrollY,
        });
      } else {
        setAlertPos(null);
      }
    };

    update();
    window.addEventListener('resize', update);
    window.addEventListener('scroll', update, true);
    return () => {
      window.removeEventListener('resize', update);
      window.removeEventListener('scroll', update, true);
    };
  }, [
    form,
    form?.legBoltCircle,
    form?.outerDiameter,
    form?.vesselType,
    form?.underSlung,
  ]);

  useEffect(() => {
    if (!tipVisible || !tipRef.current) return;
    const r = tipRef.current.getBoundingClientRect();
    setTipPos({
      left: r.left + r.width / 2 + window.scrollX,
      top: r.top + window.scrollY,
    });
    const onScroll = () => {
      if (!tipRef.current) return;
      const rr = tipRef.current.getBoundingClientRect();
      setTipPos({
        left: rr.left + rr.width / 2 + window.scrollX,
        top: rr.top + window.scrollY,
      });
    };
    window.addEventListener('scroll', onScroll, true);
    window.addEventListener('resize', onScroll);
    return () => {
      window.removeEventListener('scroll', onScroll, true);
      window.removeEventListener('resize', onScroll);
    };
  }, [tipVisible]);

  // Force legQuantity to 4 and make it unchangeable for horizontal legs
  useEffect(() => {
    if (isHorizontalLeg && form.legQuantity !== '4') {
      onFieldChange('legQuantity', '4');
    }
  }, [isHorizontalLeg, form?.legQuantity, onFieldChange]);

  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Cantidad de patas
        <select
          value={isHorizontalLeg ? '4' : form.legQuantity || '2'}
          onChange={(e) => onFieldChange('legQuantity', e.target.value)}
          disabled={isHorizontalLeg}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
        >
          <option>3</option>
          <option>4</option>
          <option>6</option>
          <option>8</option>
        </select>
      </label>

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Perfil de la pata
        {(() => {
          const options = [
            'Ángulo (L)',
            'Viga (W/I)',
            'Tubo (Sch 40/80)',
            'Tubo cuadrado (HSS)',
          ];
          return (
            <select
              value={form.legProfile || options[0]}
              onChange={(e) => onFieldChange('legProfile', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
            >
              {options.map((opt) => (
                <option key={opt}>{opt}</option>
              ))}
            </select>
          );
        })()}
      </label>

      {/* Profile dimensions */}
      {isAngleProfile && (
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Ancho del ala (b) ({lengthUnit})
            <input
              type="number"
              min="0"
              step="any"
              value={form.legAngleWidth || ''}
              onChange={(e) => onFieldChange('legAngleWidth', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Espesor (t) ({lengthUnit})
            <input
              type="number"
              min="0"
              value={form.legAngleThickness || ''}
              onChange={(e) =>
                onFieldChange('legAngleThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </div>
      )}

      {isPipeProfile && (
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Diámetro exterior del tubo/pipa ({lengthUnit})
            <input
              type="number"
              min="0"
              value={form.legPipeOD || ''}
              onChange={(e) => onFieldChange('legPipeOD', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Espesor de la pared ({lengthUnit})
            <input
              type="number"
              min="0"
              value={form.legPipeThickness || ''}
              onChange={(e) =>
                onFieldChange('legPipeThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </div>
      )}

      {isHssProfile && (
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Ancho (b) ({lengthUnit})
            <input
              type="number"
              min="0"
              step="any"
              value={form.legHssWidth || ''}
              onChange={(e) => onFieldChange('legHssWidth', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Profundidad (h) ({lengthUnit})
            <input
              type="number"
              min="0"
              step="any"
              value={form.legHssDepth || ''}
              onChange={(e) => onFieldChange('legHssDepth', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Espesor de pared (t) ({lengthUnit})
            <input
              type="number"
              min="0"
              step="any"
              value={form.legHssWallThickness || ''}
              onChange={(e) =>
                onFieldChange('legHssWallThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </div>
      )}

      {isBeamProfile && (
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Profundidad de la viga (h) ({lengthUnit})
            <input
              type="number"
              min="0"
              value={form.legBeamDepth || ''}
              onChange={(e) => onFieldChange('legBeamDepth', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Ancho de brida (bf) ({lengthUnit})
            <input
              type="number"
              min="0"
              value={form.legBeamFlangeWidth || ''}
              onChange={(e) =>
                onFieldChange('legBeamFlangeWidth', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Espesor del alma (tw) ({lengthUnit})
            <input
              type="number"
              min="0"
              step="any"
              value={form.legBeamWebThickness || ''}
              onChange={(e) =>
                onFieldChange('legBeamWebThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Espesor de la brida (tf) ({lengthUnit})
            <input
              type="number"
              min="0"
              step="any"
              value={form.legBeamFlangeThickness || ''}
              onChange={(e) =>
                onFieldChange('legBeamFlangeThickness', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </div>
      )}
      {form && form.supportType && /arriostrada/i.test(form.supportType) && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Perfil del refuerzo (e.g., L2x2x1/4)
          <input
            type="text"
            value={form.braceProfile || ''}
            onChange={(e) => onFieldChange('braceProfile', e.target.value)}
            placeholder="e.g., L2x2x1/4"
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      )}

      <label className="text-sm text-gray-600 dark:text-gray-300">
        Longitud de la pata ({lengthUnit})
        <input
          type="number"
          value={form.legLength || ''}
          onChange={(e) => onFieldChange('legLength', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      {isBracedLeg && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Altura del refuerzo ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.bracingHeight || ''}
            onChange={(e) => onFieldChange('bracingHeight', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      )}

      {form && form.supportType && /arriostrada/i.test(form.supportType) && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Nivel de refuerzo
          <select
            value={form.bracingTier || '1'}
            onChange={(e) => onFieldChange('bracingTier', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
          >
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
          </select>
        </label>
      )}

      {isLeg && (isSphere || isVertical) && (
        <>
          <label className="text-sm text-gray-600 dark:text-gray-300">
            Ancho de la placa base ({lengthUnit})
            <input
              type="number"
              step="any"
              value={form.legBasePlateWidth || ''}
              onChange={(e) =>
                onFieldChange('legBasePlateWidth', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>

          <label className="text-sm text-gray-600 dark:text-gray-300">
            Longitud de la placa base ({lengthUnit})
            <input
              type="number"
              step="any"
              value={form.legBasePlateLength || ''}
              onChange={(e) =>
                onFieldChange('legBasePlateLength', e.target.value)
              }
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />
          </label>
        </>
      )}

      <div>
        {isHorizontalLeg ? (
          <>
            <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
              <label className="text-sm text-gray-600 dark:text-gray-300">
                Ancho de la placa base (mm)
                <input
                  type="number"
                  step="any"
                  min="0"
                  value={form.legBasePlateWidth || ''}
                  onChange={(e) =>
                    onFieldChange('legBasePlateWidth', e.target.value)
                  }
                  className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
                />
              </label>

              <label className="text-sm text-gray-600 dark:text-gray-300">
                Largo de la placa base (mm)
                <input
                  type="number"
                  step="any"
                  min="0"
                  value={form.legBasePlateLength || ''}
                  onChange={(e) =>
                    onFieldChange('legBasePlateLength', e.target.value)
                  }
                  className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
                />
              </label>
            </div>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              Espaciado longitudinal ({lengthUnit})
              <input
                type="number"
                step="any"
                value={form.legLongSpacing || ''}
                onChange={(e) =>
                  onFieldChange('legLongSpacing', e.target.value)
                }
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
              />
            </label>

            <label className="text-sm text-gray-600 dark:text-gray-300">
              Espaciado transversal ({lengthUnit})
              <input
                type="number"
                step="any"
                value={form.legTransSpacing || ''}
                onChange={(e) =>
                  onFieldChange('legTransSpacing', e.target.value)
                }
                className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
              />
            </label>
          </>
        ) : (
          <>
            <label className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-300">
              <span>Círculo de pernos (Dbc) ({lengthUnit})</span>
              <span
                ref={tipRef}
                onMouseEnter={() => setTipVisible(true)}
                onMouseLeave={() => setTipVisible(false)}
                className="relative inline-block"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4 text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 16h-1v-4h-1m1-4h.01M12 20a8 8 0 100-16 8 8 0 000 16z"
                  />
                </svg>
                {/* tooltip moved to portal to avoid being clipped by card */}
              </span>
            </label>

            <input
              ref={boltRef}
              type="number"
              value={form.legBoltCircle || ''}
              onChange={(e) => onFieldChange('legBoltCircle', e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
            />

            {shouldShowAlert &&
              alertPos &&
              createPortal(
                <div
                  style={{
                    position: 'absolute',
                    left: alertPos.left,
                    top: alertPos.top,
                    transform: 'translate(-50%, 0)',
                    zIndex: 9999,
                    width: 360,
                    maxWidth: '80vw',
                  }}
                >
                  <Alert
                    variant="warning"
                    title="Círculo de pernos más pequeño que el diámetro de la esfera"
                    message="El círculo de pernos (Dbc) es más pequeño que el diámetro de la esfera. Para recipientes esféricos, el círculo de pernos suele ser más grande; las patas colgantes son inestables y no se recomiendan."
                  />
                </div>,
                document.body,
              )}
            {tipVisible &&
              tipPos &&
              createPortal(
                <div
                  style={{
                    position: 'absolute',
                    left: tipPos.left,
                    top: tipPos.top,
                    transform: 'translate(-50%, -100%)',
                    zIndex: 9999,
                    whiteSpace: 'nowrap',
                  }}
                >
                  <div className="rounded-lg bg-white px-3 py-2 text-xs text-gray-700 shadow-sm dark:bg-[#1E2634] dark:text-white">
                    Para recipientes esféricos, el círculo de pernos suele ser más grande
                    que el diámetro de la esfera — las disposiciones colgantes son
                    inestables.
                  </div>
                </div>,
                document.body,
              )}
          </>
        )}
      </div>

      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Diámetro del perno ({lengthUnit})
          <input
            type="number"
            min="0"
            value={form.legBoltDiameter || ''}
            onChange={(e) => onFieldChange('legBoltDiameter', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Pernos por pata
          <input
            type="number"
            min="0"
            value={form.legBoltPerLeg || ''}
            onChange={(e) => onFieldChange('legBoltPerLeg', e.target.value)}
            className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
          />
        </label>
      </div>
    </div>
  );
};

export default Legs;
