'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FlaskConical,
  Search,
  LayoutDashboard,
  History,
  Settings,
  HelpCircle,
  Bell,
  User,
  ChevronDown,
  LogOut,
  Moon,
  Sun,
  Menu,
  X
} from 'lucide-react';
import { Button, Badge } from '@/components/ui';

interface NavigationProps {
  className?: string;
}

const navItems = [
  { href: '/', label: 'Research', icon: Search },
  { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/history', label: 'History', icon: History },
];

export const Navigation: React.FC<NavigationProps> = ({ className = '' }) => {
  const pathname = usePathname();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  
  const notifications = [
    { id: 1, title: 'Analysis Complete', message: 'Ozempic analysis finished with 12 insights', time: '2 min ago', unread: true },
    { id: 2, title: 'New Data Available', message: 'FDA updated approval status for Keytruda', time: '1 hour ago', unread: true },
    { id: 3, title: 'Weekly Report', message: 'Your weekly research summary is ready', time: '3 hours ago', unread: false },
  ];
  
  const toggleDarkMode = () => {
    const newMode = !isDarkMode;
    setIsDarkMode(newMode);
    if (typeof document !== 'undefined') {
      if (newMode) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
    }
  };
  
  return (
    <header className={`bg-white/80 backdrop-blur-lg border-b border-gray-100 sticky top-0 z-50 ${className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center group">
            <Image
              src="/pharmaAssist-logo.png"
              alt="PharmaAssist AI"
              width={180}
              height={40}
              className="h-10 w-auto object-contain"
              priority
            />
          </Link>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm transition-all ${
                    isActive
                      ? 'bg-indigo-50 text-indigo-600'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-indigo-500' : ''}`} />
                  {item.label}
                </Link>
              );
            })}
          </nav>
          
          {/* Right Section */}
          <div className="flex items-center gap-2">
            {/* Theme Toggle */}
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors hidden sm:flex"
            >
              {isDarkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            
            {/* Notifications */}
            <div className="relative hidden sm:block">
              <button 
                onClick={() => setIsNotificationsOpen(!isNotificationsOpen)}
                className="relative p-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors flex"
              >
                <Bell className="w-5 h-5" />
                <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full" />
              </button>
              
              <AnimatePresence>
                {isNotificationsOpen && (
                  <>
                    <div 
                      className="fixed inset-0" 
                      onClick={() => setIsNotificationsOpen(false)} 
                    />
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 10, scale: 0.95 }}
                      className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50"
                    >
                      <div className="p-3 border-b border-gray-100 flex items-center justify-between">
                        <p className="font-semibold text-gray-900">Notifications</p>
                        <Badge variant="info">{notifications.filter(n => n.unread).length} new</Badge>
                      </div>
                      <div className="max-h-80 overflow-y-auto">
                        {notifications.map((notification) => (
                          <div 
                            key={notification.id}
                            className={`p-3 border-b border-gray-50 hover:bg-gray-50 cursor-pointer ${notification.unread ? 'bg-indigo-50/50' : ''}`}
                          >
                            <div className="flex items-start gap-3">
                              <div className={`w-2 h-2 mt-2 rounded-full ${notification.unread ? 'bg-indigo-500' : 'bg-gray-300'}`} />
                              <div className="flex-1">
                                <p className="text-sm font-medium text-gray-900">{notification.title}</p>
                                <p className="text-xs text-gray-500 mt-0.5">{notification.message}</p>
                                <p className="text-xs text-gray-400 mt-1">{notification.time}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                      <div className="p-2 border-t border-gray-100">
                        <button className="w-full text-center text-sm text-indigo-600 hover:text-indigo-700 py-2">
                          View all notifications
                        </button>
                      </div>
                    </motion.div>
                  </>
                )}
              </AnimatePresence>
            </div>
            
            {/* Help */}
            <button className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors hidden sm:flex">
              <HelpCircle className="w-5 h-5" />
            </button>
            
            {/* Profile Dropdown */}
            <div className="relative hidden sm:block">
              <button
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className="flex items-center gap-2 p-1.5 pr-3 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-400 to-cyan-400 flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
                <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isProfileOpen ? 'rotate-180' : ''}`} />
              </button>
              
              <AnimatePresence>
                {isProfileOpen && (
                  <>
                    <div 
                      className="fixed inset-0" 
                      onClick={() => setIsProfileOpen(false)} 
                    />
                    <motion.div
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, y: 10, scale: 0.95 }}
                      className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50"
                    >
                      <div className="p-3 border-b border-gray-100">
                        <p className="font-medium text-gray-900">John Doe</p>
                        <p className="text-sm text-gray-500">john@pharmaassist.ai</p>
                      </div>
                      <div className="p-2">
                        <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                          <User className="w-4 h-4" />
                          Profile Settings
                        </button>
                        <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg transition-colors">
                          <Settings className="w-4 h-4" />
                          Preferences
                        </button>
                      </div>
                      <div className="p-2 border-t border-gray-100">
                        <button className="w-full flex items-center gap-3 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                          <LogOut className="w-4 h-4" />
                          Sign Out
                        </button>
                      </div>
                    </motion.div>
                  </>
                )}
              </AnimatePresence>
            </div>
            
            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors md:hidden"
            >
              {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-white border-t border-gray-100"
          >
            <nav className="p-4 space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;
                
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-all ${
                      isActive
                        ? 'bg-indigo-50 text-indigo-600'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <Icon className={`w-5 h-5 ${isActive ? 'text-indigo-500' : ''}`} />
                    {item.label}
                  </Link>
                );
              })}
              <div className="pt-4 border-t border-gray-100">
                <div className="flex items-center gap-3 px-4 py-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-400 to-cyan-400 flex items-center justify-center">
                    <User className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">John Doe</p>
                    <p className="text-sm text-gray-500">john@pharmaassist.ai</p>
                  </div>
                </div>
              </div>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};
