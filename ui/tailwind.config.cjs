/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // spacing
      spacing: {
        '54': '215px',
      },
    },

    // google font
    fontFamily: {
      'quicksand': 'Quicksand, sans-serif',
    },
  },
  plugins: [
    require('tailwind-scrollbar-hide'),
  ],
}
