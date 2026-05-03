/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "on-primary-fixed": "#001f27",
        "on-primary": "#003642",
        "primary": "#8bd1e8",
        "inverse-on-surface": "#20333b",
        "on-error": "#690005",
        "primary-container": "#005f73",
        "on-secondary": "#003738",
        "outline": "#899296",
        "on-secondary-container": "#002f30",
        "secondary-container": "#28a0a3",
        "surface": "#02161d",
        "surface-variant": "#24373f",
        "on-tertiary-fixed": "#002018",
        "on-tertiary-container": "#9bd9c4",
        "tertiary-fixed": "#b0efda",
        "surface-container": "#0e2229",
        "on-error-container": "#ffdad6",
        "inverse-surface": "#d1e6f0",
        "secondary": "#6bd7da",
        "tertiary-fixed-dim": "#95d3be",
        "primary-fixed-dim": "#8bd1e8",
        "on-secondary-fixed": "#002021",
        "inverse-primary": "#13677b",
        "surface-container-lowest": "#001017",
        "secondary-fixed": "#89f3f6",
        "on-primary-container": "#91d7ee",
        "surface-container-highest": "#24373f",
        "error": "#ffb4ab",
        "background": "#02161d",
        "surface-container-high": "#192d34",
        "tertiary-container": "#226150",
        "on-primary-fixed-variant": "#004e5f",
        "on-background": "#d1e6f0",
        "on-surface": "#d1e6f0",
        "secondary-fixed-dim": "#6bd7da",
        "on-tertiary": "#00382c",
        "on-surface-variant": "#bfc8cc",
        "outline-variant": "#3f484c",
        "on-secondary-fixed-variant": "#004f51",
        "error-container": "#93000a",
        "surface-tint": "#8bd1e8",
        "surface-bright": "#293c44",
        "tertiary": "#95d3be",
        "surface-dim": "#02161d",
        "on-tertiary-fixed-variant": "#0b5040",
        "primary-fixed": "#b2ebff",
        "surface-container-low": "#0a1e25"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      spacing: {
        "lg": "2.5rem",
        "margin": "2rem",
        "sm": "1rem",
        "md": "1.5rem",
        "xl": "4rem",
        "gutter": "1.5rem",
        "unit": "8px",
        "xs": "0.5rem"
      },
      fontFamily: {
        "headline-lg": ["Manrope"],
        "body-md": ["Manrope"],
        "display-xl": ["Manrope"],
        "headline-md": ["Manrope"],
        "body-lg": ["Manrope"],
        "label-md": ["Manrope"]
      },
      fontSize: {
        "headline-lg": ["2.5rem", {"lineHeight": "1.2", "letterSpacing": "-0.01em", "fontWeight": "700"}],
        "body-md": ["1rem", {"lineHeight": "1.6", "fontWeight": "400"}],
        "display-xl": ["4.5rem", {"lineHeight": "1.1", "letterSpacing": "-0.02em", "fontWeight": "800"}],
        "headline-md": ["2rem", {"lineHeight": "1.3", "fontWeight": "600"}],
        "body-lg": ["1.125rem", {"lineHeight": "1.6", "fontWeight": "400"}],
        "label-md": ["0.875rem", {"lineHeight": "1", "letterSpacing": "0.05em", "fontWeight": "600"}]
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}
