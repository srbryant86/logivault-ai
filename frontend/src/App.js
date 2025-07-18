import React from 'react';
import Header from './components/Header';
import OptimizationEngine from './components/OptimizationEngine';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <OptimizationEngine />
      </main>
    </div>
  );
}

export default App;

