import { DesignInputs, LightweightResults, UnitSystem } from './Constants';
import { calculateAnchorReactions } from './AnchorUtils';
import {
	calculateSeismicLoads,
	calculateWindLoads,
	resolveWindDesignCode,
} from './EnvironmentalUtils';
import { calculateLegReactions } from './LegUtils';
import { calculateLugReactions } from './LugUtils';
import { calculateRingReactions } from './RingUtils';
import { calculateSkirtReactions } from './SkirtUtils';
import { calculateSaddleReactions } from './SaddleUtils';

/**
 * CONSTANTES FÍSICAS
 * Nota: Se pueden mover a Constants.tsx cuando se conecte una base de datos de materiales.
 */
const g = 9.81;
const DENSIDAD_AGUA = 1000;
const DENSIDAD_ACERO = 7850;
const DENSIDAD_AISLAMIENTO = 130;
const FACTOR_MAYORACION_ACERO = 1.1;
const FACTOR_INTERNOS = 0.05;

export type PesosEquipo = {
	pesoVacio_kN: number;
	pesoFluido_kN: number;
	pesoOperativo_kN: number;
};

export type CentroGravedad = {
	cgVacio_mm: number;
	cgFluido_mm: number;
	cgOperativo_mm: number;
};

export type VesselWeightInput = {
	type: string;
	diameter: number;
	thickness: number;
	length?: number;
	height?: number;
	density?: number;
	insulationThickness?: number;
};

export type HeadsType = 'ellipsoidal' | 'hemispherical';

const normalizeVesselType = (type: string) => {
	const normalized = String(type || '').trim().toLowerCase();
	if (normalized === 'horizontal') return 'horizontal';
	if (normalized === 'columna vertical' || normalized === 'vertical') {
		return 'vertical';
	}
	if (normalized === 'esférico' || normalized === 'esferico' || normalized === 'spherical') {
		return 'spherical';
	}
	return normalized;
};

export const getMaterialDensity = (material?: string) => {
	const normalized = String(material || '').trim().toLowerCase();

	if (normalized.includes('304')) return 8000;
	if (normalized.includes('316')) return 8000;
	if (normalized.includes('inoxidable')) return 8000;
	if (normalized.includes('aleado')) return 7850;

	return DENSIDAD_ACERO;
};

export const calculateShellWeight = (vessel: VesselWeightInput) => {
	const {
		type,
		diameter,
		thickness,
		density = DENSIDAD_ACERO,
	} = vessel;

	if (!diameter || !thickness) {
		console.log('[PhysicsUtils][calculateShellWeight][return-empty]', 0);
		return 0;
	}

	const D = diameter / 1000;
	const t = thickness / 1000;
	// Se usa diámetro medio (aprox. de pared delgada) para estimar masa de envolvente metálica.
	const meanDiameter = D + t;
	let weight = 0;

	switch (normalizeVesselType(type)) {
		case 'horizontal': {
			const L = toPositive(vessel.length, 0) / 1000;
				// m = (área lateral cilíndrica) * espesor * densidad.
			weight = Math.PI * meanDiameter * L * t * density;
			break;
		}
		case 'vertical': {
			const H = toPositive(vessel.height, 0) / 1000;
				// Misma base física que horizontal, cambiando longitud por altura de virola.
			weight = Math.PI * meanDiameter * H * t * density;
			break;
		}
		case 'spherical': {
			const meanRadius = meanDiameter / 2;
				// Casco esférico: m = (4πr²) * espesor * densidad.
			weight = 4 * Math.PI * meanRadius ** 2 * t * density;
			break;
		}
		default:
				console.log('[PhysicsUtils][calculateShellWeight][return-unsupported-type]', 0);
				return 0;
	}

	console.log('[PhysicsUtils][calculateShellWeight][return]', weight);
	return weight;
};

export const calculateFluidWeight = (params: {
	type: string;
	diameter: number;
	length?: number;
	height?: number;
	thickness: number;
	corrosionAllowance?: number;
	levelPercent: number;
	specificGravity: number;
}) => {
	const {
		type,
		diameter,
		thickness,
		corrosionAllowance = 0,
		levelPercent,
		specificGravity,
	} = params;
	if (!diameter || !thickness) {
		console.log('[PhysicsUtils][calculateFluidWeight][return-empty]', 0);
		return 0;
	}

	const D_o = diameter / 1000;
	const t = thickness / 1000;
	const c_a = corrosionAllowance / 1000;
	const effectiveThickness = Math.max(t - c_a, 0);
	// Diámetro interno hidráulico disponible para el fluido.
	const D_i = D_o - 2 * effectiveThickness;

	if (D_i <= 0) {
		console.log('[PhysicsUtils][calculateFluidWeight][return-invalid-Di]', 0);
		return 0;
	}

	const normalizedType = normalizeVesselType(type);
	let volume = 0;

	const boundedLevelPercent = Math.min(100, Math.max(0, levelPercent));
	const r = D_i / 2;
	// h es la altura de líquido equivalente dentro de la sección interna.
	const h = Math.min(D_i, Math.max(0, D_i * (boundedLevelPercent / 100)));

	if (normalizedType === 'horizontal') {
		const L = toPositive(params.length, 0) / 1000;
		if (!L || h <= 0) {
			console.log('[PhysicsUtils][calculateFluidWeight][horizontal-empty]', 0);
			return 0;
		}
		if (h >= D_i) {
			const areaCompleta = Math.PI * r ** 2;
			volume = areaCompleta * L;
		} else {
			const cosArg = Math.min(1, Math.max(-1, (r - h) / r));
			const theta = 2 * Math.acos(cosArg);
			// Tanque horizontal parcialmente lleno: área de segmento circular mojado.
			const areaSegmento = (r ** 2 / 2) * (theta - Math.sin(theta));
			volume = areaSegmento * L;
		}
	} else if (normalizedType === 'vertical') {
		const areaInterna = (Math.PI / 4) * D_i ** 2;
		const H = toPositive(params.height, 0) / 1000;
		if (!H || boundedLevelPercent <= 0) {
			console.log('[PhysicsUtils][calculateFluidWeight][vertical-empty]', 0);
			return 0;
		}
		const alturaLiquidoVertical = H * (boundedLevelPercent / 100);
		// En vertical se asume sección constante: V = A * altura de líquido.
		volume = areaInterna * alturaLiquidoVertical;
	} else if (normalizedType === 'spherical') {
		if (h <= 0) {
			console.log('[PhysicsUtils][calculateFluidWeight][spherical-empty]', 0);
			return 0;
		}
		// Esfera parcialmente llena: volumen de casquete esférico.
		volume = (Math.PI * h ** 2 / 3) * (3 * r - h);
	}

	// Convierte volumen a masa usando SG relativa al agua (ρ = 1000 * SG).
	const fluidWeight = volume * (DENSIDAD_AGUA * specificGravity);
	console.log('[PhysicsUtils][calculateFluidWeight][return]', fluidWeight);
	return fluidWeight;
};

