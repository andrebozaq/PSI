import { toPositive } from './PhysicsUtils';

export type SkirtDesignInputs = {
	pesoOperativo_kN: number;
	momentoGobernante_kNm: number;
	vesselDiameter_mm: number;
	skirtGeometry: string;
	skirtHeight_mm: number;
	skirtThickness_mm: number;
	skirtBaseDiameter_mm?: number;
	skirtTopDiameter_mm?: number;
	skirtAccessHoleDiameter_mm?: number;
	skirtRingID_mm: number;
	skirtRingOD_mm: number;
	skirtRingThickness_mm: number;
	skirtBoltCircleDiameter_mm: number;
	skirtAnchorBoltCount: number;
	skirtAnchorChairs: boolean;
	skirtChairHeight_mm?: number;
	skirtChairTopPlateWidth_mm?: number;
	skirtChairTopPlateThickness_mm?: number;
};

export type SkirtReactions = {
	esfuerzoCompresionFaldon_MPa: number;
	esfuerzoTensionFaldon_MPa: number;
	presionConcreto_MPa: number;
	tensionMaxPerno_kN: number;
	esfuerzoPlacaSilla_MPa: number;
	alertaPandeoFaldon: boolean;
	alertaLevantamientoFaldon: boolean;
	alertaAgujeroAcceso: boolean;
	alertaSillaAnclaje: boolean;
};

export const calculateSkirtReactions = (
	inputs: SkirtDesignInputs,
): SkirtReactions => {
	const W_N = toPositive(inputs.pesoOperativo_kN, 0) * 1000;
	const M_Nmm = toPositive(inputs.momentoGobernante_kNm, 0) * 1000000;
	const isConical = inputs.skirtGeometry === 'conical';
	const t = toPositive(inputs.skirtThickness_mm, 0);
	const H = toPositive(inputs.skirtHeight_mm, 0);

	let D_base = toPositive(inputs.vesselDiameter_mm, 0);
	if (isConical && toPositive(inputs.skirtBaseDiameter_mm, 0) > 0) {
		D_base = toPositive(inputs.skirtBaseDiameter_mm, 0);
	}

	if (W_N === 0 || D_base === 0 || t === 0) {
		return {
			esfuerzoCompresionFaldon_MPa: 0,
			esfuerzoTensionFaldon_MPa: 0,
			presionConcreto_MPa: 0,
			tensionMaxPerno_kN: 0,
			esfuerzoPlacaSilla_MPa: 0,
			alertaPandeoFaldon: false,
			alertaLevantamientoFaldon: false,
			alertaAgujeroAcceso: false,
			alertaSillaAnclaje: false,
		};
	}

	const D_m = D_base - t;
	let cosTheta = 1;
	if (isConical && H > 0) {
		const D_top = toPositive(inputs.skirtTopDiameter_mm, inputs.vesselDiameter_mm);
		const radioDiff = (D_base - D_top) / 2;
		const theta_rad = Math.atan(radioDiff / H);
		cosTheta = Math.cos(theta_rad);
	}

	const Area_skirt = (Math.PI * D_m * t) / cosTheta;
	const Z_skirt = (Math.PI * Math.pow(D_m, 2) * t) / (4 * cosTheta);
	const esfuerzoAxialPeso = W_N / Area_skirt;
	const esfuerzoFlexion = M_Nmm / Z_skirt;
	const esfuerzoCompresionFaldon = esfuerzoAxialPeso + esfuerzoFlexion;
	const esfuerzoTensionFaldon = esfuerzoFlexion - esfuerzoAxialPeso;

	const OD_ring = toPositive(inputs.skirtRingOD_mm, 0);
	const ID_ring = toPositive(inputs.skirtRingID_mm, 0);
	let presionConcreto = 0;
	if (OD_ring > ID_ring) {
		const Area_ring =
			(Math.PI / 4) * (Math.pow(OD_ring, 2) - Math.pow(ID_ring, 2));
		const Z_ring =
			((Math.PI / 32) * (Math.pow(OD_ring, 4) - Math.pow(ID_ring, 4))) /
			OD_ring;
		presionConcreto = W_N / Area_ring + M_Nmm / Z_ring;
	}

	const N_bolts = toPositive(inputs.skirtAnchorBoltCount, 0);
	const D_bc = toPositive(inputs.skirtBoltCircleDiameter_mm, 0);
	let tensionMaxPerno_N = 0;
	if (N_bolts > 0 && D_bc > 0) {
		const tensionPorMomento = (4 * M_Nmm) / (N_bolts * D_bc);
		const compresionPorPeso = W_N / N_bolts;
		tensionMaxPerno_N = tensionPorMomento - compresionPorPeso;
	}

	let esfuerzoPlacaSilla_MPa = 0;
	let alertaSillaAnclaje = false;
	if (inputs.skirtAnchorChairs && tensionMaxPerno_N > 0) {
		const anchoPlaca = toPositive(inputs.skirtChairTopPlateWidth_mm, 1);
		const espesorPlaca = toPositive(inputs.skirtChairTopPlateThickness_mm, 1);
		if (anchoPlaca > 0 && espesorPlaca > 0) {
			esfuerzoPlacaSilla_MPa =
				(1.5 * tensionMaxPerno_N * anchoPlaca) /
				(anchoPlaca * Math.pow(espesorPlaca, 2));
			alertaSillaAnclaje = esfuerzoPlacaSilla_MPa > 150;
		}
	}

	const alertaPandeoFaldon = esfuerzoCompresionFaldon > 100;
	const alertaLevantamientoFaldon = tensionMaxPerno_N > 0;
	const hole_dia = toPositive(inputs.skirtAccessHoleDiameter_mm, 0);
	const alertaAgujeroAcceso = hole_dia > D_base / 3;

	const result = {
		esfuerzoCompresionFaldon_MPa: Number(esfuerzoCompresionFaldon.toFixed(2)),
		esfuerzoTensionFaldon_MPa: Number(Math.max(esfuerzoTensionFaldon, 0).toFixed(2)),
		presionConcreto_MPa: Number(presionConcreto.toFixed(2)),
		tensionMaxPerno_kN: Number((Math.max(tensionMaxPerno_N, 0) / 1000).toFixed(2)),
		esfuerzoPlacaSilla_MPa: Number(esfuerzoPlacaSilla_MPa.toFixed(2)),
		alertaPandeoFaldon,
		alertaLevantamientoFaldon,
		alertaAgujeroAcceso,
		alertaSillaAnclaje,
	};

	console.log('[SkirtUtils][calculateSkirtReactions]', result);
	return result;
};
