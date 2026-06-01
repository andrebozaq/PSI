export const getFirebaseErrorMessage = (errorCode: string): { field: 'email' | 'password' | 'general'; message: string } => {
  switch (errorCode) {
    // Errores de Login
    case 'auth/invalid-email':
      return { field: 'email', message: 'El formato del correo electrónico no es válido.' };
    case 'auth/user-disabled':
      return { field: 'general', message: 'Esta cuenta ha sido deshabilitada por el administrador.' };
    case 'auth/user-not-found':
      return { field: 'email', message: 'No encontramos una cuenta asociada a este correo.' };
    case 'auth/wrong-password':
    case 'auth/invalid-credential':
      return { field: 'password', message: 'El correo o la contraseña son incorrectos.' };
    
    // Errores de Registro
    case 'auth/email-already-in-use':
      return { field: 'email', message: 'Este correo ya está registrado. Intenta iniciar sesión.' };
    case 'auth/weak-password':
      return { field: 'password', message: 'La contraseña es muy débil. Debe tener al menos 6 caracteres.' };
    
    // Errores de Google
    case 'auth/popup-closed-by-user':
      return { field: 'general', message: 'Se cerró la ventana emergente antes de completar el inicio de sesión.' };
    case 'auth/cancelled-popup-request':
      return { field: 'general', message: 'Operación cancelada. Solo se permite una ventana a la vez.' };
    
    // Errores de Recuperación
    case 'auth/too-many-requests':
      return { field: 'general', message: 'Demasiados intentos fallidos. Por favor, intenta de nuevo más tarde.' };
      
    // Default
    default:
      return { field: 'general', message: 'Ocurrió un error inesperado. Por favor, intenta de nuevo.' };
  }
};
