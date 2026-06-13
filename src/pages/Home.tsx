import { Link } from 'react-router';
import { Autoplay, Pagination } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import {
  TbArrowRight,
  TbCircleCheck,
  TbClock,
  TbFileDescription,
  TbServer2,
} from 'react-icons/tb';
import PageMeta from '../components/common/PageMeta';
import { useState, useEffect } from 'react';
import { collection, query, where, getDocs } from 'firebase/firestore';
import { db } from '../config/firebase';
import { useAuth } from '../features/auth/contexts/AuthContext';

const moduleSlides = [
  {
    title: 'Diseño de soportes',
    copy: 'Dimensiona y verifica soportes de recipientes a presión con cargas reales.',
    path: '/soporte-diseno',
    tag: 'Mecánica',
    accent: 'from-indigo-600 to-blue-500',
  },
  {
    title: 'Análisis de soportes',
    copy: 'Evalúa esfuerzos, estabilidad y combinaciones de carga en minutos.',
    path: '/soporte-analisis-editor',
    tag: 'Integridad',
    accent: 'from-sky-500 to-cyan-500',
  },
  {
    title: 'Recipientes a presión',
    copy: 'Calcula espesores, boquillas y pruebas según ASME VIII.',
    path: '/recipientes-analisis',
    tag: 'Presión',
    accent: 'from-amber-500 to-orange-500',
  },
  {
    title: 'Elementos estructurales',
    copy: 'Vigas y soldaduras listas para revisión de códigos locales.',
    path: '/vigas-analisis',
    tag: 'Estructuras',
    accent: 'from-emerald-500 to-teal-500',
  },
];

