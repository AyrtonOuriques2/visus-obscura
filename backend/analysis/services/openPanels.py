import re
from httpx import AsyncClient

common_admin_paths = [
    'admin', 'administrator', 'cpanel', 'dashboard',
    'login', 'admin/login', 'admin.php'
]

login_keywords = re.compile(r'login|sign\s?in|admin panel|authentication', re.IGNORECASE)

async def checkPanels(base_url):
    open_panels = []
    
    for path in common_admin_paths:
        try:
            async with AsyncClient(timeout=5, follow_redirects=True) as client:
                r = await client.get(f"{base_url}/{path}")
                if 200 <= r.status_code < 300 and login_keywords.search(r.text):
                    open_panels.append(path)
        except Exception as e:
            open_panels.append({
                "path": path,
                "error": True,
                "msg": str(e)
            })
    
    return open_panels