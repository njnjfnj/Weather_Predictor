import React from 'react';
import { motion } from 'framer-motion';
interface FeatureTabProps {
  label: string;
  isActive: boolean;
  onClick: () => void;
}

const FeatureTab: React.FC<FeatureTabProps> = ({ label, isActive, onClick }) => {
    return (<motion.div
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className={`tab p-2 cursor-pointer ${
        isActive ? 'bg-white text-gray-800 font-main' : 'font-main text-white text-white'
        }`}
        onClick={onClick}
    >
        {label}
    </motion.div>)
};

export default FeatureTab;
