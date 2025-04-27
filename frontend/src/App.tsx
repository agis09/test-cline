import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<string[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Making request to backend...");
    try {
      const response = await axios.post('/search', { "query": query });
      console.log("Received response from backend...");
      setResults(response.data.results);
    } catch (error) {
      console.error("Error making request:", error);
      setResults(["Error: Could not connect to backend."]);
    }
  };

  return (
    <div className="App">
      <h1>Deep Research</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
      <div>
        {results.map((result, index) => (
          <p key={index}>{result}</p>
        ))}
      </div>
    </div>
  );
}

export default App;
