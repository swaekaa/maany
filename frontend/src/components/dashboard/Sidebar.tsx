import React, { useState } from 'react';
import { 
  Home, 
  Book, 
  DollarSign, 
  FileText, 
  Award, 
  MessageCircle, 
  Library,
  Menu,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface MenuItem {
  icon: React.ElementType;
  label: string;
  active?: boolean;
}

const menuItems: MenuItem[] = [
  { icon: Home, label: 'Home', active: true },
  { icon: Book, label: 'Academics' },
  { icon: DollarSign, label: 'Finance' },
  { icon: FileText, label: 'Examination' },
  { icon: Award, label: 'Scholarship' },
  { icon: MessageCircle, label: 'Counselling' },
  { icon: Library, label: 'E-Library' },
];

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  return (
    <>
      {/* Mobile Menu Button */}
      <div className="md:hidden fixed top-4 left-4 z-50">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsMobileOpen(!isMobileOpen)}
          className="bg-card-glass backdrop-blur-glass border border-glass-border"
        >
          {isMobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </Button>
      </div>

      {/* Sidebar */}
      <aside 
        className={cn(
          "fixed md:sticky top-0 h-screen bg-gradient-orange transition-all duration-300 z-40",
          "flex flex-col shadow-lg",
          // Desktop sizing
          isCollapsed ? "w-16" : "w-64",
          // Mobile visibility
          "md:translate-x-0",
          isMobileOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/20">
          {!isCollapsed && (
            <h2 className="text-white font-semibold text-lg">SLCM Menu</h2>
          )}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="hidden md:flex text-white hover:bg-white/10 transition-colors duration-200"
          >
            <Menu className="w-5 h-5" />
          </Button>
        </div>

        {/* Navigation Menu */}
        <nav className="flex-1 py-6 space-y-2 px-4">
          {menuItems.map((item, index) => {
            const Icon = item.icon;
            return (
              <button
                key={index}
                className={cn(
                  "w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200",
                  "text-white/90 hover:text-white hover:bg-white/15",
                  item.active && "bg-white/20 text-white font-medium shadow-md"
                )}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {!isCollapsed && (
                  <span className="font-medium">{item.label}</span>
                )}
              </button>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-white/20">
          <div className="text-center">
            {!isCollapsed ? (
              <p className="text-white/80 text-xs">
                © 2024 MUJ SLCM
              </p>
            ) : (
              <div className="w-8 h-8 bg-white/10 rounded-lg mx-auto"></div>
            )}
          </div>
        </div>
      </aside>

      {/* Mobile Overlay */}
      {isMobileOpen && (
        <div 
          className="md:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setIsMobileOpen(false)}
        />
      )}
    </>
  );
};

export default Sidebar;