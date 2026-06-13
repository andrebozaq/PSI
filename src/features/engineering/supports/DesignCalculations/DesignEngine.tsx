import {
	BlockResults,
	DesignInputs,
	EMPTY_BLOCK_RESULTS,
	EMPTY_FINAL_RESULTS,
	EMPTY_LIGHTWEIGHT_RESULTS,
	FinalDesignResults,
	LightweightResults,
	RecommendedDimension,
	SupportKind,
	VerificationRow,
} from './Constants';
import { computeLegBlock } from './LegCalc';
import { computeLugBlock } from './LugCalc';
import { computeLightweightResults } from './PhysicsUtils';
import { computeRingBlock } from './RingCalc';
import { computeSaddleBlock } from './SaddleCalc';
import { computeSkirtBlock } from './SkirtCalc';
import { DESIGN_ALLOWABLES } from './DesignThresholds';

export type CalculationSnapshot = {
	lightweight: LightweightResults;
	block: BlockResults;
	final: FinalDesignResults;
};

/**
 * Objetivo: inicializar el estado de cálculo del wizard.
 * Entradas: ninguna.
 * Salida: `CalculationSnapshot` vacío con etapas lightweight, block y final en `idle`.
 * Norma/Criterio: arranque determinístico del pipeline de cálculo.
 */
export const createEmptySnapshot = (): CalculationSnapshot => ({
	lightweight: EMPTY_LIGHTWEIGHT_RESULTS,
	block: EMPTY_BLOCK_RESULTS,
	final: EMPTY_FINAL_RESULTS,
});

/**
 * Objetivo: mapear el soporte de UI al tipo interno de cálculo.
 * Entradas: texto de soporte seleccionado (`supportType`).
 * Salida: `SupportKind` normalizado.
 * Norma/Criterio: prioriza coincidencia por regex para Skirt/Leg/Lug/Ring/Saddle.
 */
export const resolveSupportKind = (supportType: unknown): SupportKind => {
	const support = String(supportType ?? '');
	if (/^Skirt/i.test(support)) return 'Skirt';
	if (/^Leg/i.test(support)) return 'Leg';
	if (/^Lug/i.test(support)) return 'Lug';
	if (/Ring/i.test(support)) return 'Ring';
	if (/Saddle/i.test(support)) return 'Saddle';
	return 'Unknown';
};

/**
 * Objetivo: ejecutar la etapa intermedia de bloque según soporte.
 * Entradas: `DesignInputs` ya normalizados para el contexto del wizard.
 * Salida: `BlockResults` con valores intermedios y advertencias por módulo.
 * Norma/Criterio: enrutamiento por `SupportKind` al `*Calc` correspondiente.
 */
export const computeBlockResults = (input: DesignInputs): BlockResults => {
	const supportKind = resolveSupportKind(input.supportType);

	if (supportKind === 'Skirt') {
		const result = computeSkirtBlock(input);
		console.log('[DesignEngine][computeBlockResults][Skirt]', result);
		return result;
	}
	if (supportKind === 'Leg') {
		const result = computeLegBlock(input);
		console.log('[DesignEngine][computeBlockResults][Leg]', result);
		return result;
	}
	if (supportKind === 'Lug') {
		const result = computeLugBlock(input);
		console.log('[DesignEngine][computeBlockResults][Lug]', result);
		return result;
	}
	if (supportKind === 'Ring') {
		const result = computeRingBlock(input);
		console.log('[DesignEngine][computeBlockResults][Ring]', result);
		return result;
	}
	if (supportKind === 'Saddle') {
		const result = computeSaddleBlock(input);
		console.log('[DesignEngine][computeBlockResults][Saddle]', result);
		return result;
	}

	const result: BlockResults = {
		status: 'ready',
		values: {},
		warnings: ['No hay cálculo de bloque definido para este tipo de soporte.'],
	};
	console.log('[DesignEngine][computeBlockResults][default]', result);
	return result;
};

/**
 * Objetivo: ensamblar la salida final legible del reporte de diseño.
 * Entradas: `DesignInputs`, resultados de bloque y derivados lightweight.
 * Salida: `FinalDesignResults` (dimensiones, verificaciones y notas).
 * Norma/Criterio: aplica allowables centralizados y conversión SI/US para presentación.
 */
