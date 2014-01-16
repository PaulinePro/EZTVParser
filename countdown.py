#!/usr/bin/python

import requests
import bs4

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'
URL_PREFIX = 'http://eztv.it'


def getCountDown():
    url = URL_PREFIX + '/countdown/'
    headers = {'User-agent': USER_AGENT}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        shows = []

        soup = bs4.BeautifulSoup(response.content)
        for tr in soup.find_all('tr', attrs={'name': 'hover'}):
            title = ''
            link = ''
            return_date = ''
            return_day = ''
            trailer = ''

            i = 0
            for td in tr.find_all('td'):
                if i == 0:
                    a = td.find('a')
                    if a is not None:
                        title = a.get_text()
                        link = URL_PREFIX + a.get('href')
                elif i == 1:
                    return_date = td.get_text()
                elif i == 2:
                    return_day = td.get_text()
                elif i == 3:
                    a = td.find('a')
                    if a is not None:
                        trailer = a.get('href')
                i += 1

            shows.append({'title': title,
                          'link': link,
                          'return_date': return_date,
                          'return_day': return_day,
                          'trailer': trailer})

        return shows
    return None


def main():
    shows = getCountDown()

if __name__ == '__main__':
    main()
