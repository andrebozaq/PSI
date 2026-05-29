import { useState } from 'react';
import { TbRulerMeasure2 } from 'react-icons/tb';
import { FaTemperatureLow } from 'react-icons/fa';
import { LuCircleGauge } from 'react-icons/lu';
import { MdOutlineTimer } from 'react-icons/md';
import { LuWeight } from 'react-icons/lu';
import { SlEnergy } from 'react-icons/sl';
import { FaFill } from 'react-icons/fa';

export interface TabData {
  id: string;
  label: string;
  icon: React.ReactNode;
  content: string;
}

interface TabButtonProps extends TabData {
  isActive: boolean;
  onClick: () => void;
}

const tabData: TabData[] = [
  {
    id: 'longitud',
    label: 'Longitud',
    icon: <TbRulerMeasure2 />,
    content:
      'Longitud ipsum dolor sit amet consectetur. Non vitae facilisis urna tortor placerat egestas donec. Faucibus diam gravida enim elit lacus a. Tincidunt fermentum condimentum quis et a et tempus. Tristique urna nisi nulla elit sit libero scelerisque ante.',
  },
  {
    id: 'temperatura',
    label: 'Temperatura',
    icon: <FaTemperatureLow />,
    content:
      'Temperatura ipsum dolor sit amet consectetur. Non vitae facilisis urna tortor placerat egestas donec. Faucibus diam gravida enim elit lacus a. Tincidunt fermentum condimentum quis et a et tempus. Tristique urna nisi nulla elit sit libero scelerisque ante.',
  },
  {
    id: 'presion',
    label: 'Presión',
    icon: <LuCircleGauge />,
    content:
      'Presión ipsum dolor sit amet consectetur. Non vitae facilisis urna tortor placerat egestas donec. Faucibus diam gravida enim elit lacus a. Tincidunt fermentum condimentum quis et a et tempus. Tristique urna nisi nulla elit sit libero scelerisque ante.',
  },
  {
    id: 'volumen',
    label: 'Volumen',
    icon: <FaFill />,
    content:
      'Volumen ipsum dolor sit amet consectetur. Non vitae facilisis urna tortor placerat egestas donec. Faucibus diam gravida enim elit lacus a. Tincidunt fermentum condimentum quis et a et tempus. Tristique urna nisi nulla elit sit libero scelerisque ante.',
  },
  {
    id: 'tiempo',
    label: 'Tiempo',
    icon: <MdOutlineTimer />,
    content:
      'Tiempo ipsum dolor sit amet consectetur. Non vitae facilisis urna tortor placerat egestas donec. Faucibus diam gravida enim elit lacus a. Tincidunt fermentum condimentum quis et a et tempus. Tristique urna nisi nulla elit sit libero scelerisque ante.',
  },
  {
    id: 'peso',
    label: 'Peso',
    icon: <LuWeight />,
    content:
      'Peso ipsum dolor sit amet consectetur. Non vitae facilisis urna tortor placerat egestas donec. Faucibus diam gravida enim elit lacus a. Tincidunt fermentum condimentum quis et a et tempus. Tristique urna nisi nulla elit sit libero scelerisque ante.',
  },
  {
    id: 'energia',
    label: 'Energía',
    icon: <SlEnergy />,
    content:
      'Energía ipsum dolor sit amet consectetur. Non vitae facilisis urna tortor placerat egestas donec. Faucibus diam gravida enim elit lacus a. Tincidunt fermentum condimentum quis et a et tempus. Tristique urna nisi nulla elit sit libero scelerisque ante.',
  },
];

const TabButton: React.FC<TabButtonProps> = ({
  label,
  icon,
  isActive,
  onClick,
}) => {
  return (
    <button
      className={`inline-flex items-center gap-2 border-b-2 px-2.5 py-2 text-sm font-medium transition-colors duration-200 ${
        isActive
          ? 'text-brand-500 border-brand-500 dark:text-brand-400 dark:border-brand-400'
          : 'text-gray-500 border-transparent hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
      }`}
      onClick={onClick}
    >
      {icon}
      {label}
    </button>
  );
};

interface TabContentProps {
  content: string;
  isActive: boolean;
}

const TabContent: React.FC<TabContentProps> = ({ content, isActive }) => {
  if (!isActive) return null;

  return (
    <div>
      <p className="text-sm text-gray-500 dark:text-gray-400">{content}</p>
    </div>
  );
};

export default function TabWithUnderlineAndIcon() {
  const [activeTab, setActiveTab] = useState<TabData['id']>(tabData[0].id);

  return (
    <div className="p-6 border border-gray-200 rounded-xl dark:border-gray-800">
      <div className="border-b border-gray-200 dark:border-gray-800">
        <nav className="flex space-x-2 overflow-x-auto scrollbar-thin scrollbar-thumb-gray-200 dark:scrollbar-thumb-gray-600">
          {tabData.map((tab) => (
            <TabButton
              key={tab.id}
              {...tab}
              isActive={activeTab === tab.id}
              onClick={() => setActiveTab(tab.id)}
            />
          ))}
        </nav>
      </div>

      <div className="pt-4">
        {tabData.map((tab) => (
          <TabContent
            key={tab.id}
            content={tab.content}
            isActive={activeTab === tab.id}
          />
        ))}
      </div>
    </div>
  );
}
