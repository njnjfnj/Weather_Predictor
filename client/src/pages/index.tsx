import * as React from "react"
import type { HeadFC, PageProps } from "gatsby"
import SearchBar from "../components/SearchBar"
import WeatherBlock from "../components/HomeGeneralWeather"
import Thermometer from "../components/Thermometer"
import HorizontalSliderTabs from "../components/HorizontalSliderTabs"
const IndexPage: React.FC<PageProps> = () => {
  return (
    <main className="bg-black flex flex-col justify-between w-screen h-screen p-3">
      <SearchBar onSearch={(searchTerm: string) => {
        console.log(`Search term: ${searchTerm}`);
      }} />
      <WeatherBlock city="Miami" temperature={23} datetime="29-06-2024 22:31:00" weather_category="Clouds"/>
      <Thermometer temperature={23}></Thermometer>
      <HorizontalSliderTabs/>
    </main>
  )
}

export default IndexPage

export const Head: HeadFC = () => <title>Home Page</title>
