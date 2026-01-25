import React, { useRef, useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import Alert from '../../../components/ui/alert/Alert';

const Legs: React.FC<{
  form: any;
  onFieldChange: (k: string, v: any) => void;
}> = ({ form, onFieldChange }) => {
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
  }, [isHorizontalLeg, form?.legQuantity]);

  return (
    <div className="space-y-2">
      <label className="text-sm text-gray-600 dark:text-gray-300">
        Leg quantity
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
        Leg profile
        {(() => {
          const isBraced = !!(
            form &&
            form.supportType &&
            /arriostrada/i.test(form.supportType)
          );
          const options = isBraced
            ? [
                'Angle (L)',
                'Beam (W/I)',
                'Pipe (Sch 40/80)',
                'Square Tube (HSS)',
              ]
            : ['Rectangular', 'Angle', 'Tube'];
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
      {form && form.supportType && /arriostrada/i.test(form.supportType) && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Brace profile (e.g., L2x2x1/4)
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
        Leg length
        <input
          type="number"
          value={form.legLength || ''}
          onChange={(e) => onFieldChange('legLength', e.target.value)}
          className="mt-1 w-full rounded-lg border border-gray-200 bg-transparent px-3 py-2 text-sm dark:border-gray-700 dark:text-gray-100"
        />
      </label>

      {form && form.supportType && /arriostrada/i.test(form.supportType) && (
        <label className="text-sm text-gray-600 dark:text-gray-300">
          Bracing tier
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
            Base plate width
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
            Base plate length
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
            <label className="text-sm text-gray-600 dark:text-gray-300">
              Longitudinal spacing
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
              Transverse spacing
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
              <span>Bolt circle (Dbc)</span>
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
                    title="Bolt circle smaller than sphere diameter"
                    message="Bolt circle (Dbc) is smaller than the sphere diameter. For spherical vessels the bolt circle is typically larger; under-slung legs are unstable and not recommended."
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
                    For spherical vessels the bolt circle is typically larger
                    than the sphere diameter — under-slung arrangements are
                    unstable.
                  </div>
                </div>,
                document.body,
              )}
          </>
        )}
      </div>
    </div>
  );
};

export default Legs;
