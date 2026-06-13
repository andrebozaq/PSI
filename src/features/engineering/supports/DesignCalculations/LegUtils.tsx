import { toPositive } from './PhysicsUtils';

const E_STEEL_MPA = 200000;
const FY_STEEL_MPA = 250;
const AISC_SAFETY_FACTOR = 1.67;

export const STANDARD_LEG_PROFILES: Record<
	string,
	{ name: string; area_mm2: number; r_mm: number }
> = {
	PIPE_4_SCH40: { name: 'Pipe 4" Sch 40', area_mm2: 2050, r_mm: 38.3 },
	PIPE_6_SCH40: { name: 'Pipe 6" Sch 40', area_mm2: 3600, r_mm: 57.0 },
	PIPE_8_SCH40: { name: 'Pipe 8" Sch 40', area_mm2: 5420, r_mm: 74.6 },
	PIPE_10_SCH40: { name: 'Pipe 10" Sch 40', area_mm2: 7680, r_mm: 92.6 },
};

export type LegDesignInputs = {
	vesselType: string;
	pesoOperativo_kN: number;
	momentoGobernante_kNm: number;
	fuerzaCorteGobernante_kN: number;
	vesselDiameter_mm: number;

	// Inputs de geometría base
	numberOfLegs?: number;
	legLength_mm?: number;

	// Para verticales y esféricos (patrón circular)
	pitchDiameter_mm?: number;

	// Para horizontales (patrón rectangular)
	legSpacing_mm?: number;
	legWidth_mm?: number;

	// Arriostramiento
	isBraced?: boolean;
	braceLevels?: number;

	// Placa base / pernos (preparación para chequeos siguientes)
	basePlateWidth_mm?: number;
	basePlateLength_mm?: number;
	boltDiameter_mm?: number;
	boltsPerLeg?: number;
};

export type LegReactions = {
	cargaVerticalBase_kN: number;
	cargaPorMomento_kN: number;
	compresionMaxima_kN: number;
	tensionMaxima_kN: number;
	cortePorPata_kN: number;
	alertaLevantamiento: boolean;
};

export type LegVerificationInputs = {
	compresionMaxima_kN: number;
	legLength_mm: number;
	profileKey?: string;
	profileLabel?: string;
	legAngleWidth_mm?: number;
	legAngleThickness_mm?: number;
	legPipeOD_mm?: number;
	legPipeThickness_mm?: number;
	isBraced?: boolean;
	braceLevels?: number;
	kFactor?: number;
};

export type LegVerificationResult = {
	perfilUsado: string;
	segmentosPandeo: number;
	longitudEfectiva_mm: number;
	esbeltez: number;
	esfuerzoReal_MPa: number;
	esfuerzoAdmisible_MPa: number;
	ratio: number;
	pasaDiseño: boolean;
	fallaPorEsbeltez: boolean;
};

const normalizeVesselType = (type: string) => {
	const normalized = String(type || '').trim().toLowerCase();
	if (normalized === 'horizontal') return 'horizontal';
	if (normalized === 'columna vertical' || normalized === 'vertical') return 'vertical';
	if (normalized === 'esférico' || normalized === 'esferico' || normalized === 'spherical') {
		return 'spherical';
	}
	return normalized;
};

type ResolvedProfile = { name: string; area_mm2: number; r_mm: number };

const buildPipeProfileFromGeometry = (
	od_mm: number,
	thickness_mm: number,
): ResolvedProfile | null => {
	if (od_mm <= 0 || thickness_mm <= 0) return null;
	const di_mm = Math.max(od_mm - 2 * thickness_mm, 0);
	const area_mm2 = (Math.PI / 4) * (od_mm ** 2 - di_mm ** 2);
	if (area_mm2 <= 0) return null;
	const inertia_mm4 = (Math.PI / 64) * (od_mm ** 4 - di_mm ** 4);
	const r_mm = Math.sqrt(inertia_mm4 / area_mm2);

	return {
		name: `Pipe ${od_mm.toFixed(1)}x${thickness_mm.toFixed(1)} mm`,
		area_mm2,
		r_mm,
	};
};

