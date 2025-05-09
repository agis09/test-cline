import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import { marked } from 'marked';

function App() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      setChatHistory([...chatHistory, `User: ${message}`, `Agent: processing......`]);
      const response = await axios.post('/chat', { "message": message });
      const agentResponse = response.data.response;
      const parsedMessage = marked.parse(agentResponse);
      setChatHistory(prevChatHistory => [...prevChatHistory, `User: ${message}`, `Agent: ${parsedMessage}`]);
      setMessage(''); // Clear the input field after sending
    } catch (error) {
      console.error("Error making request:", error);
      setChatHistory([...chatHistory, "Error: Could not connect to backend."]);
    } finally {
      setIsLoading(false);
    }
  };

  // useEffect to set up proxy
  useEffect(() => {
    const setupProxy = async () => {
      const proxyUrl = 'http://localhost:8000'; // Replace with your backend URL
      axios.defaults.baseURL = proxyUrl;
    };

    setupProxy();
  }, []);

  return (
    <div className="App">
      <h1>Chat with Agent</h1>
      {isLoading && <p>Waiting for response...</p>}
      <div className="chat-history">
        {chatHistory.map((message, index) => {
          const isUser = message.startsWith("User:");
          const messageClass = isUser ? "user-message" : "agent-message";
          return (
            <p key={index} className={messageClass} dangerouslySetInnerHTML={{ __html: message }} />
          );
        })}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default App;
