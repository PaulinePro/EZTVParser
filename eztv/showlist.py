#!/usr/bin/python

import requests
import bs4

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'
URL_PREFIX = 'http://eztv.it'


def getShowList():
    url = URL_PREFIX + '/showlist/'
    headers = {'User-agent': USER_AGENT}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        shows = []

        soup = bs4.BeautifulSoup(response.content)
        for tr in soup.find_all('tr', attrs={'name': 'hover'}):
            title = ''
            link = ''
            status = ''

            a = tr.find('a')
            if a is not None:
                title = a.get_text()
                link = URL_PREFIX + a.get('href')

            font = tr.find('font')
            if font is not None:
                status = font.get_text()

            shows.append({'title': title,
                          'link': link,
                          'status': status})
        return shows
    return None


def main():
    shows = getShowList()

if __name__ == '__main__':
    main()
