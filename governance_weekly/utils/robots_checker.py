import urllib.robotparser
from urllib.parse import urlparse
import requests
import logging

logger = logging.getLogger(__name__)

class RobotsChecker:
    _cache = {}  # Store both parser and raw content

    @classmethod
    def is_allowed(cls, url, user_agent):
        parsed = urlparse(url)
        base_key = f"{parsed.scheme}://{parsed.netloc}"
        
        if base_key not in cls._cache:
            robots_url = f"{base_key}/robots.txt"
            try:
                # Fetch robots.txt manually to check content
                r = requests.get(robots_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                robots_content = r.text if r.status_code == 200 else ""
                
                # Check if robots.txt is essentially empty or fully permissive
                # "Disallow:" with nothing after means allow all
                lines = [l.strip().lower() for l in robots_content.split('\n') if l.strip() and not l.strip().startswith('#')]
                disallow_lines = [l for l in lines if l.startswith('disallow:')]
                
                # If no disallow rules or only empty disallow (allow all)
                is_permissive = len(disallow_lines) == 0 or all(l == 'disallow:' for l in disallow_lines)
                
                if is_permissive:
                    cls._cache[base_key] = {'permissive': True, 'parser': None}
                else:
                    rp = urllib.robotparser.RobotFileParser()
                    rp.set_url(robots_url)
                    rp.read()
                    cls._cache[base_key] = {'permissive': False, 'parser': rp}
                    
            except Exception as e:
                logger.warning(f"Could not read robots.txt for {parsed.netloc}: {e}")
                # Default to allowed if robots.txt unreachable
                cls._cache[base_key] = {'permissive': True, 'parser': None}
        
        cache_entry = cls._cache[base_key]
        if cache_entry['permissive']:
            return True
        return cache_entry['parser'].can_fetch(user_agent, url)

def is_allowed(url, user_agent):
    return RobotsChecker.is_allowed(url, user_agent)
