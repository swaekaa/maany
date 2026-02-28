import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import mujLogo from '@/assets/muj-logo.png';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!username || !password) {
      toast({
        title: "Missing Information",
        description: "Please fill in all fields",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      toast({
        title: "Login Successful",
        description: "Welcome to SLCM Portal",
      });
      navigate('/dashboard');
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-orange-light flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Glass-morphism Login Card */}
        <Card className="backdrop-blur-glass bg-card-glass border-glass-border shadow-glass">
          <CardHeader className="text-center space-y-4 pb-8">
            {/* University Logo */}
            <div className="flex justify-center">
              <div className="w-20 h-20 rounded-full bg-gradient-orange flex items-center justify-center shadow-elegant">
                <img 
                  src={mujLogo} 
                  alt="MUJ Logo" 
                  className="w-16 h-16 rounded-full"
                />
              </div>
            </div>
            
            {/* University Branding */}
            <div className="space-y-2">
              <h1 className="text-2xl font-semibold text-foreground">
                Manipal University Jaipur
              </h1>
              <p className="text-muted-foreground font-light">
                Student Life Cycle Management System
              </p>
            </div>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleLogin} className="space-y-6">
              {/* Username Field */}
              <div className="space-y-2">
                <Label htmlFor="username" className="text-sm font-medium">
                  Username / Roll Number
                </Label>
                <Input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter your roll number"
                  className="transition-all duration-200 focus:border-input-focus focus:ring-1 focus:ring-input-focus"
                />
              </div>

              {/* Password Field */}
              <div className="space-y-2">
                <Label htmlFor="password" className="text-sm font-medium">
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="transition-all duration-200 focus:border-input-focus focus:ring-1 focus:ring-input-focus"
                />
              </div>

              {/* Login Button */}
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full h-12 bg-gradient-orange text-primary-foreground font-medium shadow-md hover:shadow-lg transition-all duration-300 hover:scale-[1.02] disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {isLoading ? (
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Signing in...</span>
                  </div>
                ) : (
                  'Sign In to SLCM'
                )}
              </Button>
            </form>

            {/* Additional Links */}
            <div className="mt-6 text-center space-y-2">
              <button className="text-sm text-accent hover:text-accent-hover transition-colors duration-200">
                Forgot Password?
              </button>
              <p className="text-xs text-muted-foreground">
                Having trouble? Contact IT Support
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-muted-foreground">
          <p>© 2024 Manipal University Jaipur. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
};

export default Login;