export const computeFinalResults = (
	input: DesignInputs,
	block: BlockResults,
	lightweight?: LightweightResults,
): FinalDesignResults => {
	const supportKind = resolveSupportKind(input.supportType);
	const derived = lightweight?.derived;
	const targetUnitSystem =
		String(input.unitSystem ?? 'SI').toUpperCase() === 'US' ? 'US' : 'SI';
	const lengthUnit = targetUnitSystem === 'US' ? 'in' : 'mm';
	const forceUnit = targetUnitSystem === 'US' ? 'kips' : 'kN';
	const stressUnit = targetUnitSystem === 'US' ? 'psi' : 'MPa';
	const areaUnit = targetUnitSystem === 'US' ? 'in²' : 'mm²';
	const sectionUnit = targetUnitSystem === 'US' ? 'in³' : 'mm³';

	const toFiniteNumber = (value: unknown, fallback = 0) => {
		const numeric = Number(value);
		return Number.isFinite(numeric) ? numeric : fallback;
	};

	const fmt = (value: unknown, digits = 2) => {
		const numeric = Number(value);
		if (!Number.isFinite(numeric)) return '-';
		return numeric.toFixed(digits);
	};

	const fromSiLength = (valueMm: unknown) => {
		const numeric = toFiniteNumber(valueMm, 0);
		return targetUnitSystem === 'US' ? numeric / 25.4 : numeric;
	};

	const fromSiForce = (valuekN: unknown) => {
		const numeric = toFiniteNumber(valuekN, 0);
		return targetUnitSystem === 'US' ? numeric * 0.2248089431 : numeric;
	};

	const fromSiStress = (valueMPa: unknown) => {
		const numeric = toFiniteNumber(valueMPa, 0);
		return targetUnitSystem === 'US' ? numeric * 145.037738 : numeric;
	};

	const fromSiArea = (valueMm2: unknown) => {
		const numeric = toFiniteNumber(valueMm2, 0);
		return targetUnitSystem === 'US' ? numeric / 645.16 : numeric;
	};

	const fromSiSection = (valueMm3: unknown) => {
		const numeric = toFiniteNumber(valueMm3, 0);
		return targetUnitSystem === 'US' ? numeric / 16387.064 : numeric;
	};

	const toSiLength = (value: unknown) => {
		const numeric = toFiniteNumber(value, 0);
		return targetUnitSystem === 'US' ? numeric * 25.4 : numeric;
	};

	const toSiStress = (value: unknown) => {
		const numeric = toFiniteNumber(value, 0);
		return targetUnitSystem === 'US' ? numeric / 145.037738 : numeric;
	};

	const normalizeNoteUnits = (text: string) => {
		if (targetUnitSystem === 'SI') return text;
		return text
			.replace(/\bMPa\b/g, 'psi')
			.replace(/\bkN\b/g, 'kips')
			.replace(/\bmm\b/g, 'in');
	};

	const roundUp = (value: number, step: number) => {
		if (!Number.isFinite(value) || value <= 0) return 0;
		if (!Number.isFinite(step) || step <= 0) return value;
		return Math.ceil(value / step) * step;
	};

	const fabricationSteps =
		targetUnitSystem === 'US'
			? { length: 1 / 16, area: 0.25, section: 0.1 }
			: { length: 1, area: 100, section: 1000 };

	const fabLength = (valueMm: number) =>
		roundUp(fromSiLength(valueMm), fabricationSteps.length);
	const fabArea = (valueMm2: number) =>
		roundUp(fromSiArea(valueMm2), fabricationSteps.area);
	const fabSection = (valueMm3: number) =>
		roundUp(fromSiSection(valueMm3), fabricationSteps.section);

	const W_N = toFiniteNumber(derived?.pesoOperativo_kN, 0) * 1000;
	const M_Nmm = toFiniteNumber(derived?.momentoGobernante_kNm, 0) * 1_000_000;
	const D_mm = toSiLength(input.outerDiameter);
	const concreteStrength_MPa = Math.max(0.1, toSiStress(input.concreteStrength ?? 21));
	const tieneDatosMinimos =
		toFiniteNumber(input.outerDiameter, 0) > 0 &&
		(toFiniteNumber(input.length, 0) > 0 || toFiniteNumber(input.height, 0) > 0) &&
		toFiniteNumber(derived?.pesoOperativo_kN, 0) > 0;

	const resolveStatus = (
		passes: boolean,
		failStatus: 'No cumple' | 'Revisar' = 'No cumple',
	): 'Cumple' | 'No cumple' | 'Revisar' | 'Pendiente' => {
		if (!tieneDatosMinimos) return 'Pendiente';
		return passes ? 'Cumple' : failStatus;
	};

	const resolveActual = (value: string) => (tieneDatosMinimos ? value : 'N/A');

	let recommendedDimensions: RecommendedDimension[] = [
		{
			parameter: 'Dimensiones mínimas recomendadas',
			value: 'Pendiente de cálculo en DesignEngine',
		},
	];
	let verificationRows: VerificationRow[] = [
		{
			check: 'Carga real vs carga permisible',
			actual: 'Pendiente',
			allowable: 'Pendiente',
			status: 'Pendiente',
		},
	];

	if (supportKind === 'Leg') {
		const ratio = toFiniteNumber(block.values.leg_ratioCompresion, 0);
		const esbeltez = toFiniteNumber(block.values.leg_esbeltez, 0);
		const pasaDiseno = Boolean(block.values.leg_pasaDiseño);
		const fallaEsbeltez = Boolean(block.values.leg_fallaPorEsbeltez);
		const alertaLevantamiento = Boolean(derived?.leg_alertaLevantamiento);

		const areaPerfilMin_mm2 =
			(toFiniteNumber(derived?.leg_compresionMaxima_kN, 0) * 1000) /
			DESIGN_ALLOWABLES.SKIRT_COMP_MPA;

		recommendedDimensions = [
			{
				parameter: 'Perfil recomendado de pata',
				value: String(block.values.leg_perfilUsado ?? 'Pendiente'),
			},
			{
				parameter: 'Longitud efectiva de pandeo',
				value: `${fmt(fromSiLength(block.values.leg_longitudEfectiva_mm))} ${lengthUnit}`,
			},
			{
				parameter: 'Arriostramiento',
				value: Boolean(block.values.isBraced)
					? `Sí (${fmt(block.values.braceLevels, 0)} nivel(es))`
					: 'No',
			},
			{
				parameter: 'Área mínima de sección del perfil (diseño)',
				value: `${fmt(fromSiArea(areaPerfilMin_mm2))} ${areaUnit} → ${fmt(fabArea(areaPerfilMin_mm2))} ${areaUnit} (recomendado)`,
			},
		];

		if (esbeltez > DESIGN_ALLOWABLES.LEG_SLENDERNESS) {
			recommendedDimensions.push({
				parameter: 'Niveles de arriostramiento recomendados',
				value: `AGREGAR (KL/r = ${fmt(esbeltez, 1)} > ${DESIGN_ALLOWABLES.LEG_SLENDERNESS})`,
			});
		}

		verificationRows = [
			{
				check: 'Compresión axial AISC',
				actual: resolveActual(`Ratio = ${fmt(ratio, 3)}`),
				allowable: `≤ ${fmt(DESIGN_ALLOWABLES.LEG_RATIO, 3)}`,
				status: resolveStatus(pasaDiseno),
			},
			{
				check: 'Esbeltez de pata (KL/r)',
				actual: resolveActual(fmt(esbeltez, 2)),
				allowable: `≤ ${DESIGN_ALLOWABLES.LEG_SLENDERNESS}`,
				status: resolveStatus(!fallaEsbeltez),
			},
			{
				check: 'Levantamiento por volcamiento',
				actual: resolveActual(alertaLevantamiento ? 'Sí' : 'No'),
				allowable: 'No',
				status: resolveStatus(!alertaLevantamiento),
			},
			{
				check: 'Compresión máxima por pata',
				actual: resolveActual(`${fmt(fromSiForce(derived?.leg_compresionMaxima_kN))} ${forceUnit}`),
				allowable: 'Según perfil seleccionado',
				status: resolveStatus(pasaDiseno, 'Revisar'),
			},
		];
	}

	if (supportKind === 'Ring') {
		const area = toFiniteNumber(derived?.ring_areaSeccion_mm2, 0);
		const z = toFiniteNumber(derived?.ring_moduloSeccion_mm3, 0);
		const sFlex = toFiniteNumber(derived?.ring_esfuerzoFlexionAnillo_MPa, 0);
		const sCorte = toFiniteNumber(derived?.ring_esfuerzoCorteAnillo_MPa, 0);
		const pBase = toFiniteNumber(derived?.ring_presionPlacaBase_MPa, 0);
		const alertaFlex = Boolean(derived?.ring_alertaFlexion);
		const alertaBase = Boolean(derived?.ring_alertaPresionBase);

		recommendedDimensions = [
			{
				parameter: 'Perfil de anillo',
				value: String(input.ringProfile ?? 'Barra'),
			},
			{
				parameter: 'Geometría alma/brida',
				value: `h=${fmt(input.ringWebHeight ?? 0)} ${lengthUnit}, tw=${fmt(input.ringWebThickness ?? 0)} ${lengthUnit}, bf=${fmt(input.ringFlangeWidth ?? 0)} ${lengthUnit}, tf=${fmt(input.ringFlangeThickness ?? 0)} ${lengthUnit}`,
			},
			{
				parameter: 'Placa base por apoyo',
				value: `${fmt(input.ringBasePlateWidth ?? 0)} x ${fmt(input.ringBasePlateLength ?? 0)} ${lengthUnit}`,
			},
		];

		const numApoyos = Math.max(1, toFiniteNumber(input.ringGussetQty ?? 4, 4));
		const cargaPorApoyo_N = W_N / numApoyos;
		const excentricidad_mm = Math.max(1, toSiLength(input.ringWebHeight ?? 100) / 2);
		const momentoApoyo_Nmm = cargaPorApoyo_N * excentricidad_mm;
		const zMin_mm3 = momentoApoyo_Nmm / DESIGN_ALLOWABLES.RING_FLEX_MPA;
		const areaPlacaBaseMin_mm2 = cargaPorApoyo_N / (0.85 * concreteStrength_MPa);

		recommendedDimensions.push(
			{
				parameter: 'Módulo de sección mínimo requerido (diseño)',
				value: `${fmt(fromSiSection(zMin_mm3))} ${sectionUnit} → ${fmt(fabSection(zMin_mm3))} ${sectionUnit} (recomendado)`,
			},
			{
				parameter: 'Área mínima de placa base (diseño)',
				value: `${fmt(fromSiArea(areaPlacaBaseMin_mm2))} ${areaUnit} → ${fmt(fabArea(areaPlacaBaseMin_mm2))} ${areaUnit} (recomendado)`,
			},
		);

		verificationRows = [
			{
				check: 'Área de sección del anillo',
				actual: resolveActual(`${fmt(fromSiArea(area))} ${areaUnit}`),
				allowable: 'Mayor es mejor',
				status: resolveStatus(area > 0),
			},
			{
				check: 'Módulo de sección Z',
				actual: resolveActual(`${fmt(fromSiSection(z))} ${sectionUnit}`),
				allowable: 'Mayor es mejor',
				status: resolveStatus(z > 0),
			},
			{
				check: 'Flexión en anillo',
				actual: resolveActual(`${fmt(fromSiStress(sFlex))} ${stressUnit}`),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.RING_FLEX_MPA))} ${stressUnit}`,
				status: resolveStatus(!alertaFlex),
			},
			{
				check: 'Corte en anillo',
				actual: resolveActual(`${fmt(fromSiStress(sCorte))} ${stressUnit}`),
				allowable: 'Según material',
				status: resolveStatus(false, 'Revisar'),
			},
			{
				check: 'Presión en placa base',
				actual: resolveActual(`${fmt(fromSiStress(pBase))} ${stressUnit}`),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.RING_BASE_MPA))} ${stressUnit}`,
				status: resolveStatus(!alertaBase),
			},
		];
	}

	if (supportKind === 'Lug') {
		const pMax = toFiniteNumber(derived?.lug_cargaMaxPorMensula_kN, 0);
		const sFlex = toFiniteNumber(derived?.lug_esfuerzoFlexionMensula_MPa, 0);
		const sCorte = toFiniteNumber(derived?.lug_esfuerzoCorteMensula_MPa, 0);
		const pPad = toFiniteNumber(derived?.lug_presionPlacaApoyo_MPa, 0);
		const alertaFlex = Boolean(derived?.lug_alertaFlexionMensula);
		const alertaPad = Boolean(derived?.lug_alertaFaltaPlaca);

		recommendedDimensions = [
			{
				parameter: 'Cantidad de ménsulas',
				value: `${fmt(input.lugQuantity ?? 2, 0)} uds`,
			},
			{
				parameter: 'Espesor de ménsula',
				value: `${fmt(input.lugThickness ?? 0)} ${lengthUnit}`,
			},
			{
				parameter: 'Refuerzo / Pad Plate',
				value: `Gusset: ${String(input.lugGusset ?? false) === 'true' ? 'Sí' : 'No'} | Pad: ${String(input.lugPadPlate ?? false) === 'true' ? 'Sí' : 'No'}`,
			},
		];

		const Pmax_N = pMax * 1000;
		const e_mm = Math.max(1, toSiLength(input.lugEccentricity ?? 50));
		const b_mm = Math.max(1, toSiLength(input.lugWidth ?? 150));
		const tLugMin_mm = Math.sqrt(
			Math.max(0, (6 * Pmax_N * e_mm) / (b_mm * DESIGN_ALLOWABLES.LUG_FLEX_MPA)),
		);

		recommendedDimensions.push({
			parameter: 'Espesor mínimo de ménsula (diseño sin gusset)',
			value: `${fmt(fromSiLength(tLugMin_mm))} ${lengthUnit} → ${fmt(fabLength(tLugMin_mm))} ${lengthUnit} (recomendado)`,
		});

		verificationRows = [
			{
				check: 'Carga máxima por ménsula',
				actual: resolveActual(`${fmt(fromSiForce(pMax))} ${forceUnit}`),
				allowable: 'Según arreglo estructural',
				status: resolveStatus(false, 'Revisar'),
			},
			{
				check: 'Flexión en ménsula',
				actual: resolveActual(`${fmt(fromSiStress(sFlex))} ${stressUnit}`),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.LUG_FLEX_MPA))} ${stressUnit}`,
				status: resolveStatus(!alertaFlex),
			},
			{
				check: 'Corte en ménsula',
				actual: resolveActual(`${fmt(fromSiStress(sCorte))} ${stressUnit}`),
				allowable: 'Según material',
				status: resolveStatus(false, 'Revisar'),
			},
			{
				check: 'Presión en placa de apoyo',
				actual: resolveActual(
					String(input.lugPadPlate ?? false) === 'true'
						? `${fmt(fromSiStress(pPad))} ${stressUnit}`
						: 'No aplica',
				),
				allowable: '≤ capacidad local de pared',
				status: resolveStatus(!alertaPad, 'Revisar'),
			},
			{
				check: 'Recomendación de Pad Plate',
				actual: resolveActual(alertaPad ? 'Requerida' : 'No requerida'),
				allowable: 'No requerida',
				status: resolveStatus(!alertaPad),
			},
		];
	}

	if (supportKind === 'Saddle') {
		const horn = toFiniteNumber(derived?.saddle_esfuerzoCuerno_MPa, 0);
		const s1 = toFiniteNumber(derived?.saddle_esfuerzoFlexionSilleta_MPa, 0);
		const s2 = toFiniteNumber(derived?.saddle_esfuerzoFlexionCentro_MPa, 0);
		const ss = toFiniteNumber(derived?.saddle_esfuerzoCompresionSilleta_MPa, 0);
		const alertaCuerno = Boolean(derived?.saddle_alertaCuerno);
		const alertaFlexion = Boolean(derived?.saddle_alertaFlexion);
		const alertaSilleta = Boolean(derived?.saddle_alertaSilleta);

		recommendedDimensions = [
			{
				parameter: 'Ubicación recomendada de silleta (A)',
				value: `${fmt(toFiniteNumber(input.length, 0) * 0.2)} ${lengthUnit} (≈ 0.2·L)`,
			},
			{
				parameter: 'Ángulo de contacto',
				value: `${String(input.saddleContactAngle ?? '120')}°`,
			},
			{
				parameter: 'Costillas de refuerzo',
				value: `${fmt(input.saddleRibCount ?? 3, 0)} uds @ ${fmt(input.saddleRibThickness ?? 0)} ${lengthUnit}`,
			},
		];

		const Qsilleta_N = W_N / 2;
		const areaAlmaMin_mm2 = Qsilleta_N / DESIGN_ALLOWABLES.SADDLE_COMP_MPA;
		const areaPlacaBaseMin_mm2 = Qsilleta_N / (0.85 * concreteStrength_MPa);

		recommendedDimensions.push(
			{
				parameter: 'Área efectiva mínima (alma + costillas)',
				value: `${fmt(fromSiArea(areaAlmaMin_mm2))} ${areaUnit} → ${fmt(fabArea(areaAlmaMin_mm2))} ${areaUnit} (recomendado)`,
			},
			{
				parameter: 'Área mínima de placa base sobre concreto',
				value: `${fmt(fromSiArea(areaPlacaBaseMin_mm2))} ${areaUnit} → ${fmt(fabArea(areaPlacaBaseMin_mm2))} ${areaUnit} (recomendado)`,
			},
		);

		if (alertaCuerno) {
			recommendedDimensions.push({
				parameter: 'Placa de desgaste (Wear Plate)',
				value: 'REQUERIDA (esfuerzo en cuerno excedido)',
			});
		}

		verificationRows = [
			{
				check: 'Esfuerzo cuerno Zick S4',
				actual: resolveActual(`${fmt(fromSiStress(horn))} ${stressUnit}`),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.SADDLE_HORN_MPA))} ${stressUnit}`,
				status: resolveStatus(!alertaCuerno),
			},
			{
				check: 'Flexión longitudinal en silleta (S1)',
				actual: resolveActual(`${fmt(fromSiStress(s1))} ${stressUnit}`),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.SADDLE_FLEX_MPA))} ${stressUnit}`,
				status: resolveStatus(s1 <= DESIGN_ALLOWABLES.SADDLE_FLEX_MPA),
			},
			{
				check: 'Flexión longitudinal en centro (S2)',
				actual: resolveActual(`${fmt(fromSiStress(s2))} ${stressUnit}`),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.SADDLE_FLEX_MPA))} ${stressUnit}`,
				status: resolveStatus(s2 <= DESIGN_ALLOWABLES.SADDLE_FLEX_MPA),
			},
			{
				check: 'Compresión local de silleta',
				actual: resolveActual(`${fmt(fromSiStress(ss))} ${stressUnit}`),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.SADDLE_COMP_MPA))} ${stressUnit}`,
				status: resolveStatus(!alertaSilleta),
			},
		];

		if (
			alertaFlexion &&
			s1 <= DESIGN_ALLOWABLES.SADDLE_FLEX_MPA &&
			s2 <= DESIGN_ALLOWABLES.SADDLE_FLEX_MPA
		) {
			verificationRows[1].status = tieneDatosMinimos ? 'Revisar' : 'Pendiente';
			verificationRows[2].status = tieneDatosMinimos ? 'Revisar' : 'Pendiente';
		}
	}

	if (supportKind === 'Skirt') {
		const sComp = toFiniteNumber(derived?.skirt_esfuerzoCompresionFaldon_MPa, 0);
		const sTen = toFiniteNumber(derived?.skirt_esfuerzoTensionFaldon_MPa, 0);
		const pConc = toFiniteNumber(derived?.skirt_presionConcreto_MPa, 0);
		const tBolt = toFiniteNumber(derived?.skirt_tensionMaxPerno_kN, 0);
		const sChair = toFiniteNumber(derived?.skirt_esfuerzoPlacaSilla_MPa, 0);
		const alertaPandeo = Boolean(derived?.skirt_alertaPandeoFaldon);
		const alertaLift = Boolean(derived?.skirt_alertaLevantamientoFaldon);
		const alertaHole = Boolean(derived?.skirt_alertaAgujeroAcceso);
		const alertaSilla = Boolean(derived?.skirt_alertaSillaAnclaje);

		recommendedDimensions = [
			{
				parameter: 'Espesor de faldón seleccionado',
				value: `${fmt(input.skirtThickness ?? 0)} ${lengthUnit}`,
			},
			{
				parameter: 'Anillo base (ID/OD)',
				value: `${fmt(input.skirtRingID ?? 0)} / ${fmt(input.skirtRingOD ?? 0)} ${lengthUnit}`,
			},
			{
				parameter: 'Pernos de anclaje',
				value: `${fmt(input.skirtAnchorBoltCount ?? input.boltQuantity ?? 0, 0)} uds`,
			},
			{
				parameter: 'Sillas de anclaje',
				value:
					String(input.skirtAnchorChairs ?? 'false') === 'true'
						? `Sí (Top plate ${fmt(input.skirtChairTopPlateThickness ?? 0)} ${lengthUnit})`
						: 'No',
			},
		];

		const fuerzaCompresionTotal_N =
			W_N + (M_Nmm > 0 && D_mm > 0 ? (4 * M_Nmm) / D_mm : 0);
		const tMinSkirt_mm =
			D_mm > 0
				? fuerzaCompresionTotal_N /
					(Math.PI * D_mm * DESIGN_ALLOWABLES.SKIRT_COMP_MPA)
				: 0;
		const areaAnilloBaseMin_mm2 = fuerzaCompresionTotal_N / (0.85 * concreteStrength_MPa);

		recommendedDimensions.push(
			{
				parameter: 'Espesor mínimo de faldón (diseño)',
				value: `${fmt(fromSiLength(tMinSkirt_mm))} ${lengthUnit} → ${fmt(fabLength(tMinSkirt_mm))} ${lengthUnit} (recomendado)`,
			},
			{
				parameter: 'Área mínima de anillo base (diseño)',
				value: `${fmt(fromSiArea(areaAnilloBaseMin_mm2))} ${areaUnit} → ${fmt(fabArea(areaAnilloBaseMin_mm2))} ${areaUnit} (recomendado)`,
			},
		);

		verificationRows = [
			{
				check: 'Compresión en pared del faldón',
				actual: resolveActual(`${fmt(fromSiStress(sComp))} ${stressUnit}`),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.SKIRT_COMP_MPA))} ${stressUnit}`,
				status: resolveStatus(!alertaPandeo),
			},
			{
				check: 'Tensión en pared del faldón',
				actual: resolveActual(`${fmt(fromSiStress(sTen))} ${stressUnit}`),
				allowable: 'Control por material / anclaje',
				status: resolveStatus(!alertaLift, 'Revisar'),
			},
			{
				check: 'Presión sobre concreto (base ring)',
				actual: resolveActual(`${fmt(fromSiStress(pConc))} ${stressUnit}`),
				allowable: 'Según capacidad de fundación',
				status: resolveStatus(false, 'Revisar'),
			},
			{
				check: 'Tracción máxima por perno',
				actual: resolveActual(`${fmt(fromSiForce(tBolt))} ${forceUnit}`),
				allowable: '≤ capacidad de perno',
				status: resolveStatus(!alertaLift),
			},
			{
				check: 'Agujero de acceso (manhole)',
				actual: resolveActual(alertaHole ? '> D/3' : '≤ D/3'),
				allowable: '≤ D/3',
				status: resolveStatus(!alertaHole, 'Revisar'),
			},
			{
				check: 'Placa superior de silla de anclaje',
				actual: resolveActual(
					String(input.skirtAnchorChairs ?? 'false') === 'true'
						? `${fmt(fromSiStress(sChair))} ${stressUnit}`
						: 'No aplica',
				),
				allowable: `≤ ${fmt(fromSiStress(DESIGN_ALLOWABLES.SKIRT_CHAIR_MPA))} ${stressUnit}`,
				status:
					!tieneDatosMinimos
						? 'Pendiente'
						: String(input.skirtAnchorChairs ?? 'false') !== 'true'
						? 'Pendiente'
						: !alertaSilla
							? 'Cumple'
							: 'No cumple',
			},
		];
	}

	const hasAnchorInput =
		toFiniteNumber(input.boltQuantity ?? input.anchorBoltQuantity ?? input.skirtAnchorBoltCount, 0) >
		0 ||
		toFiniteNumber(
			input.boltDiameter ??
				input.anchorBoltDiameter ??
				input.legBoltDiameter ??
				input.skirtAnchorBoltDiameter,
			0,
		) > 0;
	const boltQuantityInput = toFiniteNumber(
		input.boltQuantity ?? input.anchorBoltQuantity ?? input.skirtAnchorBoltCount,
		0,
	);
	const boltDiameterInput = toFiniteNumber(
		input.boltDiameter ??
			input.anchorBoltDiameter ??
			input.legBoltDiameter ??
			input.skirtAnchorBoltDiameter,
		0,
	);
	const anclajeDatosMinimos =
		tieneDatosMinimos && boltQuantityInput > 0 && boltDiameterInput > 0;

	if (hasAnchorInput) {
		recommendedDimensions = [
			...recommendedDimensions,
			{
				parameter: 'Anclaje — configuración base',
				value: `${fmt(input.boltQuantity ?? input.anchorBoltQuantity ?? input.skirtAnchorBoltCount ?? 0, 0)} uds | Ø ${fmt(input.boltDiameter ?? input.anchorBoltDiameter ?? input.legBoltDiameter ?? input.skirtAnchorBoltDiameter ?? 0)} ${lengthUnit} | ${String(input.boltMaterial ?? 'Acero al carbono')}`,
			},
			{
				parameter: 'Anclaje — empotramiento y concreto',
				value: `hef=${fmt(input.embedmentDepth ?? 0)} ${lengthUnit} | f'c=${fmt(input.concreteStrength ?? 21)} ${stressUnit} | borde=${fmt(input.anchorEdgeDistance ?? 0)} ${lengthUnit}`,
			},
		];

		const tensionDiseno_kN =
			supportKind === 'Skirt'
				? toFiniteNumber(derived?.skirt_tensionMaxPerno_kN, 0)
				: supportKind === 'Leg'
					? Math.max(0, -toFiniteNumber(derived?.leg_tensionMaxima_kN, 0))
					: 0;

		if (tensionDiseno_kN > 0) {
			const boltMaterial = String(input.boltMaterial ?? 'Acero al carbono').toLowerCase();
			const Fu_MPa = boltMaterial.includes('a490')
				? 1040
				: boltMaterial.includes('a325')
					? 830
					: boltMaterial.includes('inox')
						? 515
						: 400;
			const aseReq_mm2 = (tensionDiseno_kN * 1000) / (0.75 * Fu_MPa);
			const dReq_mm = Math.sqrt((aseReq_mm2 * 4) / (Math.PI * 0.75));
			recommendedDimensions.push({
				parameter: 'Diámetro mínimo de perno (diseño)',
				value: `Ø ${fmt(fromSiLength(dReq_mm))} ${lengthUnit} → Ø ${fmt(fabLength(dReq_mm))} ${lengthUnit} (recomendado)`,
			});
		} else {
			recommendedDimensions.push({
				parameter: 'Criterio sísmico (tensión de anclaje)',
				value: 'Pernos gobernados solo por corte (sin levantamiento)',
			});
		}

		const steelRatio = toFiniteNumber(derived?.anchor_ratioInteraccionAcero, 0);
		const concreteRatio = toFiniteNumber(derived?.anchor_ratioConcreto, 0);
		const steelAlert = Boolean(derived?.anchor_alertaAcero);
		const concreteAlert = Boolean(derived?.anchor_alertaConcreto);
		const edgeAlert = Boolean(derived?.anchor_alertaBorde);

		verificationRows = [
			...verificationRows,
			{
				check: 'Anclaje acero (AISC interacción T+V)',
				actual: anclajeDatosMinimos ? `Ratio = ${fmt(steelRatio, 3)}` : 'N/A',
				allowable: `≤ ${fmt(DESIGN_ALLOWABLES.ANCHOR_STEEL_RATIO, 3)}`,
				status: !anclajeDatosMinimos ? 'Pendiente' : !steelAlert ? 'Cumple' : 'No cumple',
			},
			{
				check: 'Anclaje concreto (ACI breakout)',
				actual: anclajeDatosMinimos ? `Ratio = ${fmt(concreteRatio, 3)}` : 'N/A',
				allowable: `≤ ${fmt(DESIGN_ALLOWABLES.ANCHOR_CONCRETE_RATIO, 3)}`,
				status: !anclajeDatosMinimos ? 'Pendiente' : !concreteAlert ? 'Cumple' : 'No cumple',
			},
			{
				check: 'Distancia al borde de anclaje',
				actual: anclajeDatosMinimos ? (edgeAlert ? 'Penalizada' : 'Adecuada') : 'N/A',
				allowable: 'Adecuada',
				status: !anclajeDatosMinimos ? 'Pendiente' : !edgeAlert ? 'Cumple' : 'Revisar',
			},
		];
	}

	const anchorConclusion = (() => {
		if (!hasAnchorInput) return '';
		if (!anclajeDatosMinimos) {
			return 'Anclaje: REVISAR DATOS (faltan cantidad y/o diámetro de pernos para validar acero y concreto).';
		}
		const findings: string[] = [];
		if (Boolean(derived?.anchor_alertaAcero)) findings.push('ACERO');
		if (Boolean(derived?.anchor_alertaConcreto)) findings.push('CONCRETO');
		if (Boolean(derived?.anchor_alertaBorde)) findings.push('BORDE');

		if (!findings.length) {
			return 'Anclaje: OK (acero y concreto dentro de criterios simplificados).';
		}

		const reasons: string[] = [];
		if (findings.includes('ACERO')) {
			reasons.push('interacción tracción+corte supera el criterio de acero');
		}
		if (findings.includes('CONCRETO')) {
			reasons.push('riesgo de breakout en concreto por tracción');
		}
		if (findings.includes('BORDE')) {
			reasons.push('la cercanía al borde penaliza la capacidad');
		}

		return `Anclaje: REVISAR ${findings.join(' Y ')} (${reasons.join('; ')}).`;
	})();

	const baseNotes = [
		'Resultado preliminar: pendiente de implementación normativa (ASME/COVENIN).',
		`Sistema de unidades activo en reporte: ${targetUnitSystem} (${lengthUnit}, ${forceUnit}, ${stressUnit}).`,
		...(anchorConclusion ? [anchorConclusion] : []),
		...(lightweight?.warnings ?? []),
		...block.warnings,
	].map((note) => normalizeNoteUnits(String(note)));

	if (!tieneDatosMinimos) {
		baseNotes.push(
			normalizeNoteUnits(
				'ADVERTENCIA: El reporte muestra valores en cero porque faltan dimensiones críticas (Diámetro, Longitud/Altura o Peso operativo). Ingrese estos datos para obtener un cálculo real.',
			),
		);
	}

	const result: FinalDesignResults = {
		status: 'ready',
		supportKind,
		recommendedDimensions,
		verificationRows,
		notes: baseNotes,
	};
	console.log('[DesignEngine][computeFinalResults][return]', result);
	return result;
};

