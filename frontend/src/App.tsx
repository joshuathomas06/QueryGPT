import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Database, Loader2, AlertCircle, CheckCircle2, History, Plus, Copy, Check, ChevronDown, Sparkles, X } from 'lucide-react';
import './App.css';

interface QueryResult {
  sql_query: string;
  results: Array<Record<string, any>>;
  explanation: string;
  success: boolean;
  error?: string;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  result?: QueryResult;
}

function App() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [history, setHistory] = useState<QueryResult[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [copied, setCopied] = useState('');
  const [examples] = useState([
    {
      title: 'Cloud Provider Costs',
      prompt: 'What is the total cost by cloud provider this month?'
    },
    {
      title: 'Environment Analysis',
      prompt: 'Which environments have the highest costs?'
    },
    {
      title: 'Cost Center Breakdown',
      prompt: 'Show me cost breakdown by cost center'
    },
    {
      title: 'AWS Tag Analysis',
      prompt: 'What are the most expensive tags in AWS?'
    }
  ]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: question.trim()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setQuestion('');
    setLoading(true);
    
    try {
      const response = await axios.post('/api/query', {
        question: userMessage.content
      });
      
      const newResult = response.data;
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '',
        result: newResult
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      setHistory(prev => [newResult, ...prev.slice(0, 19)]); // Keep only last 20 queries
    } catch (error) {
      console.error('Error:', error);
      const errorResult: QueryResult = {
        sql_query: '',
        results: [],
        explanation: 'Failed to connect to the server. Please make sure the API is running on port 8000.',
        success: false,
        error: 'Connection error'
      };
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '',
        result: errorResult
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(type);
      setTimeout(() => setCopied(''), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  const handleExampleClick = (prompt: string) => {
    setQuestion(prompt);
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [question]);

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="header-left">
            <h1>QueryGPT</h1>
            <button className="model-selector">
              <span>Claude 3.5</span>
              <ChevronDown size={16} />
            </button>
          </div>
          <div className="header-actions">
            <button 
              className="header-btn"
              onClick={() => setHistory([])}
              title="New Chat"
            >
              <Plus size={20} />
            </button>
            <button 
              className="header-btn"
              onClick={() => setShowHistory(!showHistory)}
              title="Query History"
            >
              <History size={20} />
            </button>
          </div>
        </div>
      </header>

      <main className="main">
        <div className="chat-container">
          {messages.length === 0 ? (
            <div className="center-prompt">
              <h2>What's on your mind today?</h2>
              <div className="examples-container">
                {examples.map((example, index) => (
                  <div
                    key={index}
                    className="example-card"
                    onClick={() => handleExampleClick(example.prompt)}
                  >
                    <h3>{example.title}</h3>
                    <p>{example.prompt}</p>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages-container">
              {messages.map((message) => (
                <div key={message.id} className={`message ${message.role}`}>
                  <div className="message-content">
                    <div className="message-icon">
                      {message.role === 'user' ? 'U' : <Database size={16} />}
                    </div>
                    <div className="message-body">
                      {message.role === 'user' ? (
                        <p>{message.content}</p>
                      ) : (
                        message.result && (
                          <div className="result-container">
                            <div className={`result-header ${message.result.success ? 'success' : 'error'}`}>
                              {message.result.success ? (
                                <><CheckCircle2 className="status-icon" size={16} /> Query executed successfully</>
                              ) : (
                                <><AlertCircle className="status-icon" size={16} /> Query failed</>
                              )}
                            </div>

                            {message.result.sql_query && (
                              <div className="sql-section">
                                <div className="section-header">
                                  <h3>Generated SQL:</h3>
                                  <button
                                    className="copy-btn"
                                    onClick={() => copyToClipboard(message.result!.sql_query, 'sql')}
                                    title="Copy SQL"
                                  >
                                    {copied === 'sql' ? <Check size={14} /> : <Copy size={14} />}
                                    <span>Copy</span>
                                  </button>
                                </div>
                                <pre className="sql-code">{message.result.sql_query}</pre>
                              </div>
                            )}

                            <div className="explanation-section">
                              <h3>Explanation:</h3>
                              <p className="explanation">{message.result.explanation}</p>
                            </div>

                            {message.result.success && message.result.results.length > 0 && (
                              <div className="results-section">
                                <h3>Results ({message.result.results.length} rows):</h3>
                                <div className="results-table-container">
                                  <table className="results-table">
                                    <thead>
                                      <tr>
                                        {Object.keys(message.result.results[0]).map(key => (
                                          <th key={key}>{key}</th>
                                        ))}
                                      </tr>
                                    </thead>
                                    <tbody>
                                      {message.result.results.slice(0, 100).map((row, index) => (
                                        <tr key={index}>
                                          {Object.values(row).map((value, i) => (
                                            <td key={i}>{String(value)}</td>
                                          ))}
                                        </tr>
                                      ))}
                                    </tbody>
                                  </table>
                                </div>
                                {message.result.results.length > 100 && (
                                  <p className="result-info">Showing first 100 results of {message.result.results.length} total</p>
                                )}
                              </div>
                            )}

                            {message.result.success && message.result.results.length === 0 && (
                              <div className="empty-results">
                                <p>Query executed successfully but returned no results.</p>
                              </div>
                            )}
                          </div>
                        )
                      )}
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}

          {showHistory && history.length > 0 && (
            <div className="history-section">
              <div className="section-header">
                <h3>Query History</h3>
                <button
                  className="clear-btn"
                  onClick={() => setHistory([])}
                  title="Clear History"
                >
                  Clear All
                </button>
              </div>
              <div className="history-list">
                {history.map((item, index) => (
                  <div key={index} className="history-item">
                    <div className="history-sql">
                      <code>{item.sql_query || 'Natural language query'}</code>
                    </div>
                    <div className="history-meta">
                      <span className={`history-status ${item.success ? 'success' : 'error'}`}>
                        {item.success ? '✓' : '✗'}
                      </span>
                      <span className="history-count">
                        {item.success ? `${item.results.length} rows` : 'Failed'}
                      </span>
                      <button
                        className="copy-btn-small"
                        onClick={() => copyToClipboard(item.sql_query, `history-${index}`)}
                        title="Copy SQL"
                      >
                        {copied === `history-${index}` ? <Check size={12} /> : <Copy size={12} />}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="input-section">
          <div className="input-wrapper">
            <form onSubmit={handleSubmit} className="query-form">
              <div className="input-container">
                <div className="input-actions">
                  <button type="button" className="tool-button">
                    <Plus size={16} />
                    <span>Tools</span>
                  </button>
                </div>
                <textarea
                  ref={textareaRef}
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask anything"
                  className="query-input"
                  rows={1}
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={!question.trim() || loading}
                  className={`send-button ${question.trim() ? 'active' : ''}`}
                >
                  {loading ? <Loader2 className="spinner" size={20} /> : <Send size={20} />}
                </button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
