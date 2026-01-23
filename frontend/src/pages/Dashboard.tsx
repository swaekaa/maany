import React, { useState } from 'react';
import Header from '@/components/dashboard/Header';
import Sidebar from '@/components/dashboard/Sidebar';
import MainContent from '@/components/dashboard/MainContent';
import ChatWidget from '@/components/dashboard/ChatWidget';
import APIConnectionTest from '@/components/APIConnectionTest';
import { Button } from '@/components/ui/button';
import { Settings } from 'lucide-react';

const Dashboard = () => {
  const [showAPITest, setShowAPITest] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <Header />
      
      {/* Main Layout */}
      <div className="flex overflow-x-hidden">
        {/* Sidebar */}
        <Sidebar />
        
        {/* Main Content */}
        <MainContent />
      </div>
      
      {/* Chat Widget - Manny */}
      <ChatWidget />
      
      {/* API Test Toggle Button */}
      <div className="fixed bottom-6 left-6 z-40">
        <Button
          onClick={() => setShowAPITest(!showAPITest)}
          variant="outline"
          size="sm"
          className="bg-white shadow-lg hover:shadow-xl transition-all duration-300"
        >
          <Settings className="w-4 h-4 mr-2" />
          API Test
        </Button>
      </div>
      
      {/* API Connection Test Modal */}
      {showAPITest && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto">
            <div className="p-4 border-b flex items-center justify-between">
              <h2 className="text-lg font-semibold">Backend API Connection Test</h2>
              <Button
                onClick={() => setShowAPITest(false)}
                variant="ghost"
                size="sm"
              >
                ×
              </Button>
            </div>
            <div className="p-6">
              <APIConnectionTest />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;