/**
 * Objetivo: ejecutar únicamente el cálculo lightweight en tiempo real.
 * Entradas: `DesignInputs` y snapshot previo opcional.
 * Salida: nuevo `CalculationSnapshot` con etapa lightweight actualizada.
 * Norma/Criterio: recalculo rápido on-change sin forzar etapa final.
 */
export const runLightweightStage = (
	input: DesignInputs,
	previous?: CalculationSnapshot,
): CalculationSnapshot => {
	const current = previous ?? createEmptySnapshot();
	const result = {
		...current,
		lightweight: computeLightweightResults(input),
	};
	console.log('[DesignEngine][runLightweightStage][return]', result);
	return result;
};

/**
 * Objetivo: ejecutar la etapa de bloque reutilizando derivados lightweight.
 * Entradas: `DesignInputs` y snapshot previo opcional.
 * Salida: nuevo `CalculationSnapshot` con etapa block actualizada.
 * Norma/Criterio: compone `blockInput` como mezcla de input crudo + `lightweight.derived`.
 */
export const runBlockStage = (
	input: DesignInputs,
	previous?: CalculationSnapshot,
): CalculationSnapshot => {
	const current = previous ?? createEmptySnapshot();
	const lightweight =
		current.lightweight.status === 'ready'
			? current.lightweight
			: computeLightweightResults(input);
	const blockInput: DesignInputs = {
		...input,
		...lightweight.derived,
	};
	const block = computeBlockResults(blockInput);

	const result = {
		...current,
		lightweight,
		block,
	};
	console.log('[DesignEngine][runBlockStage][return]', result);
	return result;
};

/**
 * Objetivo: ejecutar el pipeline completo del wizard hasta reporte final.
 * Entradas: `DesignInputs` y snapshot previo opcional.
 * Salida: `CalculationSnapshot` con etapa `final` lista para UI.
 * Norma/Criterio: secuencia obligatoria `runBlockStage` → `computeFinalResults`.
 */
export const runFinalStage = (
	input: DesignInputs,
	previous?: CalculationSnapshot,
): CalculationSnapshot => {
	const withBlock = runBlockStage(input, previous);
	const final = computeFinalResults(input, withBlock.block, withBlock.lightweight);

	const result = {
		...withBlock,
		final,
	};
	console.log('[DesignEngine][runFinalStage][return]', result);
	return result;
};

