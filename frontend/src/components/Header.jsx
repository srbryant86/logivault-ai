import React from 'react';

export default function Header() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">L</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">LogiVault™</h1>
              <p className="text-sm text-gray-600">Precision Writing. Zero Hallucination. Audit-Grade Intelligence.</p>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-6">
            <span className="text-sm text-gray-500">Nonfiction Intelligence Engine</span>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Trust-Locked</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

