import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router';
import { doc, getDoc, getDocs, collection, onSnapshot, query, orderBy, addDoc, deleteDoc, updateDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '../lib/firebaseConfig';
import { useAuth } from '../contexts/AuthContext';
import { FiArrowLeft, FiClock, FiUser, FiMessageCircle, FiEdit2, FiTrash2 } from 'react-icons/fi';
import { Modal } from '../components/ui/modal';

interface Post {
  id: string;
  title: string;
  content: string;
  category: string;
  authorName: string;
  authorId: string;
  authorPhoto?: string;
  createdAt: any;
}

interface Comment {
  id: string;
  content: string;
  authorName: string;
  authorId: string;
  authorPhoto?: string;
  createdAt: any;
}

const PostDetail: React.FC = () => {
  const { postId } = useParams<{ postId: string }>();
  const navigate = useNavigate();
  const { userProfile, currentUser } = useAuth();

  const [post, setPost] = useState<Post | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [newComment, setNewComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [usersMap, setUsersMap] = useState<Record<string, string>>({});
  const [postToDelete, setPostToDelete] = useState(false);
  
  // Edit Comment State
  const [editingCommentId, setEditingCommentId] = useState<string | null>(null);
  const [editCommentContent, setEditCommentContent] = useState('');

  // Delete Comment State
  const [commentToDelete, setCommentToDelete] = useState<string | null>(null);

  // Fetch post details and listen to comments
  useEffect(() => {
    if (!postId) return;

    const fetchPost = async () => {
      try {
        const docRef = doc(db, 'posts', postId);
        const docSnap = await getDoc(docRef);
        if (docSnap.exists()) {
          setPost({ id: docSnap.id, ...docSnap.data() } as Post);
        } else {
          setPost(null);
        }
      } catch (error) {
        console.error('Error fetching post:', error);
      }
    };

    const fetchUsers = async () => {
      try {
        const usersSnap = await getDocs(collection(db, 'users'));
        const map: Record<string, string> = {};
        usersSnap.forEach((doc) => {
          map[doc.id] = doc.data().avatarUrl || '';
        });
        setUsersMap(map);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    fetchPost();
    fetchUsers();

    // Listen to comments subcollection
    const commentsRef = collection(db, 'posts', postId, 'comments');
    const q = query(commentsRef, orderBy('createdAt', 'asc'));
    
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const commentsData = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      })) as Comment[];
      setComments(commentsData);
      setLoading(false);
    }, (error) => {
      console.error('Error fetching comments:', error);
      setLoading(false);
    });

    return () => unsubscribe();
  }, [postId]);

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newComment.trim() || !postId) return;

    setIsSubmitting(true);
    try {
      const authorName = userProfile 
        ? `${userProfile.firstName} ${userProfile.lastName}`.trim() 
        : 'Usuario Anónimo';

      await addDoc(collection(db, 'posts', postId, 'comments'), {
        content: newComment,
        authorName,
        authorId: currentUser?.uid || 'anonymous',
        authorPhoto: currentUser?.photoURL || '',
        createdAt: serverTimestamp(),
      });
      setNewComment('');
    } catch (error) {
      console.error('Error adding comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteComment = async () => {
    if (!postId || !commentToDelete) return;
    try {
      await deleteDoc(doc(db, 'posts', postId, 'comments', commentToDelete));
      setCommentToDelete(null);
    } catch (error) {
      console.error('Error deleting comment:', error);
    }
  };

  const handleDeletePost = async () => {
    if (!postId) return;
    try {
      await deleteDoc(doc(db, 'posts', postId));
      navigate('/foro');
    } catch (error) {
      console.error('Error deleting post:', error);
    }
  };

  const handleStartEdit = (comment: Comment) => {
    setEditingCommentId(comment.id);
    setEditCommentContent(comment.content);
  };

  const handleCancelEdit = () => {
    setEditingCommentId(null);
    setEditCommentContent('');
  };

  const handleSaveEdit = async (commentId: string) => {
    if (!postId || !editCommentContent.trim()) return;
    try {
      await updateDoc(doc(db, 'posts', postId, 'comments', commentId), {
        content: editCommentContent
      });
      setEditingCommentId(null);
      setEditCommentContent('');
    } catch (error) {
      console.error('Error updating comment:', error);
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'Soportes': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
      case 'Materiales': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
      case 'Normativas': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400';
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const formatDate = (timestamp: any) => {
    if (!timestamp) return 'Justo ahora';
    const date = timestamp.toDate();
    return new Intl.DateTimeFormat('es-ES', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-solid border-brand-500 border-t-transparent"></div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="p-4 mx-auto max-w-screen-xl md:p-6 2xl:p-10 text-center">
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white/90">Pregunta no encontrada</h2>
        <button
          onClick={() => navigate('/foro')}
          className="mt-4 inline-flex items-center gap-2 text-brand-500 hover:text-brand-600 transition-colors"
        >
          <FiArrowLeft /> Volver al Foro
        </button>
      </div>
    );
  }

  return (
    <div className="p-4 mx-auto max-w-screen-xl md:p-6 2xl:p-10">
      <button
        onClick={() => navigate('/foro')}
        className="mb-6 inline-flex items-center gap-2 text-sm font-medium text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white transition-colors"
      >
        <FiArrowLeft className="h-4 w-4" />
        Volver al Foro
      </button>

      {/* Post Original */}
      <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] mb-8">
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between border-b border-gray-100 pb-6 dark:border-gray-800">
          <div>
            <span className={`inline-block rounded-full px-3 py-1 text-xs font-medium mb-3 ${getCategoryColor(post.category)}`}>
              {post.category}
            </span>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-gray-800 dark:text-white/90 break-words">
                {post.title}
              </h1>
              {currentUser?.uid === post.authorId && (
                <button
                  onClick={() => setPostToDelete(true)}
                  className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-colors"
                  title="Eliminar pregunta"
                >
                  <FiTrash2 className="h-5 w-5" />
                </button>
              )}
            </div>
          </div>
          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
            <div className="flex items-center gap-2 bg-gray-100 dark:bg-slate-800/60 px-3 py-1.5 rounded-full">
              {usersMap[post.authorId] || post.authorPhoto ? (
                <img src={usersMap[post.authorId] || post.authorPhoto} alt={post.authorName} className="h-5 w-5 rounded-full object-cover border border-gray-200 dark:border-gray-700" />
              ) : (
                <div className="h-5 w-5 rounded-full bg-brand-500/10 flex items-center justify-center text-brand-600 dark:text-brand-400">
                  <FiUser className="h-3.5 w-3.5" />
                </div>
              )}
              <span className="font-medium text-gray-700 dark:text-gray-300">{post.authorName}</span>
            </div>
            <div className="flex items-center gap-1.5 bg-gray-100 dark:bg-slate-800/60 px-3 py-1.5 rounded-full">
              <FiClock className="h-4 w-4" />
              <span>{formatDate(post.createdAt)}</span>
            </div>
          </div>
        </div>
        <div className="prose prose-sm dark:prose-invert max-w-none break-words text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
          {post.content}
        </div>
      </div>

      {/* Sección de Comentarios */}
      <div className="pl-0 sm:pl-8 border-l-0 sm:border-l-2 border-gray-100 dark:border-gray-800">
        <h3 className="mb-6 text-lg font-semibold text-gray-800 dark:text-white/90 flex items-center gap-2">
          <FiMessageCircle className="text-gray-400" />
          {comments.length} Respuestas
        </h3>

        {/* Lista de Comentarios */}
        <div className="flex flex-col gap-5 mb-8">
          {comments.length === 0 ? (
            <p className="text-sm text-gray-500 dark:text-gray-400 py-4 italic">
              Nadie ha respondido aún. ¡Sé el primero en aportar una solución!
            </p>
          ) : (
            comments.map((comment) => (
              <div 
                key={comment.id} 
                className="rounded-lg bg-gray-50/80 p-5 dark:bg-slate-800/40 border border-gray-100 dark:border-slate-800 shadow-sm group"
              >
                <div className="mb-3 flex items-center justify-between border-b border-gray-200/50 pb-3 dark:border-gray-700/50">
                  <div className="flex items-center gap-2 text-sm">
                    {usersMap[comment.authorId] || comment.authorPhoto ? (
                      <img src={usersMap[comment.authorId] || comment.authorPhoto} alt={comment.authorName} className="h-8 w-8 rounded-full object-cover shrink-0 border border-gray-200 dark:border-gray-700" />
                    ) : (
                      <div className="h-8 w-8 rounded-full bg-brand-500/10 flex items-center justify-center text-brand-600 dark:text-brand-400 shrink-0">
                        <FiUser className="h-4 w-4" />
                      </div>
                    )}
                    <span className="font-medium text-gray-800 dark:text-white/90 truncate">
                      {comment.authorName}
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    {/* Author Actions */}
                    {currentUser?.uid === comment.authorId && editingCommentId !== comment.id && (
                      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => handleStartEdit(comment)}
                          className="p-1 text-gray-400 hover:text-brand-500 hover:bg-brand-50 dark:hover:bg-brand-500/10 rounded transition-colors"
                          title="Editar respuesta"
                        >
                          <FiEdit2 className="h-3.5 w-3.5" />
                        </button>
                        <button
                          onClick={() => setCommentToDelete(comment.id)}
                          className="p-1 text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 rounded transition-colors"
                          title="Eliminar respuesta"
                        >
                          <FiTrash2 className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    )}
                    
                    <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 shrink-0">
                      <FiClock className="h-3.5 w-3.5" />
                      <span>{formatDate(comment.createdAt)}</span>
                    </div>
                  </div>
                </div>
                
                {editingCommentId === comment.id ? (
                  <div className="mt-2">
                    <textarea
                      value={editCommentContent}
                      onChange={(e) => setEditCommentContent(e.target.value)}
                      rows={3}
                      className="w-full rounded-lg border border-brand-300 bg-white px-3 py-2 text-sm text-gray-800 outline-none transition focus:border-brand-500 dark:border-brand-700 dark:bg-gray-900 dark:text-white/90"
                    />
                    <div className="mt-3 flex justify-end gap-2">
                      <button
                        onClick={handleCancelEdit}
                        className="rounded-lg px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800 transition-colors"
                      >
                        Cancelar
                      </button>
                      <button
                        onClick={() => handleSaveEdit(comment.id)}
                        disabled={!editCommentContent.trim()}
                        className="rounded-lg bg-brand-500 px-3 py-1.5 text-xs font-medium text-white hover:bg-brand-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Guardar
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="text-sm text-gray-700 dark:text-gray-300 break-words whitespace-pre-wrap">
                    {comment.content}
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Caja de Respuesta */}
        <div className="rounded-lg border border-gray-200 bg-white p-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
          <h4 className="mb-4 text-sm font-medium text-gray-800 dark:text-white/90">
            Escribe tu respuesta
          </h4>
          <form onSubmit={handleAddComment}>
            <textarea
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              rows={4}
              placeholder="Comparte tu conocimiento o haz sugerencias aquí..."
              required
              className="w-full rounded-lg border border-gray-300 bg-transparent px-4 py-3 text-sm text-gray-800 outline-none transition focus:border-brand-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-500"
            ></textarea>
            <div className="mt-4 flex justify-end">
              <button
                type="submit"
                disabled={isSubmitting || !newComment.trim()}
                className="rounded-lg bg-brand-500 px-6 py-2.5 text-sm font-medium text-white transition-colors hover:bg-brand-600 disabled:opacity-70 disabled:cursor-not-allowed shadow-sm"
              >
                {isSubmitting ? 'Publicando...' : 'Publicar Respuesta'}
              </button>
            </div>
          </form>
        </div>
      </div>

      <Modal isOpen={!!commentToDelete} onClose={() => setCommentToDelete(null)} className="max-w-md p-6">
        <div className="text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30 mb-4">
            <FiTrash2 className="h-6 w-6 text-red-600 dark:text-red-500" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">Eliminar respuesta</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            ¿Estás seguro de que quieres eliminar esta respuesta? Esta acción no se puede deshacer.
          </p>
          <div className="mt-6 flex justify-center gap-3">
            <button
              onClick={() => setCommentToDelete(null)}
              className="rounded-lg px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 dark:bg-slate-800 dark:border-slate-700 dark:text-gray-300 dark:hover:bg-slate-700 transition-colors"
            >
              Cancelar
            </button>
            <button
              onClick={handleDeleteComment}
              className="rounded-lg px-4 py-2.5 text-sm font-medium text-white bg-red-600 hover:bg-red-700 transition-colors"
            >
              Eliminar
            </button>
          </div>
        </div>
      </Modal>
      <Modal isOpen={postToDelete} onClose={() => setPostToDelete(false)} className="max-w-md p-6">
        <div className="text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30 mb-4">
            <FiTrash2 className="h-6 w-6 text-red-600 dark:text-red-500" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">Eliminar pregunta</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            ¿Estás seguro de que quieres eliminar esta pregunta y todas sus respuestas? Esta acción no se puede deshacer.
          </p>
          <div className="mt-6 flex justify-center gap-3">
            <button
              onClick={() => setPostToDelete(false)}
              className="rounded-lg px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 dark:bg-slate-800 dark:border-slate-700 dark:text-gray-300 dark:hover:bg-slate-700 transition-colors"
            >
              Cancelar
            </button>
            <button
              onClick={handleDeletePost}
              className="rounded-lg px-4 py-2.5 text-sm font-medium text-white bg-red-600 hover:bg-red-700 transition-colors"
            >
              Eliminar
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default PostDetail;
