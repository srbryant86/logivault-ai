import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ClaudeEditor from './ClaudeEditor';

// Mock the API service
jest.mock('../services/api', () => ({
  submitPromptToClaude: jest.fn(),
}));

// Mock the optimization service
jest.mock('../services/optimization', () => ({
  cleanResponse: jest.fn(response => response),
  formatEditorial: jest.fn(response => response),
}));

// Mock the session logger
jest.mock('../services/sessionLogger', () => ({
  logSession: jest.fn(),
}));

describe('ClaudeEditor Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  test('renders form elements', () => {
    render(<ClaudeEditor />);
    
    const textarea = screen.getByPlaceholderText('Enter your editorial request...');
    const button = screen.getByText('Submit to Claude');
    
    expect(textarea).toBeInTheDocument();
    expect(button).toBeInTheDocument();
  });

  test('submit button is disabled when prompt is empty', () => {
    render(<ClaudeEditor />);
    
    const button = screen.getByText('Submit to Claude');
    expect(button).toBeDisabled();
  });

  test('submit button is enabled when prompt is not empty', () => {
    render(<ClaudeEditor />);
    
    const textarea = screen.getByPlaceholderText('Enter your editorial request...');
    const button = screen.getByText('Submit to Claude');
    
    fireEvent.change(textarea, { target: { value: 'Test prompt' } });
    expect(button).not.toBeDisabled();
  });

  test('displays loading state when submitting', async () => {
    const { submitPromptToClaude } = require('../services/api');
    submitPromptToClaude.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));
    
    render(<ClaudeEditor />);
    
    const textarea = screen.getByPlaceholderText('Enter your editorial request...');
    const button = screen.getByText('Submit to Claude');
    
    fireEvent.change(textarea, { target: { value: 'Test prompt' } });
    fireEvent.click(button);
    
    expect(screen.getByText('Generating...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('Submit to Claude')).toBeInTheDocument();
    });
  });
});