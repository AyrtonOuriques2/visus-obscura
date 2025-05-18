from httpx import AsyncClient

from analysis.utils.header_config import HEADERS


SENSITIVE_KEYWORDS = [
    "admin", "backup", "config", "private", "secret", "test",
    "debug", "staging", "dev", "db", "sql", "login", "dump", "old", ".git", "api"
]

def is_suspicious(path):
    lowered = path.lower()
    return any(keyword in lowered for keyword in SENSITIVE_KEYWORDS)

async def checkRobots(url):
    robots_url = url + "/robots.txt"
    try:
        async with AsyncClient(timeout=5) as client:
            response = await client.get(robots_url, headers=HEADERS)

            if not 200 <=  response.status_code < 300:
                return {"found": False, "status_code": response.status_code}

            lines = response.text.splitlines()
            disallowed = []
            allowed = []
            sitemaps = []
            user_agents = []
            suspicious = []
            has_wildcards = False
            has_end_anchors = False

            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if is_suspicious(path):
                        suspicious.append({"type": "Disallow", "path": path})
                    else:
                        disallowed.append(path)
                    if "*" in path:
                        has_wildcards = True
                    if "$" in path:
                        has_end_anchors = True

                elif line.lower().startswith("allow:"):
                    path = line.split(":", 1)[1].strip()
                    if is_suspicious(path):
                        suspicious.append({"type": "Allow", "path": path})
                    else:
                        allowed.append(path)
                    if "*" in path:
                        has_wildcards = True
                    if "$" in path:
                        has_end_anchors = True

                elif line.lower().startswith("sitemap:"):
                    sitemap_url = line.split(":", 1)[1].strip()
                    sitemaps.append(sitemap_url)

                elif line.lower().startswith("user-agent:"):
                    agent = line.split(":", 1)[1].strip()
                    user_agents.append(agent)

            return {
                "found": True,
                "status_code": response.status_code,
                "user_agents": user_agents if user_agents else "",
                "disallowed_paths": disallowed if disallowed else "",
                "allowed_paths": allowed if allowed else "",
                "sitemaps": sitemaps if sitemaps else "",
                "uses_wildcards": has_wildcards,
                "uses_end_anchors": has_end_anchors,
                "suspicious_entries": suspicious if suspicious else ""
            }

    except Exception as e:
        raise e