import React, {useState} from "react"
import type { HeadFC, PageProps } from "gatsby"
import WeatherBlock from "../../components/Home/HomeGeneralWeather"
import Thermometer from "../../components/Home/Thermometer"

import Layout from "../../components/Layout/Layout"

const TomorrowPage: React.FC<PageProps> = () => {
  
  return (
    <Layout>      
      <WeatherBlock city="Miami" temperature={23} datetime="29-06-2024 22:31:00" weather_category="Clouds"/>
      <Thermometer temperature={23}></Thermometer>
    </Layout>

  )
}

export default TomorrowPage

export const Head: HeadFC = () => <title>Tomorrow Weather</title>
