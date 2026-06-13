import { collection, addDoc, getDocs, deleteDoc } from "firebase/firestore";
import { db } from "../config/firebase";

const materialsDataset = [
  // --- ACEROS DE RECIPIENTE (PLANCHAS) ---
  {
    standard: "ASME VIII",
    name: "SA-516 Gr. 70",
    type: "carbon_steel",
    density_kg_m3: 7850,
    yieldStrength_MPa: 260,
    ultimateStrength_MPa: 485,
    elasticModulus_MPa: 200000
  },
  {
    standard: "ASME VIII",
    name: "SA-516 Gr. 60",
    type: "carbon_steel",
    density_kg_m3: 7850,
    yieldStrength_MPa: 220,
    ultimateStrength_MPa: 415,
    elasticModulus_MPa: 200000
  },
  {
    standard: "ASME VIII",
    name: "SA-240 Type 304L",
    type: "stainless_steel",
    density_kg_m3: 8000,
    yieldStrength_MPa: 170,
    ultimateStrength_MPa: 485,
    elasticModulus_MPa: 193000
  },
  {
    standard: "ASME VIII",
    name: "SA-240 Type 316L",
    type: "stainless_steel",
    density_kg_m3: 8000,
    yieldStrength_MPa: 170,
    ultimateStrength_MPa: 485,
    elasticModulus_MPa: 193000
  },

  // --- ACEROS ESTRUCTURALES Y TUBERÍAS (SOPORTES) ---
  {
    standard: "ASTM",
    name: "A36 (SA-36)",
    type: "carbon_steel",
    density_kg_m3: 7850,
    yieldStrength_MPa: 250,
    ultimateStrength_MPa: 400,
    elasticModulus_MPa: 200000
  },
  {
    standard: "ASME VIII",
    name: "SA-106 Gr. B (Tubería)",
    type: "carbon_steel",
    density_kg_m3: 7850,
    yieldStrength_MPa: 240,
    ultimateStrength_MPa: 415,
    elasticModulus_MPa: 200000
  },

  // --- PERNOS Y VARILLAS DE ANCLAJE ---
  {
    standard: "ASTM",
    name: "A307 (Grado B)",
    type: "carbon_steel",
    density_kg_m3: 7850,
    yieldStrength_MPa: 250,
    ultimateStrength_MPa: 414,
    elasticModulus_MPa: 200000
  },
  {
    standard: "ASTM",
    name: "A325 / F3125",
    type: "carbon_steel",
    density_kg_m3: 7850,
    yieldStrength_MPa: 630,
    ultimateStrength_MPa: 830,
    elasticModulus_MPa: 200000
  },
  {
    standard: "ASTM",
    name: "A490 / F3125",
    "type": "alloy",
    density_kg_m3: 7850,
    yieldStrength_MPa: 900,
    ultimateStrength_MPa: 1040,
    elasticModulus_MPa: 200000
  },
  {
    standard: "ASTM",
    name: "F1554 Gr. 36 (Anchor Rod)",
    type: "carbon_steel",
    density_kg_m3: 7850,
    yieldStrength_MPa: 248,
    ultimateStrength_MPa: 400,
    elasticModulus_MPa: 200000
  },
  {
    standard: "ASTM",
    name: "F1554 Gr. 105 (Anchor Rod)",
    type: "alloy",
    density_kg_m3: 7850,
    yieldStrength_MPa: 724,
    ultimateStrength_MPa: 862,
    elasticModulus_MPa: 200000
  }
];

export const seedMaterialsDatabase = async () => {
  try {
    const materialsRef = collection(db, "materials");
    const snapshot = await getDocs(materialsRef);
    
    // Si ya existen datos, los borramos para asegurar que tenemos la nueva versión
    if (!snapshot.empty) {
      console.info("Limpiando la base de datos de materiales actual...");
      for (const docSnapshot of snapshot.docs) {
        await deleteDoc(docSnapshot.ref);
      }
      console.info("Limpieza completada.");
    }

    console.log("Iniciando siembra de la librería completa de materiales...");
    for (const material of materialsDataset) {
      await addDoc(materialsRef, material);
    }
    console.log("¡Librería completa de materiales sembrada con éxito en Firestore!");
  } catch (error) {
    console.error("Error al sembrar materiales:", error);
  }
};
