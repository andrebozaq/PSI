import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

// TODO: Reemplaza esto con los datos de tu consola de Firebase
// (Settings -> General -> Your apps -> Firebase SDK snippet)
const firebaseConfig = {
  apiKey: "AIzaSyAuDf7OoDm0nwCteY8kuowYhD8gqy5EtV0",
  authDomain: "psi-db-620fc.firebaseapp.com",
  projectId: "psi-db-620fc",
  storageBucket: "psi-db-620fc.firebasestorage.app",
  messagingSenderId: "247322182281",
  appId: "1:247322182281:web:db9200fd3b72dd0de5fc58",
  measurementId: "G-N3Q2V3RNX2"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);

// Exportar los servicios que usaremos
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);
