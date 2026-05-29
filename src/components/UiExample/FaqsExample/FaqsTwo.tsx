import { useState } from 'react';
import FaqTwo from '../../faqs/FaqTwo';

const accordionTwoData = [
  {
    title: 'Qué es PSI?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Esta aplicación es gratuita?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Esta aplicación se mantiene actualizada?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Puedo utilizar la app cuanto quiera?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Cuál es el próposito de esta app?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Cómo utilizo la app?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Será gratis para siempre?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Cuál es el alcance de esta app?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Cómo se financia este proyecto?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
  {
    title: 'Preguntas?',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec quis magna ac nibh malesuada consectetur at vitae ipsum orem ipsum dolor sit amet, consectetur adipiscing elit nam fermentum, leo et lacinia accumsan.',
  },
];

export default function FaqsTwo() {
  // State to manage the open accordion for both groups separately
  const [openIndexFirstGroup, setOpenIndexFirstGroup] = useState<number | null>(
    0
  );
  const [openIndexSecondGroup, setOpenIndexSecondGroup] = useState<
    number | null
  >(0);

  // Handle toggle for first group
  const handleToggleFirstGroup = (index: number) => {
    setOpenIndexFirstGroup(openIndexFirstGroup === index ? null : index);
  };

  // Handle toggle for second group
  const handleToggleSecondGroup = (index: number) => {
    setOpenIndexSecondGroup(openIndexSecondGroup === index ? null : index);
  };

  // A
  // A reusable function to render the FAQ items
  const renderFaqItems = (
    data: typeof accordionTwoData,
    openIndex: number | null,
    handleToggle: (index: number) => void
  ) =>
    data.map((item, index) => (
      <FaqTwo
        key={index}
        title={item.title}
        content={item.content}
        isOpen={openIndex === index}
        toggleAccordionTwo={() => handleToggle(index)}
      />
    ));
  return (
    <div className="grid gird-cols-1 gap-x-8 gap-y-5 xl:grid-cols-2">
      <div className="space-y-3">
        {renderFaqItems(
          accordionTwoData.slice(0, 3),
          openIndexFirstGroup,
          handleToggleFirstGroup
        )}{' '}
        {/* First group */}
      </div>
      <div className="space-y-3">
        {renderFaqItems(
          accordionTwoData.slice(3, 7),
          openIndexSecondGroup,
          handleToggleSecondGroup
        )}{' '}
        {/* Second group */}
      </div>
    </div>
  );
}
