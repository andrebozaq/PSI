import { useEffect, useMemo, useRef, useState } from 'react';
import { TbTransfer, TbX } from 'react-icons/tb';

// Unit definitions by category. Non-temperature units are normalized to an SI-style base unit.
const unitCategories = {
  length: {
    label: 'Longitud',
    units: {
      m: 1,
      cm: 0.01,
      mm: 0.001,
      km: 1000,
      in: 0.0254,
      ft: 0.3048,
      yd: 0.9144,
      mi: 1609.344,
    },
  },
  time: {
    label: 'Tiempo',
    units: {
      s: 1,
      min: 60,
      hr: 3600,
      day: 86400,
    },
  },
  temperature: {
    label: 'Temperatura',
    units: {
      C: 1,
      F: 1,
      K: 1,
    },
  },
  speed: {
    label: 'Velocidad',
    units: {
      'm/s': 1,
      'km/h': 1 / 3.6,
      mph: 0.44704,
      knot: 0.514444,
    },
  },
  force: {
    label: 'Fuerza',
    units: {
      N: 1,
      kN: 1000,
      lbf: 4.4482216,
      kgf: 9.80665,
    },
  },
  weight: {
    label: 'Peso',
    units: {
      kg: 1,
      g: 0.001,
      lb: 0.45359237,
      ton: 1000,
    },
  },
  energy: {
    label: 'Energía',
    units: {
      J: 1,
      kJ: 1000,
      MJ: 1_000_000,
      Wh: 3600,
      kWh: 3_600_000,
      BTU: 1055.05585,
    },
  },
  pressure: {
    label: 'Presión',
    units: {
      Pa: 1,
      kPa: 1000,
      MPa: 1_000_000,
      bar: 100_000,
      psi: 6894.75729,
    },
  },
  moment: {
    label: 'Momento',
    units: {
      'N·m': 1,
      'kN·m': 1000,
      'ft·lbf': 1.35581795,
      'in·lbf': 0.112984829,
      'kgf·m': 9.80665,
    },
  },
} as const;

type CategoryKey = keyof typeof unitCategories;

type TemperatureUnit = 'C' | 'F' | 'K';

type ConverterState = {
  category: CategoryKey;
  fromUnit: string;
  toUnit: string;
  input: string;
  output: string;
};

const temperatureConvert = (
  value: number,
  from: TemperatureUnit,
  to: TemperatureUnit,
) => {
  if (Number.isNaN(value)) return NaN;
  let inC = value;
  if (from === 'F') inC = (value - 32) * (5 / 9);
  if (from === 'K') inC = value - 273.15;

  if (to === 'C') return inC;
  if (to === 'F') return inC * (9 / 5) + 32;
  return inC + 273.15;
};

const convertValue = (state: ConverterState) => {
  const raw = parseFloat(state.input);
  if (Number.isNaN(raw)) return '';

  if (state.category === 'temperature') {
    const result = temperatureConvert(
      raw,
      state.fromUnit as TemperatureUnit,
      state.toUnit as TemperatureUnit,
    );
    return Number.isNaN(result) ? '' : result.toString();
  }

  const { units } = unitCategories[state.category];
  const fromFactor = units[state.fromUnit as keyof typeof units];
  const toFactor = units[state.toUnit as keyof typeof units];
  if (!fromFactor || !toFactor) return '';

  const base = raw * fromFactor;
  const converted = base / toFactor;
  return Number.isFinite(converted) ? converted.toString() : '';
};

const getDefaultUnits = (category: CategoryKey) => {
  const unitKeys = Object.keys(unitCategories[category].units);
  return {
    from: unitKeys[0],
    to: unitKeys[1] ?? unitKeys[0],
  };
};