const buildAngleProfileFromGeometry = (
	width_mm: number,
	thickness_mm: number,
): ResolvedProfile | null => {
	if (width_mm <= 0 || thickness_mm <= 0) return null;
	const area_mm2 = Math.max(2 * width_mm * thickness_mm - thickness_mm ** 2, 0);
	if (area_mm2 <= 0) return null;
	const r_mm = Math.max(0.2 * width_mm, thickness_mm);

	return {
		name: `Ángulo L ${width_mm.toFixed(1)}x${width_mm.toFixed(1)}x${thickness_mm.toFixed(1)} mm`,
		area_mm2,
		r_mm,
	};
};

const resolveProfileForVerification = (
	inputs: LegVerificationInputs,
): ResolvedProfile => {
	const key = String(inputs.profileKey ?? '').trim();
	if (key && STANDARD_LEG_PROFILES[key]) return STANDARD_LEG_PROFILES[key];

	const label = String(inputs.profileLabel ?? '').toLowerCase();
	const isAngle = /angulo|ángulo|\(l\)|angle/.test(label);
	const isPipe = /pipe|tube|tubo|sch/.test(label);

	if (isAngle) {
		const angle = buildAngleProfileFromGeometry(
			toPositive(inputs.legAngleWidth_mm, 0),
			toPositive(inputs.legAngleThickness_mm, 0),
		);
		if (angle) return angle;
	}

	if (isPipe) {
		const pipe = buildPipeProfileFromGeometry(
			toPositive(inputs.legPipeOD_mm, 0),
			toPositive(inputs.legPipeThickness_mm, 0),
		);
		if (pipe) return pipe;
	}

	return STANDARD_LEG_PROFILES.PIPE_6_SCH40;
};

/**
 * FUNCIÓN: calculateLegReactions
 * Determina las reacciones máximas en la base de las patas de soporte
 * aplicando los principios del Pressure Vessel Design Manual (Moss).
 */
export const calculateLegReactions = (inputs: LegDesignInputs): LegReactions => {
	const W = toPositive(inputs.pesoOperativo_kN, 0);
	const M = toPositive(inputs.momentoGobernante_kNm, 0);
	const V = toPositive(inputs.fuerzaCorteGobernante_kN, 0);
	const D_vessel = toPositive(inputs.vesselDiameter_mm, 0) / 1000;
	const normalizedType = normalizeVesselType(inputs.vesselType);
	const N = toPositive(inputs.numberOfLegs, 4);

	if (N === 0) {
		return {
			cargaVerticalBase_kN: 0,
			cargaPorMomento_kN: 0,
			compresionMaxima_kN: 0,
			tensionMaxima_kN: 0,
			cortePorPata_kN: 0,
			alertaLevantamiento: false,
		};
	}

	const cargaVerticalBase = W / N;

	let cargaPorMomento = 0;

	if (normalizedType === 'horizontal') {
		const L_span =
			toPositive(inputs.legSpacing_mm, 0) > 0
				? toPositive(inputs.legSpacing_mm, 0) / 1000
				: D_vessel * 1.5;
		const B_width =
			toPositive(inputs.legWidth_mm, 0) > 0
				? toPositive(inputs.legWidth_mm, 0) / 1000
				: D_vessel;
		const brazoMinimo = Math.min(L_span, B_width);

		if (brazoMinimo <= 0 || N < 2) {
			return {
				cargaVerticalBase_kN: 0,
				cargaPorMomento_kN: 0,
				compresionMaxima_kN: 0,
				tensionMaxima_kN: 0,
				cortePorPata_kN: 0,
				alertaLevantamiento: false,
			};
		}

		cargaPorMomento = M / (brazoMinimo * (N / 2));
	} else {
		const D_circle =
			toPositive(inputs.pitchDiameter_mm, 0) > 0
				? toPositive(inputs.pitchDiameter_mm, 0) / 1000
				: D_vessel;

		if (D_circle <= 0) {
			return {
				cargaVerticalBase_kN: 0,
				cargaPorMomento_kN: 0,
				compresionMaxima_kN: 0,
				tensionMaxima_kN: 0,
				cortePorPata_kN: 0,
				alertaLevantamiento: false,
			};
		}

		cargaPorMomento = (4 * M) / (N * D_circle);
	}

	const cortePorPata = V / N;
	const compresionMaxima = cargaVerticalBase + cargaPorMomento;
	const tensionMaxima = cargaVerticalBase - cargaPorMomento;

	const result = {
		cargaVerticalBase_kN: Number(cargaVerticalBase.toFixed(2)),
		cargaPorMomento_kN: Number(cargaPorMomento.toFixed(2)),
		compresionMaxima_kN: Number(compresionMaxima.toFixed(2)),
		tensionMaxima_kN: Number(tensionMaxima.toFixed(2)),
		cortePorPata_kN: Number(cortePorPata.toFixed(2)),
		alertaLevantamiento: tensionMaxima < 0,
	};

	console.log('[LegUtils][calculateLegReactions]', result);
	return result;
};

