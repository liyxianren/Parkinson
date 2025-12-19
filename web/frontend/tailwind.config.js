/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 震颤卫士品牌色
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        // 严重度颜色
        severity: {
          0: '#10b981', // 无震颤 - 绿色
          1: '#84cc16', // 轻度 - 青绿
          2: '#eab308', // 中轻度 - 黄色
          3: '#f97316', // 中度 - 橙色
          4: '#ef4444', // 重度 - 红色
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