export const calculateHeadsWeight = (
	diameter: number,
	thickness: number,
	density: number,
	headType: HeadsType = 'ellipsoidal',
	vesselType?: string,
) => {
	if (!diameter || !thickness || !density) {
		console.log('[PhysicsUtils][calculateHeadsWeight][return-empty]', 0);
		return 0;
	}

	if (normalizeVesselType(String(vesselType ?? '')) === 'spherical') {
		console.log('[PhysicsUtils][calculateHeadsWeight][return-spherical-no-heads]', 0);
		return 0;
	}

	const D = diameter / 1000;
	const t = thickness / 1000;
	let headsWeight = 0;

	if (headType === 'ellipsoidal') {
		// Factor 2.18: aproximación estándar para dos fondos elipsoidales 2:1.
		headsWeight = 2.18 * D ** 2 * t * density;
	} else if (headType === 'hemispherical') {
		// Dos hemisferios equivalen al área de una esfera completa: πD².
		headsWeight = Math.PI * D ** 2 * t * density;
	}

	console.log('[PhysicsUtils][calculateHeadsWeight][return]', headsWeight);
	return headsWeight;
};

const computeEquipmentWeights = (params: {
	vesselType: string;
	outerDiameter: number;
	wallThickness: number;
	corrosionAllowance?: number;
	length?: number;
	height?: number;
	liquidLevelPercent: number;
	fluidSpecificGravity: number;
	materialDensity: number;
	headType?: HeadsType;
}): PesosEquipo => {
	const {
		vesselType,
		outerDiameter,
		wallThickness,
		corrosionAllowance = 0,
		length,
		height,
		liquidLevelPercent,
		fluidSpecificGravity,
		materialDensity,
		headType = 'ellipsoidal',
	} = params;

	if (!outerDiameter || !wallThickness) {
		const result = { pesoVacio_kN: 0, pesoFluido_kN: 0, pesoOperativo_kN: 0 };
		console.log('[PhysicsUtils][computeEquipmentWeights][return-empty]', result);
		return result;
	}

	const normalizedType = normalizeVesselType(vesselType);

	// Masa estructural principal del cuerpo del recipiente.
	const masaShell_kg = calculateShellWeight({
		type: vesselType,
		diameter: outerDiameter,
		thickness: wallThickness,
		length,
		height,
		density: materialDensity,
	});
	// En recipientes esféricos no se suman cabezales porque la geometría ya es cerrada.
	const masaHeads_kg = normalizedType === 'spherical'
		? 0
		: calculateHeadsWeight(
			outerDiameter,
			wallThickness,
			materialDensity,
			headType,
			vesselType,
		);
	// Ajustes de ingeniería: internos + mayoración por accesorios/contingencias de fabricación.
	const masaInternals_kg = masaShell_kg * FACTOR_INTERNOS;
	const masaVacia_kg =
		(masaShell_kg + masaHeads_kg + masaInternals_kg) *
		FACTOR_MAYORACION_ACERO;
	// Carga de operación por inventario de fluido en el nivel especificado.
	const masaFluido_kg = calculateFluidWeight({
		type: vesselType,
		diameter: outerDiameter,
		length,
		height,
		thickness: wallThickness,
		corrosionAllowance,
		levelPercent: liquidLevelPercent,
		specificGravity: fluidSpecificGravity,
	});

	// Conversión final de masa a peso: W = m·g.
	const pesoVacio_kN = (masaVacia_kg * g) / 1000;
	const pesoFluido_kN = (masaFluido_kg * g) / 1000;
	const pesoOperativo_kN = pesoVacio_kN + pesoFluido_kN;

	const result = {
		pesoVacio_kN: Number(pesoVacio_kN.toFixed(2)),
		pesoFluido_kN: Number(pesoFluido_kN.toFixed(2)),
		pesoOperativo_kN: Number(pesoOperativo_kN.toFixed(2)),
	};
	console.log('[PhysicsUtils][computeEquipmentWeights][return]', result);
	return result;
};

/**
 * FUNCIÓN: calcularPesosDelEquipo
 * Esquema Híbrido: Cálculo Ligero / On-Change
 *
 * Esta función está diseñada para ejecutarse con onBlur o debounce.
 * Devuelve pesos estimados en kN a partir de geometría y nivel de fluido.
 */
export const calcularPesosDelEquipo = (
	diametroExt_mm: number,
	longitud_mm: number,
	espesor_mm: number,
	nivelLiquido_pct: number,
	gravedadEspecifica: number,
	vesselType: string = 'horizontal',
	altura_mm = 0,
	density: number = DENSIDAD_ACERO,
	headType: HeadsType = 'ellipsoidal',
): PesosEquipo => {
	const result = computeEquipmentWeights({
		vesselType,
		outerDiameter: diametroExt_mm,
		wallThickness: espesor_mm,
		length: longitud_mm,
		height: altura_mm,
		liquidLevelPercent: nivelLiquido_pct,
		fluidSpecificGravity: gravedadEspecifica,
		materialDensity: density,
		headType,
	});
	console.log('[PhysicsUtils][calcularPesosDelEquipo][return]', result);
	return result;
};

export const calculateEquipmentWeightsFromInputs = (
	input: DesignInputs,
): PesosEquipo => {
	const vesselType = String(input.vesselType ?? input.orientation ?? '');
	const outerDiameter = toPositive(input.outerDiameter, 0);
	const wallThickness = toPositive(input.wallThickness, 0);
	const corrosionAllowance = toPositive(input.corrosionAllowance, 0);
	const length = toPositive(input.length, 0);
	const height = toPositive(input.height, 0);
	const liquidLevelPercent = toPositive(input.liquidLevelPercent, 100);
	const fluidSpecificGravity = toPositive(input.fluidSpecificGravity, 1);
	const materialDensity = getMaterialDensity(String(input.vesselMaterial ?? ''));
	const headType = String(input.headType ?? 'ellipsoidal').toLowerCase() === 'hemispherical'
		? 'hemispherical'
		: 'ellipsoidal';

	const result = computeEquipmentWeights({
		vesselType,
		outerDiameter,
		wallThickness,
		corrosionAllowance,
		length,
		height,
		liquidLevelPercent,
		fluidSpecificGravity,
		materialDensity,
		headType,
	});
	console.log('[PhysicsUtils][calculateEquipmentWeightsFromInputs][return]', result);
	return result;
};

