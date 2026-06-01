import { useEffect, useState } from 'react';
import { collection, query, where, getDocs, addDoc, serverTimestamp } from 'firebase/firestore';
import { Link, useNavigate } from 'react-router';
import { db } from '../lib/firebaseConfig';
import { FiFileText, FiEdit, FiCopy, FiTrash2, FiSearch } from 'react-icons/fi';
import { useAuth } from '../contexts/AuthContext';
import { Table, TableHeader, TableBody, TableRow, TableCell } from '../components/ui/table';
import Badge from '../components/ui/badge/Badge';
import { Modal } from '../components/ui/modal';

export default function SavedProjects() {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [projectToDelete, setProjectToDelete] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [supportFilter, setSupportFilter] = useState('Todos');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const getProjectStatus = (project: any) => {
    const rows = project.results?.final?.verificationRows;
    if (!rows || rows.length === 0) return 'Pendiente';
    const hasFail = rows.some((r: any) => 
      String(r.status).toLowerCase().includes('no cumple') || 
      String(r.status).toLowerCase().includes('falla')
    );
    if (hasFail) return 'No cumple';
    return 'Cumple';
  };

  const getMiniSummary = (project: any) => {
    const inputs = project.inputs;
    if (!inputs) return 'N/A';
    const parts = [];
    if (inputs.outerDiameter) parts.push(`Ø ${inputs.outerDiameter} mm`);
    if (inputs.length) parts.push(`L: ${inputs.length} mm`);
    else if (inputs.height) parts.push(`H: ${inputs.height} mm`);
    return parts.length > 0 ? parts.join(' | ') : 'N/A';
  };

  const fetchProjects = async () => {
    if (!currentUser) return;
    try {
      const q = query(
        collection(db, 'studies'),
        where('userId', '==', currentUser.uid)
      );
      const querySnapshot = await getDocs(q);
      
      const docs = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));

      docs.sort((a: any, b: any) => {
        const timeA = a.createdAt?.toMillis ? a.createdAt.toMillis() : 0;
        const timeB = b.createdAt?.toMillis ? b.createdAt.toMillis() : 0;
        return timeB - timeA;
      });

      setProjects(docs);
    } catch (error) {
      console.error("Error obteniendo los proyectos:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDuplicate = async (project: any) => {
    try {
      const { id, ...projectData } = project; // Quitamos el ID viejo
      
      const newProject = {
        ...projectData,
        projectName: `${project.projectName || 'Sin título'} (Copia)`,
        createdAt: serverTimestamp(),
        updatedAt: serverTimestamp()
      };

      await addDoc(collection(db, 'studies'), newProject);
      await fetchProjects(); // Recargamos la tabla para ver la copia inmediatamente
    } catch (error) {
      console.error("Error al duplicar:", error);
    }
  };

  const confirmDelete = async () => {
    if (!projectToDelete) return;
    try {
      const { doc, deleteDoc } = await import('firebase/firestore');
      await deleteDoc(doc(db, 'studies', projectToDelete.id));
      setProjects(projects.filter((p) => p.id !== projectToDelete.id));
      setIsDeleteModalOpen(false);
      setProjectToDelete(null);
    } catch (error) {
      console.error('Error al borrar:', error);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, [currentUser]);

  const formatDate = (timestamp: any) => {
    if (!timestamp) return '-';
    const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp);
    return date.toLocaleDateString('es-VE', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const filteredProjects = projects.filter((p) => {
    const matchesSearch = (p.projectName || '').toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = supportFilter === 'Todos' || p.supportType === supportFilter;
    return matchesSearch && matchesFilter;
  });

  const totalItems = filteredProjects.length;
  const totalPages = Math.max(1, Math.ceil(totalItems / itemsPerPage));
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentProjects = filteredProjects.slice(startIndex, endIndex);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Diseños Guardados</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Historial de cálculos de soportes y análisis previos.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto">
          <div className="relative flex-grow sm:flex-grow-0 sm:w-64">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
              <FiSearch />
            </span>
            <input
              type="text"
              placeholder="Buscar proyecto..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setCurrentPage(1);
              }}
              className="h-10 w-full rounded-lg border border-gray-300 bg-white pl-10 pr-4 text-sm text-gray-700 outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500"
            />
          </div>
          <select
            value={supportFilter}
            onChange={(e) => {
              setSupportFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="h-10 rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-700 outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 dark:border-gray-700 dark:bg-gray-800 dark:text-white dark:focus:border-brand-500"
          >
            <option value="Todos">Todos los soportes</option>
            <option value="Saddle">Silletas (Saddle)</option>
            <option value="Skirt">Faldón (Skirt)</option>
            <option value="Leg">Patas (Legs)</option>
            <option value="Lug">Orejas (Lugs)</option>
            <option value="Ring">Anillo (Ring)</option>
          </select>
          <Link
            to="/soporte-diseno"
            className="flex h-10 items-center justify-center rounded-lg bg-brand-500 px-4 text-sm font-semibold text-white shadow-theme-sm transition hover:bg-brand-600"
          >
            + Nuevo Cálculo
          </Link>
        </div>
      </div>

      <div className="w-full overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-[#111c2a]">
        <div className="overflow-x-auto">
          {loading ? (
            <div className="flex h-32 items-center justify-center text-sm text-gray-500 dark:text-gray-400">
              Cargando base de datos...
            </div>
          ) : projects.length === 0 ? (
            <div className="flex h-32 items-center justify-center text-sm text-gray-500 dark:text-gray-400">
              No tienes proyectos guardados aún.
            </div>
          ) : (
            <Table className="divide-y divide-gray-200 dark:divide-gray-800">
              <TableHeader className="bg-gray-50 dark:bg-white/[0.02]">
                <TableRow>
                  <TableCell isHeader className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                    Proyecto / Recipiente
                  </TableCell>
                  <TableCell isHeader className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                    Soporte
                  </TableCell>
                  <TableCell isHeader className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                    Modalidad
                  </TableCell>
                  <TableCell isHeader className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                    Unidades
                  </TableCell>
                  <TableCell isHeader className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                    Fecha
                  </TableCell>
                  <TableCell isHeader className="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                    Estado
                  </TableCell>
                  <TableCell isHeader className="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
                    Acciones
                  </TableCell>
                </TableRow>
              </TableHeader>
              <TableBody className="divide-y divide-gray-200 dark:divide-gray-800">
                {currentProjects.map((project) => (
                  <TableRow key={project.id} className="transition hover:bg-gray-50 dark:hover:bg-white/[0.02]">
                    <TableCell className="whitespace-nowrap px-6 py-4">
                      <div className="font-medium text-gray-900 dark:text-white">
                        {project.projectName || 'Sin título'}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {getMiniSummary(project)}
                      </div>
                    </TableCell>
                    <TableCell className="whitespace-nowrap px-6 py-4 text-sm text-gray-700 dark:text-gray-300">
                      {project.supportType || '-'}
                    </TableCell>
                    <TableCell className="whitespace-nowrap px-6 py-4">
                      <Badge color={project.mode === 'design' ? 'info' : 'primary'} variant="light">
                        {project.mode === 'design' ? 'Diseño' : 'Análisis'}
                      </Badge>
                    </TableCell>
                    <TableCell className="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-700 dark:text-gray-300">
                      {project.unitSystem}
                    </TableCell>
                    <TableCell className="whitespace-nowrap px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {formatDate(project.createdAt)}
                    </TableCell>
                    <TableCell className="whitespace-nowrap px-6 py-4">
                      {(() => {
                        const status = project.calculationStatus;
                        if (status === 'PASS') {
                          return (
                            <div className="flex items-center gap-2.5 pl-1">
                              <span className="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_0_4px_rgba(16,185,129,0.2)]" />
                              <span className="text-sm font-medium text-emerald-700 dark:text-emerald-400">Cumple</span>
                            </div>
                          );
                        }
                        if (status === 'FAIL' || status === 'ERROR') {
                          return (
                            <div className="flex items-center gap-2.5 pl-1">
                              <span className="h-2 w-2 rounded-full bg-red-500 shadow-[0_0_0_4px_rgba(239,68,68,0.2)]" />
                              <span className="text-sm font-medium text-red-700 dark:text-red-400">No cumple</span>
                            </div>
                          );
                        }
                        return (
                          <div className="flex items-center gap-2.5 pl-1">
                            <span className="h-2 w-2 rounded-full bg-amber-500 shadow-[0_0_0_4px_rgba(245,158,11,0.2)]" />
                            <span className="text-sm font-medium text-amber-700 dark:text-amber-400">Pendiente</span>
                          </div>
                        );
                      })()}
                    </TableCell>
                    <TableCell className="whitespace-nowrap px-6 py-4 text-right text-sm font-medium">
                      <div className="flex items-center justify-end gap-3">
                        {project.mode !== 'analysis' && (
                          <button
                            title="Ver Reporte"
                            onClick={() => navigate('/soporte-diseno', { state: { project, jumpToStep: 7 } })}
                            className="text-gray-500 hover:text-brand-500 dark:text-gray-400 dark:hover:text-brand-400 transition"
                          >
                            <FiFileText size={18} />
                          </button>
                        )}
                        <button
                          title="Duplicar"
                          onClick={() => handleDuplicate(project)}
                          className="text-gray-500 hover:text-green-500 dark:text-gray-400 dark:hover:text-green-400 transition"
                        >
                          <FiCopy size={18} />
                        </button>
                        <button
                          title="Editar"
                          onClick={() => navigate(project.mode === 'analysis' ? '/soporte-analisis-editor' : '/soporte-diseno', { state: { project } })}
                          className="text-gray-500 hover:text-blue-500 dark:text-gray-400 dark:hover:text-blue-400 transition"
                        >
                          <FiEdit size={18} />
                        </button>
                        <button
                          title="Borrar"
                          onClick={() => {
                            setProjectToDelete(project);
                            setIsDeleteModalOpen(true);
                          }}
                          className="text-gray-500 hover:text-red-500 dark:text-gray-400 dark:hover:text-red-400 transition"
                        >
                          <FiTrash2 size={18} />
                        </button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </div>
        
        {totalItems > 0 && (
          <div className="flex items-center justify-between border-t border-gray-200 bg-gray-50 px-6 py-4 dark:border-gray-800 dark:bg-gray-900/50">
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Mostrando {startIndex + 1} a {Math.min(endIndex, totalItems)} de {totalItems} proyectos
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                disabled={currentPage === 1}
                onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                className="rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 transition hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                Anterior
              </button>
              <button
                type="button"
                disabled={currentPage === totalPages}
                onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                className="rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 transition hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
              >
                Siguiente
              </button>
            </div>
          </div>
        )}
      </div>

      <Modal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        className="max-w-[400px] p-6 text-center"
        showCloseButton={false}
      >
        <div className="mb-4 flex justify-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-400">
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </div>
        </div>
        <h3 className="mb-2 text-lg font-bold text-gray-900 dark:text-white">Eliminar Proyecto</h3>
        <p className="mb-6 text-sm text-gray-600 dark:text-gray-400">
          ¿Estás seguro de que deseas eliminar este proyecto? Esta acción no se puede deshacer.
        </p>
        <div className="flex gap-3">
          <button
            onClick={() => setIsDeleteModalOpen(false)}
            className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-700 transition hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700"
          >
            Cancelar
          </button>
          <button
            onClick={confirmDelete}
            className="w-full rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold text-white shadow-theme-sm transition hover:bg-red-700"
          >
            Eliminar
          </button>
        </div>
      </Modal>
    </div>
  );
}
