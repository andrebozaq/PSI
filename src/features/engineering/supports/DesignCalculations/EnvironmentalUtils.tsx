// --- CONSTANTES AMBIENTALES Y AERODINÁMICAS ---
const DENSIDAD_AIRE = 1.225; // kg/m³ (nivel del mar, 15°C)
const DRAG_COEFFICIENT_CYLINDER = 0.7;
const DRAG_COEFFICIENT_SPHERE = 0.5;

// Factor práctico para enrutar COVENIN sobre la misma base física Bernoulli.
const FACTOR_EQUIVALENCIA_COVENIN = 1.15;

export type WindDesignCode = 'ASCE' | 'COVENIN';

export type WindInputs = {
	vesselType: string;
	diameter_mm: number;
	length_mm?: number;
	height_mm?: number;
	clearance_mm?: number;
	insulation_mm?: number;
	importanceFactor?: number;
	designCode?: WindDesignCode;
	windSpeed_kmh?: number;
	windPressure_kPa?: number;
};

export type WindResults = {
	presionDinamicaBase_kPa: number;
	areaProyectada_m2: number;
	fuerzaCorteBase_kN: number;
	brazoPalanca_m: number;
	momentoVolcamiento_kNm: number;
	codigoAplicado: WindDesignCode;
};

export type SeismicInputs = {
	pesoOperativo_kN: number;
	cgOperativo_mm: number;
	clearance_mm?: number;
	designCode?: string;

	// Compatibilidad con campo legado/manual
	coeficienteSismico_Cs?: number;

	// ASCE
	seismicSiteClass?: string;
	seismicSs?: number;
	seismicS1?: number;
	seismicR?: number;

	// COVENIN
	covenState?: string;
	covenSoilType?: string;
	covenImportanceGroup?: string;
	covenR?: number;
};

export type SeismicResults = {
	coeficienteSismico_Cs: number;
	fuerzaCorteBasal_kN: number;
	momentoVolcamiento_kNm: number;
	metodoAplicado: string;
};

const toNumber = (value: unknown, fallback = 0) => {
	const numeric = Number(value);
	return Number.isFinite(numeric) ? numeric : fallback;
};