/**
 * FUNCIÓN: calculateCenterOfGravity
 * Determina la ubicación del Centro de Gravedad (CG) respecto a la línea tangente (Datum).
 * - Horizontal: CG longitudinal (eje X) desde tangente izquierda.
 * - Vertical: CG de elevación (eje Z) desde tangente inferior.
 * - Esférico: CG de elevación (eje Z) desde el polo inferior.
 */
export const calculateCenterOfGravity = (params: {
	vesselType: string;
	outerDiameter: number;
	length?: number;
	height?: number;
	liquidLevelPercent: number;
	pesos: PesosEquipo;
}): CentroGravedad => {
	const { vesselType, outerDiameter, liquidLevelPercent, pesos } = params;
	const normalizedType = normalizeVesselType(vesselType);

	const D = toPositive(outerDiameter, 0);
	const L = toPositive(params.length, 0);
	const H = toPositive(params.height, 0);

	let cgVacio = 0;
	let cgFluido = 0;

	// Validación de seguridad para evitar divisiones por cero si no hay masa calculada.
	if (pesos.pesoOperativo_kN <= 0) {
		return { cgVacio_mm: 0, cgFluido_mm: 0, cgOperativo_mm: 0 };
	}

	switch (normalizedType) {
		case 'horizontal':
			// Para equipos simétricos, el CG longitudinal (X) se asume en el centro geométrico.
			cgVacio = L / 2;
			cgFluido = L / 2;
			break;

		case 'vertical':
			// CG de elevación (Z): El cuerpo vacío se asume uniforme (H/2).
			cgVacio = H / 2;
			const alturaLiquidoVertical = H * (Math.min(100, Math.max(0, liquidLevelPercent)) / 100);
			// El centroide de un cilindro de fluido está a la mitad de su altura de llenado.
			cgFluido = alturaLiquidoVertical / 2;
			break;

		case 'spherical':
			// El CG de la cáscara vacía está en el centro radial (D/2).
			cgVacio = D / 2;
			const r = D / 2;
			const h_f = D * (Math.min(100, Math.max(0, liquidLevelPercent)) / 100);

			if (h_f <= 0) {
				cgFluido = 0;
			} else {
				// Centroide de un casquete esférico de altura h_f:
				// Distancia desde el centro de la esfera: y = 3(2r-h)^2 / 4(3r-h) [aproximación]
				// Usando expresión de elevación del centroide desde la base (polo inferior).
				cgFluido = (3 * Math.pow(2 * r - h_f, 2)) / (4 * (3 * r - h_f));
			}
			break;

		default:
			return { cgVacio_mm: 0, cgFluido_mm: 0, cgOperativo_mm: 0 };
	}

	// Ponderación de momentos estáticos: CG_total = Σ(W_i * d_i) / ΣW_i
	const momentoVacio = pesos.pesoVacio_kN * cgVacio;
	const momentoFluido = pesos.pesoFluido_kN * cgFluido;
	const cgOperativo = (momentoVacio + momentoFluido) / pesos.pesoOperativo_kN;

	const result = {
		cgVacio_mm: Number(cgVacio.toFixed(2)),
		cgFluido_mm: Number(cgFluido.toFixed(2)),
		cgOperativo_mm: Number(cgOperativo.toFixed(2)),
	};
	console.log('[PhysicsUtils][calculateCenterOfGravity][return]', result);
	return result;
};

export const toNumber = (value: unknown, fallback = 0) => {
	const numeric = Number(value);
	return Number.isFinite(numeric) ? numeric : fallback;
};

export const toPositive = (value: unknown, fallback = 0) => {
	const numeric = toNumber(value, fallback);
	return numeric >= 0 ? numeric : fallback;
};

export const convertLength = (
	value: number,
	from: UnitSystem,
	to: UnitSystem,
) => {
	if (from === to) return value;
	return to === 'US' ? value / 25.4 : value * 25.4;
};

export const convertPressure = (
	value: number,
	from: UnitSystem,
	to: UnitSystem,
) => {
	if (from === to) return value;
	return to === 'US' ? value * 145.037738 : value / 145.037738;
};

/**
 * Objetivo: ejecutar el cálculo físico lightweight del wizard.
 * Entradas: `DesignInputs` del formulario y sistema de unidades de entrada.
 * Salida: `LightweightResults` con derivados físicos y advertencias de ingeniería.
 * Norma/Criterio: normaliza a SI internamente y consolida cargas viento/sismo + módulos de soporte.
 */
