import React from 'react';
import { Mail, Phone, Building2, ExternalLink, FileText } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const MainContent = () => {
  return (
    <main className="flex-1 min-h-screen bg-background">
      <div className="p-6 space-y-6">
        {/* Welcome Header */}
        <div className="bg-gradient-orange-light rounded-2xl p-6 border border-border/50">
          <h1 className="text-2xl font-semibold text-foreground mb-2">
            Welcome back, Abhinav!
          </h1>
          <p className="text-muted-foreground">
            Here's your academic dashboard overview for today.
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Class Coordinator Card */}
          <div className="xl:col-span-2">
            <Card className="shadow-soft hover:shadow-elegant transition-shadow duration-300">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Building2 className="w-5 h-5 text-primary" />
                  <span>Class Coordinator</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Coordinator Info */}
                <div className="bg-secondary/50 rounded-xl p-4 space-y-3">
                  <div className="flex items-start justify-between">
                    <div className="space-y-2">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium text-foreground">Name:</span>
                        <button className="text-accent hover:text-accent-hover font-medium transition-colors duration-200 hover:underline">
                          Dr. Sarah Johnson
                        </button>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Mail className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm text-muted-foreground">Email:</span>
                        <span className="text-sm">sarah.johnson@muj.manipal.edu</span>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Phone className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm text-muted-foreground">Phone:</span>
                        <span className="text-sm">+91 98765 43210</span>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Building2 className="w-4 h-4 text-muted-foreground" />
                        <span className="text-sm text-muted-foreground">Department:</span>
                        <button className="text-sm text-accent hover:text-accent-hover transition-colors duration-200 hover:underline">
                          Computer Science & Engineering
                        </button>
                      </div>
                    </div>
                    
                    <Badge variant="secondary" className="bg-primary/10 text-primary">
                      Active
                    </Badge>
                  </div>
                  
                  {/* Contact Action */}
                  <div className="pt-2 border-t border-border/50">
                    <button className="flex items-center space-x-2 text-sm text-accent hover:text-accent-hover transition-colors duration-200">
                      <ExternalLink className="w-4 h-4" />
                      <span>Send Message</span>
                    </button>
                  </div>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-muj-orange-light/20 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-primary">24</div>
                    <div className="text-sm text-muted-foreground">Office Hours/Week</div>
                  </div>
                  <div className="bg-accent/10 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-accent">4.8</div>
                    <div className="text-sm text-muted-foreground">Rating</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Panel - Notifications and Events */}
          <div className="space-y-6">
            {/* Notifications */}
            <Card className="shadow-soft">
              <CardHeader>
                <CardTitle className="text-lg">Recent Notifications</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center py-8">
                    <div className="w-16 h-16 bg-secondary/50 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Mail className="w-8 h-8 text-muted-foreground" />
                    </div>
                    <p className="text-muted-foreground text-sm">
                      No new notifications
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Upcoming Events */}
            <Card className="shadow-soft">
              <CardHeader>
                <CardTitle className="text-lg">Upcoming Events</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="text-center py-8">
                    <div className="w-16 h-16 bg-secondary/50 rounded-full flex items-center justify-center mx-auto mb-3">
                      <Building2 className="w-8 h-8 text-muted-foreground" />
                    </div>
                    <p className="text-muted-foreground text-sm">
                      No upcoming events
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'View Grades', icon: FileText, color: 'bg-accent/10 text-accent' },
            { label: 'Attendance', icon: Building2, color: 'bg-primary/10 text-primary' },
            { label: 'Fee Payment', icon: Phone, color: 'bg-student-name/10 text-student-name' },
            { label: 'Time Table', icon: Mail, color: 'bg-muted/50 text-muted-foreground' },
          ].map((action, index) => (
            <button
              key={index}
              className="p-4 rounded-xl border border-border hover:border-primary/30 transition-all duration-200 hover:shadow-soft group"
            >
              <div className={`w-12 h-12 rounded-lg ${action.color} flex items-center justify-center mx-auto mb-2 group-hover:scale-110 transition-transform duration-200`}>
                <action.icon className="w-6 h-6" />
              </div>
              <p className="text-sm font-medium text-center">{action.label}</p>
            </button>
          ))}
        </div>
      </div>
    </main>
  );
};

export default MainContent;