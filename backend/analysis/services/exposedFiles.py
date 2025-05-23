from httpx import AsyncClient
from asyncio import gather, Semaphore, sleep

from analysis.utils.header_config import HEADERS


paths = [
    '.env', '.env.local', '.env.dev', '.env.production',
    'config.php', 'config.json', 'config.js', 'settings.py',
    'local.settings.json', 'web.config', 'application.yml',
    'database.yml', 'appsettings.json','.git/config',
     '.gitignore', '.gitlab-ci.yml', '.travis.yml',
    '.svn/entries','backup.zip', 'backup.tar.gz', 'db.sql', 'dump.sql',
    'database.sql', 'site_backup.zip', 'backup.bak',
    '.htaccess', '.htpasswd', 'composer.json', 'package-lock.json',
    'yarn.lock', 'docker-compose.yml', 'Dockerfile',
    'Procfile', 'manifest.json','.DS_Store', 'Thumbs.db', '.idea/workspace.xml',
    '.vscode/settings.json', 'desktop.ini'
]

sem = Semaphore(2)

async def test_single_payload(client, base_url, path):
    async with sem:
        await sleep(1)

        try:
            r = await client.get(f"{base_url}/{path}" , headers=HEADERS)
            if 200 <= r.status_code < 300:
                return path
        except Exception as e:
            return{
                "error": True,
                "msg" : e
            }
        return None

async def checkOpenFiles(base_url):
    found = []

    async with AsyncClient(timeout=5) as client:
        tasks = []
        for path in paths:
            tasks.append(test_single_payload(client, base_url, path))

        response = await gather(*tasks)
    
    for res in response:
        if res:
            found.append(res)

    return found if found else ""