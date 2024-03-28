import requests

def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    request['prop'] = 'info'
    request['generator'] = 'links'
    request['inprop'] = 'url'
    previousContinue = {}
    while True:
        req = request.copy()
        req.update(previousContinue)
        result = requests.get('http://en.wikipedia.org/w/api.php', params=req).json()
        if 'error' in result:
            raise Error(result['error'])
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            yield result['query']
        if 'continue' in result:
            previousContinue = {'gplcontinue': result['continue']['gplcontinue']}
        else:
            break

count = 0
for result in query({'titles': 'Estelle Morris', 'gpllimit': '5'}):
    for url in [_['fullurl'] for _ in list(result.values())[0].values()]:
        print (url)