export default function Home() {
  const { currentUser } = useAuth();
  const [projectCount, setProjectCount] = useState<number | string>('...');

  useEffect(() => {
    const fetchProjectCount = async () => {
      if (!currentUser) {
        setProjectCount(0);
        return;
      }
      try {
        const q = query(
          collection(db, 'studies'),
          where('userId', '==', currentUser.uid)
        );
        const querySnapshot = await getDocs(q);
        setProjectCount(querySnapshot.size);
      } catch (error) {
        console.error('Error fetching projects count:', error);
        setProjectCount(0);
      }
    };
    fetchProjectCount();
  }, [currentUser]);

  const quickStats = [
    {
      label: 'Diseños guardados',
      value: String(projectCount),
      icon: <TbFileDescription className="h-5 w-5" />,
      hint: currentUser ? 'Sincronizado' : 'Sin iniciar sesión',
      link: '/proyectos',
    },
    {
      label: 'Base de datos',
      value: 'Conectada',
      icon: <TbServer2 className="h-5 w-5" />,
      hint: 'Local dev',
      status: 'online',
    },
    {
      label: 'Última sincronización',
      value: 'Al día',
      icon: <TbClock className="h-5 w-5" />,
      hint: 'Firebase',
    },
  ];

  return (
    <>
      <PageMeta
        title="PSI Inicio | Software de ingeniería"
        description="Tablero inicial con accesos rápidos, credenciales académicas y actividad reciente."
      />

      <div className="space-y-6">
        {/* Top: Navigation Carousel */}
        <section className="rounded-2xl border border-gray-200 bg-white px-5 py-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] xl:px-8">
          <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
            <div>
              <p className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">
                Navegación rápida
              </p>
              <h2 className="text-lg font-semibold text-gray-800 dark:text-white/90">
                Explora los módulos principales
              </h2>
            </div>
          </div>

          <div className="relative">
            <Swiper
              modules={[Pagination, Autoplay]}
              pagination={{ clickable: true }}
              autoplay={{ delay: 4800, disableOnInteraction: false }}
              spaceBetween={16}
              slidesPerView={1}
              breakpoints={{
                768: { slidesPerView: 2 },
                1280: { slidesPerView: 2.2 },
              }}
              className="pb-10 carouselFour"
            >
              {moduleSlides.map((slide) => (
                <SwiperSlide key={slide.title}>
                  <Link to={slide.path} className="group block h-full">
                    <div className="relative flex h-[220px] flex-col justify-between overflow-hidden rounded-2xl border border-gray-200 bg-gradient-to-br p-5 text-white shadow-sm transition duration-200 hover:shadow-lg dark:border-gray-800">
                      <div
                        className={`absolute inset-0 bg-gradient-to-br ${slide.accent} opacity-90`}
                      />
                      <div
                        className="pointer-events-none absolute inset-0 mix-blend-soft-light"
                        style={{
                          opacity: 0.08,
                          backgroundImage:
                            'linear-gradient(0deg, rgba(255,255,255,0.35) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.35) 1px, transparent 1px)',
                          backgroundSize: '18px 18px',
                        }}
                      />
                      <div className="relative flex items-center gap-2 text-sm font-semibold">
                        <span className="rounded-full bg-white/15 px-3 py-1 text-xs">
                          {slide.tag}
                        </span>
                        <span className="text-white/80">Módulo</span>
                      </div>
                      <div className="relative space-y-3">
                        <h3 className="text-xl font-semibold leading-tight">
                          {slide.title}
                        </h3>
                        <p className="max-w-[320px] text-sm leading-relaxed text-white/80">
                          {slide.copy}
                        </p>
                      </div>
                      <div className="relative inline-flex items-center gap-2 self-start rounded-full bg-white/15 px-3 py-2 text-sm font-semibold text-white transition group-hover:bg-white/25">
                        Ir ahora
                        <TbArrowRight className="h-4 w-4 transition-transform duration-200 group-hover:translate-x-1" />
                      </div>
                    </div>
                  </Link>
                </SwiperSlide>
              ))}
            </Swiper>
          </div>
        </section>

        {/* Middle: Academic Credentials */}
        <section className="rounded-2xl border border-gray-200 bg-white px-5 py-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] xl:px-8">
          <div className="flex flex-col gap-6 md:flex-row md:items-center">
            <div className="flex items-center gap-4 md:w-1/3">
              <div className="flex h-16 w-16 items-center justify-center overflow-hidden rounded-full bg-white shadow-md ring-1 ring-gray-200 dark:bg-gray-900 dark:ring-gray-800">
                <img
                  src="/images/logo/LUZ.png"
                  alt="Universidad del Zulia"
                  className="h-12 w-12 object-contain dark:hidden"
                />
                <img
                  src="/images/logo/LUZ-dark.png"
                  alt="Universidad del Zulia"
                  className="hidden h-12 w-12 object-contain dark:block"
                />
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">
                  Universidad del Zulia
                </p>
                <p className="text-sm font-semibold text-gray-800 dark:text-white/90">
                  Facultad de Ingeniería
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Escuela de Mecánica
                </p>
              </div>
            </div>

            <div className="md:flex-1">
              <div className="mb-3 flex flex-wrap items-start justify-between gap-2">
                <div>
                  <h3 className="text-base font-semibold text-gray-800 dark:text-white/90">
                    PSI - Pressure Vessel Support Indicator
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Herramienta académica para diseño y verificación de soportes
                    de recipientes a presión.
                  </p>
                </div>
                <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-200">
                  Proyecto 2025 - 2026
                </span>
              </div>

              <div className="grid gap-3 md:grid-cols-[1.2fr_1fr]">
                <div className="rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm leading-relaxed text-gray-700 shadow-sm dark:border-gray-800 dark:bg-gray-900/60 dark:text-gray-200">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                    <TbCircleCheck className="h-4 w-4" />
                    Info. del trabajo especial de grado
                  </div>
                  <div className="mt-2 space-y-1">
                    <p>Tesistas: André Boza, Rafael Ponzon</p>
                    <p>Tutor: Ing. Omar González</p>
                    <p>
                      Título: Desarrollo de un programa computacional para el
                      análisis y diseño de soportes de recipientes a presión.
                    </p>
                  </div>
                </div>

                <div className="rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm text-gray-700 shadow-sm md:border-l md:border-gray-200 md:pl-5 dark:border-gray-800 dark:bg-gray-900/70 dark:text-gray-200 dark:md:border-gray-800">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                    <TbCircleCheck className="h-4 w-4" />
                    Información de diseño
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {[
                      'ASME VIII Div 1',
                      'ASME VIII Div 2',
                      'COVENIN 1756',
                      'API refs (rev)',
                    ].map((tag) => (
                      <span
                        key={tag}
                        className="inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-800 dark:border-blue-700 dark:bg-blue-500/10 dark:text-blue-200"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Bottom: Quick Stats */}
        <section className="rounded-2xl border border-gray-200 bg-white px-5 py-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] xl:px-8">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">
                Estado rápido
              </p>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
                Actividad reciente
              </h3>
            </div>
            <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Conectado
            </span>
          </div>

          <div className="grid gap-4 sm:grid-cols-3">
            {quickStats.map((item) => {
              const Card = (
                <div
                  key={item.label}
                  className="rounded-xl border border-gray-200 bg-gray-50 px-4 py-4 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md dark:border-gray-800 dark:bg-gray-900/60"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 text-sm font-semibold text-gray-700 dark:text-gray-100">
                      <span className="relative flex h-9 w-9 items-center justify-center rounded-full bg-white text-blue-600 shadow-sm dark:bg-gray-800 dark:text-blue-300">
                        {item.status === 'online' && (
                          <span className="absolute -right-1 -top-1 h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_0_4px_rgba(16,185,129,0.35)] animate-pulse" />
                        )}
                        {item.icon}
                      </span>
                      {item.label}
                    </div>
                    <span className="text-xs text-gray-400 dark:text-gray-500">
                      {item.hint}
                    </span>
                  </div>
                  <p className="mt-3 text-2xl font-semibold text-gray-900 dark:text-white">
                    {item.value}
                  </p>
                </div>
              );

              return item.link ? (
                <Link to={item.link} key={item.label} className="block">
                  {Card}
                </Link>
              ) : (
                Card
              );
            })}
          </div>
        </section>
      </div>
    </>
  );
}
