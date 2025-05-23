import re
from httpx import AsyncClient
from asyncio import sleep

from analysis.utils.header_config import HEADERS

common_admin_paths = [
    'admin', 'administrator', 'admin1', 'admin2', 'admin_area',
    'admin-panel', 'adminpanel', 'admin_console', 'admin_dashboard',
    'admin/login', 'admin.php', 'admin.html', 'admin.aspx',
    'admin.cgi', 'admin/login.php', 'admin/index.php', 'admin/home.php',
    'cpanel', 'dashboard', 'controlpanel', 'backend', 'manage',
    'management', 'login', 'signin', 'user', 'users', 'auth',
    'authentication', 'secure', 'system', 'member', 'members',
    'moderator', 'mod', 'portal', 'console', 'cms', 'root', 'superadmin',
    'wp-admin', 'wp-login', 'typo3', 'admin/login.html'
]

login_keywords = re.compile(r'login|sign\s?in|admin panel|authentication', re.IGNORECASE)

async def checkPanels(base_url):
    open_panels = []
    
    for path in common_admin_paths:
        print("Panels request")
        try:
            async with AsyncClient(timeout=5, follow_redirects=True) as client:
                r = await client.get(f"{base_url}/{path}" , headers=HEADERS)
                if 200 <= r.status_code < 300 and login_keywords.search(r.text):
                    open_panels.append(path)
        except Exception as e:
            open_panels.append({
                "path": path,
                "error": True,
                "msg": str(e)
            })

        await sleep(1) 
    
    return open_panels if open_panels else ""