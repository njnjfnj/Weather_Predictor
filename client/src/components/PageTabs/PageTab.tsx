import React from "react";
import {motion} from "framer-motion";

interface PageTabProps {
    label: string;
    isActive: boolean;
    onClick: () => void;
}

const PageTab: React.FC<PageTabProps> = ({label, isActive, onClick}) => {
    return(
        <motion.div
        whileHover={{
            WebkitTextDecorationColor: "weak-red",
            textUnderlineOffset: 4, 
            transition: { duration: 1 },
        }}
        whileTap={{ scale: 0.8 }}
        className={`bg-transparent cursor-pointer ${
        isActive ? 'text-white text-2xl font-main underline underline-offset-4 underline-red-500 hover:underline-red-600 duration-300' : 'text-weak-red font-main'
        }`}
        onClick={onClick}
    >
        {label}

        </motion.div>
    )
}
export default PageTab;