from httpx import AsyncClient

from analysis.utils.header_config import HEADERS


paths = [
    '.env', '.git/config', 'config.php', 'config.json',
    '.htaccess', '.DS_Store', 'backup.zip'
]

async def checkOpenFiles(base_url):
    found = []

    for path in paths:
        try:
            async with AsyncClient(timeout=5) as client:
                r = await client.get(f"{base_url}/{path}" , headers=HEADERS)
                if 200 <= r.status_code < 300 and len(r.text) > 20:
                    found.append(path)
        except Exception as e:
            found.append({
                "error": True,
                "msg" : e
            })
            pass

    return found if found else ""