import { toPositive } from './PhysicsUtils';

const ZICK_FACTORS = {
	'120': {
		K1: 0.0528,
		K2: 1.171,
		K3: 0.88,
		K4: 0.32,
		K5: 0.76,
	},
	'150': {
		K1: 0.0316,
		K2: 0.799,
		K3: 0.485,
		K4: 0.204,
		K5: 0.543,
	},
} as const;

export type SaddleDesignInputs = {
	pesoOperativo_kN: number;
	fuerzaCorteGobernante_kN: number;
	vesselDiameter_mm: number;
	vesselLength_mm: number;
	vesselThickness_mm: number;
	saddleLocation_mm: number;
	saddleContactAngle: string;
	saddleWebThickness_mm: number;
	saddleBasePlateWidth_mm: number;
	saddleBasePlateLength_mm: number;
	saddleFrictionType: string;
	wearPlateEnabled: boolean;
	wearPlateThickness_mm: number;
	saddleRibCount?: number;
	saddleRibThickness_mm?: number;
};

export type SaddleReactions = {
	cargaVerticalPorSilleta_kN: number;
	cargaLongitudinalFija_kN: number;
	cargaTransversal_kN: number;
	esfuerzoCuerno_MPa: number;
	compresionPlacaBase_MPa: number;
	esfuerzoFlexionSilleta_MPa: number;
	esfuerzoFlexionCentro_MPa: number;
	esfuerzoCompresionSilleta_MPa: number;
	alertaCuerno: boolean;
	alertaFlexion: boolean;
	alertaSilleta: boolean;
};

export const calculateSaddleReactions = (
	inputs: SaddleDesignInputs,
): SaddleReactions => {
	const W_N = toPositive(inputs.pesoOperativo_kN, 0) * 1000;
	const V_N = toPositive(inputs.fuerzaCorteGobernante_kN, 0) * 1000;
	const D = toPositive(inputs.vesselDiameter_mm, 0);
	const R = D / 2;
	const L = toPositive(inputs.vesselLength_mm, 0);
	let t = toPositive(inputs.vesselThickness_mm, 0);
	const A = toPositive(inputs.saddleLocation_mm, L * 0.2);
	const angleNumeric = inputs.saddleContactAngle === '150' ? 150 : 120;
	const K = ZICK_FACTORS[String(angleNumeric) as '120' | '150'];

	if (inputs.wearPlateEnabled && toPositive(inputs.wearPlateThickness_mm, 0) > 0) {
		t += toPositive(inputs.wearPlateThickness_mm, 0);
	}

	if (W_N === 0 || R === 0 || t === 0 || L === 0) {
		return {
			cargaVerticalPorSilleta_kN: 0,
			cargaLongitudinalFija_kN: 0,
			cargaTransversal_kN: 0,
			esfuerzoCuerno_MPa: 0,
			compresionPlacaBase_MPa: 0,
			esfuerzoFlexionSilleta_MPa: 0,
			esfuerzoFlexionCentro_MPa: 0,
			esfuerzoCompresionSilleta_MPa: 0,
			alertaCuerno: false,
			alertaFlexion: false,
			alertaSilleta: false,
		};
	}

	const Q = W_N / 2;
	let cargaLongitudinalFija = V_N;
	if (/alta\s*fricci[oó]n/i.test(String(inputs.saddleFrictionType || ''))) {
		const friccion = Q * 0.3;
		cargaLongitudinalFija = Math.max(V_N - friccion, V_N * 0.5);
	}

	const cargaTransversal = V_N / 2;
	const b = toPositive(inputs.saddleBasePlateWidth_mm, 200);
	const compresionDirecta = Q / (4 * t * (b + 10 * t));
	const flexionLocal = (3 * K.K3 * Q) / (2 * Math.pow(t, 2));
	const esfuerzoCuerno = compresionDirecta + flexionLocal;
	const H = R / 2;
	const Z = Math.PI * Math.pow(R, 2) * t;
	const A_calc = Math.max(A, 1);

	const terminoSilleta_num =
		1 - A_calc / L + (Math.pow(R, 2) - Math.pow(H, 2)) / (2 * A_calc * L);
	const terminoSilleta_den = 1 + (4 * H) / (3 * L);
	const M1 = -Q * A_calc * (1 - terminoSilleta_num / terminoSilleta_den);

	const terminoCentro_num =
		1 + (2 * (Math.pow(R, 2) - Math.pow(H, 2))) / Math.pow(L, 2);
	const M2 =
		(Q * L * 0.25) * (terminoCentro_num / terminoSilleta_den - (4 * A_calc) / L);

	const esfuerzoFlexionSilleta = Z > 0 ? Math.abs(M1 / Z) : 0;
	const esfuerzoFlexionCentro = Z > 0 ? Math.abs(M2 / Z) : 0;

	const anchoBase = toPositive(inputs.saddleBasePlateWidth_mm, 1);
	const largoBase = toPositive(inputs.saddleBasePlateLength_mm, 1);
	const compresionPlacaBase = Q / (anchoBase * largoBase);
	const anchoAlma_mm = D * Math.sin((angleNumeric / 2) * (Math.PI / 180));
	const t_alma = toPositive(inputs.saddleWebThickness_mm, 0);
	const numCostillas = toPositive(inputs.saddleRibCount, 3);
	const t_costilla = toPositive(inputs.saddleRibThickness_mm, 0);
	const areaAlma_mm2 = anchoAlma_mm * t_alma;
	const areaCostillas_mm2 = numCostillas * t_costilla * anchoBase;
	const areaEfectivaSilleta_mm2 = areaAlma_mm2 + areaCostillas_mm2;
	const esfuerzoCompresionSilleta =
		areaEfectivaSilleta_mm2 > 0 ? Q / areaEfectivaSilleta_mm2 : 0;
	const alertaCuerno = esfuerzoCuerno > 150;
	const alertaFlexion =
		Math.max(esfuerzoFlexionSilleta, esfuerzoFlexionCentro) > 100;
	const alertaSilleta = esfuerzoCompresionSilleta > 100;

	const result = {
		cargaVerticalPorSilleta_kN: Number((Q / 1000).toFixed(2)),
		cargaLongitudinalFija_kN: Number((cargaLongitudinalFija / 1000).toFixed(2)),
		cargaTransversal_kN: Number((cargaTransversal / 1000).toFixed(2)),
		esfuerzoCuerno_MPa: Number(esfuerzoCuerno.toFixed(2)),
		compresionPlacaBase_MPa: Number(compresionPlacaBase.toFixed(2)),
		esfuerzoFlexionSilleta_MPa: Number(esfuerzoFlexionSilleta.toFixed(2)),
		esfuerzoFlexionCentro_MPa: Number(esfuerzoFlexionCentro.toFixed(2)),
		esfuerzoCompresionSilleta_MPa: Number(esfuerzoCompresionSilleta.toFixed(2)),
		alertaCuerno,
		alertaFlexion,
		alertaSilleta,
	};

	console.log('[SaddleUtils][calculateSaddleReactions]', result);
	return result;
};
