import { BlockResults, DesignInputs } from './Constants';
import { toPositive } from './PhysicsUtils';

/**
 * Objetivo: construir la etapa de bloque para soporte tipo faldón.
 * Entradas: `DesignInputs` del wizard (diámetro base, espesor y cantidad de pernos).
 * Salida: `BlockResults` con valores mínimos y advertencias por omisiones de entrada.
 * Norma/Criterio: control preliminar de datos antes de verificaciones estructurales finales.
 */
export const computeSkirtBlock = (input: DesignInputs): BlockResults => {
	const skirtDiameter = toPositive(input.skirtBaseDiameter, 0);
	const skirtThickness = toPositive(input.skirtThickness, 0);
	const boltCount = toPositive(input.boltQuantity, 0);

	const warnings: string[] = [];

	if (skirtDiameter === 0) warnings.push('Falta diámetro de base del faldón.');
	if (skirtThickness === 0) warnings.push('Falta espesor del faldón.');
	if (boltCount === 0) warnings.push('Falta cantidad de pernos de anclaje.');

	const result: BlockResults = {
		status: 'ready',
		values: {
			skirtDiameter,
			skirtThickness,
			boltCount,
		},
		warnings,
	};
	console.log('[SkirtCalc][computeSkirtBlock][return]', result);
	return result;
};

