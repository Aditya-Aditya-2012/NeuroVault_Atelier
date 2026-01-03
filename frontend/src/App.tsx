import { useState, useEffect } from 'react';
import { GalleryGrid } from './components/GalleryGrid';
import { AuthModal } from './components/AuthModal';
import { PlusCircle, LogOut } from 'lucide-react';
import { authApi } from './api/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'));

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      {!isAuthenticated && (
        <AuthModal onLoginSuccess={() => setIsAuthenticated(true)} />
      )}

      <nav className="sticky top-0 z-50 border-b border-white/5 bg-slate-950/80 backdrop-blur-md px-8 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold text-emerald-400">NeuroVault</h1>
          <p className="text-[10px] text-slate-500 font-mono">ATELIER V1.0</p>
        </div>
        
        <div className="flex items-center gap-4">
          <button className="flex items-center gap-2 bg-emerald-500 text-slate-950 px-4 py-2 rounded-lg font-bold text-sm">
            <PlusCircle className="w-4 h-4" /> Deposit
          </button>
          <button 
            onClick={() => authApi.logout()}
            className="p-2 text-slate-500 hover:text-red-400 transition-colors"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-8">
        <GalleryGrid />
      </main>
    </div>
  );
}

export default App;