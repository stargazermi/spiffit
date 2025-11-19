# Optional: Persistent cache that survives page reloads
# Not needed for hackathon demo, but included for reference

import json
import os
from datetime import datetime, timedelta
import hashlib

class PersistentCache:
    """
    Cache that survives page reloads by writing to disk
    """
    
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, prompt: str) -> str:
        """Generate a hash-based cache key"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get path to cache file"""
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, prompt: str, max_age_hours: int = 24):
        """
        Get cached result if it exists and is fresh
        
        Args:
            prompt: The query prompt
            max_age_hours: Maximum age of cache in hours
            
        Returns:
            Cached result or None if not found/expired
        """
        cache_key = self._get_cache_key(prompt)
        cache_path = self._get_cache_path(cache_key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
            
            # Check if cache is expired
            cached_time = datetime.fromisoformat(data['timestamp'])
            age = datetime.now() - cached_time
            
            if age > timedelta(hours=max_age_hours):
                # Cache expired
                os.remove(cache_path)
                return None
            
            return data['result']
        
        except Exception as e:
            print(f"Error reading cache: {e}")
            return None
    
    def set(self, prompt: str, result):
        """
        Store result in cache
        
        Args:
            prompt: The query prompt
            result: The result to cache
        """
        cache_key = self._get_cache_key(prompt)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'prompt': prompt,
                'result': result
            }
            
            with open(cache_path, 'w') as f:
                json.dump(data, f)
        
        except Exception as e:
            print(f"Error writing cache: {e}")
    
    def clear_all(self):
        """Clear all cached results"""
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")


# Usage example:
"""
from cache_persistent import PersistentCache

# Initialize cache
cache = PersistentCache()

# Try to get from cache
result = cache.get(voice_prompt)

if result:
    logger.info("⚡ Using persistent cache (survives reloads!)")
    time.sleep(3)  # Artificial delay
else:
    logger.info("🔄 Cache miss - querying Genie...")
    result = multi_agent.query(voice_prompt)
    cache.set(voice_prompt, result)
"""

