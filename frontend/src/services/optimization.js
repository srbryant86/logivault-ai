// src/services/optimization.js

/**
 * Trims excess whitespace and normalizes line breaks
 */
export function cleanResponse(rawText) {
  return rawText
    .replace(/\r?\n\s*\r?\n/g, '\n\n')   // collapse blank lines
    .replace(/\s{2,}/g, ' ')             // collapse multiple spaces
    .trim();
}

/**
 * Converts basic Markdown into readable HTML
 */
export function formatEditorial(content) {
  return content
    .replace(/### (.*?)\n/g, '<h3>$1</h3>')
    .replace(/## (.*?)\n/g, '<h2>$1</h2>')
    .replace(/# (.*?)\n/g, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br />');
}