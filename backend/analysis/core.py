from analysis.services.headerAnalysis import checkHeaders
import re

pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(\/.*)?$')

async def sentToAnalysis(url: str):
    if not pattern.match(url):
        raise Exception('Please try a valid url')
    try:
        headerReport = await checkHeaders(url)
        
        return headerReport
    except Exception as E:
        raise E
        
