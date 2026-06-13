export type UnitSystem = 'SI' | 'US';

export type CalculationStatus = 'idle' | 'ready' | 'stale';

export type SupportKind = 'Skirt' | 'Leg' | 'Lug' | 'Ring' | 'Saddle' | 'Unknown';

export type DesignInputs = Record<string, string | number | boolean | undefined>;

export type LightweightDerived = Record<string, number | string | boolean> & {
	diameterToThicknessRatio: number;
	pressureTimesDiameter: number;
	windIndicator: number;
	pesoVacio_kN: number;
	pesoFluido_kN: number;
	pesoOperativo_kN: number;
	corrosionAllowance_mm: number;
	jointEfficiency: number;
	cgVacio_mm: number;
	cgFluido_mm: number;
	cgOperativo_mm: number;
	presionDinamicaBase_kPa: number;
	areaProyectada_m2: number;
	fuerzaCorteBase_kN: number;
	brazoPalanca_m: number;
	momentoVolcamiento_kNm: number;
	viento_fuerzaCorteBase_kN: number;
	viento_brazoPalanca_m: number;
	viento_momentoVolcamiento_kNm: number;
	codigoVientoAplicado: string;
	sismo_fuerzaCorteBasal_kN: number;
	sismo_momentoVolcamiento_kNm: number;
	coeficienteSismico_Cs: number;
	cargaGobernante_Ambiental: string;
	momentoGobernante_kNm: number;
	fuerzaCorteGobernante_kN: number;
	leg_cargaVerticalBase_kN: number;
	leg_cargaPorMomento_kN: number;
	leg_compresionMaxima_kN: number;
	leg_tensionMaxima_kN: number;
	leg_cortePorPata_kN: number;
	leg_alertaLevantamiento: boolean;
	saddle_cargaVerticalPorSilleta_kN: number;
	saddle_cargaLongitudinalFija_kN: number;
	saddle_cargaTransversal_kN: number;
	saddle_esfuerzoCuerno_MPa: number;
	saddle_compresionPlacaBase_MPa: number;
	saddle_esfuerzoFlexionSilleta_MPa: number;
	saddle_esfuerzoFlexionCentro_MPa: number;
	saddle_esfuerzoCompresionSilleta_MPa: number;
	saddle_alertaCuerno: boolean;
	saddle_alertaFlexion: boolean;
	saddle_alertaSilleta: boolean;
	skirt_esfuerzoCompresionFaldon_MPa: number;
	skirt_esfuerzoTensionFaldon_MPa: number;
	skirt_presionConcreto_MPa: number;
	skirt_tensionMaxPerno_kN: number;
	skirt_esfuerzoPlacaSilla_MPa: number;
	skirt_alertaPandeoFaldon: boolean;
	skirt_alertaLevantamientoFaldon: boolean;
	skirt_alertaAgujeroAcceso: boolean;
	skirt_alertaSillaAnclaje: boolean;
	lug_cargaMaxPorMensula_kN: number;
	lug_esfuerzoFlexionMensula_MPa: number;
	lug_esfuerzoCorteMensula_MPa: number;
	lug_presionPlacaApoyo_MPa: number;
	lug_alertaFlexionMensula: boolean;
	lug_alertaFaltaPlaca: boolean;
	ring_areaSeccion_mm2: number;
	ring_moduloSeccion_mm3: number;
	ring_esfuerzoFlexionAnillo_MPa: number;
	ring_esfuerzoCorteAnillo_MPa: number;
	ring_presionPlacaBase_MPa: number;
	ring_alertaFlexion: boolean;
	ring_alertaPresionBase: boolean;
	anchor_ratioInteraccionAcero: number;
	anchor_ratioConcreto: number;
	anchor_alertaAcero: boolean;
	anchor_alertaConcreto: boolean;
	anchor_alertaBorde: boolean;
};

export type LightweightResults = {
	status: CalculationStatus;
	derived: LightweightDerived;
	warnings: string[];
};

export type BlockResults = {
	status: CalculationStatus;
	values: Record<string, number | string | boolean>;
	warnings: string[];
};

export type RecommendedDimension = {
	parameter: string;
	value: string;
};

export type VerificationRow = {
	check: string;
	actual: string;
	allowable: string;
	status: string;
};

