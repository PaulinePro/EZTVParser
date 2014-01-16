#!/usr/bin/python

import requests
import bs4

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'
URL_PREFIX = 'http://eztv.it'


def getCalendar():
    url = URL_PREFIX + '/calendar/'
    headers = {'User-agent': USER_AGENT}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        calendar = []

        soup = bs4.BeautifulSoup(response.content)
        tables = soup.find_all('table', class_='forum_header_border')[1:]
        for table in tables:
            shows = []
            weekday = ''

            header_td = table.find('td', class_='forum_thread_header')
            if header_td is not None:
                weekday = header_td.get_text().strip()

            for tr in table.find_all('tr', attrs={'name': 'hover'}):
                link = ''
                image_url = ''
                title = ''
                trailer = ''

                i = 0
                for td in tr.find_all('td', class_='forum_thread_post'):
                    if i == 0:
                        a = td.find('a')
                        if a is not None:
                            link = URL_PREFIX + a.get('href')
                            img = a.find('img')
                            if img is not None:
                                image_url = img.get('src')
                                if not image_url.startswith('http'):
                                    image_url = 'http:' + image_url
                    elif i == 1:
                        a = td.find_all('a')
                        if len(a) == 1:
                            title = a[0].get_text()
                        elif len(a) == 2:
                            trailer = a[0].get('href')
                            title = a[1].get_text()
                    i += 1

                shows.append({'title': title,
                              'link': link,
                              'trailer': trailer,
                              'image_url': image_url})
            calendar.append({'weekday': weekday,
                             'shows': shows})
        return calendar
    return None


def main():
    shows = getCalendar()

if __name__ == '__main__':
    main()
