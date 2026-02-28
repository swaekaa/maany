import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  CheckCircle, 
  XCircle, 
  Loader2, 
  RefreshCw, 
  Server, 
  MessageCircle,
  Volume2,
  Shield,
  Zap
} from 'lucide-react';
import { apiService, AppInfo, ChatResponse, TTSHealthResponse, DemoUsersResponse } from '@/services/apiservice';

interface ConnectionStatus {
  health: boolean;
  chat: boolean;
  tts: boolean;
  auth: boolean;
  overall: boolean;
}

interface TestResults {
  ping?: { status: string; message: string; version: string };
  info?: AppInfo;
  chat?: ChatResponse;
  tts?: TTSHealthResponse;
  auth?: DemoUsersResponse;
  error?: string;
}

const APIConnectionTest: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<ConnectionStatus>({
    health: false,
    chat: false,
    tts: false,
    auth: false,
    overall: false,
  });
  const [results, setResults] = useState<TestResults>({});
  const [lastTest, setLastTest] = useState<Date | null>(null);

  const runTests = async () => {
    setIsLoading(true);
    setResults({});
    const newStatus: ConnectionStatus = {
      health: false,
      chat: false,
      tts: false,
      auth: false,
      overall: false,
    };

    try {
      // Test 1: Health Check
      console.log('Testing health endpoint...');
      const pingResult = await apiService.ping();
      newStatus.health = true;
      setResults(prev => ({ ...prev, ping: pingResult }));

      // Test 2: App Info
      console.log('Getting app info...');
      const infoResult = await apiService.getInfo();
      setResults(prev => ({ ...prev, info: infoResult }));

      // Test 3: Chat API
      console.log('Testing chat endpoint...');
      const chatResult = await apiService.sendMessage({
        user_id: 'test_user_frontend',
        message: 'Hello from frontend! Testing connection.',
        language: 'en',
      });
      newStatus.chat = true;
      setResults(prev => ({ ...prev, chat: chatResult }));

      // Test 4: TTS Health
      console.log('Testing TTS endpoint...');
      const ttsResult = await apiService.getTTSHealth();
      newStatus.tts = true;
      setResults(prev => ({ ...prev, tts: ttsResult }));

      // Test 5: Demo Users (Auth)
      console.log('Testing auth endpoint...');
      const authResult = await apiService.getDemoUsers();
      newStatus.auth = true;
      setResults(prev => ({ ...prev, auth: authResult }));

      // Overall status
      newStatus.overall = newStatus.health && newStatus.chat && newStatus.tts && newStatus.auth;

    } catch (error) {
      console.error('API Test Error:', error);
      setResults(prev => ({ 
        ...prev, 
        error: error instanceof Error ? error.message : 'Unknown error occurred' 
      }));
    } finally {
      setStatus(newStatus);
      setIsLoading(false);
      setLastTest(new Date());
    }
  };

  // Auto-run tests on component mount
  useEffect(() => {
    runTests();
  }, []);

  const StatusIcon = ({ success }: { success: boolean }) => (
    success ? (
      <CheckCircle className="h-4 w-4 text-green-500" />
    ) : (
      <XCircle className="h-4 w-4 text-red-500" />
    )
  );

  const getStatusBadge = (success: boolean) => (
    <Badge variant={success ? "default" : "destructive"} className="ml-2">
      {success ? "Connected" : "Failed"}
    </Badge>
  );

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Server className="h-5 w-5" />
          <span>Backend API Connection Status</span>
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <StatusIcon success={status.overall} />
          )}
        </CardTitle>
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">
            Testing connection to http://localhost:8000
          </div>
          <Button
            onClick={runTests}
            disabled={isLoading}
            size="sm"
            variant="outline"
            className="flex items-center space-x-1"
          >
            <RefreshCw className={`h-3 w-3 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Overall Status */}
        <Alert className={status.overall ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}>
          <Zap className="h-4 w-4" />
          <AlertDescription>
            <strong>Overall Status:</strong> {status.overall ? "All systems operational!" : "Some services are down"}
            {getStatusBadge(status.overall)}
          </AlertDescription>
        </Alert>

        {/* Individual Service Status */}
        <div className="grid grid-cols-2 gap-4">
          {/* Health Check */}
          <div className="flex items-center justify-between p-3 rounded-lg border">
            <div className="flex items-center space-x-2">
              <Server className="h-4 w-4" />
              <span className="text-sm font-medium">Health Check</span>
            </div>
            <div className="flex items-center">
              <StatusIcon success={status.health} />
              {getStatusBadge(status.health)}
            </div>
          </div>

          {/* Chat API */}
          <div className="flex items-center justify-between p-3 rounded-lg border">
            <div className="flex items-center space-x-2">
              <MessageCircle className="h-4 w-4" />
              <span className="text-sm font-medium">Chat API</span>
            </div>
            <div className="flex items-center">
              <StatusIcon success={status.chat} />
              {getStatusBadge(status.chat)}
            </div>
          </div>

          {/* TTS Service */}
          <div className="flex items-center justify-between p-3 rounded-lg border">
            <div className="flex items-center space-x-2">
              <Volume2 className="h-4 w-4" />
              <span className="text-sm font-medium">TTS Service</span>
            </div>
            <div className="flex items-center">
              <StatusIcon success={status.tts} />
              {getStatusBadge(status.tts)}
            </div>
          </div>

          {/* Authentication */}
          <div className="flex items-center justify-between p-3 rounded-lg border">
            <div className="flex items-center space-x-2">
              <Shield className="h-4 w-4" />
              <span className="text-sm font-medium">Authentication</span>
            </div>
            <div className="flex items-center">
              <StatusIcon success={status.auth} />
              {getStatusBadge(status.auth)}
            </div>
          </div>
        </div>

        {/* Test Results */}
        {(results.ping || results.error) && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Test Results:</h4>
            
            {results.ping && (
              <div className="p-3 bg-muted rounded-lg">
                <div className="text-xs font-mono">
                  <div><strong>API:</strong> {results.ping.message}</div>
                  <div><strong>Version:</strong> {results.ping.version}</div>
                </div>
              </div>
            )}

            {results.chat && (
              <div className="p-3 bg-muted rounded-lg">
                <div className="text-xs font-mono">
                  <div><strong>Chat Response:</strong> {results.chat.response?.substring(0, 100)}...</div>
                  <div><strong>Conversation ID:</strong> {results.chat.conversation_id}</div>
                  <div><strong>Category:</strong> {results.chat.flags?.category}</div>
                </div>
              </div>
            )}

            {results.error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <div className="text-xs text-red-700">
                  <strong>Error:</strong> {results.error}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Last Test Time */}
        {lastTest && (
          <div className="text-xs text-muted-foreground text-center">
            Last tested: {lastTest.toLocaleTimeString()}
          </div>
        )}

        {/* Quick Actions */}
        <div className="flex space-x-2">
          <Button
            onClick={() => window.open('http://localhost:8000/docs', '_blank')}
            variant="outline"
            size="sm"
            className="flex-1"
          >
            Open API Docs
          </Button>
          <Button
            onClick={() => window.open('http://localhost:8000', '_blank')}
            variant="outline"
            size="sm"
            className="flex-1"
          >
            Backend Homepage
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default APIConnectionTest;
