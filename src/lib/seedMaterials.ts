import { collection, setDoc, doc } from 'firebase/firestore';
import { db } from '../config/firebase';
import { STANDARD_LEG_PROFILES } from '../features/engineering/supports/DesignCalculations/LegUtils';

const BOLT_MATERIALS: Record<string, { Fu: number; Fy: number }> = {
	'Acero al carbono': { Fu: 400, Fy: 250 },
	'Acero inoxidable': { Fu: 515, Fy: 205 },
	A325: { Fu: 830, Fy: 630 },
	A490: { Fu: 1040, Fy: 900 },
};

export interface MaterialDocument {
    id: string;
    category: 'bolt' | 'profile';
    name: string;
    Fy: number;
    Fu?: number;
    area_mm2?: number;
    r_mm?: number;
}

export const seedMaterialsToFirestore = async () => {
    try {
        console.log('Iniciando migración de materiales a Firestore...');
        const materialsRef = collection(db, 'materials');

        // Pernos (Bolts)
        for (const [key, mat] of Object.entries(BOLT_MATERIALS)) {
            const docRef = doc(materialsRef, key);
            await setDoc(docRef, {
                id: key,
                category: 'bolt',
                name: key,
                Fy: mat.Fy,
                Fu: mat.Fu,
            });
            console.log(`Material guardado (Perno): ${key}`);
        }

        // Perfiles (Profiles)
        for (const [key, profile] of Object.entries(STANDARD_LEG_PROFILES)) {
            const docRef = doc(materialsRef, key);
            await setDoc(docRef, {
                id: key,
                category: 'profile',
                name: profile.name,
                Fy: 250, // FY_STEEL_MPA usado por defecto en LegUtils
                area_mm2: profile.area_mm2,
                r_mm: profile.r_mm,
            });
            console.log(`Material guardado (Perfil): ${key}`);
        }

        console.log('✅ Migración de materiales completada exitosamente.');
    } catch (error) {
        console.error('❌ Error migrando materiales:', error);
    }
};
