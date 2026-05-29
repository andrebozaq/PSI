import { useState } from 'react';
import FaqOne from '../../faqs/FaqOne';

const accordionData = [
  {
    title: 'Qué es PSI?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Esta aplicación es gratuita?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Esta aplicación se mantiene actualizada?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Puedo utilizar la app cuanto quiera?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Cuál es el próposito de esta app?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Cómo utilizo la app?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Será gratis para siempre?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Cuál es el alcance de esta app?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Cómo se financia este proyecto?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
  {
    title: 'Preguntas?',
    content: 'FILHO DA PUTA PREGUMTIAS FREKENTUES',
  },
];

export default function FaqsOne() {
  // State to track the currently open accordion
  const [openIndex, setOpenIndex] = useState<number | null>(0); // Initially open the first accordion

  const handleToggle = (index: number) => {
    setOpenIndex(openIndex === index ? null : index); // Close if open, otherwise open the clicked one
  };
  return (
    <div className="space-y-4">
      {accordionData.map((item, index) => (
        <FaqOne
          key={index}
          title={item.title}
          content={item.content}
          isOpen={openIndex === index} // Check if this accordion should be open
          toggleAccordion={() => handleToggle(index)} // Pass toggle function
        />
      ))}
    </div>
  );
}
