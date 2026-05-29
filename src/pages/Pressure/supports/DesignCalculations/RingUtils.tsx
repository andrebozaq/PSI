import { toPositive } from './PhysicsUtils';

export type RingDesignInputs = {
	pesoOperativo_kN: number;
	vesselDiameter_mm: number;
	ringProfile: string;
	ringWebHeight_mm: number;
	ringWebThickness_mm: number;
	ringFlangeWidth_mm: number;
	ringFlangeThickness_mm: number;
	ringBasePlateWidth_mm: number;
	ringBasePlateLength_mm: number;
	ringGussets: boolean;
	ringGussetQty: number;
	ringGussetThickness_mm: number;
	ringGussetWidth_mm: number;
};

export type RingReactions = {
	areaSeccion_mm2: number;
	moduloSeccion_mm3: number;
	esfuerzoFlexionAnillo_MPa: number;
	esfuerzoCorteAnillo_MPa: number;
	presionPlacaBase_MPa: number;
	alertaFlexion: boolean;
	alertaPresionBase: boolean;
};

const calculateRingProperties = (inputs: RingDesignInputs) => {
	const h = toPositive(inputs.ringWebHeight_mm, 1);
	const tw = toPositive(inputs.ringWebThickness_mm, 1);
	const bf = toPositive(inputs.ringFlangeWidth_mm, 0);
	const tf = toPositive(inputs.ringFlangeThickness_mm, 0);

	let Area = 0;
	let Z = 0;

	switch (inputs.ringProfile) {
		case 'Viga I': {
			Area = 2 * bf * tf + (h - 2 * tf) * tw;
			const I_viga =
				(bf * Math.pow(h, 3) - (bf - tw) * Math.pow(h - 2 * tf, 3)) / 12;
			Z = I_viga / (h / 2);
			break;
		}
		case 'Sección T': {
			Area = bf * tf + h * tw;
			const y_bar = (bf * tf * (h + tf / 2) + h * tw * (h / 2)) / Area;
			const I_alma =
				tw * Math.pow(h, 3) / 12 + h * tw * Math.pow(y_bar - h / 2, 2);
			const I_brida =
				bf * Math.pow(tf, 3) / 12 +
				bf * tf * Math.pow(h + tf / 2 - y_bar, 2);
			const I_T = I_alma + I_brida;
			const c_max = Math.max(y_bar, h + tf - y_bar);
			Z = I_T / c_max;
			break;
		}
		case 'Barra':
		default:
			Area = h * tw;
			Z = (tw * Math.pow(h, 2)) / 6;
			break;
	}

	return { Area, Z };
};

export const calculateRingReactions = (inputs: RingDesignInputs): RingReactions => {
	const W_N = toPositive(inputs.pesoOperativo_kN, 0) * 1000;
	const D = toPositive(inputs.vesselDiameter_mm, 0);

	if (W_N === 0 || D === 0) {
		return {
			areaSeccion_mm2: 0,
			moduloSeccion_mm3: 0,
			esfuerzoFlexionAnillo_MPa: 0,
			esfuerzoCorteAnillo_MPa: 0,
			presionPlacaBase_MPa: 0,
			alertaFlexion: false,
			alertaPresionBase: false,
		};
	}

	const { Area, Z } = calculateRingProperties(inputs);
	const numApoyos = inputs.ringGussets
		? Math.max(toPositive(inputs.ringGussetQty, 4), 2)
		: 4;
	const cargaPorApoyo_N = W_N / numApoyos;
	const excentricidad_e = toPositive(inputs.ringWebHeight_mm, 1) / 2;
	const Momento_Nmm = cargaPorApoyo_N * excentricidad_e;
	const esfuerzoFlexionAnillo = Z > 0 ? Momento_Nmm / Z : 0;
	const esfuerzoCorteAnillo = Area > 0 ? cargaPorApoyo_N / Area : 0;

	const pad_W = toPositive(inputs.ringBasePlateWidth_mm, 1);
	const pad_L = toPositive(inputs.ringBasePlateLength_mm, 1);
	const areaPlacaBase = pad_W * pad_L;
	const presionPlacaBase = areaPlacaBase > 0 ? cargaPorApoyo_N / areaPlacaBase : 0;

	const alertaFlexion = esfuerzoFlexionAnillo > 150;
	const alertaPresionBase = presionPlacaBase > 15;

	const result = {
		areaSeccion_mm2: Number(Area.toFixed(2)),
		moduloSeccion_mm3: Number(Z.toFixed(2)),
		esfuerzoFlexionAnillo_MPa: Number(esfuerzoFlexionAnillo.toFixed(2)),
		esfuerzoCorteAnillo_MPa: Number(esfuerzoCorteAnillo.toFixed(2)),
		presionPlacaBase_MPa: Number(presionPlacaBase.toFixed(2)),
		alertaFlexion,
		alertaPresionBase,
	};

	console.log('[RingUtils][calculateRingReactions]', result);
	return result;
};
