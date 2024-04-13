def handleRequest(request):
    return __new__(Response('Python Worker hello world!'))

addEventListener('fetch', (lambda event: event.respondWith(handleRequest(event.request))))