const ConverterFab: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [keyboardOffset, setKeyboardOffset] = useState(0);
  const [state, setState] = useState<ConverterState>(() => {
    const { from, to } = getDefaultUnits('pressure');
    return {
      category: 'pressure',
      fromUnit: from,
      toUnit: to,
      input: '',
      output: '',
    };
  });

  const cardRef = useRef<HTMLDivElement | null>(null);

  const unitOptions = useMemo(() => {
    const { units } = unitCategories[state.category];
    return Object.keys(units);
  }, [state.category]);

  useEffect(() => {
    setState((prev) => {
      const nextUnits = getDefaultUnits(prev.category);
      return {
        ...prev,
        fromUnit: nextUnits.from,
        toUnit: nextUnits.to,
      };
    });
  }, [state.category]);

  useEffect(() => {
    setState((prev) => ({ ...prev, output: convertValue(prev) }));
  }, [state.category, state.fromUnit, state.toUnit, state.input]);

  useEffect(() => {
    const handleClickAway = (e: MouseEvent) => {
      if (!cardRef.current) return;
      if (!cardRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    if (open) document.addEventListener('mousedown', handleClickAway);
    return () => document.removeEventListener('mousedown', handleClickAway);
  }, [open]);

  const handleSwap = () => {
    setState((prev) => ({
      ...prev,
      fromUnit: prev.toUnit,
      toUnit: prev.fromUnit,
    }));
  };

  const handleChange = (key: keyof ConverterState, value: string) => {
    setState((prev) => ({ ...prev, [key]: value }));
  };

  // Track virtual keyboard height on mobile to lift the widget above it.
  useEffect(() => {
    const vv = window.visualViewport;
    if (!vv) return;
    const handle = () => {
      // Keyboard height approximated by lost viewport height minus offsetTop (for iOS safe areas)
      const keyboardHeight = Math.max(
        0,
        window.innerHeight - (vv.height + vv.offsetTop),
      );
      // Keep at least the base 24px bottom space; lift just above keyboard when it appears
      const offset = keyboardHeight > 40 ? keyboardHeight + 12 : 0;
      setKeyboardOffset(offset);
    };
    vv.addEventListener('resize', handle);
    vv.addEventListener('scroll', handle);
    handle();
    return () => {
      vv.removeEventListener('resize', handle);
      vv.removeEventListener('scroll', handle);
    };
  }, []);

  const fieldSelectClasses =
    'mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-[16px] text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100 sm:text-sm';
  const fieldInputClasses =
    'mt-1 w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-[16px] text-gray-800 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100 sm:text-sm';
  const fieldOutputClasses =
    'mt-1 w-full rounded-lg border border-gray-200 bg-gray-50 px-3 py-2 text-[16px] text-gray-800 dark:border-gray-700 dark:bg-gray-800/80 dark:text-gray-100 sm:text-sm';

  return (
    <div
      className="fixed right-6 z-[9999] flex flex-col items-end gap-3 print:hidden"
      style={{ bottom: `calc(1.5rem + ${keyboardOffset}px)` }}
    >
      {open && (
        <div
          ref={cardRef}
          className="w-[320px] rounded-xl border border-gray-200 bg-white shadow-2xl dark:border-gray-800 dark:bg-gray-900"
        >
          <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-800">
            <div className="text-sm font-semibold text-gray-800 dark:text-gray-100">
              Conversor de Unidades
            </div>
            <button
              type="button"
              onClick={() => setOpen(false)}
              className="rounded-md p-1 text-gray-500 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-white/5"
              aria-label="Close converter"
            >
              <TbX className="h-5 w-5" />
            </button>
          </div>

          <div className="space-y-3 px-4 py-4">
            <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400">
              Categoría
              <select
                value={state.category}
                onChange={(e) => handleChange('category', e.target.value)}
                className={fieldSelectClasses}
              >
                {Object.entries(unitCategories).map(([key, value]) => (
                  <option key={key} value={key}>
                    {value.label}
                  </option>
                ))}
              </select>
            </label>

            <div className="grid grid-cols-[1fr_auto_1fr] items-end gap-2">
              <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400">
                De
                <select
                  value={state.fromUnit}
                  onChange={(e) => handleChange('fromUnit', e.target.value)}
                  className={fieldSelectClasses}
                >
                  {unitOptions.map((u) => (
                    <option key={u} value={u}>
                      {u}
                    </option>
                  ))}
                </select>
              </label>

              <div className="pb-1">
                <button
                  type="button"
                  onClick={handleSwap}
                  className="mt-6 inline-flex h-10 w-10 items-center justify-center rounded-full border border-gray-200 bg-white text-slate-800 shadow-sm hover:bg-slate-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100 dark:hover:bg-gray-700"
                  aria-label="Swap units"
                >
                  <TbTransfer className="h-5 w-5" />
                </button>
              </div>

              <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400">
                A
                <select
                  value={state.toUnit}
                  onChange={(e) => handleChange('toUnit', e.target.value)}
                  className={fieldSelectClasses}
                >
                  {unitOptions.map((u) => (
                    <option key={u} value={u}>
                      {u}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <div className="grid grid-cols-[1fr_auto_1fr] items-end gap-2">
              <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400">
                Entrada
                <input
                  type="number"
                  value={state.input}
                  onChange={(e) => handleChange('input', e.target.value)}
                  className={fieldInputClasses}
                  placeholder="Ingrese valor"
                />
              </label>

              <div className="flex items-center justify-center pb-1 text-gray-400 dark:text-gray-500">
                <TbTransfer className="h-5 w-5" />
              </div>

              <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400">
                Salida
                <input
                  readOnly
                  value={state.output}
                  className={fieldOutputClasses}
                  placeholder="Resultado"
                />
              </label>
            </div>
          </div>
        </div>
      )}

      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="flex h-14 w-14 items-center justify-center rounded-full bg-[#0b1f3a] text-white shadow-xl transition hover:bg-[#1a46c2] focus:outline-hidden focus:ring-4 focus:ring-[#1d4ed8]/40 dark:bg-[#1d4ed8] dark:hover:bg-[#1a46c2]"
        aria-label="Alternar conversor de unidades"
      >
        <TbTransfer className="h-6 w-6" />
      </button>
    </div>
  );
};

export default ConverterFab;
