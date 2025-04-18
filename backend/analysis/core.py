from httpx import AsyncClient

async def sentToAnalysis(url: str):
    report = {}
    headerReport = await checkHeaders(url)
    
    return headerReport

async def checkHeaders(url: str):
    client = AsyncClient()
    response = await client.get(url)

    return response.headers 