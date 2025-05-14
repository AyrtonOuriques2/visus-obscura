from httpx import AsyncClient

REDIRECT_PARAMS = ["next", "url", "redirect", "return", "continue", "next.php", "url.php", "redirect.php", "return.php", "continue.php"]

REDIRECT_PAYLOADS = [
    "https://evil.com",
    "//evil.com",
    "/\\evil.com",
    "///evil.com",
    "http://evil.com",
    "https:evil.com",           
    "evil.com",                 
    "evil.com@trusted.com",    
    "@evil.com",                
    "%2F%2Fevil.com",          
    "%5Cevil.com",              
]

async def redirectCheck(base_url: str):
    results = []

    async with AsyncClient(follow_redirects=False, timeout=5.0) as client:
        for param in REDIRECT_PARAMS:
            for payload in REDIRECT_PAYLOADS:
                test_url = f"{base_url}?{param}={payload}"
                try:
                    response = await client.get(test_url)
                    location = response.headers.get("location", "")

                    if (
                        response.status_code in (301, 302)
                        and location
                        and "evil.com" in location
                        and len(location)<= 25
                    ):
                        results.append({
                            "param": param,
                            "payload": payload,
                            "vulnerable": True,
                            "payload_url": test_url,
                            "redirect_location": location
                        })
                except Exception as e:
                    results.append({
                        "param": param,
                        "payload": payload,
                        "error": str(e)
                    })

    return results
