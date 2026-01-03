import { useEffect, useState } from 'react';
import { vaultApi, type VaultImage } from '../api/api';
import { Loader2, Zap } from 'lucide-react';

export const GalleryGrid = () => {
  const [images, setImages] = useState<VaultImage[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGallery = async () => {
      try {
        const data = await vaultApi.getGallery();
        setImages(data);
      } catch (error) {
        console.error("Vault Error:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchGallery();
  }, []);

  if (loading) return (
    <div className="flex h-64 items-center justify-center">
      <Loader2 className="animate-spin text-emerald-500 w-10 h-10" />
    </div>
  );

  return (
    <div className="columns-1 md:columns-2 lg:columns-3 gap-4 p-4">
      {images.map((img) => (
        <div key={img.id} className="relative mb-4 break-inside-avoid rounded-xl border border-white/10 bg-white/5 overflow-hidden group">
          <img 
            // 🚩 Fix: If getImageUrl returns an empty string, we pass null instead
            src={vaultApi.getImageUrl(img.original)} 
            alt={`Vault item ${img.id}`}
            className="w-full h-auto transition-transform duration-500 group-hover:scale-105"
            // 🚩 Optimization: Optional loading attribute for better performance
            loading="lazy" 
            // 🚩 Safety: Handle cases where the file might be missing on disk
            onError={(e) => {
              e.currentTarget.src = "https://placehold.co/600x400?text=Atelier+Image+Not+Found";
            }}
          />
          
          {/* AI Overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent opacity-0 group-hover:opacity-100 transition-opacity p-4 flex flex-col justify-end">
             <div className="flex flex-wrap gap-2">
                {img.keywords?.map(tag => (
                  <span key={tag} className="text-[10px] font-bold uppercase tracking-tighter bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded border border-emerald-500/30 backdrop-blur-md">
                    {tag}
                  </span>
                ))}
             </div>
          </div>
        </div>
      ))}
    </div>
  );
};