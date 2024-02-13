import React, {useState} from "react";
import SearchBar from "../SearchBar"
import FeatureTabs from '../FeatureTabs/FeatureTabs';
import PageTabs from "../PageTabs/PageTabs"

const featureTabsData = [
  { label: 'weather', content: 'Weather' },
  { label: 'precipitation', content: 'Precipitation'},
  { label: 'wind', content: 'Wind'},
  { label: 'details', content: 'Details' },
];

const pageTabsData = [
  { label: 'tomorrow', content: 'Tomorrow'},
  { label: '10 days', content: '10 days'},

];

interface LayoutProps{
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({children}) => {
    const [activeFeatureTabIndex, setActiveFeatureTabIndex] = useState();
    const [activePageTabIndex, setActivePageTabIndex] = useState(0);
    
    const handleFeatureTabClick = (index: number) => setActiveFeatureTabIndex(index);
    const handlePageTabClick = (index: number) => setActivePageTabIndex(index);

    return (
    <main className="bg-black flex flex-col justify-between w-screen h-screen p-3">
        <SearchBar onSearch={(searchTerm: string) => {
            console.log(`Search term: ${searchTerm}`);
        }} />
        {children}

        <div className="flex flex-col justify-center items-center gap-y-12 mb-8">
            <FeatureTabs
            data={featureTabsData}
            activeTabIndex={activeFeatureTabIndex}
            onTabClick={handleFeatureTabClick}/>
            <PageTabs
            data={pageTabsData}
            activeTabIndex={activePageTabIndex}
            onTabClick={handlePageTabClick}/>


      </div>
    </main>
    )
}

export default Layout;


