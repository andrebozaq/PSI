import { 
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword, 
    sendPasswordResetEmail,
    GoogleAuthProvider,
    signInWithPopup,
    signOut,
    updateProfile
} from "firebase/auth";
import { doc, setDoc, getDoc } from "firebase/firestore";
import { auth, db } from "../lib/firebaseConfig";

const googleProvider = new GoogleAuthProvider();

// Función auxiliar para guardar el usuario en Firestore tras registrarse
const saveUserToFirestore = async (user: any, additionalData: any = {}) => {
    const userRef = doc(db, 'users', user.uid);
    const docSnap = await getDoc(userRef);
    
    // Si el usuario no existe en la BD, lo creamos
    if (!docSnap.exists()) {
        const displayName = additionalData.displayName || user.displayName || 'Ingeniero';
        const nameParts = displayName.split(' ');
        const firstName = nameParts[0] || '';
        const lastName = nameParts.slice(1).join(' ') || '';

        await setDoc(userRef, {
            uid: user.uid,
            email: user.email,
            firstName: additionalData.firstName || firstName,
            lastName: additionalData.lastName || lastName,
            phone: '',
            bio: '',
            avatarUrl: additionalData.avatarUrl || '/images/user/owner.png',
            createdAt: Date.now(),
        });
    }
};

// 1. Registro con Correo
export const registerWithEmail = async (email: string, pass: string, firstName: string, lastName: string, avatarUrl: string = '/images/user/owner.png') => {
    const userCredential = await createUserWithEmailAndPassword(auth, email, pass);
    await saveUserToFirestore(userCredential.user, { firstName, lastName, avatarUrl });
    if (userCredential.user) {
        await updateProfile(userCredential.user, { photoURL: avatarUrl, displayName: `${firstName} ${lastName}` });
    }
    return userCredential.user;
};

// 2. Login con Correo
export const loginWithEmail = async (email: string, pass: string) => {
    const userCredential = await signInWithEmailAndPassword(auth, email, pass);
    return userCredential.user;
};

// 3. Login con Google
export const loginWithGoogle = async () => {
    const userCredential = await signInWithPopup(auth, googleProvider);
    await saveUserToFirestore(userCredential.user, { avatarUrl: userCredential.user.photoURL });
    return userCredential.user;
};

// 4. Recuperar Contraseña
export const resetPassword = async (email: string) => {
    await sendPasswordResetEmail(auth, email);
    return true;
};

// 5. Cerrar Sesión
export const logout = async () => {
    await signOut(auth);
};
