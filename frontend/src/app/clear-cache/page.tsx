'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function ClearCachePage() {
  const router = useRouter();

  useEffect(() => {
    // Clear all localStorage
    if (typeof window !== 'undefined') {
      localStorage.clear();
      console.log('LocalStorage cleared');
    }
    
    // Redirect to login page
    router.push('/login');
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-4">Clearing Cache...</h1>
        <p>Redirecting to login page...</p>
      </div>
    </div>
  );
} 