from django.core.cache import cache


class CacheManager:

    @staticmethod
    def cache_data(key_prefix: str, time: int = 60):
        def decorator(func):
            def wrapper(*args, **kwargs):
                user_id = args[1].id
                key = f'{key_prefix}//{user_id}'
                data = cache.get(key)
                if data:
                    return data
                data = func(*args, **kwargs)
                cache.set(key, data, time)
                return data
            return wrapper
        return decorator

    @staticmethod
    def delete_cache_data(key_prefix: str, user_id: int):
        key = f'{key_prefix}//{user_id}'
        if cache.get(key):
            cache.delete(key)
