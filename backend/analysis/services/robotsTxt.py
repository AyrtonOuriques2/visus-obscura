from httpx import AsyncClient


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
            response = await client.get(robots_url)

            if response.status_code != 200:
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
                    disallowed.append(path)
                    if is_suspicious(path):
                        suspicious.append({"type": "Disallow", "path": path})
                    if "*" in path:
                        has_wildcards = True
                    if "$" in path:
                        has_end_anchors = True

                elif line.lower().startswith("allow:"):
                    path = line.split(":", 1)[1].strip()
                    allowed.append(path)
                    if is_suspicious(path):
                        suspicious.append({"type": "Allow", "path": path})
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
                "user_agents": user_agents,
                "disallowed_paths": disallowed,
                "allowed_paths": allowed,
                "sitemaps": sitemaps,
                "uses_wildcards": has_wildcards,
                "uses_end_anchors": has_end_anchors,
                "suspicious_entries": suspicious
            }

    except Exception as e:
        raise e