"""
Performance optimization and caching system for Aclarador
"""

import time
import hashlib
import pickle
import json
import os
from typing import Dict, List, Any, Optional, Callable
from functools import wraps
from dataclasses import dataclass, asdict
import threading
from datetime import datetime, timedelta

@dataclass
class CacheEntry:
    """Represents a cached result"""
    key: str
    value: Any
    timestamp: float
    access_count: int
    last_access: float
    expiry_time: Optional[float] = None

class InMemoryCache:
    """Thread-safe in-memory cache with LRU eviction"""
    
    def __init__(self, max_size: int = 100, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl  # seconds
        self.cache: Dict[str, CacheEntry] = {}
        self.access_order: List[str] = []
        self._lock = threading.RLock()
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {'args': args, 'kwargs': sorted(kwargs.items())}
        key_string = json.dumps(key_data, default=str, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self._lock:
            if key not in self.cache:
                self.misses += 1
                return None
            
            entry = self.cache[key]
            
            # Check expiry
            if entry.expiry_time and time.time() > entry.expiry_time:
                del self.cache[key]
                if key in self.access_order:
                    self.access_order.remove(key)
                self.misses += 1
                return None
            
            # Update access info
            entry.access_count += 1
            entry.last_access = time.time()
            
            # Update LRU order
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)
            
            self.hits += 1
            return entry.value
    
    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Put value in cache"""
        with self._lock:
            now = time.time()
            expiry = now + (ttl or self.default_ttl)
            
            entry = CacheEntry(
                key=key,
                value=value,
                timestamp=now,
                access_count=1,
                last_access=now,
                expiry_time=expiry
            )
            
            # Evict if at capacity
            if len(self.cache) >= self.max_size and key not in self.cache:
                self._evict_lru()
            
            self.cache[key] = entry
            
            # Update access order
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)
    
    def _evict_lru(self) -> None:
        """Evict least recently used item"""
        if self.access_order:
            lru_key = self.access_order.pop(0)
            if lru_key in self.cache:
                del self.cache[lru_key]
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            self.cache.clear()
            self.access_order.clear()
            self.hits = 0
            self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            total_requests = self.hits + self.misses
            hit_rate = self.hits / total_requests if total_requests > 0 else 0
            
            return {
                'size': len(self.cache),
                'max_size': self.max_size,
                'hits': self.hits,
                'misses': self.misses,
                'hit_rate': hit_rate,
                'total_requests': total_requests
            }

class PersistentCache:
    """File-based persistent cache"""
    
    def __init__(self, cache_dir: str = "./cache", max_file_age: int = 86400):
        self.cache_dir = cache_dir
        self.max_file_age = max_file_age  # seconds
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        """Get file path for cache key"""
        return os.path.join(self.cache_dir, f"{key}.cache")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from persistent cache"""
        file_path = self._get_file_path(key)
        
        if not os.path.exists(file_path):
            return None
        
        # Check file age
        file_age = time.time() - os.path.getmtime(file_path)
        if file_age > self.max_file_age:
            try:
                os.remove(file_path)
            except OSError:
                pass
            return None
        
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except (pickle.PickleError, IOError):
            return None
    
    def put(self, key: str, value: Any) -> None:
        """Put value in persistent cache"""
        file_path = self._get_file_path(key)
        
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(value, f)
        except (pickle.PickleError, IOError):
            pass  # Fail silently
    
    def clear(self) -> None:
        """Clear persistent cache"""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    os.remove(os.path.join(self.cache_dir, filename))
        except OSError:
            pass

class PerformanceOptimizer:
    """Main performance optimization system"""
    
    def __init__(self, cache_dir: str = "./cache"):
        self.memory_cache = InMemoryCache(max_size=200, default_ttl=1800)  # 30 min
        self.persistent_cache = PersistentCache(cache_dir, max_file_age=86400)  # 24 hours
        self.performance_metrics = {
            'processing_times': [],
            'cache_performance': {},
            'optimization_applied': []
        }
    
    def cached(self, ttl: Optional[int] = None, persistent: bool = False):
        """Decorator for caching function results"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self.memory_cache._generate_key(func.__name__, *args, **kwargs)
                
                # Try memory cache first
                result = self.memory_cache.get(cache_key)
                if result is not None:
                    return result
                
                # Try persistent cache if enabled
                if persistent:
                    result = self.persistent_cache.get(cache_key)
                    if result is not None:
                        # Store in memory cache for faster access
                        self.memory_cache.put(cache_key, result, ttl)
                        return result
                
                # Execute function and cache result
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Cache the result
                self.memory_cache.put(cache_key, result, ttl)
                if persistent:
                    self.persistent_cache.put(cache_key, result)
                
                # Record performance metrics
                self.performance_metrics['processing_times'].append({
                    'function': func.__name__,
                    'execution_time': execution_time,
                    'timestamp': time.time(),
                    'cached': False
                })
                
                return result
            
            return wrapper
        return decorator
    
    def batch_process_texts(self, texts: List[str], process_func: Callable) -> List[Any]:
        """Optimize batch processing of multiple texts"""
        results = []
        
        # Group similar texts to benefit from caching
        text_groups = self._group_similar_texts(texts)
        
        for group in text_groups:
            # Process first text in group normally
            if group:
                first_result = process_func(group[0])
                results.append(first_result)
                
                # For similar texts, use optimized processing
                for text in group[1:]:
                    optimized_result = self._process_similar_text(text, group[0], first_result, process_func)
                    results.append(optimized_result)
        
        return results
    
    def _group_similar_texts(self, texts: List[str]) -> List[List[str]]:
        """Group similar texts for optimized processing"""
        groups = []
        processed = set()
        
        for i, text in enumerate(texts):
            if i in processed:
                continue
            
            group = [text]
            processed.add(i)
            
            # Find similar texts (simple similarity based on length and first words)
            text_words = text.split()[:5]  # First 5 words
            
            for j, other_text in enumerate(texts[i+1:], i+1):
                if j in processed:
                    continue
                
                other_words = other_text.split()[:5]
                
                # Simple similarity check
                common_words = set(text_words) & set(other_words)
                length_similarity = abs(len(text) - len(other_text)) / max(len(text), len(other_text))
                
                if len(common_words) >= 2 and length_similarity < 0.3:
                    group.append(other_text)
                    processed.add(j)
            
            groups.append(group)
        
        return groups
    
    def _process_similar_text(self, text: str, reference_text: str, reference_result: Any, process_func: Callable) -> Any:
        """Process similar text using reference result for optimization"""
        # For similar texts, we can potentially reuse some analysis
        # This is a simplified implementation - in practice, you'd do more sophisticated optimization
        
        # If texts are very similar, return cached result with minimal changes
        similarity = self._calculate_text_similarity(text, reference_text)
        
        if similarity > 0.8:
            # High similarity - use reference result with minor adjustments
            return self._adjust_result_for_similar_text(text, reference_result)
        else:
            # Process normally
            return process_func(text)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def _adjust_result_for_similar_text(self, text: str, reference_result: Any) -> Any:
        """Adjust reference result for similar text"""
        # This is a simplified implementation
        # In practice, you'd make intelligent adjustments based on the differences
        
        if isinstance(reference_result, dict):
            adjusted_result = reference_result.copy()
            # Adjust text-specific fields
            if 'original_text' in adjusted_result:
                adjusted_result['original_text'] = text
            if 'corrected_text' in adjusted_result:
                # For now, just return the original text
                # In a real implementation, you'd apply similar corrections
                adjusted_result['corrected_text'] = text
            
            return adjusted_result
        
        return reference_result
    
    def preload_cache(self, common_texts: List[str], process_func: Callable) -> None:
        """Preload cache with common text patterns"""
        print("Preloading cache with common patterns...")
        
        for i, text in enumerate(common_texts):
            print(f"Processing pattern {i+1}/{len(common_texts)}")
            # This will cache the results
            process_func(text)
        
        print("Cache preloading completed")
    
    def optimize_agent_coordination(self, coordinator, enable_parallel: bool = True) -> None:
        """Optimize agent coordination for better performance"""
        
        if enable_parallel and not hasattr(coordinator, '_performance_optimized'):
            # Mark as optimized to avoid double optimization
            coordinator._performance_optimized = True
            
            # Add caching to agent methods
            coordinator.grammar.analyze = self.cached(ttl=1800)(coordinator.grammar.analyze)
            coordinator.style.analyze = self.cached(ttl=1800)(coordinator.style.analyze)
            coordinator.seo.analyze = self.cached(ttl=1800)(coordinator.seo.analyze)
            coordinator.validator.analyze = self.cached(ttl=900)(coordinator.validator.analyze)
            
            print("Agent coordination optimized with caching")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        
        # Calculate processing time statistics
        times = [m['execution_time'] for m in self.performance_metrics['processing_times']]
        
        if times:
            time_stats = {
                'total_requests': len(times),
                'avg_time': sum(times) / len(times),
                'min_time': min(times),
                'max_time': max(times),
                'total_time': sum(times)
            }
        else:
            time_stats = {
                'total_requests': 0,
                'avg_time': 0,
                'min_time': 0,
                'max_time': 0,
                'total_time': 0
            }
        
        return {
            'cache_stats': self.memory_cache.get_stats(),
            'processing_stats': time_stats,
            'optimizations_applied': len(self.performance_metrics['optimization_applied']),
            'timestamp': time.time()
        }
    
    def clear_all_caches(self) -> None:
        """Clear both memory and persistent caches"""
        self.memory_cache.clear()
        self.persistent_cache.clear()
        print("All caches cleared")
    
    def suggest_optimizations(self) -> List[str]:
        """Suggest performance optimizations based on usage patterns"""
        suggestions = []
        
        stats = self.get_performance_report()
        cache_stats = stats['cache_stats']
        processing_stats = stats['processing_stats']
        
        # Cache-based suggestions
        if cache_stats['hit_rate'] < 0.5:
            suggestions.append("Considere aumentar el TTL del cache para mejorar hit rate")
        
        if cache_stats['size'] == cache_stats['max_size']:
            suggestions.append("Considere aumentar el tamaño máximo del cache")
        
        # Performance-based suggestions
        if processing_stats['avg_time'] > 5.0:
            suggestions.append("Tiempo de procesamiento alto - considere optimizar agentes")
        
        if processing_stats['total_requests'] > 100 and cache_stats['hit_rate'] < 0.3:
            suggestions.append("Habilite cache persistente para patrones repetidos")
        
        return suggestions

def performance_monitor(func: Callable) -> Callable:
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
            raise
        finally:
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Log performance data (in production, you'd send this to monitoring system)
            performance_data = {
                'function': func.__name__,
                'execution_time': execution_time,
                'success': success,
                'error': error,
                'timestamp': start_time,
                'args_count': len(args),
                'kwargs_count': len(kwargs)
            }
            
            # In production, send to monitoring system
            # For now, just store in memory
            if not hasattr(wrapper, 'performance_log'):
                wrapper.performance_log = []
            wrapper.performance_log.append(performance_data)
        
        return result
    
    return wrapper

class OptimizedAgentCoordinator:
    """Performance-optimized version of agent coordinator"""
    
    def __init__(self, base_coordinator, performance_optimizer: PerformanceOptimizer):
        self.base_coordinator = base_coordinator
        self.optimizer = performance_optimizer
        self.optimizer.optimize_agent_coordination(base_coordinator)
    
    @performance_monitor
    def process_text_optimized(self, text: str, selected_agents: List[str] = None) -> Dict[str, Any]:
        """Process text with performance optimizations"""
        return self.base_coordinator.process_text(text, selected_agents)
    
    def process_multiple_texts(self, texts: List[str], selected_agents: List[str] = None) -> List[Dict[str, Any]]:
        """Process multiple texts with batch optimizations"""
        return self.optimizer.batch_process_texts(
            texts,
            lambda text: self.base_coordinator.process_text(text, selected_agents)
        )
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return self.optimizer.get_performance_report()