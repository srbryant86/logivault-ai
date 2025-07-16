import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Header from './Header';

describe('Header Component', () => {
  test('renders header title', () => {
    render(<Header />);
    const headerTitle = screen.getByText('📘 Logivault Editor');
    expect(headerTitle).toBeInTheDocument();
  });

  test('renders as a header element', () => {
    render(<Header />);
    const headerElement = screen.getByRole('banner');
    expect(headerElement).toBeInTheDocument();
  });
});