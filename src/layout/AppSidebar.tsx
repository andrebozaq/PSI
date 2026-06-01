import { useCallback, useEffect, useRef, useState } from 'react';
import { GiIBeam } from 'react-icons/gi';
import { MdPropaneTank } from 'react-icons/md';
import { BsPatchQuestionFill } from 'react-icons/bs';

import { Link, useLocation } from 'react-router';

// Assume these icons are imported from an icon library
import {
  BoxCubeIcon,
  ChatIcon,
  ChevronDownIcon,
  DocsIcon,
  HorizontaLDots,
  ListIcon,
  MailIcon,
  PageIcon,
  PieChartIcon,
  PlugInIcon,
  TableIcon,
  UserCircleIcon,
} from '../icons';
import { useSidebar } from '../context/SidebarContext';
import SidebarWidget from './SidebarWidget';

export type NavItem = {
  name: string;
  icon: React.ReactNode;
  path?: string;
  subItems?: { name: string; path: string; pro?: boolean; new?: boolean }[];
};

export const navItems: NavItem[] = [
  {
    icon: [
      <svg
        className="fill-current"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          fillRule="evenodd"
          clipRule="evenodd"
          d="M7.48994 3.61404C7.79216 3.38738 8.20771 3.38738 8.50993 3.61404L12.3433 6.48904C12.5573 6.64957 12.6833 6.9015 12.6833 7.16904V11.8333C12.6833 12.3028 12.3027 12.6833 11.8333 12.6833H8.64993V10.8333C8.64993 10.4744 8.35892 10.1833 7.99993 10.1833C7.64095 10.1833 7.34993 10.4744 7.34993 10.8333V12.6833H4.1666C3.69716 12.6833 3.3166 12.3028 3.3166 11.8333V7.16904C3.3166 6.9015 3.44257 6.64957 3.6566 6.48904L7.48994 3.61404ZM7.99478 13.9833H4.1666C2.97919 13.9833 2.0166 13.0207 2.0166 11.8333V7.16904C2.0166 6.49231 2.33522 5.85508 2.8766 5.44904L6.70994 2.57404C7.47438 2.00071 8.52549 2.00071 9.28993 2.57404L13.1233 5.44904C13.6647 5.85508 13.9833 6.49232 13.9833 7.16904V11.8333C13.9833 13.0207 13.0207 13.9833 11.8333 13.9833H8.00509C8.00337 13.9833 8.00166 13.9833 7.99993 13.9833C7.99821 13.9833 7.9965 13.9833 7.99478 13.9833Z"
          fill=""
        />
      </svg>,
    ],
    name: 'Inicio',
    path: '/',
  },
  {
    icon: <MdPropaneTank />,
    name: 'Elementos a presión',
    subItems: [
      { name: 'Recipientes', path: '/recipientes-analisis', pro: false },
      {
        name: 'Análisis de soportes',
        path: '/soporte-analisis-editor',
        pro: false,
      },
      { name: 'Diseño de soportes', path: '/soporte-diseno', pro: false },
    ],
  },
  {
    icon: <GiIBeam />,
    name: 'Elementos estructurales',
    subItems: [
      { name: 'Vigas', path: '/proximamente', new: false, pro: false },
      {
        name: 'Análisis de soldadura',
        path: '/proximamente',
        new: false,
        pro: false,
      },
      {
        name: 'Diseño de soldadura',
        path: '/proximamente',
        new: false,
        pro: false,
      },
    ],
  },
  {
    name: 'Librería de Materiales',
    icon: <ListIcon />,
    subItems: [
      { name: 'Elementos de formulario', path: '/form-elements', pro: false },
      { name: 'Layout de formulario', path: '/form-layout', pro: false },
    ],
  },
  {
    name: 'Normativas',
    icon: <TableIcon />,
    subItems: [
      { name: 'Materiales ASME VIII DIV 1', path: '/basic-tables', pro: false },
      { name: 'Materiales ASME VIII DIV 2', path: '/data-tables', pro: false },
    ],
  },
  {
    name: 'Configuración del Motor',
    icon: <PageIcon />,
    subItems: [
      { name: 'File Manager', path: '/file-manager', pro: false },
      { name: 'Pricing Tables', path: '/pricing-tables', pro: false },

      { name: 'Blank Page', path: '/blank', pro: false },
      { name: '404 Error', path: '/error-404', pro: false },
      { name: '500 Error', path: '/error-500', pro: false },
      { name: '503 Error', path: '/error-503', pro: false },
      { name: 'Próximamente', path: '/proximamente', pro: false },
      { name: 'Maintenance', path: '/maintenance', pro: false },
      { name: 'Success', path: '/success', pro: false },
    ],
  },
  {
    icon: <DocsIcon />,
    name: 'Proyectos guardados',
    path: '/proyectos',
  },
  {
    icon: <UserCircleIcon />,
    name: 'Perfil de Usuario',
    path: '/perfil',
  },
  {
    icon: <BsPatchQuestionFill />,
    name: 'Preguntas frecuentes',
    path: '/faq',
  },
];

