#File for storing info in and manipulating the cache
#to store unix time so we can just compare numbers not datetime objects
import time

#import the time to live
from config import News_TTL, Wiki_TTL

#internal Dictionary, shouldn't be touched by other functions
_cache = {}  # { company: (data, expires_at, source) }

#creates a cache that holds the value, time, and source of the research target
def cache_set(key, value, ttl, source = None):
    #tuple that unpacks cleanly
    _cache[key] = (value, time.time() + ttl, source)

#search the cache for a the target, is its expired or doesn't exits, delete it
def cache_get(key):
	if key not in _cache:
		return None
    #tuple unpacking
	value, expires_at, source = _cache[key]
	if time.time() > expires_at:
		del _cache[key]  # expired, throw it out so it doesn't sit in ram
		return None
	return value, source
