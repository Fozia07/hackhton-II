/**
 * Animation Theme Configuration
 * Light, gentle animation presets
 */

export const animations = {
  durations: {
    quick: 150,
    gentle: 250,
    smooth: 300,
    slow: 400,
  },
  easings: {
    easeInOutCubic: 'cubic-bezier(0.65, 0, 0.35, 1)',
    easeInOutQuart: 'cubic-bezier(0.76, 0, 0.24, 1)',
    easeOutExpo: 'cubic-bezier(0.16, 1, 0.3, 1)',
    easeOutCubic: 'cubic-bezier(0.33, 1, 0.68, 1)',
    easeInCubic: 'cubic-bezier(0.32, 0, 0.67, 0)',
    materialStandard: 'cubic-bezier(0.4, 0, 0.2, 1)',
    materialDeceleration: 'cubic-bezier(0, 0, 0.2, 1)',
    materialAcceleration: 'cubic-bezier(0.4, 0, 1, 1)',
  },
  transitions: {
    quick: 'all 150ms cubic-bezier(0.76, 0, 0.24, 1)',
    gentle: 'all 250ms cubic-bezier(0.65, 0, 0.35, 1)',
    smooth: 'all 300ms cubic-bezier(0.16, 1, 0.3, 1)',
    slow: 'all 400ms cubic-bezier(0.4, 0, 0.2, 1)',
  },
  microInteractions: {
    buttonHover: {
      scale: 1.02,
      duration: 200,
    },
    buttonPress: {
      scale: 0.98,
      duration: 100,
    },
    cardHover: {
      translateY: -2,
      scale: 1.01,
      duration: 250,
    },
  },
} as const;

export type AnimationConfig = typeof animations;