export const othersItems: NavItem[] = [
  {
    icon: <PieChartIcon />,
    name: 'Gráficos',
    subItems: [
      { name: 'Line Chart', path: '/line-chart', pro: true },
      { name: 'Bar Chart', path: '/bar-chart', pro: true },
      { name: 'Pie Chart', path: '/pie-chart', pro: true },
    ],
  },
  {
    icon: <BoxCubeIcon />,
    name: 'Elementos de UI',
    subItems: [
      { name: 'Alerts', path: '/alerts', pro: false },
      { name: 'Avatar', path: '/avatars', pro: false },
      { name: 'Badge', path: '/badge', pro: false },
      { name: 'Breadcrumb', path: '/breadcrumb', pro: true },
      { name: 'Buttons', path: '/buttons', pro: false },
      { name: 'Buttons Group', path: '/buttons-group', pro: true },
      { name: 'Cards', path: '/cards', pro: true },
      { name: 'Carousel', path: '/carousel', pro: true },
      { name: 'Dropdowns', path: '/dropdowns', pro: true },
      { name: 'Images', path: '/images', pro: false },
      { name: 'Links', path: '/links', pro: true },
      { name: 'List', path: '/list', pro: true },
      { name: 'Modals', path: '/modals', pro: true },
      { name: 'Notification', path: '/notifications', pro: true },
      { name: 'Pagination', path: '/pagination', pro: true },
      { name: 'Popovers', path: '/popovers', pro: true },
      { name: 'Progressbar', path: '/progress-bar', pro: true },
      { name: 'Ribbons', path: '/ribbons', pro: true },
      { name: 'Spinners', path: '/spinners', pro: true },
      { name: 'Tabs', path: '/tabs', pro: true },
      { name: 'Tooltips', path: '/tooltips', pro: true },
      { name: 'Videos', path: '/videos', pro: false },
    ],
  },
  {
    icon: <PlugInIcon />,
    name: 'Autenticación',
    subItems: [
      { name: 'Log in', path: '/login', pro: false },
      { name: 'Registrarse', path: '/registro', pro: false },
      { name: 'Recuperar contraseña', path: '/reset-password', pro: true },
      {
        name: 'Verificación de dos pasos',
        path: '/two-step-verification',
        pro: true,
      },
    ],
  },
];

export const supportItems: NavItem[] = [
  {
    icon: <ChatIcon />,
    name: 'Chat',
    path: '/chat',
  },
  {
    icon: <MailIcon />,
    name: 'Email',
    subItems: [
      { name: 'Inbox', path: '/inbox' },
      { name: 'Details', path: '/inbox-details' },
    ],
  },
  {
    icon: <DocsIcon />,
    name: 'Documentación',
    path: '/documentacion',
  },
];

