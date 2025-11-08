import React, { useState, useEffect, useRef, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { API_URL } from '../config';

interface Document {
  id: number;
  filename: string;
  file_type: string;
  created_at: string;
}

interface POC {
  id: number;
  poc_id: string;
  poc_name: string;
  description: string;
  created_at: string;
}

interface PRD {
  prd_name: string;
  file_path: string;
  feature_name: string;
  created_at: string;
}

interface Message {
  role: 'user' | 'agent';
  content: string;
  timestamp: Date;
}

const PRDBuilder: React.FC = () => {
  const { token } = useAuth();
  const [activeTab, setActiveTab] = useState<'documents' | 'prds'>('documents');
  
  // Documents state
  const [documents, setDocuments] = useState<Document[]>([]);
  const [uploading, setUploading] = useState(false);
  
  // PRDs state
  const [prds, setPrds] = useState<PRD[]>([]);
  const [selectedPrd, setSelectedPrd] = useState<PRD | null>(null);
  const [prdContent, setPrdContent] = useState<string>('');
  
  // Chat state
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadDocuments = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/api/poc/documents`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDocuments(response.data);
    } catch (error) {
      console.error('Failed to load documents:', error);
    }
  }, [token]);

  const loadPRDs = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/api/poc/list-prds`);
      setPrds(response.data);
    } catch (error) {
      console.error('Failed to load PRDs:', error);
    }
  }, []);

  // Load documents and PRDs
  useEffect(() => {
    if (token) {
      loadDocuments();
      loadPRDs();
    }
  }, [token, loadDocuments, loadPRDs]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${API_URL}/api/poc/upload`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      loadDocuments();
      if (fileInputRef.current) fileInputRef.current.value = '';
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (docId: number) => {
    if (!window.confirm('Delete this document?')) return;

    try {
      await axios.delete(`${API_URL}/api/poc/documents/${docId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      loadDocuments();
    } catch (error) {
      alert('Failed to delete document');
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const userInput = input;
    setInput('');
    setIsTyping(true);

    // Check if user is asking to generate PRD
    const generatePrdKeywords = ['generate prd', 'generate a prd', 'create prd', 'create a prd', 'build prd', 'build a prd'];
    const shouldGeneratePrd = generatePrdKeywords.some(keyword => userInput.toLowerCase().includes(keyword));

    if (shouldGeneratePrd && conversationId) {
      try {
        // Generate PRD
        const prdResponse = await axios.post(
          `${API_URL}/api/poc/generate-prd`,
          {
            requirements: {} // Agent will extract from conversation
          },
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );

        const successMessage: Message = {
          role: 'agent',
          content: `✅ PRD Generated!\n\n**File**: ${prdResponse.data.prd_name}\n**Feature**: ${prdResponse.data.feature_name}\n**Location**: /prd/${prdResponse.data.prd_name}\n\nYour PRD has been saved with complete implementation instructions for Cursor AI. You can now use the command "Build my PRD" to implement this feature.`,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, successMessage]);
        loadPRDs(); // Refresh PRD list
      } catch (error: any) {
        const errorMessage: Message = {
          role: 'agent',
          content: 'Error generating PRD: ' + (error.response?.data?.detail || 'Failed to generate PRD'),
          timestamp: new Date()
        };
        setMessages(prev => [...prev, errorMessage]);
      } finally {
        setIsTyping(false);
      }
      return;
    }

    // Normal chat flow
    try {
      const response = await axios.post(
        `${API_URL}/api/poc/chat`,
        {
          prompt: userInput,
          conversation_history: conversationId ? { conversation_id: conversationId } : null
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      const agentMessage: Message = {
        role: 'agent',
        content: response.data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, agentMessage]);
      setConversationId(response.data.conversation_id);
    } catch (error: any) {
      const errorMessage: Message = {
        role: 'agent',
        content: 'Error: ' + (error.response?.data?.detail || 'Failed to get response'),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };


  return (
    <div className="flex h-full bg-white">
      {/* Left Panel (40%) */}
      <div className="w-2/5 bg-white border-r border-gray-200 flex flex-col">
        {/* Tab Switcher */}
        <div className="flex border-b border-gray-200">
          <button
            className={`flex-1 py-3 px-4 text-sm font-medium transition ${
              activeTab === 'documents'
                ? 'text-gray-900 border-b-2 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('documents')}
          >
            Documents
          </button>
          <button
            className={`flex-1 py-3 px-4 text-sm font-medium transition ${
              activeTab === 'prds'
                ? 'text-gray-900 border-b-2 border-indigo-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('prds')}
          >
            PRDs
          </button>
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {activeTab === 'documents' ? (
            <div>
              {/* Upload Zone */}
              <div className="mb-4">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.txt,.md,.png,.jpg,.jpeg"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className={`block w-full p-6 border-2 border-dashed rounded-lg text-center cursor-pointer transition ${
                    uploading
                      ? 'border-gray-200 bg-gray-50'
                      : 'border-gray-200 hover:border-indigo-300 hover:bg-gray-50'
                  }`}
                >
                  {uploading ? (
                    <span className="text-gray-500">Uploading...</span>
                  ) : (
                    <div>
                      <span className="text-gray-900 font-medium">Upload Document</span>
                      <p className="text-sm text-gray-500 mt-1">PDF, TXT, MD, PNG, JPG</p>
                    </div>
                  )}
                </label>
              </div>

              {/* Document List */}
              <div className="space-y-2">
                {documents.length === 0 ? (
                  <p className="text-gray-500 text-sm">No documents uploaded yet</p>
                ) : (
                  documents.map(doc => (
                    <div
                      key={doc.id}
                      className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:border-gray-300 transition"
                    >
                      <div className="flex-1">
                        <p className="font-medium text-sm">{doc.filename}</p>
                        <p className="text-xs text-gray-500">
                          {doc.file_type.toUpperCase()} • {new Date(doc.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <button
                        onClick={() => handleDeleteDocument(doc.id)}
                        className="ml-2 text-gray-400 hover:text-gray-600 text-xl"
                      >
                        ×
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              {prds.length === 0 ? (
                <p className="text-gray-500 text-sm">No PRDs created yet</p>
              ) : (
                prds.map(prd => (
                  <div
                    key={prd.prd_name}
                    className={`p-3 rounded-lg cursor-pointer transition ${
                      selectedPrd?.prd_name === prd.prd_name
                        ? 'bg-indigo-50 border border-indigo-200'
                        : 'border border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={async () => {
                      setSelectedPrd(prd);
                      // Load PRD content
                      try {
                        const response = await axios.get(`${API_URL}/api/poc/prd/${prd.prd_name}`);
                        setPrdContent(response.data.content);
                      } catch (error) {
                        console.error('Failed to load PRD content:', error);
                        setPrdContent('Failed to load PRD content');
                      }
                    }}
                  >
                    <p className="font-medium text-sm">{prd.feature_name}</p>
                    <p className="text-xs text-gray-600 mt-1">{prd.prd_name}</p>
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(prd.created_at).toLocaleDateString()}
                    </p>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </div>

      {/* Right Panel (60%) */}
      <div className="w-3/5 flex flex-col bg-white">
        {/* Chat Header */}
        <div className="border-b border-gray-200 p-6">
          <h1 className="text-xl font-semibold text-gray-900">PRD Builder</h1>
          <p className="text-sm text-gray-500 mt-1">Technical Product Manager AI</p>
        </div>

        {/* Messages or PRD Preview */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {selectedPrd && prdContent ? (
            <div>
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-gray-900">{selectedPrd.feature_name}</h2>
                <button
                  onClick={() => {
                    setSelectedPrd(null);
                    setPrdContent('');
                  }}
                  className="text-gray-400 hover:text-gray-600 text-xl"
                >
                  ×
                </button>
              </div>
              <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono overflow-x-auto">
                  {prdContent}
                </pre>
              </div>
              <div className="mt-4 p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
                <p className="text-sm text-gray-700">
                  <strong>To implement:</strong> Tell Cursor "Build my PRD"
                </p>
              </div>
            </div>
          ) : messages.length === 0 ? (
            <div className="text-center text-gray-400 mt-16">
              <p className="text-lg font-medium">Start a conversation</p>
              <p className="text-sm mt-2">Tell me what you'd like to build</p>
            </div>
          ) : null}
          
          {!selectedPrd && messages.length > 0 && (
            <>
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                  msg.role === 'user'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                }`}
              >
                    <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                    <p className={`text-xs mt-2 ${
                      msg.role === 'user' ? 'text-indigo-100' : 'text-gray-500'
                }`}>
                  {msg.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
            </>
          )}
          
          {!selectedPrd && isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg p-4">
                <p className="text-sm text-gray-500">Agent is typing...</p>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area - Hide when viewing PRD */}
        {!selectedPrd && (
          <div className="border-t border-gray-200 p-6">
            <div className="flex space-x-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type your message..."
                className="flex-1 px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
              disabled={isTyping}
            />
            <button
              onClick={handleSendMessage}
              disabled={isTyping || !input.trim()}
                className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </div>
        </div>
        )}
      </div>
    </div>
  );
};

export default PRDBuilder;
