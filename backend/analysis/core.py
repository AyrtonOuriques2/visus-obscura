from httpx import AsyncClient

async def sentToAnalysis(url: str):
    try:
        headerReport = await checkHeaders(url)
        
        return headerReport
    except Exception as E:
        raise E
        

async def checkHeaders(url: str):
    try:
        client = AsyncClient()
        response = await client.get(url)

        return response.headers 
    except Exception as E:
        raise E
        