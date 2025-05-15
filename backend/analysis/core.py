from analysis.services.headerAnalysis import checkHeaders
from analysis.services.certificateAnalysis import certificateCheck
from analysis.services.ssl_tlsCheck import ssl_tlsCheck
from analysis.services.openRedirects import redirectCheck
from analysis.services.robotsTxt import checkRobots
from analysis.services.exposedFiles import checkOpenFiles
from analysis.services.openPanels import checkPanels
from analysis.services.stackAnalysis import detectStack


import re
from socket import gethostbyname
from urllib.parse import urlparse
from httpx import AsyncClient, RequestError, AsyncHTTPTransport
from asyncio import gather, to_thread


pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(\/.*)?$')

def parse(url: str) -> str:
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
                    server_addr = gethostbyname(url_base)
                    return response, server_addr, scheme 
                return response, server_addr[0], scheme 
        except RequestError:
            continue
    raise Exception(f"Could not connect to {url_base} via HTTP or HTTPS")

async def sentToAnalysis(url: str):
    #todo flag to check all ips of an domain (will take long time)
    if url.startswith(('http://', 'https://')):
        url = url.removeprefix("http://")
        url = url.removeprefix("https://")


    response, serverAddr, scheme = await try_request(url)

    parsedUrl = parse(scheme + url)


    try:
        headerReport = checkHeaders(response.headers)

        stackReport, panelsReport, filesReport, robotsReport, redirectReport, ssl_tlsReport, httpsReport = await gather(
            to_thread(detectStack, response.text),
            checkPanels(scheme + parsedUrl),
            checkOpenFiles(scheme + parsedUrl),
            checkRobots(scheme + parsedUrl),
            redirectCheck(scheme + parsedUrl),
            to_thread(ssl_tlsCheck, wrap_ipv6(serverAddr), parsedUrl),
            to_thread(certificateCheck, serverAddr, parsedUrl)
        )

        report = {
            "stackReport" : stackReport,
            "panelsReport" : panelsReport,
            "filesReport" : filesReport,
            "robotsReport" : robotsReport,
            "redirectReport" : redirectReport,
            "headerReport" : headerReport,
            "httpsReport": httpsReport,
            "ssl_tlsReport" : ssl_tlsReport
        }

        return report

    except Exception as E:
        raise E


#force provided ip dns resolve
# ConnectError("[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: IP address mismatch, 
# certificate is not valid for '20.201.28.151'

# from httpx import AsyncClient, AsyncHTTPTransport
# import socket

# class CustomResolver:
#     def __init__(self, ip):
#         self.ip = ip

#     async def resolve(self, host, port=0, family=socket.AF_INET):
#         return [{
#             "hostname": host,
#             "host": self.ip,
#             "port": port,
#             "family": family,
#             "proto": 0,
#             "flags": socket.AI_NUMERICHOST,
#         }]

# transport = AsyncHTTPTransport(resolver=CustomResolver("20.201.28.151"))

# async with AsyncClient(transport=transport, timeout=5) as client:
#     r = await client.get("https://example.com/some_path")
        
