from analysis.services.headerAnalysis import checkHeaders
from analysis.services.certificateAnalysis import certificateCheck
from analysis.services.ssl_tlsCheck import ssl_tlsCheck

import re
from urllib.parse import urlparse



pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(\/.*)?$')

def parse(url: str) -> str:
    if not url.startswith(('http://', 'https://')):
        return url
    parsed = urlparse(url)
    if (not parsed.hostname):
        raise Exception("Error fetching hostname")
    return parsed.hostname

async def sentToAnalysis(url: str):

    parsedUrl = parse(url)

    if not pattern.match(url):
        raise Exception('Please try a valid url')
    try:
        headerReport = await checkHeaders(parsedUrl)
        ssl_tlsReport = await ssl_tlsCheck(parsedUrl)
        httpsReport = await certificateCheck(ssl_tlsReport["ip"], parsedUrl)

        report = [
            headerReport,
            httpsReport,
            ssl_tlsReport
        ]
        return report
    except Exception as E:
        raise E
        
