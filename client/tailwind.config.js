/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    `./src/pages/**/*.{js,jsx,ts,tsx}`,
    `./src/components/**/*.{js,jsx,ts,tsx}`,
  ],
  theme: {
    extend: {
      colors: {
        'weak-red': '#FF0000',
      },
      fontFamily:{
        'main': ['main']
      }
    },
  },
  plugins: [],
}
