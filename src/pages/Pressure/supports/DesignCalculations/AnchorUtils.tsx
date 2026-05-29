import { toPositive } from './PhysicsUtils';

const BOLT_MATERIALS: Record<string, { Fu: number; Fy: number }> = {
	'Acero al carbono': { Fu: 400, Fy: 250 },
	'Acero inoxidable': { Fu: 515, Fy: 205 },
	A325: { Fu: 830, Fy: 630 },
	A490: { Fu: 1040, Fy: 900 },
};

type BoltMaterialKey = keyof typeof BOLT_MATERIALS;

/**
 * Objetivo: normalizar el material ingresado en UI y mapearlo
 * a una clave válida de la base ligera de pernos.
 * Entradas: nombre de material en texto libre.
 * Salida: clave normalizada (`Acero al carbono`, `Acero inoxidable`, `A325`, `A490`).
 * Norma/Criterio: catálogo interno simplificado para chequeos preliminares.
 */
const resolveBoltMaterial = (inputMaterial: string): BoltMaterialKey => {
	const normalized = String(inputMaterial ?? '').trim().toLowerCase();
	if (normalized.includes('inox')) return 'Acero inoxidable';
	if (normalized.includes('a325')) return 'A325';
	if (normalized.includes('a490')) return 'A490';
	if (normalized.includes('carbon')) return 'Acero al carbono';
	if (normalized.includes('acero al carbono')) return 'Acero al carbono';
	return 'Acero al carbono';
};

export type AnchorDesignInputs = {
	tensionPorPerno_kN: number;
	cortePorPerno_kN: number;
	boltQuantity: number;
	boltDiameter_mm: number;
	boltMaterial: string;
	embedmentDepth_mm: number;
	concreteStrength_MPa: number;
	anchorType: string;
	anchorEdgeDistance_mm: number;
};

export type AnchorReactions = {
	capacidadTensionAcero_kN: number;
	capacidadCorteAcero_kN: number;
	ratioInteraccionAcero: number;
	capacidadDesprendimientoConcreto_kN: number;
	ratioConcreto: number;
	alertaAcero: boolean;
	alertaConcreto: boolean;
	alertaBorde: boolean;
};

/**
 * Objetivo: evaluar el desempeño del anclaje frente a tracción/corte en acero
 * y frente a desprendimiento de concreto.
 * Entradas: cargas por perno, geometría del perno, material, profundidad de anclaje,
 * resistencia del concreto y distancia al borde.
 * Salida: capacidades de acero y concreto, ratios de utilización y banderas de alerta.
 * Norma/Criterio: AISC simplificado (acero) + ACI 318 simplificado (breakout y borde).
 */
export const calculateAnchorReactions = (
	inputs: AnchorDesignInputs,
): AnchorReactions => {
	const Tu = toPositive(inputs.tensionPorPerno_kN, 0);
	const Vu = toPositive(inputs.cortePorPerno_kN, 0);
	const d = toPositive(inputs.boltDiameter_mm, 0);
	const hef = toPositive(inputs.embedmentDepth_mm, 0);
	const fc = toPositive(inputs.concreteStrength_MPa, 21);
	const c1 = toPositive(inputs.anchorEdgeDistance_mm, 0);

	const material = BOLT_MATERIALS[resolveBoltMaterial(inputs.boltMaterial)];

	if (d === 0) {
		return {
			capacidadTensionAcero_kN: 0,
			capacidadCorteAcero_kN: 0,
			ratioInteraccionAcero: 0,
			capacidadDesprendimientoConcreto_kN: 0,
			ratioConcreto: 0,
			alertaAcero: false,
			alertaConcreto: false,
			alertaBorde: false,
		};
	}

	const Ag = (Math.PI / 4) * d ** 2;
	const Ase = 0.75 * Ag;

	const phi_tension = 0.75;
	const phi_corte = 0.65;

	const Nsa_N = Ase * material.Fu;
	const Vsa_N = 0.6 * Ase * material.Fu;

	const phiNsa_kN = (phi_tension * Nsa_N) / 1000;
	const phiVsa_kN = (phi_corte * Vsa_N) / 1000;

	const ratioTension = phiNsa_kN > 0 ? Tu / phiNsa_kN : 0;
	const ratioCorte = phiVsa_kN > 0 ? Vu / phiVsa_kN : 0;
	const ratioInteraccionAcero = ratioTension + ratioCorte;

	let phiNcb_kN = 0;
	let ratioConcreto = 0;
	let alertaBorde = false;

	if (hef > 0 && fc > 0) {
		const phi_concreto = 0.7;
		const kc = 10;
		const Nb_N = kc * Math.sqrt(fc) * hef ** 1.5;

		let psi_edge = 1;
		if (c1 > 0 && c1 < 1.5 * hef) {
			psi_edge = 0.7 + 0.3 * (c1 / (1.5 * hef));
			alertaBorde = true;
		}

		phiNcb_kN = (phi_concreto * Nb_N * psi_edge) / 1000;
		ratioConcreto = phiNcb_kN > 0 ? Tu / phiNcb_kN : 0;
	}

	const alertaAcero = ratioInteraccionAcero > 1;
	const alertaConcreto = hef > 0 ? ratioConcreto > 1 : false;

	const result = {
		capacidadTensionAcero_kN: Number(phiNsa_kN.toFixed(2)),
		capacidadCorteAcero_kN: Number(phiVsa_kN.toFixed(2)),
		ratioInteraccionAcero: Number(ratioInteraccionAcero.toFixed(3)),
		capacidadDesprendimientoConcreto_kN: Number(phiNcb_kN.toFixed(2)),
		ratioConcreto: Number(ratioConcreto.toFixed(3)),
		alertaAcero,
		alertaConcreto,
		alertaBorde,
	};

	console.log('[AnchorUtils][calculateAnchorReactions]', result);
	return result;
};