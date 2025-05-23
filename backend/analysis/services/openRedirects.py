from asyncio import gather, Semaphore, sleep
from httpx import AsyncClient
from analysis.utils.header_config import HEADERS

REDIRECT_PARAMS = [
    "next", "url", "redirect", "return", "continue",
    "next.php", "url.php", "redirect.php", "return.php", "continue.php"
]

REDIRECT_PAYLOADS = [
    "https://evil.com", "//evil.com", "/\\evil.com", "///evil.com",
    "http://evil.com", "https:evil.com", "evil.com",
    "evil.com@trusted.com", "@evil.com", "%2F%2Fevil.com", "%5Cevil.com"
]

sem = Semaphore(5)

async def test_single_php_payload(client, base_url, param, payload):
    async with sem:
        await sleep(1)

        test_url = f"{base_url.rstrip('/')}/{param}"
        
        try:
            response = await client.get(test_url, headers=HEADERS)
            if 200 <= response.status_code < 300:
                for override_param in ["redirect", "url"]:
                    full_url = f"{test_url}?{override_param}={payload}"
                    response = await client.get(full_url, headers=HEADERS)
                    location = response.headers.get("location", "")
                    if (
                        response.status_code in (301, 302)
                        and location
                        and "evil.com" in location
                        and len(location) <= 25
                    ):
                        return {
                            "param": param,
                            "payload": payload,
                            "vulnerable": True,
                            "payload_url": full_url,
                            "redirect_location": location
                        }
        except Exception as e:
            return {
                "param": param,
                "payload": payload,
                "error": str(e)
            }

        return None

async def test_single_payload(client, base_url, param, payload):
    async with sem:

        await sleep(1)

        test_url = f"{base_url}?{param}={payload}"
        
        try:
            response = await client.get(test_url, headers=HEADERS)
            location = response.headers.get("location", "")
            if (
                response.status_code in (301, 302)
                and location
                and "evil.com" in location
                and len(location) <= 25
            ):
                return {
                    "param": param,
                    "payload": payload,
                    "vulnerable": True,
                    "payload_url": test_url,
                    "redirect_location": location
                }
        except Exception as e:
            return {
                "param": param,
                "payload": payload,
                "error": str(e)
            }

        return None

async def redirectCheck(base_url: str):
    results = []

    async with AsyncClient(follow_redirects=False, timeout=5) as client:
        tasks = []

        for param in REDIRECT_PARAMS:
            if param.endswith('.php'):
                test_url = f"{base_url.rstrip('/')}/{param}"
                try:
                    response = await client.get(test_url, headers=HEADERS)
                    if 200 <= response.status_code < 300:
                        for payload in REDIRECT_PAYLOADS:
                            tasks.append(test_single_php_payload(client, base_url, param, payload))
                except:
                    continue
            else:
                for payload in REDIRECT_PAYLOADS:
                    tasks.append(test_single_payload(client, base_url, param, payload))

        responses = await gather(*tasks)

    for res in responses:
        if res:
            results.append(res)

    return results if results else ""