#!/usr/bin/python

import requests
import bs4
import re

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'
URL_PREFIX = 'http://eztv.it'


def getShowInfo(url):
    headers = {'User-agent': USER_AGENT}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.content)
        table = soup.find('table', class_='forum_header_border_normal')
        if table is None:
            return None

        title = ''
        td = table.find('td', class_='section_post_header')
        if td is not None:
            texts = list(td.stripped_strings)
            if len(texts) == 2:
                title = texts[1]

        logo = ''
        td = table.find('td', class_='show_info_main_logo')
        if td is not None:
            img = td.find('img')
            if img is not None:
                logo = img.get('src')
                if not logo.startswith('http'):
                    logo = 'http:' + logo

        banner = ''
        td = table.find('td', class_='show_info_banner_logo')
        if td is not None:
            img = td.find('img')
            if img is not None:
                banner = img.get('src')
                if not banner.startswith('http'):
                    banner = 'http:' + banner

        airs = ''
        status = ''
        returns = ''
        td = table.find('td', class_='show_info_airs_status')
        if td is not None:
            texts = list(td.stripped_strings)
            if len(texts) >= 5:
                airs = texts[1]
                status = texts[3]
                if len(texts) == 6:
                    returns = texts[5]

        description = ''
        description_table = table.find(
            'table', class_='section_thread_post show_info_description')
        if description_table is not None:
            td = description_table.find('td')
            if td is not None:
                description = td.get_text().strip()

        links = []
        td = table.find('td', class_='show_info_tvnews_column')
        if td is not None:
            for a in td.find_all('a'):
                links.append(URL_PREFIX + a.get('href'))

        shows = []
        show_table = table.find('table', class_='forum_header_noborder')
        for tr in show_table.find_all('tr'):
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

        return {'title': title,
                'logo': logo,
                'banner': banner,
                'airs': airs,
                'status': status,
                'returns': returns,
                'description': description,
                'links': links,
                'shows': shows}
    return None


def main():
    show = getShowInfo('http://eztv.it/shows/257/south-park/')

if __name__ == '__main__':
    main()
