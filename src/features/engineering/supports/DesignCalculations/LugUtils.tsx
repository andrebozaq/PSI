import { toPositive } from './PhysicsUtils';

export type LugDesignInputs = {
	pesoOperativo_kN: number;
	momentoGobernante_kNm: number;
	vesselDiameter_mm: number;
	lugQuantity: number;
	lugElevation_mm?: number;
	lugWidth_mm: number;
	lugLength_mm: number;
	lugThickness_mm: number;
	lugEccentricity_mm: number;
	lugHoleDiameter_mm?: number;
	lugGusset: boolean;
	lugGussetThickness_mm?: number;
	lugPadPlate: boolean;
	lugPadWidth_mm?: number;
	lugPadLength_mm?: number;
	lugPadThickness_mm?: number;
};

export type LugReactions = {
	cargaMaxPorMensula_kN: number;
	esfuerzoFlexionMensula_MPa: number;
	esfuerzoCorteMensula_MPa: number;
	presionPlacaApoyo_MPa: number;
	alertaFlexionMensula: boolean;
	alertaFaltaPlaca: boolean;
};

export const calculateLugReactions = (inputs: LugDesignInputs): LugReactions => {
	const W_N = toPositive(inputs.pesoOperativo_kN, 0) * 1000;
	const M_Nmm = toPositive(inputs.momentoGobernante_kNm, 0) * 1000000;
	const D = toPositive(inputs.vesselDiameter_mm, 0);
	const N = toPositive(inputs.lugQuantity, 2);
	const e = toPositive(inputs.lugEccentricity_mm, 0);

	if (W_N === 0 || D === 0 || N === 0) {
		return {
			cargaMaxPorMensula_kN: 0,
			esfuerzoFlexionMensula_MPa: 0,
			esfuerzoCorteMensula_MPa: 0,
			presionPlacaApoyo_MPa: 0,
			alertaFlexionMensula: false,
			alertaFaltaPlaca: false,
		};
	}

	const D_support = D + 2 * e;
	const cargaPorPeso = W_N / N;
	let cargaPorMomento = 0;
	if (D_support > 0) {
		cargaPorMomento = (4 * M_Nmm) / (N * D_support);
	}

	const P_max_N = cargaPorPeso + cargaPorMomento;
	const b = toPositive(inputs.lugWidth_mm, 1);
	const L_lug = toPositive(inputs.lugLength_mm, 1);
	const t = toPositive(inputs.lugThickness_mm, 1);
	const M_lug = P_max_N * e;

	let Z_lug = 0;
	if (inputs.lugGusset && toPositive(inputs.lugGussetThickness_mm, 0) > 0) {
		const t_g = toPositive(inputs.lugGussetThickness_mm, 0);
		Z_lug = (t_g * Math.pow(L_lug, 2)) / 3;
	} else {
		Z_lug = (b * Math.pow(t, 2)) / 6;
	}

	const esfuerzoFlexionMensula = Z_lug > 0 ? M_lug / Z_lug : 0;
	const areaCorte = b * t;
	const esfuerzoCorteMensula = areaCorte > 0 ? P_max_N / areaCorte : 0;

	let presionPlacaApoyo_MPa = 0;
	let alertaFaltaPlaca = false;
	if (inputs.lugPadPlate) {
		const pad_W = toPositive(inputs.lugPadWidth_mm, 1);
		const pad_L = toPositive(inputs.lugPadLength_mm, 1);
		const areaPad = pad_W * pad_L;
		presionPlacaApoyo_MPa = areaPad > 0 ? P_max_N / areaPad : 0;
	} else if (P_max_N > 50000) {
		alertaFaltaPlaca = true;
	}

	const alertaFlexionMensula = esfuerzoFlexionMensula > 150;

	const result = {
		cargaMaxPorMensula_kN: Number((P_max_N / 1000).toFixed(2)),
		esfuerzoFlexionMensula_MPa: Number(esfuerzoFlexionMensula.toFixed(2)),
		esfuerzoCorteMensula_MPa: Number(esfuerzoCorteMensula.toFixed(2)),
		presionPlacaApoyo_MPa: Number(presionPlacaApoyo_MPa.toFixed(2)),
		alertaFlexionMensula,
		alertaFaltaPlaca,
	};

	console.log('[LugUtils][calculateLugReactions]', result);
	return result;
};
