import React from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import ClaudeEditor from './components/ClaudeEditor';

function App() {
  return (
    <div>
      <Header />

      {/* 💠 Main Content Grid with Tailwind */}
      <main className="grid grid-cols-1 md:grid-cols-[1fr_3fr] gap-8 px-8 py-6">
        <Dashboard />
        <ClaudeEditor />
      </main>

      {/* 🔧 Tailwind Test Block */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-500 text-white text-3xl p-4 mt-8 rounded-lg shadow-lg text-center">
        ✅ Tailwind is working!
      </div>
    </div>
  );
}

export default App;