import re
from httpx import AsyncClient
from asyncio import gather, Semaphore, sleep

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

login_keywords = re.compile(
    r'login|log-in|sign[\-_ ]?in|signin|auth|authenticate|authentication|account|user|users|session|admin|dashboard|access|portal',
    re.IGNORECASE
)


sem = Semaphore(2)

async def test_single_payload(client, base_url, path):
    async with sem:
        await sleep(1)

        try:
            r = await client.get(f"{base_url}/{path}" , headers=HEADERS)

            if r.status_code in (301,302):
                target = r.headers.get("location", "")
                if login_keywords.search(target):
                    return f"{path} → {target}"
            

            if 200 <= r.status_code < 300 and login_keywords.search(r.text):
                return path
        except Exception as e:
            return{
                "path": path,
                "error": True,
                "msg": str(e)
            }
        return None

async def checkPanels(base_url):
    open_panels = []

    async with AsyncClient(timeout=5) as client:
        tasks = []
        for path in common_admin_paths:
            tasks.append(test_single_payload(client, base_url, path))

        response = await gather(*tasks)
    
    for res in response:
        if res:
            open_panels.append(res)

    return open_panels if open_panels else ""