export const verifyLegProfile = (
	inputs: LegVerificationInputs,
): LegVerificationResult => {
	const P_Newtons = toPositive(inputs.compresionMaxima_kN, 0) * 1000;
	const L = toPositive(inputs.legLength_mm, 0);
	const K = toPositive(inputs.kFactor, 1.2);
	const isBraced = Boolean(inputs.isBraced);
	const braceLevels = Math.max(0, Math.floor(toPositive(inputs.braceLevels, 0)));
	const unbracedSegments = isBraced ? braceLevels + 1 : 1;
	const effectiveLength_mm = L / unbracedSegments;

	const profile = resolveProfileForVerification(inputs);

	if (P_Newtons === 0 || L === 0) {
		const result = {
			perfilUsado: profile.name,
			segmentosPandeo: unbracedSegments,
			longitudEfectiva_mm: Number(effectiveLength_mm.toFixed(2)),
			esbeltez: 0,
			esfuerzoReal_MPa: 0,
			esfuerzoAdmisible_MPa: 0,
			ratio: 0,
			pasaDiseño: true,
			fallaPorEsbeltez: false,
		};
		console.log('[LegUtils][verifyLegProfile]', result);
		return result;
	}

	const esbeltez = (K * effectiveLength_mm) / profile.r_mm;
	const fallaPorEsbeltez = esbeltez > 200;
	const esfuerzoReal = P_Newtons / profile.area_mm2;
	const Fe = (Math.PI ** 2 * E_STEEL_MPA) / (esbeltez ** 2);

	let Fcr = 0;
	const limiteEsbeltez = 4.71 * Math.sqrt(E_STEEL_MPA / FY_STEEL_MPA);

	if (esbeltez <= limiteEsbeltez) {
		Fcr = Math.pow(0.658, FY_STEEL_MPA / Fe) * FY_STEEL_MPA;
	} else {
		Fcr = 0.877 * Fe;
	}

	const esfuerzoAdmisible = Fcr / AISC_SAFETY_FACTOR;
	const ratio = esfuerzoReal / esfuerzoAdmisible;
	const pasaDiseño = ratio <= 1 && !fallaPorEsbeltez;

	const result = {
		perfilUsado: profile.name,
		segmentosPandeo: unbracedSegments,
		longitudEfectiva_mm: Number(effectiveLength_mm.toFixed(2)),
		esbeltez: Number(esbeltez.toFixed(2)),
		esfuerzoReal_MPa: Number(esfuerzoReal.toFixed(2)),
		esfuerzoAdmisible_MPa: Number(esfuerzoAdmisible.toFixed(2)),
		ratio: Number(ratio.toFixed(3)),
		pasaDiseño,
		fallaPorEsbeltez,
	};

	console.log('[LegUtils][verifyLegProfile]', result);
	return result;
};
