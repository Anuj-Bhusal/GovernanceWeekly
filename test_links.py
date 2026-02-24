import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

# Test MyRepublica
print("=== MyRepublica Links ===")
try:
    r = requests.get("https://myrepublica.nagariknetwork.com", headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True) if "/news/" in a["href"]][:10]
    for l in links:
        print(l)
except Exception as e:
    print(f"Error: {e}")

print("\n=== Setopati Links ===")
try:
    r = requests.get("https://www.setopati.com", headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True) if "/politics/" in a["href"] or "/social/" in a["href"]][:10]
    for l in links:
        print(l)
except Exception as e:
    print(f"Error: {e}")