export const computeLightweightResults = (
	input: DesignInputs,
	unitSystem: UnitSystem = 'SI',
): LightweightResults => {
	const sourceUnitSystem =
		String(input.unitSystem ?? unitSystem).toUpperCase() === 'US' ? 'US' : 'SI';

	const outerDiameter = convertLength(
		toPositive(input.outerDiameter, 0),
		sourceUnitSystem,
		'SI',
	);
	const wallThickness = convertLength(
		toPositive(input.wallThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const corrosionAllowance = convertLength(
		toPositive(input.corrosionAllowance, 0),
		sourceUnitSystem,
		'SI',
	);
	const insulationThickness = convertLength(
		toPositive(input.insulationThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const designPressure = convertPressure(
		toPositive(input.designPressure, 0),
		sourceUnitSystem,
		'SI',
	);
	const length = convertLength(
		toPositive(input.length, 0),
		sourceUnitSystem,
		'SI',
	);
	const height = convertLength(
		toPositive(input.height, 0),
		sourceUnitSystem,
		'SI',
	);
	const clearance = convertLength(
		toPositive(
		input.clearance ?? input.clearance_mm ?? input.saddleHeight ?? input.skirtHeight,
		0,
		),
		sourceUnitSystem,
		'SI',
	);
	const liquidLevelPercent = toPositive(input.liquidLevelPercent, 100);
	const fluidSpecificGravity = toPositive(input.fluidSpecificGravity, 1);
	const vesselType = String(input.vesselType ?? input.orientation ?? '');
	const windSpeed_kmh = toPositive(input.windSpeed ?? input.windSpeed_kmh, 0);
	const windPressureRaw = toPositive(
		input.windPressure ?? input.windPressure_kPa ?? input.windValue,
		0,
	);
	const windPressure_kPa =
		sourceUnitSystem === 'US' ? windPressureRaw * 6.894757 : windPressureRaw;
	const windImportanceFactor = toPositive(input.windImportanceFactor, 1);
	const windDesignCode = resolveWindDesignCode(
		input.windDesignCode ?? input.designCode,
	);
	const designCode = String(input.designCode ?? 'ASME/ASCE');
	const jointEfficiencyRaw = String(
		input.jointEfficiency ?? input.weldEfficiency ?? input.eficienciaSoldadura ?? '1.0',
	);
	const jointEfficiency = Number.parseFloat(jointEfficiencyRaw.split(' ')[0]) || 1;
	const normalizedVesselType = normalizeVesselType(vesselType);
	const normalizedInput: DesignInputs = {
		...input,
		vesselType,
		orientation: vesselType,
		outerDiameter,
		wallThickness,
		corrosionAllowance,
		insulationThickness,
		length,
		height,
		liquidLevelPercent,
		fluidSpecificGravity,
	};

	const equipmentWeights = calculateEquipmentWeightsFromInputs(normalizedInput);

	const representativeLength_mm =
		normalizedVesselType === 'horizontal'
			? length
			: normalizedVesselType === 'vertical'
				? height
				: outerDiameter;
	const outerRadius_m = outerDiameter / 2000;
	const insulatedOuterRadius_m = outerRadius_m + insulationThickness / 1000;
	const shellLength_m = representativeLength_mm / 1000;
	const insulationVolume_m3 =
		insulationThickness > 0 && shellLength_m > 0
			? Math.PI * (insulatedOuterRadius_m ** 2 - outerRadius_m ** 2) * shellLength_m
			: 0;
	const insulationWeight_kN = (insulationVolume_m3 * DENSIDAD_AISLAMIENTO * g) / 1000;

	equipmentWeights.pesoVacio_kN = Number(
		(equipmentWeights.pesoVacio_kN + insulationWeight_kN).toFixed(2),
	);
	equipmentWeights.pesoOperativo_kN = Number(
		(equipmentWeights.pesoOperativo_kN + insulationWeight_kN).toFixed(2),
	);

	const windLoads = calculateWindLoads({
		vesselType,
		diameter_mm: outerDiameter,
		length_mm: length,
		height_mm: height,
		clearance_mm: clearance,
		insulation_mm: insulationThickness,
		importanceFactor: windImportanceFactor,
		windSpeed_kmh,
		windPressure_kPa,
		designCode: windDesignCode,
	});
	const cgs = calculateCenterOfGravity({
		vesselType,
		outerDiameter,
		length,
		height,
		liquidLevelPercent,
		pesos: equipmentWeights,
	});
	const seismicLoads = calculateSeismicLoads({
		pesoOperativo_kN: equipmentWeights.pesoOperativo_kN,
		cgOperativo_mm: cgs.cgOperativo_mm,
		clearance_mm: clearance,
		designCode,
		coeficienteSismico_Cs: toPositive(
			input.seismicCoefficient ?? input.seismicCoefficient_Cs,
			0,
		),
		seismicSiteClass: String(input.seismicSiteClass ?? 'D'),
		seismicSs: toPositive(input.seismicSs, 0.5),
		seismicS1: toPositive(input.seismicS1, 0.2),
		seismicR: toPositive(input.seismicR ?? input.covenR, 3),
		covenState: String(input.covenState ?? ''),
		covenSoilType: String(input.covenSoilType ?? 'S1'),
		covenImportanceGroup: String(input.covenImportanceGroup ?? 'B2'),
		covenR: toPositive(input.covenR ?? input.seismicR, 3),
	});

	const momentoGobernante_kNm = Math.max(
		windLoads.momentoVolcamiento_kNm,
		seismicLoads.momentoVolcamiento_kNm,
	);
	const fuerzaCorteGobernante_kN = Math.max(
		windLoads.fuerzaCorteBase_kN,
		seismicLoads.fuerzaCorteBasal_kN,
	);
	const cargaGobernante =
		momentoGobernante_kNm <= 0
			? 'NINGUNA'
			: windLoads.momentoVolcamiento_kNm >= seismicLoads.momentoVolcamiento_kNm
				? 'VIENTO'
				: 'SISMO';
	const numberOfLegs = toPositive(
		input.numberOfLegs ?? input.numLegs ?? input.legQuantity,
		4,
	);
	const pitchDiameter_mm = convertLength(
		toPositive(
			input.pitchDiameter ??
				input.pitchDiameter_mm ??
				input.boltCircleDiameter ??
				input.legBoltCircle,
			0,
		),
		sourceUnitSystem,
		'SI',
	);
	const legSpacing_mm = convertLength(
		toPositive(input.legSpacing_mm ?? input.legSpacing ?? input.legLongSpacing, 0),
		sourceUnitSystem,
		'SI',
	);
	const legWidth_mm = convertLength(
		toPositive(input.legWidth_mm ?? input.legWidth ?? input.legTransSpacing, 0),
		sourceUnitSystem,
		'SI',
	);
	const legReactions = calculateLegReactions({
		vesselType,
		pesoOperativo_kN: equipmentWeights.pesoOperativo_kN,
		momentoGobernante_kNm,
		fuerzaCorteGobernante_kN,
		vesselDiameter_mm: outerDiameter,
		numberOfLegs,
		pitchDiameter_mm,
		legSpacing_mm,
		legWidth_mm,
	});
	const saddleLocation_mm = convertLength(
		toPositive(input.saddleLocation, length * 0.2),
		sourceUnitSystem,
		'SI',
	);
	const saddleWebThickness_mm = convertLength(
		toPositive(input.saddleWebThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const saddleBasePlateWidth_mm = convertLength(
		toPositive(input.saddleBasePlateWidth, 0),
		sourceUnitSystem,
		'SI',
	);
	const saddleBasePlateLength_mm = convertLength(
		toPositive(input.saddleBasePlateLength, 0),
		sourceUnitSystem,
		'SI',
	);
	const wearPlateThickness_mm = convertLength(
		toPositive(input.wearPlateThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const saddleRibCount = toPositive(input.saddleRibCount, 3);
	const saddleRibThickness_mm = convertLength(
		toPositive(input.saddleRibThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const wearPlateEnabled = String(input.wearPlateEnabled) === 'true';
	const saddleReactions = calculateSaddleReactions({
		pesoOperativo_kN: equipmentWeights.pesoOperativo_kN,
		fuerzaCorteGobernante_kN,
		vesselDiameter_mm: outerDiameter,
		vesselLength_mm: length,
		vesselThickness_mm: wallThickness,
		saddleLocation_mm,
		saddleContactAngle: String(input.saddleContactAngle ?? '120'),
		saddleWebThickness_mm,
		saddleBasePlateWidth_mm,
		saddleBasePlateLength_mm,
		saddleFrictionType: String(input.saddleFrictionType ?? 'Sin fricción'),
		wearPlateEnabled,
		wearPlateThickness_mm,
		saddleRibCount,
		saddleRibThickness_mm,
	});
	const skirtGeometry = String(input.skirtGeometry ?? 'cylindrical');
	const skirtHeight_mm = convertLength(
		toPositive(input.skirtHeight, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtThickness_mm = convertLength(
		toPositive(input.skirtThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtBaseDiameter_mm = convertLength(
		toPositive(input.skirtBaseDiameter, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtTopDiameter_mm = convertLength(
		toPositive(input.skirtTopDiameter, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtAccessHoleDiameter_mm = convertLength(
		toPositive(input.skirtAccessHoleDiameter, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtRingID_mm = convertLength(
		toPositive(input.skirtRingID, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtRingOD_mm = convertLength(
		toPositive(input.skirtRingOD, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtRingThickness_mm = convertLength(
		toPositive(input.skirtRingThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtBoltCircleDiameter_mm = convertLength(
		toPositive(input.skirtBoltCircleDiameter, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtAnchorChairs = String(input.skirtAnchorChairs) === 'true';
	const skirtChairHeight_mm = convertLength(
		toPositive(input.skirtChairHeight, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtChairTopPlateWidth_mm = convertLength(
		toPositive(input.skirtChairTopPlateWidth, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtChairTopPlateThickness_mm = convertLength(
		toPositive(input.skirtChairTopPlateThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const skirtAnchorBoltCount = toPositive(
		input.skirtAnchorBoltCount ?? input.boltQuantity,
		0,
	);
	const skirtReactions = calculateSkirtReactions({
		pesoOperativo_kN: equipmentWeights.pesoOperativo_kN,
		momentoGobernante_kNm,
		vesselDiameter_mm: outerDiameter,
		skirtGeometry,
		skirtHeight_mm,
		skirtThickness_mm,
		skirtBaseDiameter_mm,
		skirtTopDiameter_mm,
		skirtAccessHoleDiameter_mm,
		skirtRingID_mm,
		skirtRingOD_mm,
		skirtRingThickness_mm,
		skirtBoltCircleDiameter_mm,
		skirtAnchorBoltCount,
		skirtAnchorChairs,
		skirtChairHeight_mm,
		skirtChairTopPlateWidth_mm,
		skirtChairTopPlateThickness_mm,
	});
	const lugQuantity = toPositive(input.lugQuantity, 2);
	const lugElevation_mm = convertLength(
		toPositive(input.lugElevation, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugWidth_mm = convertLength(
		toPositive(input.lugWidth, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugLength_mm = convertLength(
		toPositive(input.lugLength, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugThickness_mm = convertLength(
		toPositive(input.lugThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugEccentricity_mm = convertLength(
		toPositive(input.lugEccentricity, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugHoleDiameter_mm = convertLength(
		toPositive(input.lugHoleDiameter, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugGusset =
		input.lugGusset === true || String(input.lugGusset).toLowerCase() === 'true';
	const lugGussetThickness_mm = convertLength(
		toPositive(input.lugGussetThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugPadPlate =
		input.lugPadPlate === true || String(input.lugPadPlate).toLowerCase() === 'true';
	const lugPadWidth_mm = convertLength(
		toPositive(input.lugPadWidth, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugPadLength_mm = convertLength(
		toPositive(input.lugPadLength, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugPadThickness_mm = convertLength(
		toPositive(input.lugPadThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const lugReactions = calculateLugReactions({
		pesoOperativo_kN: equipmentWeights.pesoOperativo_kN,
		momentoGobernante_kNm,
		vesselDiameter_mm: outerDiameter,
		lugQuantity,
		lugElevation_mm,
		lugWidth_mm,
		lugLength_mm,
		lugThickness_mm,
		lugEccentricity_mm,
		lugHoleDiameter_mm,
		lugGusset,
		lugGussetThickness_mm,
		lugPadPlate,
		lugPadWidth_mm,
		lugPadLength_mm,
		lugPadThickness_mm,
	});
	const ringProfile = String(input.ringProfile ?? 'Barra');
	const ringWebHeight_mm = convertLength(
		toPositive(input.ringWebHeight, 0),
		sourceUnitSystem,
		'SI',
	);
	const ringWebThickness_mm = convertLength(
		toPositive(input.ringWebThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const ringFlangeWidth_mm = convertLength(
		toPositive(input.ringFlangeWidth, 0),
		sourceUnitSystem,
		'SI',
	);
	const ringFlangeThickness_mm = convertLength(
		toPositive(input.ringFlangeThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const ringBasePlateWidth_mm = convertLength(
		toPositive(input.ringBasePlateWidth, 0),
		sourceUnitSystem,
		'SI',
	);
	const ringBasePlateLength_mm = convertLength(
		toPositive(input.ringBasePlateLength, 0),
		sourceUnitSystem,
		'SI',
	);
	const ringGussets =
		input.ringGussets === true ||
		String(input.ringGussets).toLowerCase() === 'true';
	const ringGussetQty = toPositive(input.ringGussetQty, 4);
	const ringGussetThickness_mm = convertLength(
		toPositive(input.ringGussetThickness, 0),
		sourceUnitSystem,
		'SI',
	);
	const ringGussetWidth_mm = convertLength(
		toPositive(input.ringGussetWidth, 0),
		sourceUnitSystem,
		'SI',
	);
	const ringReactions = calculateRingReactions({
		pesoOperativo_kN: equipmentWeights.pesoOperativo_kN,
		vesselDiameter_mm: outerDiameter,
		ringProfile,
		ringWebHeight_mm,
		ringWebThickness_mm,
		ringFlangeWidth_mm,
		ringFlangeThickness_mm,
		ringBasePlateWidth_mm,
		ringBasePlateLength_mm,
		ringGussets,
		ringGussetQty,
		ringGussetThickness_mm,
		ringGussetWidth_mm,
	});

	let tensionPorPerno_kN = 0;
	let cortePorPerno_kN = 0;
	const supportType = String(input.supportType ?? '');
	const boltQuantity = Math.max(
		1,
		toPositive(
			input.boltQuantity ?? input.anchorBoltQuantity ?? input.skirtAnchorBoltCount,
			4,
		),
	);

	if (/skirt|fald[oó]n/i.test(supportType)) {
		tensionPorPerno_kN = skirtReactions.tensionMaxPerno_kN;
		cortePorPerno_kN = fuerzaCorteGobernante_kN / boltQuantity;
	} else if (/leg|pata/i.test(supportType)) {
		tensionPorPerno_kN = Math.max(0, -legReactions.tensionMaxima_kN);
		cortePorPerno_kN = legReactions.cortePorPata_kN;
	} else if (/saddle|silleta/i.test(supportType)) {
		tensionPorPerno_kN = 0;
		const denominator = Math.max(1, boltQuantity / 2);
		cortePorPerno_kN =
			Math.max(
				saddleReactions.cargaLongitudinalFija_kN,
				saddleReactions.cargaTransversal_kN,
			) / denominator;
	}

	const anchorReactions = calculateAnchorReactions({
		tensionPorPerno_kN,
		cortePorPerno_kN,
		boltQuantity,
		boltDiameter_mm: convertLength(
			toPositive(
				input.boltDiameter ??
					input.anchorBoltDiameter ??
					input.legBoltDiameter ??
					input.skirtAnchorBoltDiameter,
				0,
			),
			sourceUnitSystem,
			'SI',
		),
		boltMaterial: String(input.boltMaterial ?? 'Acero al carbono'),
		embedmentDepth_mm: convertLength(
			toPositive(input.embedmentDepth, 0),
			sourceUnitSystem,
			'SI',
		),
		concreteStrength_MPa: convertPressure(
			toPositive(input.concreteStrength, 21),
			sourceUnitSystem,
			'SI',
		),
		anchorType: String(input.anchorType ?? ''),
		anchorEdgeDistance_mm: convertLength(
			toPositive(input.anchorEdgeDistance, 0),
			sourceUnitSystem,
			'SI',
		),
	});

	const warnings: string[] = [];
	const displayUnitSystem = sourceUnitSystem;
	const stressUnit = displayUnitSystem === 'US' ? 'psi' : 'MPa';
	const lengthUnit = displayUnitSystem === 'US' ? 'in' : 'mm';
	const toDisplayStress = (valueMPa: number) =>
		displayUnitSystem === 'US' ? valueMPa * 145.037738 : valueMPa;
	const toDisplayLength = (valueMm: number) =>
		displayUnitSystem === 'US' ? valueMm / 25.4 : valueMm;
	const fmt = (value: number, digits = 2) =>
		Number.isFinite(value) ? value.toFixed(digits) : '-';

	if (outerDiameter > 0 && wallThickness > 0 && wallThickness * 2 > outerDiameter) {
		warnings.push('El espesor de pared supera el diámetro exterior disponible.');
	}

	if (
		normalizedVesselType === 'vertical' &&
		height > 0 &&
		outerDiameter > 0 &&
		height / outerDiameter > 15
	) {
		warnings.push('Relación de esbeltez (H/D) > 15. Se recomienda análisis dinámico de viento (Vortex Shedding).');
	}

	if (legReactions.alertaLevantamiento) {
		warnings.push('¡ALERTA!: El momento de volcamiento supera la carga muerta. Las patas a barlovento entrarán en tensión. Se requiere diseño riguroso de pernos de anclaje (Anchor Bolts).');
	}

	if (saddleReactions.alertaCuerno && normalizedVesselType === 'horizontal') {
		warnings.push(
			`¡ALERTA!: El esfuerzo en el cuerno de la silleta (${fmt(toDisplayStress(saddleReactions.esfuerzoCuerno_MPa))} ${stressUnit}) excede valores típicos. Considere ángulo de contacto 150° o añadir una Placa de Desgaste (Wear Plate).`,
		);
	}

	if (saddleReactions.alertaFlexion && normalizedVesselType === 'horizontal') {
		warnings.push('¡ALERTA!: Alto esfuerzo de flexión longitudinal. Mueva las silletas más cerca del 20% de la longitud del equipo (A ≈ 0.2*L).');
	}

	if (saddleReactions.alertaSilleta && normalizedVesselType === 'horizontal') {
		warnings.push(
			`¡ALERTA!: La silleta de soporte está sobre-esforzada a compresión (${fmt(toDisplayStress(saddleReactions.esfuerzoCompresionSilleta_MPa))} ${stressUnit}). Aumente el espesor del alma, agregue más costillas o incremente el espesor de las costillas.`,
		);
	}

	if (
		skirtReactions.alertaLevantamientoFaldon &&
		(/^skirt/i.test(String(input.supportType ?? '')) ||
			normalizedVesselType === 'vertical')
	) {
		warnings.push('¡ALERTA!: Momento de volcamiento severo en el Faldón. Se requiere diseño de pernos de anclaje a tracción.');
	}

	if (skirtReactions.alertaAgujeroAcceso) {
		warnings.push('El agujero de acceso (Manhole) es mayor a 1/3 del diámetro del faldón. Se requiere un análisis de refuerzo local alrededor de la apertura.');
	}

	if (skirtReactions.alertaSillaAnclaje && /^skirt/i.test(String(input.supportType ?? ''))) {
		warnings.push(
			`¡ALERTA!: La placa superior de la silla de anclaje se doblará por la tracción del perno (esfuerzo ≈ ${fmt(toDisplayStress(skirtReactions.esfuerzoPlacaSilla_MPa))} ${stressUnit}). Aumente el espesor de la placa superior (Top Plate).`,
		);
	}

	if (lugReactions.alertaFlexionMensula && /^lug/i.test(String(input.supportType ?? ''))) {
		warnings.push(
			`¡ALERTA!: Esfuerzo de flexión excesivo en la ménsula (${fmt(toDisplayStress(lugReactions.esfuerzoFlexionMensula_MPa))} ${stressUnit}). Aumente el espesor o active el uso de Refuerzos (Gussets).`,
		);
	}

	if (lugReactions.alertaFaltaPlaca && /^lug/i.test(String(input.supportType ?? ''))) {
		warnings.push('Recomendación: Debido a la alta carga transferida, se recomienda activar el uso de una Placa de Apoyo (Pad Plate) para no desgarrar la pared del recipiente.');
	}

	if (ringReactions.alertaFlexion && /^ring/i.test(String(input.supportType ?? ''))) {
		warnings.push(
			`¡ALERTA!: El anillo está fallando por flexión (${fmt(toDisplayStress(ringReactions.esfuerzoFlexionAnillo_MPa))} ${stressUnit}). Cambie el perfil de "Barra" a "Viga I" o "Sección T" para aumentar la inercia, o incremente las dimensiones del alma/brida.`,
		);
	}

	if (ringReactions.alertaPresionBase && /^ring/i.test(String(input.supportType ?? ''))) {
		warnings.push(
			`¡ALERTA!: La presión en la placa base del anillo (${fmt(toDisplayStress(ringReactions.presionPlacaBase_MPa))} ${stressUnit}) supera los límites del concreto/acero de soporte. Aumente el ancho o largo de la placa base.`,
		);
	}

	if (anchorReactions.alertaAcero) {
		warnings.push(
			`¡ALERTA DE ANCLAJE!: Los pernos fallarán por cizalladura o tracción (ratio acero = ${fmt(anchorReactions.ratioInteraccionAcero, 3)}). Aumente el diámetro (${lengthUnit}), la cantidad o cambie a un material de mayor resistencia (ej. A325).`,
		);
	}

	if (anchorReactions.alertaConcreto) {
		warnings.push(
			`¡ALERTA DE FUNDACIÓN!: Falla por desprendimiento de concreto (Breakout) (ratio concreto = ${fmt(anchorReactions.ratioConcreto, 3)}). Aumente la profundidad de anclaje (${lengthUnit}) o la resistencia del concreto (${stressUnit}).`,
		);
	}

	if (anchorReactions.alertaBorde) {
		warnings.push(
			`Nota: La cercanía del perno al borde de la fundación está reduciendo severamente su capacidad de carga (borde = ${fmt(toDisplayLength(convertLength(toPositive(input.anchorEdgeDistance, 0), sourceUnitSystem, 'SI')))} ${lengthUnit}).`,
		);
	}

	const result: LightweightResults = {
		status: 'ready',
		derived: {
			// D/t permite inferir esbeltez local y sensibilidad a inestabilidad/abolladura.
			diameterToThicknessRatio:
				wallThickness > 0 ? outerDiameter / wallThickness : 0,
			// Indicador rápido de severidad de presión respecto al tamaño del equipo.
			pressureTimesDiameter: designPressure * outerDiameter,
			windIndicator: windSpeed_kmh || windPressure_kPa,
			pesoVacio_kN: equipmentWeights.pesoVacio_kN,
			pesoFluido_kN: equipmentWeights.pesoFluido_kN,
			pesoOperativo_kN: equipmentWeights.pesoOperativo_kN,
			corrosionAllowance_mm: corrosionAllowance,
			jointEfficiency,
			cgVacio_mm: cgs.cgVacio_mm,
			cgFluido_mm: cgs.cgFluido_mm,
			cgOperativo_mm: cgs.cgOperativo_mm,
			presionDinamicaBase_kPa: windLoads.presionDinamicaBase_kPa,
			areaProyectada_m2: windLoads.areaProyectada_m2,
			fuerzaCorteBase_kN: windLoads.fuerzaCorteBase_kN,
			brazoPalanca_m: windLoads.brazoPalanca_m,
			momentoVolcamiento_kNm: windLoads.momentoVolcamiento_kNm,
			viento_fuerzaCorteBase_kN: windLoads.fuerzaCorteBase_kN,
			viento_brazoPalanca_m: windLoads.brazoPalanca_m,
			viento_momentoVolcamiento_kNm: windLoads.momentoVolcamiento_kNm,
			codigoVientoAplicado: windLoads.codigoAplicado,
			sismo_fuerzaCorteBasal_kN: seismicLoads.fuerzaCorteBasal_kN,
			sismo_momentoVolcamiento_kNm: seismicLoads.momentoVolcamiento_kNm,
			coeficienteSismico_Cs: seismicLoads.coeficienteSismico_Cs,
			cargaGobernante_Ambiental: cargaGobernante,
			momentoGobernante_kNm,
			fuerzaCorteGobernante_kN,
			leg_cargaVerticalBase_kN: legReactions.cargaVerticalBase_kN,
			leg_cargaPorMomento_kN: legReactions.cargaPorMomento_kN,
			leg_compresionMaxima_kN: legReactions.compresionMaxima_kN,
			leg_tensionMaxima_kN: legReactions.tensionMaxima_kN,
			leg_cortePorPata_kN: legReactions.cortePorPata_kN,
			leg_alertaLevantamiento: legReactions.alertaLevantamiento,
			saddle_cargaVerticalPorSilleta_kN: saddleReactions.cargaVerticalPorSilleta_kN,
			saddle_cargaLongitudinalFija_kN: saddleReactions.cargaLongitudinalFija_kN,
			saddle_cargaTransversal_kN: saddleReactions.cargaTransversal_kN,
			saddle_esfuerzoCuerno_MPa: saddleReactions.esfuerzoCuerno_MPa,
			saddle_compresionPlacaBase_MPa: saddleReactions.compresionPlacaBase_MPa,
			saddle_esfuerzoFlexionSilleta_MPa: saddleReactions.esfuerzoFlexionSilleta_MPa,
			saddle_esfuerzoFlexionCentro_MPa: saddleReactions.esfuerzoFlexionCentro_MPa,
			saddle_esfuerzoCompresionSilleta_MPa:
				saddleReactions.esfuerzoCompresionSilleta_MPa,
			saddle_alertaCuerno: saddleReactions.alertaCuerno,
			saddle_alertaFlexion: saddleReactions.alertaFlexion,
			saddle_alertaSilleta: saddleReactions.alertaSilleta,
			skirt_esfuerzoCompresionFaldon_MPa:
				skirtReactions.esfuerzoCompresionFaldon_MPa,
			skirt_esfuerzoTensionFaldon_MPa:
				skirtReactions.esfuerzoTensionFaldon_MPa,
			skirt_presionConcreto_MPa: skirtReactions.presionConcreto_MPa,
			skirt_tensionMaxPerno_kN: skirtReactions.tensionMaxPerno_kN,
			skirt_esfuerzoPlacaSilla_MPa: skirtReactions.esfuerzoPlacaSilla_MPa,
			skirt_alertaPandeoFaldon: skirtReactions.alertaPandeoFaldon,
			skirt_alertaLevantamientoFaldon:
				skirtReactions.alertaLevantamientoFaldon,
			skirt_alertaAgujeroAcceso: skirtReactions.alertaAgujeroAcceso,
			skirt_alertaSillaAnclaje: skirtReactions.alertaSillaAnclaje,
			lug_cargaMaxPorMensula_kN: lugReactions.cargaMaxPorMensula_kN,
			lug_esfuerzoFlexionMensula_MPa: lugReactions.esfuerzoFlexionMensula_MPa,
			lug_esfuerzoCorteMensula_MPa: lugReactions.esfuerzoCorteMensula_MPa,
			lug_presionPlacaApoyo_MPa: lugReactions.presionPlacaApoyo_MPa,
			lug_alertaFlexionMensula: lugReactions.alertaFlexionMensula,
			lug_alertaFaltaPlaca: lugReactions.alertaFaltaPlaca,
			ring_areaSeccion_mm2: ringReactions.areaSeccion_mm2,
			ring_moduloSeccion_mm3: ringReactions.moduloSeccion_mm3,
			ring_esfuerzoFlexionAnillo_MPa: ringReactions.esfuerzoFlexionAnillo_MPa,
			ring_esfuerzoCorteAnillo_MPa: ringReactions.esfuerzoCorteAnillo_MPa,
			ring_presionPlacaBase_MPa: ringReactions.presionPlacaBase_MPa,
			ring_alertaFlexion: ringReactions.alertaFlexion,
			ring_alertaPresionBase: ringReactions.alertaPresionBase,
			anchor_ratioInteraccionAcero: anchorReactions.ratioInteraccionAcero,
			anchor_ratioConcreto: anchorReactions.ratioConcreto,
			anchor_alertaAcero: anchorReactions.alertaAcero,
			anchor_alertaConcreto: anchorReactions.alertaConcreto,
			anchor_alertaBorde: anchorReactions.alertaBorde,
		},
		warnings,
	};

	console.log('[PhysicsUtils][computeLightweightResults][summary]', {
		sourceUnitSystem,
		pesoOperativo_kN: result.derived.pesoOperativo_kN,
		corrosionAllowance_mm: result.derived.corrosionAllowance_mm,
		jointEfficiency: result.derived.jointEfficiency,
		cgOperativo_mm: result.derived.cgOperativo_mm,
		viento_momentoVolcamiento_kNm: result.derived.viento_momentoVolcamiento_kNm,
		sismo_momentoVolcamiento_kNm: result.derived.sismo_momentoVolcamiento_kNm,
		coeficienteSismico_Cs: result.derived.coeficienteSismico_Cs,
		cargaGobernante_Ambiental: result.derived.cargaGobernante_Ambiental,
		momentoGobernante_kNm: result.derived.momentoGobernante_kNm,
		fuerzaCorteGobernante_kN: result.derived.fuerzaCorteGobernante_kN,
		codigoVientoAplicado: result.derived.codigoVientoAplicado,
		leg_compresionMaxima_kN: result.derived.leg_compresionMaxima_kN,
		leg_tensionMaxima_kN: result.derived.leg_tensionMaxima_kN,
		leg_alertaLevantamiento: result.derived.leg_alertaLevantamiento,
		saddle_esfuerzoCuerno_MPa: result.derived.saddle_esfuerzoCuerno_MPa,
		saddle_alertaCuerno: result.derived.saddle_alertaCuerno,
		saddle_esfuerzoFlexionSilleta_MPa: result.derived.saddle_esfuerzoFlexionSilleta_MPa,
		saddle_esfuerzoFlexionCentro_MPa: result.derived.saddle_esfuerzoFlexionCentro_MPa,
		saddle_alertaFlexion: result.derived.saddle_alertaFlexion,
		saddle_esfuerzoCompresionSilleta_MPa:
			result.derived.saddle_esfuerzoCompresionSilleta_MPa,
		saddle_alertaSilleta: result.derived.saddle_alertaSilleta,
		skirt_esfuerzoCompresionFaldon_MPa:
			result.derived.skirt_esfuerzoCompresionFaldon_MPa,
		skirt_tensionMaxPerno_kN: result.derived.skirt_tensionMaxPerno_kN,
		skirt_esfuerzoPlacaSilla_MPa:
			result.derived.skirt_esfuerzoPlacaSilla_MPa,
		skirt_alertaLevantamientoFaldon:
			result.derived.skirt_alertaLevantamientoFaldon,
		skirt_alertaSillaAnclaje: result.derived.skirt_alertaSillaAnclaje,
		lug_cargaMaxPorMensula_kN: result.derived.lug_cargaMaxPorMensula_kN,
		lug_esfuerzoFlexionMensula_MPa: result.derived.lug_esfuerzoFlexionMensula_MPa,
		lug_alertaFlexionMensula: result.derived.lug_alertaFlexionMensula,
		ring_esfuerzoFlexionAnillo_MPa: result.derived.ring_esfuerzoFlexionAnillo_MPa,
		ring_presionPlacaBase_MPa: result.derived.ring_presionPlacaBase_MPa,
		ring_alertaFlexion: result.derived.ring_alertaFlexion,
		anchor_ratioInteraccionAcero: result.derived.anchor_ratioInteraccionAcero,
		anchor_ratioConcreto: result.derived.anchor_ratioConcreto,
		anchor_alertaAcero: result.derived.anchor_alertaAcero,
		anchor_alertaConcreto: result.derived.anchor_alertaConcreto,
	});
	console.log('[PhysicsUtils][computeLightweightResults][return]', result);
	return result;
};

export const debounce = <TArgs extends unknown[]>(
	callback: (...args: TArgs) => void,
	delayMs: number,
) => {
	let timer: ReturnType<typeof setTimeout> | null = null;

	return (...args: TArgs) => {
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => {
			callback(...args);
		}, delayMs);
	};
};

