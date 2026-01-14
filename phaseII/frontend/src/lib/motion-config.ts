/**
 * Motion Configuration Utilities
 * Light, gentle animation presets for Modern UI Enhancement
 */

import type { Transition, Variants } from 'framer-motion';

/**
 * Easing Functions - Gentle, refined curves
 */
export const easings = {
  easeInOutCubic: [0.65, 0, 0.35, 1] as const,
  easeInOutQuart: [0.76, 0, 0.24, 1] as const,
  easeOutExpo: [0.16, 1, 0.3, 1] as const,
  easeOutCubic: [0.33, 1, 0.68, 1] as const,
  easeInCubic: [0.32, 0, 0.67, 0] as const,
  materialStandard: [0.4, 0, 0.2, 1] as const,
  materialDeceleration: [0, 0, 0.2, 1] as const,
  materialAcceleration: [0.4, 0, 1, 1] as const,
} as const;

/**
 * Transition Presets - Light, gentle timing
 */
export const transitions = {
  quick: {
    type: 'tween',
    duration: 0.15,
    ease: easings.easeInOutQuart,
  } as Transition,

  gentle: {
    type: 'tween',
    duration: 0.25,
    ease: easings.easeInOutCubic,
  } as Transition,

  smooth: {
    type: 'tween',
    duration: 0.3,
    ease: easings.easeOutExpo,
  } as Transition,

  slow: {
    type: 'tween',
    duration: 0.4,
    ease: easings.materialStandard,
  } as Transition,

  springGentle: {
    type: 'spring',
    stiffness: 200,
    damping: 25,
    mass: 1,
  } as Transition,
} as const;

/**
 * Animation Variants - Common animation patterns
 */
export const variants = {
  fadeIn: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
  } as Variants,

  fadeInUp: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 },
  } as Variants,

  scaleIn: {
    initial: { opacity: 0, scale: 0.95 },
    animate: { opacity: 1, scale: 1 },
    exit: { opacity: 0, scale: 0.95 },
  } as Variants,

  slideIn: {
    initial: { x: -20, opacity: 0 },
    animate: { x: 0, opacity: 1 },
    exit: { x: 20, opacity: 0 },
  } as Variants,

  slideInRight: {
    initial: { x: 100, opacity: 0 },
    animate: { x: 0, opacity: 1 },
    exit: { x: 100, opacity: 0 },
  } as Variants,
} as const;

/**
 * Micro-Interaction Presets - Subtle, obvious feedback
 */
export const microInteractions = {
  buttonHover: {
    scale: 1.02,
    transition: { duration: 0.2, ease: 'easeOut' },
  },

  buttonPress: {
    scale: 0.98,
    transition: { duration: 0.1, ease: 'easeOut' },
  },

  cardHover: {
    y: -2,
    scale: 1.01,
    transition: { duration: 0.25, ease: 'easeOut' },
  },

  modalEnter: {
    opacity: [0, 1],
    scale: [0.95, 1],
    transition: { duration: 0.3, ease: 'easeOut' },
  },

  toastSlide: {
    x: [100, 0],
    opacity: [0, 1],
    transition: { duration: 0.3, ease: 'easeOut' },
  },

  checkboxCheck: {
    pathLength: [0, 1],
    transition: { duration: 0.2, ease: easings.easeInOutCubic },
  },
} as const;

/**
 * Helper function to get transition with reduced motion support
 */
export function getTransition(
  preset: keyof typeof transitions,
  reducedMotion: boolean = false
): Transition {
  if (reducedMotion) {
    return { duration: 0.01 };
  }
  return transitions[preset];
}

/**
 * Helper function to get variants with reduced motion support
 */
export function getVariants(
  preset: keyof typeof variants,
  reducedMotion: boolean = false
): Variants {
  if (reducedMotion) {
    return {
      initial: { opacity: 1 },
      animate: { opacity: 1 },
      exit: { opacity: 1 },
    };
  }
  return variants[preset];
}

/**
 * Stagger configuration for list animations
 */
export const staggerConfig = {
  container: {
    animate: {
      transition: {
        staggerChildren: 0.05,
        delayChildren: 0.1,
      },
    },
  },
  item: variants.fadeInUp,
} as const;
