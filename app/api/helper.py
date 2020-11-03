from .http import mock

def merge_mock(url,parse=None):
    counturl = url + '/count'
    readurl = url + '/read'
    readurl_limit = readurl + '?limit=50'
    count = mock(counturl,parse)['data']
    if count <= 50:
        res = mock(readurl_limit,parse)['data']
        return res
    
    page = math.ceil(count/50)
    print ("page: ",page)
    all = []
    for i in range(1,page+1):
        url = readurl + "?limit=50&page=%s" % i
        all = all + mock(url,parse)['data']
    return all