export type FinalDesignResults = {
	status: CalculationStatus;
	supportKind: SupportKind;
	recommendedDimensions: RecommendedDimension[];
	verificationRows: VerificationRow[];
	notes: string[];
};

export const EMPTY_LIGHTWEIGHT_RESULTS: LightweightResults = {
	status: 'idle',
	derived: {
		diameterToThicknessRatio: 0,
		pressureTimesDiameter: 0,
		windIndicator: 0,
		pesoVacio_kN: 0,
		pesoFluido_kN: 0,
		pesoOperativo_kN: 0,
		corrosionAllowance_mm: 0,
		jointEfficiency: 1,
		cgVacio_mm: 0,
		cgFluido_mm: 0,
		cgOperativo_mm: 0,
		presionDinamicaBase_kPa: 0,
		areaProyectada_m2: 0,
		fuerzaCorteBase_kN: 0,
		brazoPalanca_m: 0,
		momentoVolcamiento_kNm: 0,
		viento_fuerzaCorteBase_kN: 0,
		viento_brazoPalanca_m: 0,
		viento_momentoVolcamiento_kNm: 0,
		codigoVientoAplicado: 'ASCE',
		sismo_fuerzaCorteBasal_kN: 0,
		sismo_momentoVolcamiento_kNm: 0,
		coeficienteSismico_Cs: 0,
		cargaGobernante_Ambiental: 'NINGUNA',
		momentoGobernante_kNm: 0,
		fuerzaCorteGobernante_kN: 0,
		leg_cargaVerticalBase_kN: 0,
		leg_cargaPorMomento_kN: 0,
		leg_compresionMaxima_kN: 0,
		leg_tensionMaxima_kN: 0,
		leg_cortePorPata_kN: 0,
		leg_alertaLevantamiento: false,
		saddle_cargaVerticalPorSilleta_kN: 0,
		saddle_cargaLongitudinalFija_kN: 0,
		saddle_cargaTransversal_kN: 0,
		saddle_esfuerzoCuerno_MPa: 0,
		saddle_compresionPlacaBase_MPa: 0,
		saddle_esfuerzoFlexionSilleta_MPa: 0,
		saddle_esfuerzoFlexionCentro_MPa: 0,
		saddle_esfuerzoCompresionSilleta_MPa: 0,
		saddle_alertaCuerno: false,
		saddle_alertaFlexion: false,
		saddle_alertaSilleta: false,
		skirt_esfuerzoCompresionFaldon_MPa: 0,
		skirt_esfuerzoTensionFaldon_MPa: 0,
		skirt_presionConcreto_MPa: 0,
		skirt_tensionMaxPerno_kN: 0,
		skirt_esfuerzoPlacaSilla_MPa: 0,
		skirt_alertaPandeoFaldon: false,
		skirt_alertaLevantamientoFaldon: false,
		skirt_alertaAgujeroAcceso: false,
		skirt_alertaSillaAnclaje: false,
		lug_cargaMaxPorMensula_kN: 0,
		lug_esfuerzoFlexionMensula_MPa: 0,
		lug_esfuerzoCorteMensula_MPa: 0,
		lug_presionPlacaApoyo_MPa: 0,
		lug_alertaFlexionMensula: false,
		lug_alertaFaltaPlaca: false,
		ring_areaSeccion_mm2: 0,
		ring_moduloSeccion_mm3: 0,
		ring_esfuerzoFlexionAnillo_MPa: 0,
		ring_esfuerzoCorteAnillo_MPa: 0,
		ring_presionPlacaBase_MPa: 0,
		ring_alertaFlexion: false,
		ring_alertaPresionBase: false,
		anchor_ratioInteraccionAcero: 0,
		anchor_ratioConcreto: 0,
		anchor_alertaAcero: false,
		anchor_alertaConcreto: false,
		anchor_alertaBorde: false,
	},
	warnings: [],
};

export const EMPTY_BLOCK_RESULTS: BlockResults = {
	status: 'idle',
	values: {},
	warnings: [],
};

export const EMPTY_FINAL_RESULTS: FinalDesignResults = {
	status: 'idle',
	supportKind: 'Unknown',
	recommendedDimensions: [],
	verificationRows: [],
	notes: [],
};

