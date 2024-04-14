from js imporr Response

async def on_fetch(request, env):
    return Response.new('Python Worker hello world!', {
        'headers' : { 'content-type' : 'text/plain' }
    }))
