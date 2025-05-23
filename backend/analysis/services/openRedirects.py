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

async def test_single_payload(client, base_url, param, payload, override_param_name=None):
    async with sem:

        await sleep(1)
        print("Redirect Request")

        if param.endswith('.php'):
            test_url = f"{base_url.rstrip('/')}/{param}?{override_param_name}={payload}"
        else:
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
            for payload in REDIRECT_PAYLOADS:
                if param.endswith('.php'):
                    tasks.append(test_single_payload(client, base_url, param, payload, override_param_name="redirect"))
                    tasks.append(test_single_payload(client, base_url, param, payload, override_param_name="url"))
                else:
                    tasks.append(test_single_payload(client, base_url, param, payload))

        responses = await gather(*tasks)

    for res in responses:
        if res:
            results.append(res)

    return results if results else ""