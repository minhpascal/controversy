import urllib2
from config import TOR_PW, NYT_UA
from TorCtl import TorCtl

headers = {
    'User-Agent': NYT_UA
}

def query(url):
    proxy_support = urllib2.ProxyHandler({
        'http' : '127.0.0.1:8118'
    })
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    request = urllib2.Request(url, None, headers)
    return urllib2.urlopen(request)

def renew_connection():
    conn = TorCtl.connect(controlAddr='127.0.0.1',
                          controlPort=9051,
                          passphrase=TOR_PW)
    conn.send_signal('NEWNYM')
    conn.close()
