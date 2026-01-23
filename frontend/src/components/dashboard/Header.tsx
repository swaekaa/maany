import React, { useState } from 'react';
import { Search, Bell, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { ModeToggle } from '@/components/ui/mode-toggle';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import mujLogo from '@/assets/muj-logo.png';

const Header = () => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <header className="sticky top-0 z-50 backdrop-blur-glass bg-card border-b border-border shadow-soft">
      <div className="flex items-center justify-between px-4 md:px-6 py-4">
        {/* Left - University Logo */}
        <div className="flex items-center space-x-3 md:space-x-4">
          <img 
            src={mujLogo} 
            alt="MUJ Logo" 
            className="w-8 h-8 md:w-10 md:h-10 rounded-full flex-shrink-0"
          />
          <div className="hidden sm:block">
            <h1 className="text-base md:text-lg font-semibold text-foreground">
              Manipal University Jaipur
            </h1>
            <p className="text-xs md:text-sm text-muted-foreground">SLCM Portal</p>
          </div>
        </div>

        {/* Center - Reports Dropdown and Search */}
        <div className="hidden lg:flex items-center space-x-6">
          {/* Reports Dropdown */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button 
                variant="ghost" 
                className="flex items-center space-x-2 hover:bg-secondary transition-colors duration-200"
              >
                <span className="font-medium">Reports</span>
                <ChevronDown className="w-4 h-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="center" className="w-56 bg-background border-border">
              <DropdownMenuItem className="cursor-pointer">Academic Reports</DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer">Financial Reports</DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer">Attendance Reports</DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer">Exam Reports</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 w-60 xl:w-80 bg-secondary/50 border-secondary focus:border-input-focus transition-all duration-200"
            />
          </div>
        </div>

        {/* Right - Theme Toggle, Notifications and Profile */}
        <div className="flex items-center space-x-2 md:space-x-4">
          {/* Dark Mode Toggle */}
          <ModeToggle />
          
          {/* Notifications */}
          <div className="relative">
            <Button
              variant="ghost"
              size="icon"
              className="text-foreground hover:bg-secondary transition-colors duration-200 h-8 w-8 md:h-10 md:w-10"
            >
              <Bell className="w-4 h-4 md:w-5 md:h-5" />
            </Button>
            <Badge className="absolute -top-2 -right-2 bg-student-name text-white text-xs min-w-5 h-5 flex items-center justify-center">
              3
            </Badge>
          </div>

          {/* Student Info */}
          <div className="flex items-center space-x-3">
            <div className="text-right hidden sm:block">
              <p className="text-xs md:text-sm font-medium text-foreground">23FE10CSE00322</p>
              <p className="text-xs md:text-sm font-semibold text-student-name">ABHINAV MISHRA</p>
            </div>
            <Avatar className="w-8 h-8 md:w-10 md:h-10">
              <AvatarFallback className="bg-gradient-orange text-white text-xs md:text-sm font-semibold">
                AM
              </AvatarFallback>
            </Avatar>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;