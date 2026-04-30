---
name: Abyssal Luxury
colors:
  surface: '#02161d'
  surface-dim: '#02161d'
  surface-bright: '#293c44'
  surface-container-lowest: '#001017'
  surface-container-low: '#0a1e25'
  surface-container: '#0e2229'
  surface-container-high: '#192d34'
  surface-container-highest: '#24373f'
  on-surface: '#d1e6f0'
  on-surface-variant: '#bfc8cc'
  inverse-surface: '#d1e6f0'
  inverse-on-surface: '#20333b'
  outline: '#899296'
  outline-variant: '#3f484c'
  surface-tint: '#8bd1e8'
  primary: '#8bd1e8'
  on-primary: '#003642'
  primary-container: '#005f73'
  on-primary-container: '#91d7ee'
  inverse-primary: '#13677b'
  secondary: '#6bd7da'
  on-secondary: '#003738'
  secondary-container: '#28a0a3'
  on-secondary-container: '#002f30'
  tertiary: '#95d3be'
  on-tertiary: '#00382c'
  tertiary-container: '#226150'
  on-tertiary-container: '#9bd9c4'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#b2ebff'
  primary-fixed-dim: '#8bd1e8'
  on-primary-fixed: '#001f27'
  on-primary-fixed-variant: '#004e5f'
  secondary-fixed: '#89f3f6'
  secondary-fixed-dim: '#6bd7da'
  on-secondary-fixed: '#002021'
  on-secondary-fixed-variant: '#004f51'
  tertiary-fixed: '#b0efda'
  tertiary-fixed-dim: '#95d3be'
  on-tertiary-fixed: '#002018'
  on-tertiary-fixed-variant: '#0b5040'
  background: '#02161d'
  on-background: '#d1e6f0'
  surface-variant: '#24373f'
typography:
  display-xl:
    fontFamily: Manrope
    fontSize: 4.5rem
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 2.5rem
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Manrope
    fontSize: 2rem
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Manrope
    fontSize: 1.125rem
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Manrope
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Manrope
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  xs: 0.5rem
  sm: 1rem
  md: 1.5rem
  lg: 2.5rem
  xl: 4rem
  gutter: 1.5rem
  margin: 2rem
---

## Brand & Style

The design system is built upon a narrative of "Abyssal Luxury"—an immersive, high-end experience that mirrors the mysterious and serene depths of the ocean. It targets a sophisticated audience that values exclusivity, technological precision, and visual tranquility.

The aesthetic utilizes **Glassmorphism** as its core structural driver. By layering translucent surfaces with varying degrees of background blur, the UI achieves a sense of fluid depth. Elements are not merely placed on a screen; they float within a volumetric space. The style is punctuated by **glowing accents** and ultra-thin borders that mimic the bioluminescence found in deep-sea environments, ensuring a modern, high-contrast, yet ethereal user experience.

## Colors

The color palette transitions from the impenetrable dark of the deep ocean to the vibrant shimmer of coastal waters. 

- **Primary (#005F73):** Used for structural depth and heavy interactive states.
- **Secondary (#0A9396):** The core action color, representing clarity and movement.
- **Tertiary (#94D2BD):** A soft, luminous teal reserved for high-visibility accents, success states, and delicate borders.
- **Neutral (#001219):** The "Midnight" base. This is the foundation of the dark mode, providing a rich, near-black canvas that allows cyan and teal accents to pop.

Apply glows using the Secondary and Tertiary colors with low-opacity radial gradients to simulate bioluminescent light casting.

## Typography

The design system utilizes **Manrope** (as the closest premium alternative to Outfit) to maintain a contemporary, geometric, and highly readable feel. 

Headlines should be bold and commanding, utilizing tighter letter spacing to create a sense of prestige. Body text remains airy with generous line heights to ensure legibility against dark, blurred backgrounds. Labels and small metadata should utilize increased letter spacing and uppercase styling to provide a technical, "instrument-panel" aesthetic.

## Layout & Spacing

The design system employs a **12-column fluid grid** for web and a **4-column grid** for mobile. The spacing philosophy is rooted in "Negative Space as Luxury." 

Components are grouped using a modular 8px scale. Layouts should favor large internal paddings (md or lg) within cards to enhance the glassmorphic "breathing" effect. Alignment should be strict and mathematical, emphasizing the "modern" aspect of the brand personality.

## Elevation & Depth

Depth in this design system is achieved through **Backdrop Blurs** and **Tonal Stacking** rather than traditional black shadows.

1.  **Level 0 (Base):** The deep neutral (#001219) background.
2.  **Level 1 (Surface):** Glass panels with `backdrop-filter: blur(20px)` and a 1px solid border at 20% opacity.
3.  **Level 2 (Floating):** Floating elements like Modals or Menus, using a higher blur (40px) and a subtle outer glow (box-shadow) using the Secondary color (#0A9396) at 10% opacity.

Avoid solid fills for containers; transparency is the primary tool for establishing the marine atmosphere.

## Shapes

The design system uses a **Rounded** shape language to evoke a sleek, organic feel—like water-worn pebbles or modern submersible craft. 

- **Standard components:** 0.5rem (8px) corner radius.
- **Large Cards & Containers:** 1rem (16px) corner radius.
- **Pill elements:** Used exclusively for tags, chips, and search bars to provide a distinct visual contrast to structural blocks.

## Components

### Buttons
Primary buttons use a solid gradient from Secondary (#0A9396) to Primary (#005F73) with a subtle outer glow on hover. Secondary buttons are ghost-styled with a thin Teal (#94D2BD) border and high-blur glass background.

### Cards
Cards are the hero of the system. They must feature a `backdrop-filter: blur(16px)`, a semi-transparent fill, and a "top-light" border—a 1px border that is slightly brighter at the top than the bottom to simulate overhead light catching the edge of glass.

### Input Fields
Inputs are dark, recessed wells. On focus, the border transitions to a glowing Cyan (#0A9396) and a faint inner shadow is applied to create a "hollowed out" effect in the glass.

### Glowing Accents
Use for status indicators and active states. A 4px circle with a 12px blur radius in the Tertiary color (#94D2BD) creates the signature bioluminescent effect.

### Progress Bars & Sliders
Track components should be semi-transparent deep blue, with the active "fill" being a vibrant Cyan-to-Teal gradient, making the interactive progress appear to be glowing from within.