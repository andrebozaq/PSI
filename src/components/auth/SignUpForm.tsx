import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router';
import { useAuth } from '../../contexts/AuthContext';
import { ChevronLeftIcon, EyeCloseIcon, EyeIcon } from '../../icons';
import Label from '../form/Label';
import Input from '../form/input/InputField';
import Checkbox from '../form/input/Checkbox';
import Button from '../ui/button/Button';
import { Modal } from '../ui/modal';
import { registerWithEmail, loginWithGoogle } from '../../services/authService';
import { getFirebaseErrorMessage } from '../../utils/firebaseErrors';

const AVATARS = [
  '/images/user/owner.png',
  '/images/user/user-01.png',
  '/images/user/user-02.png',
  '/images/user/user-03.png',
  '/images/user/user-04.png',
  '/images/user/user-05.png',
  '/images/user/user-06.png',
];

export default function SignUpForm() {
  const [showPassword, setShowPassword] = useState(false);
  const [isTermsModalOpen, setIsTermsModalOpen] = useState(false);
  const [isChecked, setIsChecked] = useState(false);
  const [fname, setFname] = useState('');
  const [lname, setLname] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [selectedAvatar, setSelectedAvatar] = useState(AVATARS[0]);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<1 | 2>(1);
  const navigate = useNavigate();
  const { currentUser } = useAuth();

  useEffect(() => {
    if (currentUser) {
      navigate('/inicio');
    }
  }, [currentUser, navigate]);
  const handleNextStep = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};
    if (!fname) newErrors.fname = 'El nombre es obligatorio';
    if (!lname) newErrors.lname = 'El apellido es obligatorio';
    if (!email) newErrors.email = 'El correo es obligatorio';
    if (!password) newErrors.password = 'La contraseña es obligatoria';
    if (!confirmPassword) newErrors.confirmPassword = 'Por favor confirma tu contraseña';
    if (password && confirmPassword && password !== confirmPassword) {
      newErrors.confirmPassword = 'Las contraseñas no coinciden';
    }
    if (!isChecked) {
      newErrors.terms = 'Debes aceptar los términos y condiciones';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});
    setStep(2);
  };

  const handleFinalSubmit = async () => {
    setLoading(true);
    setErrors({});
    try {
      await registerWithEmail(email, password, fname, lname, selectedAvatar);
      navigate('/');
    } catch (err: any) {
      const { field, message } = getFirebaseErrorMessage(err.code);
      setErrors({ [field]: message });
      setStep(1); // Volver al paso 1 para mostrar el error si ocurre
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleRegister = async () => {
    setErrors({});
    setLoading(true);
    try {
      await loginWithGoogle();
      navigate('/');
    } catch (err: any) {
      const { field, message } = getFirebaseErrorMessage(err.code);
      setErrors({ [field]: message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex flex-col flex-1">
      <div className="w-full max-w-md mx-auto mb-5 sm:pt-10">
        <Link
          to="/"
          className="inline-flex items-center text-sm text-gray-500 transition-colors hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
        >
          <ChevronLeftIcon className="size-5" />
          Volver al inicio
        </Link>
      </div>
      <div className="flex flex-col justify-center flex-1 w-full max-w-md mx-auto">
        <div>
          <div className="mb-5 sm:mb-8 text-center sm:text-left">
            <h1 className="mb-2 font-semibold text-gray-800 text-title-sm dark:text-white/90 sm:text-title-md">
              {step === 1 ? 'Registro' : 'Elige tu Avatar'}
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {step === 1 ? 'Ingresa tu email y contraseña para registrarte!' : 'Selecciona una imagen que te represente en la comunidad.'}
            </p>
          </div>
          <div>
            {errors.general && <p className="mb-4 text-sm text-red-500">{errors.general}</p>}
            
            {step === 1 ? (
              <>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 sm:gap-5">
              <button 
                type="button"
                onClick={handleGoogleRegister}
                disabled={loading}
                className="inline-flex items-center justify-center gap-3 py-3 text-sm font-normal text-gray-700 transition-colors bg-gray-100 rounded-lg px-7 hover:bg-gray-200 hover:text-gray-800 dark:bg-white/5 dark:text-white/90 dark:hover:bg-white/10"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M18.7511 10.1944C18.7511 9.47495 18.6915 8.94995 18.5626 8.40552H10.1797V11.6527H15.1003C15.0011 12.4597 14.4654 13.675 13.2749 14.4916L13.2582 14.6003L15.9087 16.6126L16.0924 16.6305C17.7788 15.1041 18.7511 12.8583 18.7511 10.1944Z"
                    fill="#4285F4"
                  />
                  <path
                    d="M10.1788 18.75C12.5895 18.75 14.6133 17.9722 16.0915 16.6305L13.274 14.4916C12.5201 15.0068 11.5081 15.3666 10.1788 15.3666C7.81773 15.3666 5.81379 13.8402 5.09944 11.7305L4.99473 11.7392L2.23868 13.8295L2.20264 13.9277C3.67087 16.786 6.68674 18.75 10.1788 18.75Z"
                    fill="#34A853"
                  />
                  <path
                    d="M5.10014 11.7305C4.91165 11.186 4.80257 10.6027 4.80257 9.99992C4.80257 9.3971 4.91165 8.81379 5.09022 8.26935L5.08523 8.1534L2.29464 6.02954L2.20333 6.0721C1.5982 7.25823 1.25098 8.5902 1.25098 9.99992C1.25098 11.4096 1.5982 12.7415 2.20333 13.9277L5.10014 11.7305Z"
                    fill="#FBBC05"
                  />
                  <path
                    d="M10.1789 4.63331C11.8554 4.63331 12.9864 5.34303 13.6312 5.93612L16.1511 3.525C14.6035 2.11528 12.5895 1.25 10.1789 1.25C6.68676 1.25 3.67088 3.21387 2.20264 6.07218L5.08953 8.26943C5.81381 6.15972 7.81776 4.63331 10.1789 4.63331Z"
                    fill="#EB4335"
                  />
                </svg>
                Registrar con Google
              </button>
            </div>
            
            <div className="relative py-3 sm:py-5">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200 dark:border-gray-800"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="p-2 text-gray-400 bg-white dark:bg-gray-900 sm:px-5 sm:py-2">
                  O
                </span>
              </div>
            </div>

            <form onSubmit={handleNextStep}>
              <div className="space-y-5">
                <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
                  {/* <!-- First Name --> */}
                  <div className="sm:col-span-1">
                    <Label>
                      Nombre<span className="text-error-500">*</span>
                    </Label>
                    <Input
                      type="text"
                      id="fname"
                      name="fname"
                      placeholder="Ingresa tu primer nombre"
                      value={fname}
                      onChange={(e: any) => setFname(e.target.value)}
                      error={!!errors.fname}
                      hint={errors.fname}
                    />
                  </div>
                  {/* <!-- Last Name --> */}
                  <div className="sm:col-span-1">
                    <Label>
                      Apellido<span className="text-error-500">*</span>
                    </Label>
                    <Input
                      type="text"
                      id="lname"
                      name="lname"
                      placeholder="Ingresa tu apellido"
                      value={lname}
                      onChange={(e: any) => setLname(e.target.value)}
                      error={!!errors.lname}
                      hint={errors.lname}
                    />
                  </div>
                </div>
                {/* <!-- Email --> */}
                <div>
                  <Label>
                    Email<span className="text-error-500">*</span>
                  </Label>
                  <Input
                    type="email"
                    id="email"
                    name="email"
                    placeholder="Ingresa tu correo"
                    value={email}
                    onChange={(e: any) => setEmail(e.target.value)}
                    error={!!errors.email}
                    hint={errors.email}
                  />
                </div>
                {/* <!-- Password --> */}
                <div>
                  <Label>
                    Contraseña<span className="text-error-500">*</span>
                  </Label>
                  <div className="relative">
                    <Input
                      placeholder="Ingresa tu contraseña"
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e: any) => setPassword(e.target.value)}
                      error={!!errors.password}
                    />
                    <span
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute z-30 -translate-y-1/2 cursor-pointer right-4 top-1/2"
                    >
                      {showPassword ? (
                        <EyeIcon className="fill-gray-500 dark:fill-gray-400 size-5" />
                      ) : (
                        <EyeCloseIcon className="fill-gray-500 dark:fill-gray-400 size-5" />
                      )}
                    </span>
                  </div>
                  {errors.password && (
                    <p className="mt-1.5 text-xs text-error-500">
                      {errors.password}
                    </p>
                  )}
                </div>
                {/* <!-- Confirm Password --> */}
                <div>
                  <Label>
                    Confirmar Contraseña<span className="text-error-500">*</span>
                  </Label>
                  <div className="relative">
                    <Input
                      placeholder="Confirma tu contraseña"
                      type={showPassword ? 'text' : 'password'}
                      value={confirmPassword}
                      onChange={(e: any) => setConfirmPassword(e.target.value)}
                      error={!!errors.confirmPassword}
                    />
                    <span
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute z-30 -translate-y-1/2 cursor-pointer right-4 top-1/2"
                    >
                      {showPassword ? (
                        <EyeIcon className="fill-gray-500 dark:fill-gray-400 size-5" />
                      ) : (
                        <EyeCloseIcon className="fill-gray-500 dark:fill-gray-400 size-5" />
                      )}
                    </span>
                  </div>
                  {errors.confirmPassword && (
                    <p className="mt-1.5 text-xs text-error-500">
                      {errors.confirmPassword}
                    </p>
                  )}
                </div>
                {/* <!-- Checkbox --> */}
                <div className="flex flex-col gap-1.5">
                  <div className="flex items-center gap-3">
                    <Checkbox
                      className={`w-5 h-5 cursor-pointer ${errors.terms ? 'border-error-500' : ''}`}
                      checked={isChecked}
                      onChange={(checked) => {
                        if (checked) {
                          setIsTermsModalOpen(true);
                        } else {
                          setIsChecked(false);
                        }
                      }}
                    />
                    <p className="inline-block font-normal text-gray-500 dark:text-gray-400">
                      Al crear esta cuenta estoy de acuerdo con los{' '}
                      <span 
                        className="text-brand-500 hover:text-brand-600 cursor-pointer underline dark:text-brand-400"
                        onClick={() => setIsTermsModalOpen(true)}
                      >
                        Términos y Condiciones
                      </span>
                    </p>
                  </div>
                  {errors.terms && (
                    <p className="text-xs text-error-500">{errors.terms}</p>
                  )}
                </div>
                {/* <!-- Button --> */}
                <div>
                  <button 
                    type="submit"
                    className="flex items-center justify-center w-full px-4 py-3 text-sm font-medium text-white transition rounded-lg bg-brand-500 shadow-theme-xs hover:bg-brand-600"
                  >
                    Siguiente paso
                  </button>
                </div>
              </div>
            </form>
            </>
            ) : (
              <div className="space-y-6">
                <div className="grid grid-cols-3 gap-4 sm:grid-cols-4">
                  {AVATARS.map((url) => (
                    <div 
                      key={url}
                      onClick={() => setSelectedAvatar(url)}
                      className={`cursor-pointer rounded-full border-[3px] overflow-hidden aspect-square transition-all mx-auto w-full max-w-[80px] ${
                        selectedAvatar === url ? 'border-brand-500 scale-110 shadow-lg' : 'border-transparent hover:scale-105 opacity-70 hover:opacity-100'
                      }`}
                    >
                      <img src={url} alt="avatar option" className="object-cover w-full h-full" />
                    </div>
                  ))}
                </div>
                
                <div className="flex gap-3 pt-4">
                  <button 
                    type="button"
                    disabled={loading}
                    onClick={() => setStep(1)}
                    className="flex items-center justify-center w-1/3 px-4 py-3 text-sm font-medium text-gray-700 transition rounded-lg bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 disabled:opacity-50"
                  >
                    Atrás
                  </button>
                  <button 
                    type="button"
                    onClick={handleFinalSubmit}
                    disabled={loading}
                    className="flex items-center justify-center w-2/3 px-4 py-3 text-sm font-medium text-white transition rounded-lg bg-brand-500 shadow-theme-xs hover:bg-brand-600 disabled:opacity-50"
                  >
                    {loading ? 'Completando...' : 'Completar Registro'}
                  </button>
                </div>
              </div>
            )}

            <div className="mt-5">
              <p className="text-sm font-normal text-center text-gray-700 dark:text-gray-400 sm:text-start">
                Ya tienes una cuenta? {''}
                <Link
                  to="/login"
                  className="text-brand-500 hover:text-brand-600 dark:text-brand-400"
                >
                  Log In
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>

      <Modal isOpen={isTermsModalOpen} onClose={() => setIsTermsModalOpen(false)} className="max-w-[600px] p-6">
        <h3 className="text-xl font-bold text-gray-800 dark:text-white/90 mb-4">Términos y Condiciones</h3>
        <div className="text-sm text-gray-600 dark:text-gray-400 mb-6 max-h-60 overflow-y-auto space-y-3">
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
          </p>
          <p>
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </p>
          <p>
            Al aceptar estos términos, confirmas que has leído y comprendido las políticas de uso de esta herramienta de ingeniería, y que los cálculos proporcionados deben ser verificados por un profesional certificado.
          </p>
        </div>
        <div className="flex justify-end gap-3 mt-4">
          <Button variant="outline" size="sm" onClick={() => setIsTermsModalOpen(false)}>
            Cancelar
          </Button>
          <Button 
            size="sm"
            onClick={() => { 
              setIsChecked(true); 
              setIsTermsModalOpen(false); 
            }}
          >
            He leído y Acepto
          </Button>
        </div>
      </Modal>
    </div>
  );
}
