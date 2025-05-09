import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders chat with agent title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Chat with Agent/i);
  expect(titleElement).toBeInTheDocument();
});
