import { doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { db } from '../../../config/firebase';

export interface UserProfile {
  uid: string;
  email: string;
  firstName: string;
  lastName: string;
  phone: string;
  bio: string;
  avatarUrl: string;
}

const DEFAULT_AVATAR = '/images/user/owner.png';

/**
 * Crea o inicializa el perfil de un usuario en Firestore.
 */
export const createUserProfile = async (
  uid: string,
  email: string,
  firstName: string,
  lastName: string
): Promise<void> => {
  const userRef = doc(db, 'users', uid);
  
  const newProfile: UserProfile = {
    uid,
    email,
    firstName,
    lastName,
    phone: '',
    bio: '',
    avatarUrl: DEFAULT_AVATAR
  };

  await setDoc(userRef, newProfile);
};

/**
 * Obtiene el perfil de un usuario desde Firestore.
 */
export const getUserProfile = async (uid: string): Promise<UserProfile | null> => {
  const userRef = doc(db, 'users', uid);
  const userSnap = await getDoc(userRef);

  if (userSnap.exists()) {
    return userSnap.data() as UserProfile;
  }
  
  return null;
};

/**
 * Actualiza los campos específicos del perfil de un usuario.
 */
export const updateUserProfile = async (
  uid: string, 
  data: Partial<Omit<UserProfile, 'uid' | 'email'>>
): Promise<void> => {
  const userRef = doc(db, 'users', uid);
  await updateDoc(userRef, data);
};
