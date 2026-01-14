// GlassModal Component with Subtle Glassmorphism
'use client';

import { cn } from '@/lib/utils';
import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useReducedMotion } from '@/hooks/useReducedMotion';

interface GlassModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  className?: string;
  showCloseButton?: boolean;
}

const GlassModal = ({
  isOpen,
  onClose,
  title,
  children,
  className,
  showCloseButton = true
}: GlassModalProps) => {
  const reducedMotion = useReducedMotion();

  // Prevent body scroll when modal is open
  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop with enhanced blur for glassmorphism effect */}
          <motion.div
            initial={reducedMotion ? {} : { opacity: 0 }}
            animate={reducedMotion ? {} : { opacity: 1 }}
            exit={reducedMotion ? {} : { opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="absolute inset-0 bg-black/30 backdrop-blur-md"
            onClick={onClose}
          />

          {/* Glass Modal Content */}
          <motion.div
            initial={reducedMotion ? {} : { opacity: 0, scale: 0.95 }}
            animate={reducedMotion ? {} : { opacity: 1, scale: 1 }}
            exit={reducedMotion ? {} : { opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className={cn(
              'relative max-w-md w-full p-6 rounded-xl shadow-[var(--shadow-xl)]',
              // Glassmorphism effect
              'backdrop-blur-xl backdrop-saturate-180',
              'bg-[var(--glass-modal-bg)] border border-[var(--glass-modal-border)]',
              // Fallback for browsers that don't support backdrop-filter
              'supports-[backdrop-filter]:bg-[var(--glass-modal-bg)]',
              'supports-[not(backdrop-filter)]:bg-[var(--glass-fallback)]',
              className
            )}
            onClick={(e) => e.stopPropagation()}
          >
            {title && (
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-foreground">{title}</h3>
                {showCloseButton && (
                  <button
                    onClick={onClose}
                    className="text-muted-foreground hover:text-foreground transition-colors duration-200 text-2xl leading-none"
                    aria-label="Close modal"
                  >
                    ×
                  </button>
                )}
              </div>
            )}
            <div className="text-foreground">{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};

export { GlassModal };
