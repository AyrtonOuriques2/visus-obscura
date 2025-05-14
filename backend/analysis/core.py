from analysis.services.headerAnalysis import checkHeaders
from analysis.services.certificateAnalysis import certificateCheck
from analysis.services.ssl_tlsCheck import ssl_tlsCheck

import re
from urllib.parse import urlparse
from httpx import AsyncClient, RequestError, AsyncHTTPTransport
from asyncio import gather, to_thread




pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(\/.*)?$')

def parse(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        return url
    parsed = urlparse(url)
    if (not parsed.hostname):
        raise Exception("Error fetching hostname")
    return parsed.hostname

def wrap_ipv6(address: str) -> str:
    if ':' in address:
        return f'[{address}]'
    return address

async def try_request(url_base: str):
    for scheme in ["", "https://", "http://"]:
        try:
            async with AsyncClient(transport=AsyncHTTPTransport(local_address="0.0.0.0")) as client:
                response = await client.get(scheme + url_base, timeout=5)
                network_stream = response.extensions.get("network_stream")
                server_addr = (
                    network_stream.get_extra_info("server_addr") if network_stream else None
                )
                if (server_addr == None):
                    raise Exception(f"Failed to get ip from {url_base}")
                return response, server_addr[0] 
        except RequestError:
            continue
    raise Exception(f"Could not connect to {url_base} via HTTP or HTTPS")

async def sentToAnalysis(url: str):
    parsedUrl = parse(url)
    response, serverAddr = await try_request(parsedUrl)

    try:
        headerReport = checkHeaders(response.headers)

        ssl_tlsReport, httpsReport = await gather(
            to_thread(ssl_tlsCheck, wrap_ipv6(serverAddr), parsedUrl),
            to_thread(certificateCheck, serverAddr, parsedUrl)
        )

        report = [
            headerReport,
            httpsReport,
            ssl_tlsReport
        ]
        return report

    except Exception as E:
        raise E
        
