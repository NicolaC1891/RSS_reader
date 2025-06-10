import aiohttp
import asyncio

# RSS feed URL
bbc_url = "http://feeds.bbci.co.uk/news/world/europe/rss.xml"

# Define core function
async def main():
    # Create session
    async with aiohttp.ClientSession() as session:
        # Send request, get reply as response, wrap in context
        async with session.get(bbc_url) as response:
            print("Connection status code:", response.status)
            # Headers are response metadata (coding, content type, length etc.), stored in dict-like object
            print("Content type:", response.headers['content-type'])
            # Assign contents to variable
            content = await response.text()
            print("First 30 characters:", content[:30])
            print(content)    # This is to be parsed

# Starting main asynchronous script
asyncio.run(main())