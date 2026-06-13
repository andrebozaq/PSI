import { BlockResults, DesignInputs } from './Constants';
import { toPositive } from './PhysicsUtils';

/**
 * Objetivo: generar la validación de bloque mínima para soporte tipo ménsula.
 * Entradas: `DesignInputs` del formulario (cantidad, espesor y diámetro de agujero).
 * Salida: `BlockResults` con valores básicos y advertencias por datos faltantes.
 * Norma/Criterio: control preliminar de integridad de datos para habilitar verificación final.
 */
export const computeLugBlock = (input: DesignInputs): BlockResults => {
	const lugQuantity = toPositive(input.lugQuantity, 0);
	const lugThickness = toPositive(input.lugThickness, 0);
	const holeDiameter = toPositive(input.lugHoleDiameter, 0);

	const warnings: string[] = [];

	if (lugQuantity === 0) warnings.push('Falta cantidad de ménsulas (lug).');
	if (lugThickness === 0) warnings.push('Falta espesor del lug.');
	if (holeDiameter === 0) warnings.push('Falta diámetro del agujero del lug.');

	const result: BlockResults = {
		status: 'ready',
		values: {
			lugQuantity,
			lugThickness,
			holeDiameter,
		},
		warnings,
	};
	console.log('[LugCalc][computeLugBlock][return]', result);
	return result;
};

