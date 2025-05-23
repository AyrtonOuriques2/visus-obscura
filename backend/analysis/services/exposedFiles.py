from httpx import AsyncClient
from asyncio import sleep

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

async def checkOpenFiles(base_url):
    found = []

    for path in paths:
        print("Exposed request")
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
        await sleep(1)

    return found if found else ""