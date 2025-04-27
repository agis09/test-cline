import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<string[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/chat', { "message": message });
      setChatHistory([...chatHistory, `User: ${message}`, `Agent: ${response.data.response}`]);
      setMessage(''); // Clear the input field after sending
    } catch (error) {
      console.error("Error making request:", error);
      setChatHistory([...chatHistory, "Error: Could not connect to backend."]);
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
      <div className="chat-history">
        {chatHistory.map((message, index) => (
          <p key={index}>{message}</p>
        ))}
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
