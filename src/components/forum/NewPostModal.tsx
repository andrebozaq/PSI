import React, { useState } from 'react';
import { Modal } from '../ui/modal';

export interface NewPostData {
  title: string;
  category: string;
  content: string;
}

interface NewPostModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: NewPostData) => Promise<void>;
}

const CATEGORIES = ['Soportes', 'Materiales', 'Normativas', 'General'];

const NewPostModal: React.FC<NewPostModalProps> = ({ isOpen, onClose, onSubmit }) => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [titleError, setTitleError] = useState(false);
  const [contentError, setContentError] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const isTitleEmpty = !title.trim();
    const isContentEmpty = !content.trim();
    
    setTitleError(isTitleEmpty);
    setContentError(isContentEmpty);
    
    if (isTitleEmpty || isContentEmpty) return;

    setIsSubmitting(true);
    try {
      await onSubmit({ title, category, content });
      setTitle('');
      setCategory(CATEGORIES[0]);
      setContent('');
      onClose();
    } catch (error) {
      console.error('Error al enviar la pregunta:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} className="max-w-[600px] p-6 sm:p-10">
      <div className="mb-6">
        <h3 className="text-2xl font-semibold text-gray-800 dark:text-white/90">
          Nueva Pregunta
        </h3>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Publica tu duda o aporte para la comunidad de ingeniería.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <div>
          <label className="mb-2.5 block text-sm font-medium text-gray-800 dark:text-white/90">
            Título
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              if (e.target.value.trim()) setTitleError(false);
            }}
            placeholder="Ej. ¿Cómo calcular el espesor de un recipiente a presión?"
            className={`w-full rounded-lg border ${titleError ? 'border-red-500 focus:border-red-500 dark:border-red-500' : 'border-gray-300 focus:border-brand-500 dark:border-gray-700 dark:focus:border-brand-500'} bg-transparent px-5 py-3 text-gray-800 outline-none transition dark:bg-gray-900 dark:text-white/90`}
          />
          {titleError && (
            <p className="mt-1 text-xs text-red-500">Este campo es obligatorio</p>
          )}
        </div>

        <div>
          <label className="mb-2.5 block text-sm font-medium text-gray-800 dark:text-white/90">
            Categoría
          </label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full rounded-lg border border-gray-300 bg-transparent px-5 py-3 text-gray-800 outline-none transition focus:border-brand-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-500 appearance-none"
          >
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat} className="dark:bg-gray-900">
                {cat}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="mb-2.5 block text-sm font-medium text-gray-800 dark:text-white/90">
            Contenido
          </label>
          <textarea
            value={content}
            onChange={(e) => {
              setContent(e.target.value);
              if (e.target.value.trim()) setContentError(false);
            }}
            rows={5}
            placeholder="Describe tu pregunta o aporte con más detalle..."
            className={`w-full rounded-lg border ${contentError ? 'border-red-500 focus:border-red-500 dark:border-red-500' : 'border-gray-300 focus:border-brand-500 dark:border-gray-700 dark:focus:border-brand-500'} bg-transparent px-5 py-3 text-gray-800 outline-none transition dark:bg-gray-900 dark:text-white/90`}
          ></textarea>
          {contentError && (
            <p className="mt-1 text-xs text-red-500">Este campo es obligatorio</p>
          )}
        </div>

        <div className="mt-2 flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={onClose}
            className="rounded-lg border border-gray-300 px-5 py-2.5 text-center text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={isSubmitting}
            className="rounded-lg bg-brand-500 px-5 py-2.5 text-center text-sm font-medium text-white transition-colors hover:bg-brand-600 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Publicando...' : 'Publicar Pregunta'}
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default NewPostModal;
