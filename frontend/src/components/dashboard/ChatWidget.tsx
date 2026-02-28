import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Minimize2, Maximize2, X, Send, Menu, Volume2, VolumeX, AlertCircle, Wifi, WifiOff, Languages } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { useIsMobile } from '@/hooks/use-mobile';
import { useChat } from '@/hooks/useChat';
import { cn } from '@/lib/utils';

type ChatState = 'floating' | 'docked' | 'fullscreen';

const ChatWidget = () => {
  const isMobile = useIsMobile();
  const [chatState, setChatState] = useState<ChatState>('floating');
  const [message, setMessage] = useState('');
  const [showTooltip, setShowTooltip] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [speechRecognition, setSpeechRecognition] = useState<any>(null);
  const [speechStatus, setSpeechStatus] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('en-US');
  const [isTTSEnabled, setIsTTSEnabled] = useState(true);
  const [ttsVoices, setTTSVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [selectedTTSVoice, setSelectedTTSVoice] = useState<string>('');

  // Enhanced language options with TTS support
  const languageOptions = [
    { code: 'en-US', name: 'English', flag: '🇺🇸', initials: 'EN', ttsLang: 'en-US' },
    { code: 'hi-IN', name: 'हिंदी', flag: '🇮🇳', initials: 'HI', ttsLang: 'hi-IN' },
    { code: 'ml-IN', name: 'മലയാളം', flag: '🇮🇳', initials: 'ML', ttsLang: 'ml-IN' }
  ];

  // Use our custom chat hook
  const {
    messages,
    isLoading,
    error,
    currentConversationId,
    isConnected,
    threads,
    sendMessage: sendChatMessage,
    loadThread,
    createNewThread,
    clearChat,
    clearError,
    playAudio,
  } = useChat({ userId: 'demo_user_frontend' });

  // Initialize Speech Recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = selectedLanguage; // Use selected language
      
      recognition.onstart = () => {
        setIsRecording(true);
        setSpeechStatus(`Listening in ${languageOptions.find(lang => lang.code === selectedLanguage)?.name}...`);
      };
      
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setMessage(prev => prev + (prev ? ' ' : '') + transcript);
        setSpeechStatus('Text captured!');
        setTimeout(() => setSpeechStatus(''), 2000);
      };
      
      recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setSpeechStatus('Error: Could not recognize speech');
        setTimeout(() => setSpeechStatus(''), 3000);
      };
      
      recognition.onend = () => {
        setIsRecording(false);
        if (speechStatus === 'Listening...') {
          setSpeechStatus('');
        }
      };
      
      setSpeechRecognition(recognition);
    }
  }, [selectedLanguage]); // Re-initialize when language changes

  // Initialize TTS Voices
  useEffect(() => {
    const loadVoices = () => {
      const voices = window.speechSynthesis.getVoices();
      setTTSVoices(voices);
      
      // Auto-select voice based on selected language
      const currentLang = languageOptions.find(lang => lang.code === selectedLanguage);
      if (currentLang) {
        const preferredVoice = voices.find(voice => 
          voice.lang.startsWith(currentLang.ttsLang.split('-')[0])
        );
        if (preferredVoice) {
          setSelectedTTSVoice(preferredVoice.name);
        }
      }
    };

    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;
  }, [selectedLanguage]);

  // Text-to-Speech function
  const speakText = (text: string) => {
    if (!isTTSEnabled || !text.trim()) return;

    // Stop any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    
    // Set voice based on selection or language
    if (selectedTTSVoice) {
      const voice = ttsVoices.find(v => v.name === selectedTTSVoice);
      if (voice) utterance.voice = voice;
    } else {
      // Fallback to language-based voice selection
      const currentLang = languageOptions.find(lang => lang.code === selectedLanguage);
      if (currentLang) {
        const voice = ttsVoices.find(v => v.lang.startsWith(currentLang.ttsLang.split('-')[0]));
        if (voice) utterance.voice = voice;
      }
    }

    // Set speech properties
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 0.8;

    // Error handling
    utterance.onerror = (event) => {
      console.error('TTS Error:', event.error);
    };

    window.speechSynthesis.speak(utterance);
  };

  // Enhanced handleSendMessage with TTS for bot responses
  const handleSendMessage = async () => {
    if (message.trim() && !isLoading) {
      await sendChatMessage(message);
      setMessage('');
    }
  };

  // Remove auto-speak useEffect
  // useEffect(() => {
  //   if (messages.length > 0) {
  //     const lastMessage = messages[messages.length - 1];
  //     if (lastMessage.sender === 'bot' && isTTSEnabled) {
  //       setTimeout(() => speakText(lastMessage.text), 500);
  //     }
  //   }
  // }, [messages, isTTSEnabled]);

  // Enhanced playAudio function to handle both TTS and audio URLs
  const handlePlayAudio = (msg: any) => {
    if (msg.audioUrl) {
      // For server-generated audio, create audio element and play
      const audio = new Audio(msg.audioUrl);
      audio.play().catch(error => {
        console.error('Error playing audio:', error);
        // Fallback to TTS if audio fails
        speakText(msg.text);
      });
    } else if (msg.sender === 'bot') {
      // Use TTS for bot messages without audio URLs
      speakText(msg.text);
    }
  };

  const toggleTTS = () => {
    setIsTTSEnabled(!isTTSEnabled);
    if (!isTTSEnabled) {
      window.speechSynthesis.cancel();
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleThreadSelect = async (conversationId: string) => {
    await loadThread(conversationId);
    if (isMobile && showSidebar) {
      setShowSidebar(false);
    }
  };

  const handleNewChat = async () => {
    await createNewThread();
    if (isMobile && showSidebar) {
      setShowSidebar(false);
    }
  };

  const handleClearChat = () => {
    clearChat();
    if (isMobile && showSidebar) {
      setShowSidebar(false);
    }
  };

  const toggleSpeechRecognition = () => {
    if (!speechRecognition) {
      setSpeechStatus('Speech recognition not supported');
      setTimeout(() => setSpeechStatus(''), 3000);
      return;
    }

    if (isRecording) {
      speechRecognition.stop();
    } else {
      // Update language before starting
      speechRecognition.lang = selectedLanguage;
      speechRecognition.start();
    }
  };

  // Floating Button State
  if (chatState === 'floating') {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <div 
          className="relative"
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
        >
          <Button
            onClick={() => setChatState('docked')}
            className={cn(
              "w-14 h-14 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110 group relative",
              isConnected 
                ? "bg-gradient-orange" 
                : "bg-gray-400 hover:bg-gray-500"
            )}
          >
            <MessageCircle className="w-6 h-6 text-white group-hover:animate-pulse" />
            {/* Connection Status Indicator */}
            <div className={cn(
              "absolute -top-1 -right-1 w-4 h-4 rounded-full border-2 border-white",
              isConnected ? "bg-green-500" : "bg-red-500"
            )}>
              {isConnected ? (
                <Wifi className="w-2 h-2 text-white absolute top-0.5 left-0.5" />
              ) : (
                <WifiOff className="w-2 h-2 text-white absolute top-0.5 left-0.5" />
              )}
            </div>
          </Button>
          
          {/* Tooltip */}
          {showTooltip && (
            <div className="absolute bottom-16 right-0 bg-popover text-popover-foreground text-sm px-3 py-2 rounded-lg shadow-lg whitespace-nowrap animate-fade-in border border-border">
              <div>Chat with our chatbot Manny</div>
              <div className="text-xs text-muted-foreground">
                {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
              </div>
              <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-popover"></div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Fullscreen State
  if (chatState === 'fullscreen') {
    return (
      <div className="fixed inset-0 z-50 bg-background animate-scale-in">
        <div className="flex h-full">
          {/* Left Sidebar - Chat History */}
          <div className={cn(
            "transition-all duration-300 border-r border-border bg-card",
            showSidebar ? "w-80" : "w-0",
            isMobile && showSidebar ? "absolute inset-y-0 left-0 z-10 w-80 shadow-lg" : ""
          )}>
            {showSidebar && (
              <div className="h-full flex flex-col">
                <div className="p-4 border-b border-border">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-card-foreground">Chat History</h3>
                    <Badge variant={isConnected ? "default" : "destructive"} className="text-xs">
                      {isConnected ? 'Connected' : 'Offline'}
                    </Badge>
                  </div>
                  <Button
                    onClick={handleNewChat}
                    className="w-full mt-2 text-xs h-8"
                    disabled={!isConnected}
                  >
                    + New Chat
                  </Button>
                </div>
                <div className="flex-1 overflow-y-auto p-2">
                  {threads.map((thread) => (
                    <button
                      key={thread.conversation_id}
                      onClick={() => handleThreadSelect(thread.conversation_id)}
                      className={cn(
                        "w-full text-left p-3 rounded-lg hover:bg-secondary transition-colors duration-200 mb-2",
                        currentConversationId === thread.conversation_id && "bg-secondary"
                      )}
                    >
                      <div className="font-medium text-sm text-card-foreground mb-1">{thread.title}</div>
                      <div className="text-xs text-muted-foreground">
                        {thread.message_count} messages • {new Date(thread.updated_at).toLocaleDateString()}
                      </div>
                    </button>
                  ))}
                  {threads.length === 0 && isConnected && (
                    <div className="text-center text-muted-foreground text-sm p-4">
                      No conversations yet.<br />Start chatting to create your first thread!
                    </div>
                  )}
                  {!isConnected && (
                    <div className="text-center text-red-500 text-sm p-4">
                      <AlertCircle className="w-4 h-4 mx-auto mb-2" />
                      Unable to load conversations.<br />Check backend connection.
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Main Chat Area */}
          <div className="flex-1 flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border bg-card">
              <div className="flex items-center space-x-3">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setShowSidebar(!showSidebar)}
                  className="hover:bg-secondary transition-colors duration-200"
                >
                  <Menu className="w-4 h-4" />
                </Button>
                <Avatar className="w-8 h-8">
                  <AvatarFallback className="bg-gradient-orange text-white text-sm font-semibold">
                    M
                  </AvatarFallback>
                </Avatar>
                <h2 className="text-xl font-semibold">Manny - Your AI Assistant</h2>
                
                {/* TTS Toggle */}
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={toggleTTS}
                  className={cn(
                    "hover:bg-secondary transition-colors duration-200",
                    isTTSEnabled ? "text-green-600" : "text-gray-400"
                  )}
                  title={isTTSEnabled ? 'Disable text-to-speech' : 'Enable text-to-speech'}
                >
                  {isTTSEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
                </Button>
              </div>
              
              <div className="flex items-center space-x-2">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setChatState('docked')}
                  className="hover:bg-secondary transition-colors duration-200"
                >
                  <Minimize2 className="w-4 h-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setChatState('floating')}
                  className="hover:bg-secondary transition-colors duration-200"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-6">
              <div className="max-w-4xl mx-auto space-y-4">
                {/* Connection Error Alert */}
                {error && (
                  <Alert className="border-red-200 bg-red-50">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription className="flex items-center justify-between">
                      <span>{error}</span>
                      <Button onClick={clearError} variant="ghost" size="sm">
                        Dismiss
                      </Button>
                    </AlertDescription>
                  </Alert>
                )}

                {/* Messages */}
                {messages.map((msg) => (
                  <div key={msg.id} className={cn(
                    "flex items-start space-x-3",
                    msg.sender === 'user' && "flex-row-reverse space-x-reverse"
                  )}>
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className={cn(
                        "text-white text-sm font-semibold",
                        msg.sender === 'bot' ? "bg-gradient-orange" : "bg-primary"
                      )}>
                        {msg.sender === 'bot' ? 'M' : 'U'}
                      </AvatarFallback>
                    </Avatar>
                    <div className={cn(
                      "rounded-2xl p-4 max-w-md break-words",
                      msg.sender === 'bot' 
                        ? "bg-secondary rounded-tl-md" 
                        : "bg-primary text-primary-foreground rounded-tr-md"
                    )}>
                      <p className="text-sm">{msg.text}</p>
                      
                      {/* Sources */}
                      {msg.sources && msg.sources.length > 0 && (
                        <div className="mt-3 space-y-2">
                          <div className="text-xs font-semibold text-muted-foreground">Sources:</div>
                          {msg.sources.map((source, idx) => (
                            <div key={idx} className="text-xs bg-muted p-2 rounded">
                              <a 
                                href={source.url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="font-medium text-blue-600 hover:underline"
                              >
                                {source.title}
                              </a>
                              <div className="text-muted-foreground mt-1">{source.snippet}</div>
                            </div>
                          ))}
                        </div>
                      )}
                      
                      {/* Audio Player */}
                      {msg.sender === 'bot' && (
                        <div className="mt-3">
                          <Button
                            onClick={() => handlePlayAudio(msg)}
                            variant="ghost"
                            size="sm"
                            className="h-8 px-2 text-xs"
                            disabled={!isTTSEnabled && !msg.audioUrl}
                          >
                            <Volume2 className="w-3 h-3 mr-1" />
                            {msg.audioUrl ? 'Play Audio' : 'Speak Text'}
                          </Button>
                        </div>
                      )}
                      
                      {/* Message Metadata */}
                      {msg.flags && (
                        <div className="mt-2 text-xs text-muted-foreground">
                          {msg.flags.confidence_score && (
                            <span>Confidence: {Math.round(msg.flags.confidence_score * 100)}% • </span>
                          )}
                          {msg.flags.category && (
                            <span>Category: {msg.flags.category} • </span>
                          )}
                          <span>{msg.timestamp.toLocaleTimeString()}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {/* Loading Indicator */}
                {isLoading && (
                  <div className="flex items-start space-x-3">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className="bg-gradient-orange text-white text-sm font-semibold">
                        M
                      </AvatarFallback>
                    </Avatar>
                    <div className="bg-secondary rounded-2xl rounded-tl-md p-4">
                      <div className="flex items-center space-x-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                        <span className="text-sm text-muted-foreground">Manny is thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Message Input */}
            <div className="border-t border-border p-4 bg-card">
              <div className="max-w-4xl mx-auto">
                {/* Quick Actions */}
                <div className="flex flex-wrap gap-2 mb-3">
                  <Button
                    onClick={handleClearChat}
                    variant="outline"
                    size="sm"
                    className="text-xs h-7"
                  >
                    Clear Chat
                  </Button>
                  <Button
                    onClick={handleNewChat}
                    variant="outline"
                    size="sm"
                    className="text-xs h-7"
                    disabled={!isConnected}
                  >
                    New Thread
                  </Button>
                  <Button
                    onClick={() => window.open('http://localhost:8000/docs', '_blank')}
                    variant="outline"
                    size="sm"
                    className="text-xs h-7"
                  >
                    API Docs
                  </Button>
                </div>

                {/* TTS Voice Selector */}
                {isTTSEnabled && ttsVoices.length > 0 && (
                  <select
                    value={selectedTTSVoice}
                    onChange={(e) => setSelectedTTSVoice(e.target.value)}
                    className="text-xs h-7 px-2 border border-border rounded bg-background"
                  >
                    <option value="">Auto Voice</option>
                    {ttsVoices
                      .filter(voice => {
                        const currentLang = languageOptions.find(lang => lang.code === selectedLanguage);
                        return currentLang && voice.lang.startsWith(currentLang.ttsLang.split('-')[0]);
                      })
                      .map((voice) => (
                        <option key={voice.name} value={voice.name}>
                          {voice.name} ({voice.lang})
                        </option>
                      ))}
                  </select>
                )}

                {/* Speech Status */}
                {speechStatus && (
                  <div className={cn(
                    "mb-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300",
                    speechStatus.includes('Error') 
                      ? 'bg-red-100 text-red-700 border border-red-200' 
                      : speechStatus.includes('captured')
                      ? 'bg-green-100 text-green-700 border border-green-200'
                      : 'bg-blue-100 text-blue-700 border border-blue-200'
                  )}>
                    {speechStatus}
                  </div>
                )}

                <div className="flex items-center space-x-3">
                  <div className="relative flex-1">
                    <Input
                      type="text"
                      placeholder={isConnected ? "Ask Manny anything about SLCM..." : "Connect to backend to start chatting..."}
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      className="h-12 pr-24"
                      disabled={!isConnected || isLoading}
                    />
                    
                    {/* TTS Status Indicator */}
                    <div className="absolute right-16 top-1/2 transform -translate-y-1/2">
                      <button
                        onClick={toggleTTS}
                        className={cn(
                          "p-1 rounded-full transition-all duration-200",
                          isTTSEnabled ? "text-green-600 hover:bg-green-100" : "text-gray-400 hover:bg-gray-100"
                        )}
                        title={isTTSEnabled ? 'TTS enabled' : 'TTS disabled'}
                        type="button"
                      >
                        {isTTSEnabled ? <Volume2 className="w-3 h-3" /> : <VolumeX className="w-3 h-3" />}
                      </button>
                    </div>
                    
                    {/* Language Selector */}
                    <select
                      value={selectedLanguage}
                      onChange={(e) => setSelectedLanguage(e.target.value)}
                      className="absolute right-12 top-1/2 transform -translate-y-1/2 text-xs bg-transparent border-none focus:outline-none cursor-pointer text-gray-600 hover:text-blue-500"
                      title="Select language"
                      disabled={!isConnected || isLoading}
                    >
                      {languageOptions.map((lang) => (
                        <option key={lang.code} value={lang.code}>
                          {lang.flag} {lang.initials}
                        </option>
                      ))}
                    </select>
                    
                    {/* Mic Button */}
                    <button
                      onClick={toggleSpeechRecognition}
                      className={cn(
                        "absolute right-3 top-1/2 transform -translate-y-1/2 p-2 rounded-full transition-all duration-300",
                        isRecording
                          ? 'bg-red-500 text-white animate-pulse shadow-lg'
                          : 'hover:bg-gray-100 text-gray-500 hover:text-blue-500'
                      )}
                      title={`${isRecording ? 'Stop recording' : 'Start speech recognition'} (${languageOptions.find(lang => lang.code === selectedLanguage)?.name})`}
                      type="button"
                      disabled={!isConnected || isLoading}
                    >
                      <svg 
                        className="w-4 h-4" 
                        viewBox="0 0 24 24" 
                        fill="currentColor"
                      >
                        <path d="M12 2C13.1 2 14 2.9 14 4V10C14 11.1 13.1 12 12 12S10 11.1 10 10V4C10 2.9 10.9 2 12 2ZM19 10V12C19 15.9 15.9 19 12 19S5 15.9 5 12V10H7V12C7 14.8 9.2 17 12 17S17 14.8 17 12V10H19ZM11 22V20H13V22H11Z"/>
                      </svg>
                    </button>
                  </div>
                  
                  <Button
                    onClick={handleSendMessage}
                    disabled={!message.trim() || !isConnected || isLoading}
                    className="h-12 px-6 bg-gradient-orange"
                  >
                    <Send className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Mobile Overlay */}
        {isMobile && showSidebar && (
          <div 
            className="absolute inset-0 bg-black/50 z-5"
            onClick={() => setShowSidebar(false)}
          />
        )}
      </div>
    );
  }

  // Docked Panel State - Mobile Bottom Sheet
  if (isMobile) {
    return (
      <div className="fixed inset-x-0 bottom-0 z-50 animate-slide-in-right">
        <div className="bg-card border-t border-border rounded-t-2xl shadow-lg max-h-[70vh] flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border">
            <div className="flex items-center space-x-2">
              <Avatar className="w-6 h-6">
                <AvatarFallback className="bg-gradient-orange text-white text-xs font-semibold">
                  M
                </AvatarFallback>
              </Avatar>
              <h3 className="font-semibold text-sm">Manny</h3>
              <Badge variant={isConnected ? "default" : "destructive"} className="text-xs">
                {isConnected ? '●' : '○'}
              </Badge>
            </div>
            
            <div className="flex items-center space-x-1">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setChatState('fullscreen')}
                className="h-8 w-8 hover:bg-secondary transition-colors duration-200"
              >
                <Maximize2 className="w-4 h-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setChatState('floating')}
                className="h-8 w-8 hover:bg-secondary transition-colors duration-200"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          </div>

          {/* Error Alert */}
          {error && (
            <div className="p-3 border-b border-border">
              <Alert className="border-red-200 bg-red-50">
                <AlertCircle className="h-3 w-3" />
                <AlertDescription className="text-xs flex items-center justify-between">
                  <span>{error}</span>
                  <Button onClick={clearError} variant="ghost" size="sm" className="h-6 text-xs">
                    ×
                  </Button>
                </AlertDescription>
              </Alert>
            </div>
          )}

          {/* Chat Messages */}
          <div className="flex-1 p-4 overflow-y-auto min-h-[200px]">
            <div className="space-y-3">
              {messages.map((msg) => (
                <div key={msg.id} className={cn(
                  "flex items-start space-x-2",
                  msg.sender === 'user' && "flex-row-reverse space-x-reverse"
                )}>
                  <Avatar className="w-6 h-6">
                    <AvatarFallback className={cn(
                      "text-white text-xs font-semibold",
                      msg.sender === 'bot' ? "bg-gradient-orange" : "bg-primary"
                    )}>
                      {msg.sender === 'bot' ? 'M' : 'U'}
                    </AvatarFallback>
                  </Avatar>
                  <div className={cn(
                    "rounded-lg p-3 text-xs max-w-[250px] break-words",
                    msg.sender === 'bot' 
                      ? "bg-secondary rounded-tl-sm" 
                      : "bg-primary text-primary-foreground rounded-tr-sm"
                  )}>
                    <div>{msg.text}</div>
                    
                    {/* Enhanced Audio Button for Mobile - Always show for bot messages */}
                    {msg.sender === 'bot' && (
                      <Button
                        onClick={() => handlePlayAudio(msg)}
                        variant="ghost"
                        size="sm"
                        className="h-6 px-1 mt-2 text-xs"
                        disabled={!isTTSEnabled && !msg.audioUrl}
                      >
                        <Volume2 className="w-3 h-3 mr-1" />
                        {msg.audioUrl ? 'Audio' : 'Speak'}
                      </Button>
                    )}
                    
                    {/* Metadata */}
                    {msg.flags && (
                      <div className="mt-2 text-[10px] text-muted-foreground">
                        {msg.flags.confidence_score && (
                          <span>{Math.round(msg.flags.confidence_score * 100)}% • </span>
                        )}
                        {msg.flags.category}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              
              {/* Loading Indicator */}
              {isLoading && (
                <div className="flex items-start space-x-2">
                  <Avatar className="w-6 h-6">
                    <AvatarFallback className="bg-gradient-orange text-white text-xs font-semibold">
                      M
                    </AvatarFallback>
                  </Avatar>
                  <div className="bg-secondary rounded-lg rounded-tl-sm p-3">
                    <div className="flex items-center space-x-1">
                      <div className="flex space-x-1">
                        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                      <span className="text-xs text-muted-foreground">Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Message Input */}
          <div className="p-4 border-t border-border">
            {/* Speech Status */}
            {speechStatus && (
              <div className={cn(
                "mb-3 px-2 py-1 rounded-full text-xs font-medium transition-all duration-300",
                speechStatus.includes('Error') 
                  ? 'bg-red-100 text-red-700' 
                  : speechStatus.includes('captured')
                  ? 'bg-green-100 text-green-700'
                  : 'bg-blue-100 text-blue-700'
              )}>
                {speechStatus}
              </div>
            )}
            
            <div className="flex items-center space-x-2">
              <div className="relative flex-1">
                <Input
                  type="text"
                  placeholder={isConnected ? "Type your message..." : "Not connected..."}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="h-10 text-sm pr-20"
                  disabled={!isConnected || isLoading}
                />
                
                {/* TTS Status */}
                <button
                  onClick={toggleTTS}
                  className={cn(
                    "absolute right-12 top-1/2 transform -translate-y-1/2 p-0.5 rounded-full transition-colors duration-200",
                    isTTSEnabled ? "text-green-600" : "text-gray-400"
                  )}
                  title={isTTSEnabled ? 'TTS enabled' : 'TTS disabled'}
                  type="button"
                >
                  {isTTSEnabled ? <Volume2 className="w-2 h-2" /> : <VolumeX className="w-2 h-2" />}
                </button>
                
                {/* Language Selector */}
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="absolute right-8 top-1/2 transform -translate-y-1/2 text-xs bg-transparent border-none focus:outline-none cursor-pointer text-gray-600"
                  disabled={!isConnected || isLoading}
                >
                  {languageOptions.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.flag} {lang.initials}
                    </option>
                  ))}
                </select>
                
                {/* Mic Button */}
                <button
                  onClick={toggleSpeechRecognition}
                  className={cn(
                    "absolute right-2 top-1/2 transform -translate-y-1/2 p-1 rounded-full transition-all duration-300",
                    isRecording
                      ? 'bg-red-500 text-white animate-pulse'
                      : 'hover:bg-gray-100 text-gray-500 hover:text-blue-500'
                  )}
                  title={`${isRecording ? 'Stop recording' : 'Start speech recognition'} (${languageOptions.find(lang => lang.code === selectedLanguage)?.name})`}
                  type="button"
                  disabled={!isConnected || isLoading}
                >
                  <svg 
                    className="w-3 h-3" 
                    viewBox="0 0 24 24" 
                    fill="currentColor"
                  >
                    <path d="M12 2C13.1 2 14 2.9 14 4V10C14 11.1 13.1 12 12 12S10 11.1 10 10V4C10 2.9 10.9 2 12 2ZM19 10V12C19 15.9 15.9 19 12 19S5 15.9 5 12V10H7V12C7 14.8 9.2 17 12 17S17 14.8 17 12V10H19ZM11 22V20H13V22H11Z"/>
                  </svg>
                </button>
              </div>
              
              <Button
                onClick={handleSendMessage}
                disabled={!message.trim() || !isConnected || isLoading}
                size="icon"
                className="h-10 w-10 bg-gradient-orange"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Docked Panel State - Desktop
  return (
    <div className="fixed bottom-20 right-6 z-50 animate-slide-in-right">
      <Card className="w-80 h-96 shadow-glass backdrop-blur-glass bg-card border-border">
        {/* Header */}
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3 border-b border-border">
          <div className="flex items-center space-x-2">
            <Avatar className="w-6 h-6">
              <AvatarFallback className="bg-gradient-orange text-white text-xs font-semibold">
                M
              </AvatarFallback>
            </Avatar>
            <h3 className="font-semibold text-sm">Manny</h3>
            <Badge variant={isConnected ? "default" : "destructive"} className="text-xs">
              {isConnected ? '●' : '○'}
            </Badge>
          </div>
          
          <div className="flex items-center space-x-1">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setChatState('fullscreen')}
              className="h-6 w-6 hover:bg-secondary/50 transition-colors duration-200"
            >
              <Maximize2 className="w-3 h-3" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setChatState('floating')}
              className="h-6 w-6 hover:bg-secondary/50 transition-colors duration-200"
            >
              <Minimize2 className="w-3 h-3" />
            </Button>
          </div>
        </CardHeader>

        {/* Chat Messages */}
        <CardContent className="p-0 flex flex-col h-full">
          {/* Error Alert */}
          {error && (
            <div className="p-3 border-b border-border">
              <Alert className="border-red-200 bg-red-50">
                <AlertCircle className="h-3 w-3" />
                <AlertDescription className="text-xs flex items-center justify-between">
                  <span className="truncate">{error}</span>
                  <Button onClick={clearError} variant="ghost" size="sm" className="h-5 text-xs ml-2">
                    ×
                  </Button>
                </AlertDescription>
              </Alert>
            </div>
          )}

          <div className="flex-1 p-4 overflow-y-auto">
            <div className="space-y-3">
              {messages.map((msg) => (
                <div key={msg.id} className={cn(
                  "flex items-start space-x-2",
                  msg.sender === 'user' && "flex-row-reverse space-x-reverse"
                )}>
                  <Avatar className="w-6 h-6">
                    <AvatarFallback className={cn(
                      "text-white text-xs font-semibold",
                      msg.sender === 'bot' ? "bg-gradient-orange" : "bg-primary"
                    )}>
                      {msg.sender === 'bot' ? 'M' : 'U'}
                    </AvatarFallback>
                  </Avatar>
                  <div className={cn(
                    "rounded-lg p-3 text-xs max-w-[200px] break-words",
                    msg.sender === 'bot' 
                      ? "bg-secondary rounded-tl-sm" 
                      : "bg-primary text-primary-foreground rounded-tr-sm"
                  )}>
                    <div>{msg.text}</div>
                    
                    {/* Enhanced Audio Button - Always show for bot messages */}
                    {msg.sender === 'bot' && (
                      <Button
                        onClick={() => handlePlayAudio(msg)}
                        variant="ghost"
                        size="sm"
                        className="h-6 px-1 mt-2 text-xs"
                        disabled={!isTTSEnabled && !msg.audioUrl}
                      >
                        <Volume2 className="w-3 h-3 mr-1" />
                        {msg.audioUrl ? 'Audio' : 'Speak'}
                      </Button>
                    )}
                    
                    {/* Sources Indicator */}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-2 text-[10px] text-blue-600">
                        📚 {msg.sources.length} source{msg.sources.length > 1 ? 's' : ''}
                      </div>
                    )}
                    
                    {/* Metadata */}
                    {msg.flags && (
                      <div className="mt-2 text-[10px] text-muted-foreground">
                        {msg.flags.confidence_score && (
                          <span>{Math.round(msg.flags.confidence_score * 100)}% • </span>
                        )}
                        {msg.flags.category}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              
              {/* Loading Indicator */}
              {isLoading && (
                <div className="flex items-start space-x-2">
                  <Avatar className="w-6 h-6">
                    <AvatarFallback className="bg-gradient-orange text-white text-xs font-semibold">
                      M
                    </AvatarFallback>
                  </Avatar>
                  <div className="bg-secondary rounded-lg rounded-tl-sm p-3">
                    <div className="flex items-center space-x-1">
                      <div className="flex space-x-1">
                        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                      <span className="text-xs text-muted-foreground">Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Message Input */}
          <div className="p-3 border-t border-border">
            {/* Speech Status */}
            {speechStatus && (
              <div className={cn(
                "mb-2 px-2 py-1 rounded-full text-xs font-medium transition-all duration-300",
                speechStatus.includes('Error') 
                  ? 'bg-red-100 text-red-700' 
                  : speechStatus.includes('captured')
                  ? 'bg-green-100 text-green-700'
                  : 'bg-blue-100 text-blue-700'
              )}>
                {speechStatus}
              </div>
            )}
            
            <div className="flex items-center space-x-2">
              <div className="relative flex-1">
                <Input
                  type="text"
                  placeholder={isConnected ? "Type your message..." : "Not connected..."}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  className="h-8 text-sm pr-12"
                  disabled={!isConnected || isLoading}
                />
                
                {/* TTS Status */}
                <button
                  onClick={toggleTTS}
                  className={cn(
                    "absolute right-10 top-1/2 transform -translate-y-1/2 p-0.5 rounded-full transition-colors duration-200",
                    isTTSEnabled ? "text-green-600" : "text-gray-400"
                  )}
                  title={isTTSEnabled ? 'TTS enabled' : 'TTS disabled'}
                  type="button"
                >
                  {isTTSEnabled ? <Volume2 className="w-2 h-2" /> : <VolumeX className="w-2 h-2" />}
                </button>
                
                {/* Language Selector */}
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className="absolute right-6 top-1/2 transform -translate-y-1/2 text-xs bg-transparent border-none focus:outline-none cursor-pointer text-gray-600"
                  disabled={!isConnected || isLoading}
                >
                  {languageOptions.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.flag} {lang.initials}
                    </option>
                  ))}
                </select>
                
                {/* Mic Button */}
                <button
                  onClick={toggleSpeechRecognition}
                  className={cn(
                    "absolute right-2 top-1/2 transform -translate-y-1/2 p-1 rounded-full transition-all duration-300",
                    isRecording
                      ? 'bg-red-500 text-white animate-pulse'
                      : 'hover:bg-gray-100 text-gray-500 hover:text-blue-500'
                  )}
                  title={`${isRecording ? 'Stop recording' : 'Start speech recognition'} (${languageOptions.find(lang => lang.code === selectedLanguage)?.name})`}
                  type="button"
                  disabled={!isConnected || isLoading}
                >
                  <svg 
                    className="w-3 h-3" 
                    viewBox="0 0 24 24" 
                    fill="currentColor"
                  >
                    <path d="M12 2C13.1 2 14 2.9 14 4V10C14 11.1 13.1 12 12 12S10 11.1 10 10V4C10 2.9 10.9 2 12 2ZM19 10V12C19 15.9 15.9 19 12 19S5 15.9 5 12V10H7V12C7 14.8 9.2 17 12 17S17 14.8 17 12V10H19ZM11 22V20H13V22H11Z"/>
                  </svg>
                </button>
              </div>
              
              <Button
                onClick={handleSendMessage}
                disabled={!message.trim() || !isConnected || isLoading}
                size="icon"
                className="h-8 w-8 bg-gradient-orange"
              >
                <Send className="w-3 h-3" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ChatWidget;