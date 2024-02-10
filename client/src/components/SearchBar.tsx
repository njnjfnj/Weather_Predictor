import React, { useState } from 'react';

interface SearchBarProps {
  onSearch: (searchTerm: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSearch(searchTerm);
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center">
      <input
        type="text"
        placeholder="Find city..."
        className="font-main placeholder:text-slate-400 rounded-lg text-white placeholder:text-white px-3 py-2  bg-weak-red/[.25] focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-100 w-full "
        value={searchTerm}
        onChange={handleChange}
      />
      <button type="submit" className="flex items-center absolute right-5 top-4">
            <svg width="32" height="32" viewBox="0 0 46 46" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M30.5909 0C26.6439 0 22.6948 1.50222 19.6884 4.50864C13.895 10.3021 13.6847 19.5901 19.0558 25.6387L17.4973 27.1938L18.8057 28.5023L20.3611 26.944C26.4093 32.3151 35.697 32.1048 41.4905 26.3113C47.5031 20.2986 47.5032 10.5214 41.4905 4.50873C38.4843 1.50222 34.5383 0 30.5909 0ZM30.5909 1.83304C34.062 1.83304 37.5316 3.16027 40.1853 5.81404C45.4927 11.1215 45.4926 19.6986 40.1853 25.0059C35.0971 30.0942 27.0061 30.3032 21.6696 25.6354L21.6911 25.614C21.4591 25.4115 21.2302 25.2022 21.0092 24.9813C20.7912 24.7634 20.5857 24.5373 20.3857 24.3086L20.3642 24.3303C15.6963 18.9937 15.9054 10.9024 20.9937 5.81404C23.6475 3.16027 27.1198 1.83304 30.5909 1.83304ZM15.0996 27.4038L1.78679 40.7168L5.1998 44.1299L18.5127 30.8168L15.0996 27.4038ZM1.58001 43.1177L0 44.6945L1.30548 46L2.88233 44.42L1.58001 43.1177Z" fill="white"/>
        </svg>
      </button>
    </form>
  );
};

export default SearchBar;
