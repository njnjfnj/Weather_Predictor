import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import PageTab from './PageTab';

interface PageTabsProps {
  data: { label: string; content: string }[];
  activeTabIndex: number;
  onTabClick: (index: number) => void;
}


const PageTabs: React.FC<PageTabsProps> = ({
  data,
  activeTabIndex,
  onTabClick,
}) => {
  const [containerWidth, setContainerWidth] = useState(0);

  useEffect(() => {
    const updateWidth = () => setContainerWidth(window.innerWidth);
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, []);

  return (
    <motion.div
      whileDrag={{ x: -Math.min(0, data.length - 1) * containerWidth }}
      onDragEnd={(e) => {
        const offset = e.drag.x / containerWidth;
        if (Math.abs(offset) > 0.5) {
          onTabClick(
            activeTabIndex + (offset > 0 ? 1 : -1) % data.length
          );
        }
      }}
      dragConstraints={{ left: 0, right: 0 }}
      className="container flex justify-center gap-7 overflow-x-auto"
    >
      {data.map((tab, index) => (
        <PageTab
          key={index}
          label={tab.label}
          isActive={activeTabIndex === index}
          onClick={() => onTabClick(index)}
        />
      ))}
    </motion.div>
  );
};

export default PageTabs;

