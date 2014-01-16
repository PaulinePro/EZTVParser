#!/usr/bin/python

import requests
import bs4
import re

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'
URL_PREFIX = 'http://eztv.it'


def getEztv():
    url = URL_PREFIX
    headers = {'User-agent': USER_AGENT}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        all_shows = []

        soup = bs4.BeautifulSoup(response.content)
        table = soup.find('table', class_='forum_header_border')
        if table is None:
            return None

        shows = []
        date = ''
        for tr in table.find_all('tr'):
            class_name = tr.get('class')
            if class_name is None:
                continue

            if 'forum_space_border' in class_name:
                if date:
                    all_shows.append({'date': date,
                                      'shows': shows})
                    shows = []

                date = tr.find('b').get_text()
            elif 'forum_header_border' in class_name:
                show_link = ''
                tvrage_link = ''
                episode_link = ''
                title = ''
                size = ''
                downloads = []
                released_time = ''
                forum_link = ''

                i = 0
                for td in tr.find_all('td'):
                    if i == 0:
                        a = td.find_all('a')
                        if len(a) == 1:
                            show_link = URL_PREFIX + a[0].get('href')
                        elif len(a) == 2:
                            show_link = URL_PREFIX + a[0].get('href')
                            tvrage_link = a[1].get('href')
                    elif i == 1:
                        a = td.find('a')
                        if a is not None:
                            episode_link = URL_PREFIX + a.get('href')
                            title = a.get_text()
                            alt = a.get('alt')
                            match = re.search('.*?\((.*?)\)', alt)
                            if match is not None:
                                size = match.group(1)
                    elif i == 2:
                        for a in td.find_all('a'):
                            download_title = a.get('title')
                            download_link = a.get('href')
                            downloads.append({'title': download_title,
                                              'link': download_link})
                    elif i == 3:
                        released_time = td.get_text()
                    elif i == 4:
                        a = td.find('a')
                        if a is not None:
                            forum_link = URL_PREFIX + a.get('href')
                            if 'discuss' in forum_link:
                                forum_link = ''

                            shows.append({'show_link': show_link,
                                          'tvrage_link': tvrage_link,
                                          'episode_link': episode_link,
                                          'title': title,
                                          'size': size,
                                          'downloads': downloads,
                                          'released_time': released_time,
                                          'forum_link': forum_link})
                    i += 1

        all_shows.append({'date': date,
                          'shows': shows})

        return all_shows
    return None


def main():
    shows = getEztv()

if __name__ == '__main__':
    main()
