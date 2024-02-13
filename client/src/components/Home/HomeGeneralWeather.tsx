import React, { useState, useEffect } from 'react';

const monthNames: { [index: string]: string } = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
  };


interface WeatherBlockData {
    city: string,
    temperature: number,
    datetime: string,
    weather_category: string
}

function getMonthName(month_num: string): string | undefined {
    return monthNames[month_num];
}

const WeatherBlock: React.FC<WeatherBlockData> = ({city, temperature, datetime, weather_category}) => {
    const date: string = datetime.split(" ")[0];
    const date_arr: string[] = date.split("-");
    
    const time: string = datetime.split(" ")[1];
    const time_arr: string[] = time.split(":");

    const month = getMonthName(date_arr[1]);
    
    return (
    <div className="flex flex-col items-start ml-4 mt-8 gap-2">
      <div className="text-white text-sm font-main">Location: <span className="text-weak-red/[.55]">{city}</span></div>
      <div className="text-white font-main">Temperature: <span className="text-weak-red/[.55]">{temperature}</span>°C</div>
      <div className="text-white font-main">{date_arr[0]} {month} {date_arr[2]} <span className="text-weak-red/[.55] ml-1">{time_arr[0] + ":" + time_arr[1]}</span></div>
      <div className="text-weak-red/[.55] font-main">{weather_category}</div>
    </div>
  );
};

export default WeatherBlock;
