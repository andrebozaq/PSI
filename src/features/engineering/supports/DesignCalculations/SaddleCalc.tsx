import { BlockResults, DesignInputs } from './Constants';
import { toPositive } from './PhysicsUtils';

/**
 * Objetivo: construir la etapa de bloque para soporte tipo Silleta (Saddle).
 * Entradas: `DesignInputs` del wizard con altura y ubicación de silleta.
 * Salida: `BlockResults` con valores capturados y advertencias por omisiones.
 * Norma/Criterio: validación preliminar de datos mínimos para soporte horizontal sobre silletas.
 */
export const computeSaddleBlock = (input: DesignInputs): BlockResults => {
	const saddleHeight = toPositive(input.saddleHeight, 0);
	const saddleLocation = toPositive(input.saddleLocation, 0);

	const warnings: string[] = [];

	if (saddleHeight === 0) warnings.push('Falta altura de la silleta.');
	if (saddleLocation === 0) {
		warnings.push('Falta ubicación de la silleta (distancia A).');
	}

	const result: BlockResults = {
		status: 'ready',
		values: {
			saddleHeight,
			saddleLocation,
		},
		warnings,
	};

	console.log('[SaddleCalc][computeSaddleBlock][return]', result);
	return result;
};