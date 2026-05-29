import ChatBoxHeader from './ChatBoxHeader';
import ChatBoxSendForm from './ChatBoxSendForm';

interface ChatItem {
  id: number;
  name: string;
  role: string;
  profileImage: string;
  status: 'online' | 'offline';
  lastActive: string;
  message: string;
  isSender: boolean;
  imagePreview?: string;
}

const chatList: ChatItem[] = [
  {
    id: 1,
    name: 'Rulei',
    role: 'Estudiante - Luz',
    profileImage: './images/user/user-03.png',
    status: 'online',
    lastActive: '15 mins',
    message: 'Hacemos algo el finde?',
    isSender: false,
  },
  {
    id: 2,
    name: 'Rafita  ',
    role: 'Tesista - Luz',
    profileImage: './images/user/user-04.png',
    status: 'online',
    lastActive: '30 mins',
    message: 'Sisa, me llevo al mordisquin',
    isSender: false,
  },
  {
    id: 3,
    name: 'You',
    role: 'Tesista - Luz',
    profileImage: '',
    status: 'online',
    lastActive: 'Hace 2 horas',
    message: 'Voy pegao',
    isSender: true,
  },
  {
    id: 4,
    name: 'Rafita',
    role: 'Tesista - Luz',
    profileImage: './images/user/user-04.png',
    status: 'online',
    lastActive: 'Hace 2 horas',
    message: 'Le decimos a fruty o q',
    isSender: false,
  },
  {
    id: 5,
    name: 'You',
    role: 'Tesista - Luz',
    profileImage: '',
    status: 'online',
    lastActive: 'Hace 2 horas',
    message: 'Mmm dale sisa',
    isSender: true,
  },
  {
    id: 6,
    name: 'Rulei',
    role: 'Estudiante - Luz',
    profileImage: './images/user/user-03.png',
    status: 'online',
    lastActive: 'Hace 2 horas',
    message: 'Aquí será la jodita xD',
    isSender: false,
    imagePreview: './images/chat/chat.jpg',
  },
];

export default function ChatBox() {
  return (
    <div className="flex h-full flex-col overflow-hidden rounded-2xl border border-gray-200 bg-white dark:border-gray-800 dark:bg-white/[0.03] xl:w-3/4">
      {/* <!-- ====== Chat Box Start --> */}
      <ChatBoxHeader />
      <div className="flex-1 max-h-full p-5 space-y-6 overflow-auto custom-scrollbar xl:space-y-8 xl:p-6">
        {chatList.map((chat) => (
          <div
            key={chat.id}
            className={`flex ${
              chat.isSender ? 'justify-end' : 'items-start gap-4'
            }`}
          >
            {!chat.isSender && (
              <div className="w-10 h-10 overflow-hidden rounded-full">
                <img
                  src={chat.profileImage}
                  alt={`${chat.name} profile`}
                  className="object-cover object-center w-full h-full"
                />
              </div>
            )}

            <div className={`${chat.isSender ? 'text-right' : ''}`}>
              {chat.imagePreview && (
                <div className="mb-2 w-full max-w-[270px] overflow-hidden rounded-lg">
                  <img
                    src={chat.imagePreview}
                    alt="chat"
                    className="object-cover"
                  />
                </div>
              )}

              <div
                className={`px-3 py-2 rounded-lg ${
                  chat.isSender
                    ? 'bg-brand-500 text-white dark:bg-brand-500'
                    : 'bg-gray-100 dark:bg-white/5 text-gray-800 dark:text-white/90'
                } ${chat.isSender ? 'rounded-tr-sm' : 'rounded-tl-sm'}`}
              >
                <p className="text-sm ">{chat.message}</p>
              </div>
              <p className="mt-2 text-gray-500 text-theme-xs dark:text-gray-400">
                {chat.isSender
                  ? chat.lastActive
                  : `${chat.name}, ${chat.lastActive}`}
              </p>
            </div>
          </div>
        ))}
      </div>
      <ChatBoxSendForm />
      {/* <!-- ====== Chat Box End --> */}
    </div>
  );
}