const AppSidebar: React.FC = () => {
  const { isExpanded, isMobileOpen, isHovered, setIsHovered } = useSidebar();
  const location = useLocation();

  const [openSubmenu, setOpenSubmenu] = useState<{
    type: 'main' | 'support' | 'others';
    index: number;
  } | null>(null);
  const [subMenuHeight, setSubMenuHeight] = useState<Record<string, number>>(
    {},
  );
  const subMenuRefs = useRef<Record<string, HTMLDivElement | null>>({});

  // const isActive = (path: string) => location.pathname === path;
  const isActive = useCallback(
    (path: string) => location.pathname === path,
    [location.pathname],
  );

  useEffect(() => {
    let submenuMatched = false;
    ['main'].forEach((menuType) => {
      const items = navItems;
      items.forEach((nav, index) => {
        if (nav.subItems) {
          nav.subItems.forEach((subItem) => {
            if (isActive(subItem.path)) {
              setOpenSubmenu({
                type: 'main',
                index,
              });
              submenuMatched = true;
            }
          });
        }
      });
    });

    if (!submenuMatched) {
      setOpenSubmenu(null);
    }
  }, [location, isActive]);

  useEffect(() => {
    if (openSubmenu !== null) {
      const key = `${openSubmenu.type}-${openSubmenu.index}`;
      if (subMenuRefs.current[key]) {
        setSubMenuHeight((prevHeights) => ({
          ...prevHeights,
          [key]: subMenuRefs.current[key]?.scrollHeight || 0,
        }));
      }
    }
  }, [openSubmenu]);

  const handleSubmenuToggle = (
    index: number,
    menuType: 'main' | 'support' | 'others',
  ) => {
    setOpenSubmenu((prevOpenSubmenu) => {
      if (
        prevOpenSubmenu &&
        prevOpenSubmenu.type === menuType &&
        prevOpenSubmenu.index === index
      ) {
        return null;
      }
      return { type: menuType, index };
    });
  };

  const renderMenuItems = (
    items: NavItem[],
    menuType: 'main' | 'support' | 'others',
  ) => (
    <ul className="flex flex-col gap-4">
      {items.map((nav, index) => (
        <li key={nav.name}>
          {nav.subItems ? (
            <button
              onClick={() => handleSubmenuToggle(index, menuType)}
              className={`menu-item group ${
                openSubmenu?.type === menuType && openSubmenu?.index === index
                  ? 'menu-item-active'
                  : 'menu-item-inactive'
              } cursor-pointer ${
                !isExpanded && !isHovered
                  ? 'lg:justify-center'
                  : 'lg:justify-start'
              }`}
            >
              <span
                className={`menu-item-icon-size  ${
                  openSubmenu?.type === menuType && openSubmenu?.index === index
                    ? 'menu-item-icon-active'
                    : 'menu-item-icon-inactive'
                }`}
              >
                {nav.icon}
              </span>
              {(isExpanded || isHovered || isMobileOpen) && (
                <span className="menu-item-text">{nav.name}</span>
              )}
              {(isExpanded || isHovered || isMobileOpen) && (
                <ChevronDownIcon
                  className={`ml-auto w-5 h-5 transition-transform duration-200 ${
                    openSubmenu?.type === menuType &&
                    openSubmenu?.index === index
                      ? 'rotate-180 text-brand-500'
                      : ''
                  }`}
                />
              )}
            </button>
          ) : (
            nav.path && (
              <Link
                to={nav.path}
                className={`menu-item group ${
                  isActive(nav.path) ? 'menu-item-active' : 'menu-item-inactive'
                }`}
              >
                <span
                  className={`menu-item-icon-size ${
                    isActive(nav.path)
                      ? 'menu-item-icon-active'
                      : 'menu-item-icon-inactive'
                  }`}
                >
                  {nav.icon}
                </span>
                {(isExpanded || isHovered || isMobileOpen) && (
                  <span className="menu-item-text">{nav.name}</span>
                )}
              </Link>
            )
          )}
          {nav.subItems && (isExpanded || isHovered || isMobileOpen) && (
            <div
              ref={(el) => {
                subMenuRefs.current[`${menuType}-${index}`] = el;
              }}
              className="overflow-hidden transition-all duration-300"
              style={{
                height:
                  openSubmenu?.type === menuType && openSubmenu?.index === index
                    ? `${subMenuHeight[`${menuType}-${index}`]}px`
                    : '0px',
              }}
            >
              <ul className="mt-2 space-y-1 ml-9">
                {nav.subItems.map((subItem) => (
                  <li key={subItem.name}>
                    <Link
                      to={subItem.path}
                      className={`menu-dropdown-item ${
                        isActive(subItem.path)
                          ? 'menu-dropdown-item-active'
                          : 'menu-dropdown-item-inactive'
                      }`}
                    >
                      {subItem.name}
                      <span className="flex items-center gap-1 ml-auto">
                        {subItem.new && (
                          <span
                            className={`ml-auto ${
                              isActive(subItem.path)
                                ? 'menu-dropdown-badge-active'
                                : 'menu-dropdown-badge-inactive'
                            } menu-dropdown-badge`}
                          >
                            nuevo
                          </span>
                        )}
                        {subItem.pro && (
                          <span
                            className={`ml-auto ${
                              isActive(subItem.path)
                                ? 'menu-dropdown-badge-active'
                                : 'menu-dropdown-badge-inactive'
                            } menu-dropdown-badge`}
                          >
                            pro
                          </span>
                        )}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </li>
      ))}
    </ul>
  );

  return (
    <aside
      className={`fixed mt-0 lg:mt-0 flex flex-col top-0 px-5 left-0 bg-white dark:bg-gray-900 dark:border-gray-800 text-gray-900 h-screen transition-all duration-300 ease-in-out z-50 border-r border-gray-200 
        ${
          isExpanded || isMobileOpen
            ? 'w-[290px]'
            : isHovered
              ? 'w-[290px]'
              : 'w-[90px]'
        }
        ${isMobileOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0`}
      onMouseEnter={() => !isExpanded && setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div
        className={`py-8 flex ${
          !isExpanded && !isHovered ? 'lg:justify-center' : 'justify-start'
        }`}
      >
        <Link to="/">
          {isExpanded || isHovered || isMobileOpen ? (
            <>
              <img
                className="hidden sm:block dark:sm:hidden"
                src="/images/logo/PSI.png"
                alt="Logo"
                width={250}
                height={40}
              />
              <img
                className="hidden dark:sm:block"
                src="/images/logo/PSI.png"
                alt="Logo"
                width={250}
                height={40}
              />
            </>
          ) : (
            <img
              src="/images/logo/icon.png"
              alt="Logo"
              width={32}
              height={32}
            />
          )}
        </Link>
      </div>
      <div className="flex flex-col overflow-y-auto duration-300 ease-linear no-scrollbar">
        <nav className="mb-6">
          <div className="flex flex-col gap-4">
            <div>
              <h2
                className={`mb-4 text-xs uppercase flex leading-[20px] text-gray-400 ${
                  !isExpanded && !isHovered
                    ? 'lg:justify-center'
                    : 'justify-start'
                }`}
              >
                {isExpanded || isHovered || isMobileOpen ? (
                  'Principal'
                ) : (
                  <HorizontaLDots className="size-6" />
                )}
              </h2>
              {renderMenuItems(navItems, 'main')}
            </div>

          </div>
        </nav>
        {isExpanded || isHovered || isMobileOpen ? <SidebarWidget /> : null}
      </div>
    </aside>
  );
};

export default AppSidebar;
