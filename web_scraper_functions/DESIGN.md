---
name: Web Scraper Functions
colors:
  surface: '#101415'
  surface-dim: '#101415'
  surface-bright: '#363a3b'
  surface-container-lowest: '#0b0f10'
  surface-container-low: '#191c1e'
  surface-container: '#1d2022'
  surface-container-high: '#272a2c'
  surface-container-highest: '#323537'
  on-surface: '#e0e3e5'
  on-surface-variant: '#bac9cc'
  inverse-surface: '#e0e3e5'
  inverse-on-surface: '#2d3133'
  outline: '#849396'
  outline-variant: '#3b494c'
  surface-tint: '#00daf3'
  primary: '#c3f5ff'
  on-primary: '#00363d'
  primary-container: '#00e5ff'
  on-primary-container: '#00626e'
  inverse-primary: '#006875'
  secondary: '#b8c4ff'
  on-secondary: '#002585'
  secondary-container: '#054efc'
  on-secondary-container: '#dadeff'
  tertiary: '#e4edff'
  on-tertiary: '#233144'
  tertiary-container: '#c3d1ea'
  on-tertiary-container: '#4c5a6f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#9cf0ff'
  primary-fixed-dim: '#00daf3'
  on-primary-fixed: '#001f24'
  on-primary-fixed-variant: '#004f58'
  secondary-fixed: '#dde1ff'
  secondary-fixed-dim: '#b8c4ff'
  on-secondary-fixed: '#001454'
  on-secondary-fixed-variant: '#0037ba'
  tertiary-fixed: '#d5e3fd'
  tertiary-fixed-dim: '#b9c7e0'
  on-tertiary-fixed: '#0d1c2f'
  on-tertiary-fixed-variant: '#3a485c'
  background: '#101415'
  on-background: '#e0e3e5'
  surface-variant: '#323537'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
  container-max: 1440px
---

## Brand & Style

The design system embodies a **Deep Tech** aesthetic, positioning the product as a high-performance, intelligent utility for developers and data scientists. It moves away from the casual "Streamlit" look toward a premium, enterprise-grade environment that signals reliability, precision, and automated intelligence.

The visual direction is **Minimalist / Corporate Modern** with high-tech accents. It utilizes a dark-mode-first approach to reduce eye strain during long data-analysis sessions. The interface should feel like a sophisticated mission control center: clean, structured, and dense with information without being cluttered. Key attributes include:

- **Technical Precision:** Crisp lines and geometric layouts.
- **Intelligent Automation:** Subtle motion and state changes that suggest the backend AI is working.
- **Data-First:** High information density and clear hierarchy for complex extraction results.

## Colors

The palette is anchored in a professional **Deep Navy** base for the primary background, providing a sophisticated "infinite space" feel common in advanced developer tools. 

- **Primary:** A vibrant **Cyan** (`#00e5ff`) is used for primary actions, progress indicators, and "active" code states, cutting through the dark background with high luminosity.
- **Secondary:** A high-energy **Electric Blue** (`#024dfb`) serves as a secondary accent for interactive highlights and secondary actions, providing a clear visual distinction from primary controls.
- **Tertiary/Surface:** Various shades of **Slate** (`#334155`) define the UI containers and surfaces, creating structural depth.
- **Typography:** The neutral color is a near-white **Slate-50** (`#f8fafc`) for high legibility, with secondary text dropping to lower contrast slate tones.
- **Status:** Functional colors (Success, Error, Warning) are slightly desaturated to maintain the professional "Deep Tech" tone.

## Typography

The design system uses **Inter** as its primary typeface for its exceptional legibility and neutral, modern character. For technical data, URLs, and code-based labels, **JetBrains Mono** is introduced to reinforce the developer-centric, "under the hood" aesthetic.

- **Headlines:** Set with tight letter-spacing and bold weights to command attention in a data-dense environment.
- **Body:** Optimized for reading long extraction logs and technical documentation.
- **Mono Labels:** Used for all "Functional" data—file paths, API endpoints, and scraper status codes—to provide a visual distinction between UI controls and the data being processed.

## Layout & Spacing

The system uses a **12-column fixed grid** for desktop to ensure data visualizations and extraction logs maintain a structured, predictable alignment. 

- **Grid:** On desktop, a 1440px max-width container is centered. On mobile, the layout reflows into a single-column fluid stack with 16px margins.
- **Density:** We utilize an 8px base grid, but allow for 4px "half-steps" to maintain the high density required for data dashboards and complex input forms.
- **Rhythm:** Vertical rhythm is strictly enforced to ensure that sidebars and main content areas align perfectly, conveying a sense of engineered precision.

## Elevation & Depth

Depth is conveyed through **Tonal Layering** and **Low-Contrast Outlines** rather than heavy shadows. In a dark "Deep Tech" environment, traditional shadows often become muddy.

- **Level 0 (Background):** Deep Navy.
- **Level 1 (Cards/Panels):** Slate Surface (`#334155`) with a 1px subtle border.
- **Level 2 (Popovers/Tooltips):** Elevated surfaces with a subtle **Electric Blue** tinted glow (4px blur, 10% opacity) to suggest importance.
- **Interactive States:** Hovering over a card or list item triggers a slight border-color shift toward Cyan or Electric Blue, rather than a physical "lift."

## Shapes

The design system uses **Soft** geometry. To maintain a technical and "engineered" feel, we avoid the playfulness of fully rounded "pills."

- **Standard Radius:** 4px (0.25rem) for buttons, inputs, and small containers.
- **Large Radius:** 8px (0.5rem) for primary layout cards and modal containers.
- **Exceptions:** Status indicators (active/inactive pips) remain sharp or perfectly circular to signify binary states.

## Components

- **Buttons:** Primary buttons use a solid Cyan background with dark text. Secondary buttons are outlined or accented with **Electric Blue**.
- **Data Chips:** Small, mono-spaced tags used for showing file formats (PDF, TXT, IMG). They have a subtle slate background fill and a matching border.
- **Inputs:** Darker than the card surface with a 1px border. The focus state is a 1px Cyan or Electric Blue border with no outer glow.
- **Extraction Logs (Lists):** Each entry is separated by a subtle 1px divider. Use JetBrains Mono for the technical metadata and Inter for the status message.
- **Status Indicators:** Use the "Active Glow" effect for running processes—a small pulsing Cyan dot next to the "Scraping..." label.
- **Progress Bars:** Thin (4px) bars with a Cyan to Electric Blue gradient to indicate extraction completion percentage.