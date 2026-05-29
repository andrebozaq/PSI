import { BlockResults, DesignInputs } from './Constants';
import { toPositive } from './PhysicsUtils';
import { calculateRingReactions } from './RingUtils';

/**
 * Objetivo: ejecutar la etapa de bloque para soporte tipo anillo.
 * Entradas: `DesignInputs` con perfil, geometría de alma/brida, placa base y gussets.
 * Salida: `BlockResults` con reacciones calculadas y alertas de cumplimiento preliminar.
 * Norma/Criterio: validación mecánica simplificada sobre flexión del anillo y presión en base.
 */
export const computeRingBlock = (input: DesignInputs): BlockResults => {
	const reactions = calculateRingReactions({
		pesoOperativo_kN: toPositive(input.pesoOperativo_kN, 0),
		vesselDiameter_mm: toPositive(input.vesselDiameter_mm ?? input.outerDiameter, 0),
		ringProfile: String(input.ringProfile ?? 'Barra'),
		ringWebHeight_mm: toPositive(input.ringWebHeight, 0),
		ringWebThickness_mm: toPositive(input.ringWebThickness, 0),
		ringFlangeWidth_mm: toPositive(input.ringFlangeWidth, 0),
		ringFlangeThickness_mm: toPositive(input.ringFlangeThickness, 0),
		ringBasePlateWidth_mm: toPositive(input.ringBasePlateWidth, 0),
		ringBasePlateLength_mm: toPositive(input.ringBasePlateLength, 0),
		ringGussets:
			input.ringGussets === true ||
			String(input.ringGussets).toLowerCase() === 'true',
		ringGussetQty: toPositive(input.ringGussetQty, 4),
		ringGussetThickness_mm: toPositive(input.ringGussetThickness, 0),
		ringGussetWidth_mm: toPositive(input.ringGussetWidth, 0),
	});

	const warnings: string[] = [];

	if (toPositive(input.ringWebHeight, 0) === 0) {
		warnings.push('Falta altura del alma del anillo.');
	}
	if (toPositive(input.ringWebThickness, 0) === 0) {
		warnings.push('Falta espesor del alma del anillo.');
	}
	if (toPositive(input.ringBasePlateWidth, 0) === 0 || toPositive(input.ringBasePlateLength, 0) === 0) {
		warnings.push('Faltan dimensiones de placa base del anillo.');
	}
	if (reactions.alertaFlexion) {
		warnings.push('El anillo no cumple por flexión. Cambie perfil o aumente dimensiones.');
	}
	if (reactions.alertaPresionBase) {
		warnings.push('La placa base del anillo excede la presión recomendada.');
	}

	const result: BlockResults = {
		status: 'ready',
		values: {
			ringProfile: String(input.ringProfile ?? 'Barra'),
			ringWebHeight: toPositive(input.ringWebHeight, 0),
			ringWebThickness: toPositive(input.ringWebThickness, 0),
			ringFlangeWidth: toPositive(input.ringFlangeWidth, 0),
			ringFlangeThickness: toPositive(input.ringFlangeThickness, 0),
			ringBasePlateWidth: toPositive(input.ringBasePlateWidth, 0),
			ringBasePlateLength: toPositive(input.ringBasePlateLength, 0),
			ringGussets:
				input.ringGussets === true ||
				String(input.ringGussets).toLowerCase() === 'true',
			ringGussetQty: toPositive(input.ringGussetQty, 4),
			...reactions,
		},
		warnings,
	};

	console.log('[RingCalc][computeRingBlock][return]', result);
	return result;
};
