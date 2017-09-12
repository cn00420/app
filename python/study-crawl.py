import bs4
import urllib2 as url

visited = set()
limit = 100
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}


class Stack:
    def __init__(self):
        self.data = list()

    def push(self, elem):
        self.data.insert(0, elem)

    def pop(self):
        return self.data.pop(0)


class Queue:
    def __init__(self):
        self.data = list()

    def inq(self, elem):
        self.data.append(elem)

    def outq(self):
        return self.data.pop(0)


def recursive_crawl(page):
    global visited, limit

    if len(visited) >= limit:
        return

    try:
        html = access_page(page)
    except Exception, e:
        print 'Access %s error: %s' % (page, repr(e) + e.message)
        return

    visited.add(page)
    soup = bs4.BeautifulSoup(html, 'lxml')
    anchors = soup.find_all('a')

    for a in anchors:
        if len(visited) >= limit:
            return

        if 'href' in a.attrs and isinstance(a['href'], str) and a['href'].startswith('http'):
            if not page_visited(a['href']):
                print a['href']
                recursive_crawl(a['href'])


def deep_crawl(root):
    global visited, limit

    s = Stack()
    s.push(root)

    while len(s.data) > 0:
        page = s.pop()

        if page_visited(page):
            continue

        visited.add(page)
        if len(visited) > limit:
            break

        print page
        try:
            html = access_page(page)
        except Exception, e:
            print 'Access %s error: %s' % (page, repr(e) + e.message)
            continue

        soup = bs4.BeautifulSoup(html, 'lxml')
        anchors = soup.find_all('a')

        vec = list()
        for a in anchors:
            if 'href' in a.attrs and isinstance(a['href'], str) and a['href'].startswith('http'):
                if not page_visited(a['href']):
                    vec.insert(0, a['href'])

        for v in vec:
            s.push(v)

    del(s.data[:])


def width_crawl(root):
    global visited, limit

    q = Queue()
    q.inq(root)

    while len(q.data) > 0:
        page = q.outq()

        if page_visited(page):
            continue

        visited.add(page)
        if len(visited) > limit:
            break

        print page
        try:
            html = access_page(page)
        except Exception, e:
            print 'Access %s error: %s' % (page, e.message)
            continue

        soup = bs4.BeautifulSoup(html, 'lxml')
        anchors = soup.find_all('a')

        for a in anchors:
            if 'href' in a.attrs and isinstance(a['href'], str) and a['href'].startswith('http'):
                if not page_visited(a['href']):
                    q.inq(a['href'])

    del(q.data[:])


def access_page(page):
    global headers
    html = ''
    f = None

    try:
        req = url.Request(page, headers=headers)
        f = url.urlopen(req)

        for l in f.readlines():
            html += l
    except url.HTTPError, he:
        raise Exception(he.reason)
    except url.URLError, ue:
        raise Exception(ue.reason)
    except Exception, e:
        raise e
    finally:
        if f is not None:
            f.close()

    return html


def page_visited(page):
    global visited

    s = page
    if page.endswith('/'):
        s = page[0:len(page) - 1]

    if s in visited or s + '/' in visited or s.replace('http', 'https') in visited \
            or s.replace('http', 'https') + '/' in visited \
            or s.replace('https', 'http') in visited or s.replace('https', 'http') + '/' in visited:
        return True
    else:
        return False


recursive_crawl('http://www.baidu.com')