const toPositive = (value: unknown, fallback = 0) => {
	const numeric = toNumber(value, fallback);
	return numeric >= 0 ? numeric : fallback;
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

/**
 * Objetivo: normalizar la norma de viento seleccionada en UI.
 * Entradas: valor libre de código de diseño.
 * Salida: `WindDesignCode` (`ASCE` o `COVENIN`).
 * Norma/Criterio: detección por texto con fallback a ASCE.
 */
export const resolveWindDesignCode = (code: unknown): WindDesignCode => {
	const normalized = String(code ?? '').trim().toLowerCase();
	if (normalized.includes('covenin')) return 'COVENIN';
	return 'ASCE';
};

/**
 * Objetivo: convertir velocidad de viento a presión dinámica base.
 * Entradas: velocidad de viento en km/h.
 * Salida: presión dinámica en kPa.
 * Norma/Criterio: Bernoulli simplificado (q = 0.5·ρ·v²).
 */
export const calculateDynamicWindPressure = (speed_kmh: number): number => {
	if (speed_kmh <= 0) return 0;

	const v_ms = speed_kmh / 3.6;
	const q_Pa = 0.5 * DENSIDAD_AIRE * Math.pow(v_ms, 2);
	return q_Pa / 1000;
};

const resolveWindPressure = (inputs: WindInputs) => {
	const q_direct_kPa = toPositive(inputs.windPressure_kPa, 0);
	// Prioriza presión ya calculada por civil/estructura; si no existe, se deriva desde velocidad.
	if (q_direct_kPa > 0) return q_direct_kPa;

	return calculateDynamicWindPressure(toPositive(inputs.windSpeed_kmh, 0));
};

/**
 * Objetivo: calcular cortante basal y momento de volcamiento por viento.
 * Entradas: geometría del equipo, despeje, datos de viento y norma aplicada.
 * Salida: `WindResults` con q, área proyectada, fuerza, brazo y momento.
 * Norma/Criterio: método estático equivalente con Cd por geometría y factor normativo.
 */
export const calculateWindLoads = (inputs: WindInputs): WindResults => {
	const {
		vesselType,
		designCode = 'ASCE',
	} = inputs;

	const insulation = toPositive(inputs.insulation_mm, 0) / 1000;
	const D = toPositive(inputs.diameter_mm, 0) / 1000 + 2 * insulation;
	const L = toPositive(inputs.length_mm, 0) / 1000 + 2 * insulation;
	const H = toPositive(inputs.height_mm, 0) / 1000 + 2 * insulation;
	const clearance = toPositive(inputs.clearance_mm, 0) / 1000;
	const q_kPa = resolveWindPressure(inputs);
	const importance = toPositive(inputs.importanceFactor, 1);
	const normalizedType = normalizeVesselType(vesselType);

	if (q_kPa === 0 || D === 0) {
		return {
			presionDinamicaBase_kPa: 0,
			areaProyectada_m2: 0,
			fuerzaCorteBase_kN: 0,
			brazoPalanca_m: 0,
			momentoVolcamiento_kNm: 0,
			codigoAplicado: designCode,
		};
	}

	let areaProyectada = 0;
	let dragCoefficient = DRAG_COEFFICIENT_CYLINDER;
	let brazoPalanca = 0;

	switch (normalizedType) {
		case 'horizontal':
			// Viento transversal en horizontal: silueta lateral ≈ rectángulo D x L.
			areaProyectada = D * L;
			// El brazo se mide al centroide del área proyectada, no al CG de masa del recipiente.
			brazoPalanca = clearance + D / 2;
			break;
		case 'vertical':
			// Columna vertical: área proyectada frontal D x H.
			areaProyectada = D * H;
			brazoPalanca = clearance + H / 2;
			break;
		case 'spherical':
			// Esfera: proyección circular; menor Cd por mejor comportamiento aerodinámico.
			areaProyectada = (Math.PI / 4) * Math.pow(D, 2);
			dragCoefficient = DRAG_COEFFICIENT_SPHERE;
			brazoPalanca = clearance + D / 2;
			break;
		default:
			return {
				presionDinamicaBase_kPa: 0,
				areaProyectada_m2: 0,
				fuerzaCorteBase_kN: 0,
				brazoPalanca_m: 0,
				momentoVolcamiento_kNm: 0,
				codigoAplicado: designCode,
			};
	}

	const factorNormativo = designCode === 'COVENIN' ? FACTOR_EQUIVALENCIA_COVENIN : 1;
	// F = q · A · Cd · factor_norma.
	const fuerzaCorteBase_kN =
		q_kPa * areaProyectada * dragCoefficient * factorNormativo * importance;
	// Mv = F · brazo, principal demanda para chequeo de volcamiento/base.
	const momentoVolcamiento_kNm = fuerzaCorteBase_kN * brazoPalanca;

	const result = {
		presionDinamicaBase_kPa: Number(q_kPa.toFixed(3)),
		areaProyectada_m2: Number(areaProyectada.toFixed(2)),
		fuerzaCorteBase_kN: Number(fuerzaCorteBase_kN.toFixed(2)),
		brazoPalanca_m: Number(brazoPalanca.toFixed(2)),
		momentoVolcamiento_kNm: Number(momentoVolcamiento_kNm.toFixed(2)),
		codigoAplicado: designCode,
	};

	console.log(`[EnvironmentalUtils][calculateWindLoads][${designCode}]`, result);
	return result;
};

/**
 * Objetivo: resolver el coeficiente sísmico `Cs` para ASCE o COVENIN.
 * Entradas: parámetros sísmicos normativos y/o `Cs` manual legado.
 * Salida: `Cs` adimensional para método estático equivalente.
 * Norma/Criterio: ASCE (`Cs = SDS/R`) y COVENIN (`Cs = α·A0/R`), con prioridad a `Cs` manual.
 */
const calculateCs = (inputs: SeismicInputs): number => {
	const manualCs = toPositive(inputs.coeficienteSismico_Cs, 0);
	if (manualCs > 0) return manualCs;

	const isCovenin = String(inputs.designCode ?? '').toUpperCase().includes('COVENIN');

	if (isCovenin) {
		const R = toPositive(inputs.covenR, 3);
		if (R === 0) return 0;

		const estado = String(inputs.covenState ?? '').trim().toLowerCase();
		let A0 = 0.25;
		if (estado.includes('zulia') || estado.includes('caracas') || estado.includes('sucre')) {
			A0 = 0.3;
		}
		if (estado.includes('lara') || estado.includes('miranda')) {
			A0 = 0.35;
		}
		if (estado.includes('falcón') || estado.includes('falcon')) {
			A0 = 0.35;
		}

		const grupo = String(inputs.covenImportanceGroup ?? 'B2').trim().toUpperCase();
		let alfa = 1;
		if (grupo.includes('A')) alfa = 1.3;
		if (grupo.includes('B1')) alfa = 1.15;

		return (alfa * A0) / R;
	}

	const R = toPositive(inputs.seismicR, 3);
	if (R === 0) return 0;

	const Ss = toPositive(inputs.seismicSs, 0.5);
	const siteClass = String(inputs.seismicSiteClass ?? 'D').trim().toUpperCase();

	let Fa = 1;
	if (siteClass === 'A') Fa = 0.8;
	else if (siteClass === 'B') Fa = 1;
	else if (siteClass === 'C') Fa = Ss <= 0.5 ? 1.2 : 1;
	else if (siteClass === 'D') Fa = Ss <= 0.25 ? 1.6 : Ss <= 0.75 ? 1.2 : 1;
	else if (siteClass === 'E') Fa = Ss <= 0.25 ? 2.5 : 1.2;

	const S_MS = Fa * Ss;
	const S_DS = (2 / 3) * S_MS;
	return S_DS / R;
};

/**
 * Objetivo: calcular demanda sísmica global del equipo.
 * Entradas: peso operativo, brazo dinámico y parámetros para resolver `Cs`.
 * Salida: `SeismicResults` con `Cs`, cortante basal y momento de volcamiento.
 * Norma/Criterio: método estático equivalente `V = Cs·W` y `M = V·brazo`.
 */
export const calculateSeismicLoads = (inputs: SeismicInputs): SeismicResults => {
	const W = toPositive(inputs.pesoOperativo_kN, 0);
	const cg_metros = toPositive(inputs.cgOperativo_mm, 0) / 1000;
	const clearance = toPositive(inputs.clearance_mm, 0) / 1000;
	const Cs = calculateCs(inputs);
	const metodoAplicado = String(inputs.designCode ?? '').toUpperCase().includes('COVENIN')
		? 'COVENIN 1756'
		: 'ASCE 7';

	if (W === 0 || Cs === 0) {
		return {
			coeficienteSismico_Cs: 0,
			fuerzaCorteBasal_kN: 0,
			momentoVolcamiento_kNm: 0,
			metodoAplicado,
		};
	}

	const fuerzaCorteBasal_kN = Cs * W;
	const brazoPalanca = cg_metros + clearance;
	const momentoVolcamiento_kNm = fuerzaCorteBasal_kN * brazoPalanca;

	const result = {
		coeficienteSismico_Cs: Number(Cs.toFixed(3)),
		fuerzaCorteBasal_kN: Number(fuerzaCorteBasal_kN.toFixed(2)),
		momentoVolcamiento_kNm: Number(momentoVolcamiento_kNm.toFixed(2)),
		metodoAplicado,
	};

	console.log('[EnvironmentalUtils][calculateSeismicLoads][return]', result);
	return result;
};

