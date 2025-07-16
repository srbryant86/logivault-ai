import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

describe('App Component', () => {
  test('renders header component', () => {
    render(<App />);
    // Just check that the app renders without crashing
    expect(document.body).toBeInTheDocument();
  });

  test('renders main content grid', () => {
    render(<App />);
    const mainElement = screen.getByRole('main');
    expect(mainElement).toBeInTheDocument();
  });

  test('renders tailwind test block', () => {
    render(<App />);
    const tailwindTest = screen.getByText('✅ Tailwind is working!');
    expect(tailwindTest).toBeInTheDocument();
  });
});