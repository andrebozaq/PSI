import { BlockResults, DesignInputs } from './Constants';
import { toPositive } from './PhysicsUtils';
import { calculateLegReactions, verifyLegProfile } from './LegUtils';

/**
 * Objetivo: construir la etapa de bloque para soporte en patas.
 * Entradas: `DesignInputs` del wizard (geometría, cargas, pernos y configuración de perfil).
 * Salida: `BlockResults` con reacciones, verificación de perfil y advertencias de diseño.
 * Norma/Criterio: reparto de cargas tipo Moss + verificación de compresión/esbeltez tipo AISC simplificado.
 */
export const computeLegBlock = (input: DesignInputs): BlockResults => {
	const legQuantity = toPositive(input.legQuantity, 0);
	const legLength = toPositive(input.legLength, 0);
	const boltDiameter = toPositive(input.legBoltDiameter, 0);
	const pitchDiameter = toPositive(input.pitchDiameter_mm ?? input.legBoltCircle, 0);
	const legSpacing = toPositive(
		input.legSpacing_mm ?? input.legSpacing ?? input.legLongSpacing,
		0,
	);
	const legWidth = toPositive(
		input.legWidth_mm ?? input.legWidth ?? input.legTransSpacing,
		0,
	);
	const supportType = String(input.supportType ?? '');
	const isBraced = /arriostrada/i.test(supportType);
	const braceLevels = toPositive(input.braceLevels ?? input.bracingTier, 0);
	const boltsPerLeg = toPositive(input.boltsPerLeg ?? input.legBoltPerLeg, 0);

	const reactions = calculateLegReactions({
		vesselType: String(input.vesselType ?? input.orientation ?? ''),
		pesoOperativo_kN: toPositive(input.pesoOperativo_kN, 0),
		momentoGobernante_kNm: toPositive(input.momentoGobernante_kNm, 0),
		fuerzaCorteGobernante_kN: toPositive(input.fuerzaCorteGobernante_kN, 0),
		vesselDiameter_mm: toPositive(input.vesselDiameter_mm ?? input.outerDiameter, 0),
		numberOfLegs: legQuantity > 0 ? legQuantity : 4,
		legLength_mm: legLength,
		pitchDiameter_mm: pitchDiameter,
		legSpacing_mm: legSpacing,
		legWidth_mm: legWidth,
		isBraced,
		braceLevels,
		basePlateWidth_mm: toPositive(input.basePlateWidth_mm ?? input.legBasePlateWidth, 0),
		basePlateLength_mm: toPositive(input.basePlateLength_mm ?? input.legBasePlateLength, 0),
		boltDiameter_mm: boltDiameter,
		boltsPerLeg,
	});
	const profileKey = String(
		input.legProfileKey ?? input.legProfile ?? input.profileKey ?? 'PIPE_6_SCH40',
	);
	const verification = verifyLegProfile({
		compresionMaxima_kN: reactions.compresionMaxima_kN,
		legLength_mm: legLength,
		profileKey,
		profileLabel: String(input.legProfile ?? ''),
		legAngleWidth_mm: toPositive(input.legAngleWidth, 0),
		legAngleThickness_mm: toPositive(input.legAngleThickness, 0),
		legPipeOD_mm: toPositive(input.legPipeOD, 0),
		legPipeThickness_mm: toPositive(input.legPipeThickness, 0),
		isBraced,
		braceLevels,
		kFactor: toPositive(input.kFactor, 1.2),
	});

	const warnings: string[] = [];

	if (legQuantity === 0) warnings.push('Falta cantidad de patas.');
	if (legLength === 0) warnings.push('Falta longitud de la pata.');
	if (boltDiameter === 0) warnings.push('Falta diámetro de perno de anclaje.');
	if (toPositive(input.pesoOperativo_kN, 0) === 0) {
		warnings.push('Falta peso operativo para cálculo estructural de patas.');
	}
	if (toPositive(input.momentoGobernante_kNm, 0) === 0) {
		warnings.push('Falta momento gobernante para cálculo de compresión/tensión en patas.');
	}
	if (toPositive(input.fuerzaCorteGobernante_kN, 0) === 0) {
		warnings.push('Falta cortante gobernante para cálculo de corte por pata.');
	}
	if (reactions.alertaLevantamiento) {
		warnings.push('Se detecta levantamiento en patas. Diseñar pernos de anclaje a tracción.');
	}
	if (verification.fallaPorEsbeltez) {
		warnings.push('La pata excede esbeltez admisible (KL/r > 200). Riesgo de pandeo.');
	}
	if (!verification.pasaDiseño) {
		warnings.push('El perfil de pata no cumple compresión AISC (ratio > 1.0).');
	}

	const result: BlockResults = {
		status: 'ready',
		values: {
			legQuantity,
			legLength,
			boltDiameter,
			pitchDiameter,
			legSpacing,
			legWidth,
			isBraced,
			braceLevels,
			boltsPerLeg,
			...reactions,
			leg_perfilUsado: verification.perfilUsado,
			leg_segmentosPandeo: verification.segmentosPandeo,
			leg_longitudEfectiva_mm: verification.longitudEfectiva_mm,
			leg_esbeltez: verification.esbeltez,
			leg_esfuerzoReal_MPa: verification.esfuerzoReal_MPa,
			leg_esfuerzoAdmisible_MPa: verification.esfuerzoAdmisible_MPa,
			leg_ratioCompresion: verification.ratio,
			leg_pasaDiseño: verification.pasaDiseño,
			leg_fallaPorEsbeltez: verification.fallaPorEsbeltez,
		},
		warnings,
	};
	console.log('[LegCalc][computeLegBlock][return]', result);
	return result;
};

