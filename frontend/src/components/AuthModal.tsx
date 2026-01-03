import { useState } from 'react';
import { authApi } from '../api/api';
import { Lock, User, Loader2 } from 'lucide-react';

export const AuthModal = ({ onLoginSuccess }: { onLoginSuccess: () => void }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    const formData = new FormData(e.currentTarget);

    try {
      if (isLogin) {
        await authApi.login(formData);
      } else {
        // Prepare signup data (Note: FastAPI might expect JSON for signup)
        const signupData = Object.fromEntries(formData.entries());
        await authApi.signup(signupData);
        // Auto-login after signup
        await authApi.login(formData);
      }
      onLoginSuccess();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
      <div className="w-full max-w-md rounded-2xl border border-white/10 bg-slate-900 p-8 shadow-2xl">
        <h2 className="text-2xl font-bold text-white mb-2">
          {isLogin ? 'Welcome Back' : 'Join the Atelier'}
        </h2>
        <p className="text-slate-400 text-sm mb-6">
          {isLogin ? 'Enter your credentials to access your vault.' : 'Create an account to start your collection.'}
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="relative">
            <User className="absolute left-3 top-3 h-5 w-5 text-slate-500" />
            <input 
              name="username" 
              type="text" 
              placeholder="Username" 
              className="w-full bg-slate-950 border border-white/5 rounded-lg py-2.5 pl-10 pr-4 text-white focus:border-emerald-500 outline-none transition-all"
              required 
            />
          </div>
          <div className="relative">
            <Lock className="absolute left-3 top-3 h-5 w-5 text-slate-500" />
            <input 
              name="password" 
              type="password" 
              placeholder="Password" 
              className="w-full bg-slate-950 border border-white/5 rounded-lg py-2.5 pl-10 pr-4 text-white focus:border-emerald-500 outline-none transition-all"
              required 
            />
          </div>

          {error && <p className="text-red-400 text-xs italic">{error}</p>}

          <button 
            disabled={loading}
            className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-3 rounded-lg transition-all flex items-center justify-center gap-2"
          >
            {loading ? <Loader2 className="animate-spin h-5 w-5" /> : (isLogin ? 'Unlock Vault' : 'Create Account')}
          </button>
        </form>

        <button 
          onClick={() => setIsLogin(!isLogin)}
          className="w-full mt-6 text-slate-500 text-sm hover:text-emerald-400 transition-colors"
        >
          {isLogin ? "Don't have an account? Sign up" : "Already have an account? Log in"}
        </button>
      </div>
    </div>
  );
};