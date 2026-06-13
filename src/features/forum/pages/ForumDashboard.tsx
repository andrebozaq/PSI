import React, { useEffect, useState } from 'react';
import { collection, onSnapshot, getDocs, query, orderBy, addDoc, serverTimestamp, limit } from 'firebase/firestore';
import { db } from '../../../config/firebase';
import { useAuth } from '../../auth/contexts/AuthContext';
import NewPostModal, { NewPostData } from '../components/NewPostModal';
import { FiMessageSquare, FiClock, FiUser, FiSearch } from 'react-icons/fi';
import { useNavigate } from 'react-router';

interface Post {
  id: string;
  title: string;
  content: string;
  category: string;
  authorName: string;
  authorId: string;
  authorPhoto?: string;
  createdAt: any; // Firestore timestamp
}

const ForumDashboard: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [usersMap, setUsersMap] = useState<Record<string, string>>({});
  const { userProfile, currentUser } = useAuth();
  const navigate = useNavigate();

  const [searchTerm, setSearchTerm] = useState('');
  const [postLimit, setPostLimit] = useState(12);
  const [hasMore, setHasMore] = useState(true);

  // Escuchar posts de Firestore en tiempo real
  useEffect(() => {
    const q = query(collection(db, 'posts'), orderBy('createdAt', 'desc'), limit(postLimit));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const postsData = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      })) as Post[];
      setPosts(postsData);
      setHasMore(postsData.length === postLimit);
      setLoading(false);
    }, (error) => {
      console.error("Error fetching posts:", error);
      setLoading(false);
    });

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

    fetchUsers();

    return () => unsubscribe();
  }, [postLimit]);

  const filteredPosts = posts.filter(post => 
    post.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
    post.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleCreatePost = async (data: NewPostData) => {
    try {
      const authorName = userProfile 
        ? `${userProfile.firstName} ${userProfile.lastName}`.trim() 
        : 'Usuario Anónimo';
      
      await addDoc(collection(db, 'posts'), {
        ...data,
        authorName,
        authorId: currentUser?.uid || 'anonymous',
        authorPhoto: currentUser?.photoURL || '',
        createdAt: serverTimestamp(),
      });
    } catch (error) {
      console.error('Error adding document: ', error);
      throw error;
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

  return (
    <div className="p-4 mx-auto max-w-screen-2xl md:p-6 2xl:p-10">
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white/90 flex items-center gap-2">
            <FiMessageSquare className="text-brand-500" />
            Foro Global de Ingeniería
          </h2>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Comparte tus dudas, debate normativas y conecta con otros ingenieros.
          </p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="inline-flex items-center justify-center rounded-lg bg-brand-500 px-6 py-3 text-center font-medium text-white hover:bg-brand-600 transition-colors shadow-sm"
        >
          Nueva Pregunta
        </button>
      </div>

      <div className="mb-6 relative max-w-md">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <FiSearch className="text-gray-400" />
        </div>
        <input
          type="text"
          placeholder="Buscar preguntas..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-10 pr-4 text-sm text-gray-800 outline-none transition focus:border-brand-500 dark:border-gray-700 dark:bg-gray-900 dark:text-white/90 dark:focus:border-brand-500 shadow-sm"
        />
      </div>

      {loading && posts.length === 0 ? (
        <div className="flex items-center justify-center h-64">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-solid border-brand-500 border-t-transparent"></div>
        </div>
      ) : posts.length === 0 ? (
        <div className="rounded-xl border border-gray-200 bg-white p-10 text-center dark:border-gray-800 dark:bg-white/[0.03]">
          <FiMessageSquare className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-800 dark:text-white/90">No se encontraron preguntas</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Intenta con otros términos de búsqueda o sé el primero en iniciar una discusión.
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3">
            {filteredPosts.map((post) => (
            <div
              key={post.id}
              onClick={() => navigate(`/foro/${post.id}`)}
              className="flex flex-col rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-white/[0.03] transition-transform hover:-translate-y-1 hover:shadow-md cursor-pointer group"
            >
              <div className="mb-4 flex items-start justify-between gap-2">
                <span className={`inline-block rounded-full px-3 py-1 text-xs font-medium ${getCategoryColor(post.category)}`}>
                  {post.category}
                </span>
              </div>
              <h4 className="mb-3 text-lg font-semibold text-gray-800 dark:text-white/90 line-clamp-2 break-words">
                {post.title}
              </h4>
              <p className="mb-6 text-sm text-gray-500 dark:text-gray-400 line-clamp-3 break-words flex-grow">
                {post.content}
              </p>
              
              <div className="mt-auto flex items-center justify-between border-t border-gray-100 pt-4 dark:border-gray-800">
                <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                  {usersMap[post.authorId] || post.authorPhoto ? (
                    <img src={usersMap[post.authorId] || post.authorPhoto} alt={post.authorName} className="h-4 w-4 rounded-full object-cover border border-gray-200 dark:border-gray-700" />
                  ) : (
                    <div className="h-4 w-4 rounded-full bg-brand-500/10 flex items-center justify-center text-brand-600 dark:text-brand-400">
                      <FiUser className="h-3 w-3" />
                    </div>
                  )}
                  <span className="font-medium text-gray-700 dark:text-gray-300">{post.authorName}</span>
                </div>
                <div className="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400">
                  <FiClock className="h-3 w-3" />
                  <span>{formatDate(post.createdAt)}</span>
                </div>
              </div>
            </div>
          ))}
          </div>

          {hasMore && !searchTerm && (
            <div className="mt-8 text-center">
              <button
                onClick={() => setPostLimit(prev => prev + 12)}
                className="inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-6 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 transition-colors"
              >
                Cargar más preguntas
              </button>
            </div>
          )}
        </>
      )}

      <NewPostModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreatePost}
      />
    </div>
  );
};

export default ForumDashboard;
