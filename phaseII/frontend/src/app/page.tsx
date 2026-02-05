'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { useReducedMotion } from '@/hooks/useReducedMotion';
import { variants, transitions } from '@/lib/motion-config';

export default function HomePage() {
  const reducedMotion = useReducedMotion();

  // Gentle fade-in variants
  const fadeInUpVariant = reducedMotion ? {} : variants.fadeInUp;
  const gentleTransition = reducedMotion ? {} : transitions.gentle;

  // Stagger children animation
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-primary-100/30 dark:from-background dark:to-primary-900/10">
      <div className="container mx-auto px-4 py-16 scroll-smooth">
        {/* Hero Section with Soft Gradient */}
        <motion.section
          initial={reducedMotion ? {} : "hidden"}
          animate={reducedMotion ? {} : "visible"}
          variants={containerVariants}
          className="max-w-4xl mx-auto text-center mb-20"
        >
          <motion.div
            variants={fadeInUpVariant}
            transition={gentleTransition}
            className="mb-6"
          >
            <span className="inline-block px-4 py-2 text-sm font-semibold text-primary-700 dark:text-primary-400 bg-primary-100 dark:bg-primary-900/30 rounded-full shadow-[var(--shadow-sm)]">
              Productivity Tool
            </span>
          </motion.div>

          <motion.h1
            variants={fadeInUpVariant}
            transition={gentleTransition}
            className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 via-primary-500 to-secondary-600 dark:from-primary-400 dark:via-primary-300 dark:to-secondary-400 mb-6"
          >
            Manage Your Tasks Effortlessly
          </motion.h1>

          <motion.p
            variants={fadeInUpVariant}
            transition={gentleTransition}
            className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10"
          >
            A beautiful and intuitive todo application designed to help you stay organized, focused, and productive.
          </motion.p>

          <motion.div
            variants={fadeInUpVariant}
            transition={gentleTransition}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <Link href="/signup">
              <Button size="lg" className="px-8 py-3 text-lg w-full sm:w-auto">
                Get Started
              </Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg" className="px-8 py-3 text-lg w-full sm:w-auto">
                Sign In
              </Button>
            </Link>
          </motion.div>
        </motion.section>

        {/* Features Section with Soft Shadows and Hover Effects */}
        <motion.section
          initial={reducedMotion ? {} : "hidden"}
          animate={reducedMotion ? {} : "visible"}
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20"
        >
          <motion.div variants={fadeInUpVariant} transition={gentleTransition}>
            <Card hoverable className="text-center p-6 h-full">
              <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-primary-100 dark:bg-primary-900/30 flex items-center justify-center shadow-[var(--shadow-sm)]">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7 text-primary-600 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2 text-foreground">Task Management</h3>
              <p className="text-muted-foreground text-sm">
                Organize your tasks with ease and never miss a deadline.
              </p>
            </Card>
          </motion.div>

          <motion.div variants={fadeInUpVariant} transition={gentleTransition}>
            <Card hoverable className="text-center p-6 h-full">
              <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-success-100 dark:bg-success-900/30 flex items-center justify-center shadow-[var(--shadow-sm)]">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7 text-success-600 dark:text-success-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2 text-foreground">Secure Access</h3>
              <p className="text-muted-foreground text-sm">
                Your data is protected with industry-standard security measures.
              </p>
            </Card>
          </motion.div>

          <motion.div variants={fadeInUpVariant} transition={gentleTransition}>
            <Card hoverable className="text-center p-6 h-full">
              <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-secondary-100 dark:bg-secondary-900/30 flex items-center justify-center shadow-[var(--shadow-sm)]">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7 text-secondary-600 dark:text-secondary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2 text-foreground">Sync Across Devices</h3>
              <p className="text-muted-foreground text-sm">
                Access your tasks from anywhere, on any device.
              </p>
            </Card>
          </motion.div>
        </motion.section>

        {/* CTA Section with Soft Gradient */}
        <motion.section
          initial={reducedMotion ? {} : { opacity: 0, y: 20 }}
          animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
          transition={reducedMotion ? {} : { delay: 0.4, duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          className="text-center"
        >
          <div className="max-w-2xl mx-auto p-8 rounded-2xl bg-gradient-to-br from-primary-500 to-primary-600 dark:from-primary-600 dark:to-primary-700 text-white shadow-[var(--shadow-lg)]">
            <h2 className="text-2xl md:text-3xl font-bold mb-4">Ready to boost your productivity?</h2>
            <p className="mb-6 text-white/90">
              Join thousands of users who have transformed their daily routine with our app.
            </p>
            <Link href="/signup">
              <Button size="lg" className="bg-white text-primary-700 hover:bg-neutral-50 shadow-[var(--shadow-md)]">
                Start Free Trial
              </Button>
            </Link>
          </div>
        </motion.section>
      </div>
    </div>
  );
}