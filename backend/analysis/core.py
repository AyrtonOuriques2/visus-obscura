from analysis.services.headerAnalysis import checkHeaders
from analysis.services.certificateAnalysis import certificateCheck
import re

pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(\/.*)?$')

async def sentToAnalysis(url: str):
    if not pattern.match(url):
        raise Exception('Please try a valid url')
    try:
        headerReport = await checkHeaders(url)
        sslReport = await certificateCheck(url)
        return sslReport
    except Exception as E:
        raise E
        
