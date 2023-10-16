/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./movies/templates/movies/basic2.html"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}

