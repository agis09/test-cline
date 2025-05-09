import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders chat with agent title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Chat with Agent/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders markdown from agent response', () => {
  render(<App />);
  const markdownText = 'Agent: # Hello, world!';
  const element = screen.getByText(/Hello, world!/i);
  expect(element).toBeInTheDocument();
});
