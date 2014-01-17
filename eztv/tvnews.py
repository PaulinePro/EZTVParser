#!/usr/bin/python

import requests
import bs4

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'
URL_PREFIX = 'http://eztv.it'


def getTvnews():
    url = URL_PREFIX + '/tvnews/'
    headers = {'User-agent': USER_AGENT}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        news = []

        soup = bs4.BeautifulSoup(response.content)
        tables = soup.find_all('table', class_='forum_header_border')[2:-1]
        for table in tables:
            title = ''
            link = ''
            show_title = ''
            image_url = ''
            content = ''
            author = ''

            header_td = table.find('td', class_='tvnews_header', colspan='2')
            if header_td:
                a = header_td.find('a')
                if a:
                    title = a.get_text()
                    link = URL_PREFIX + a.get('href')

                div = header_td.find('div')
                if div:
                    show_title = div.get_text()

            td_image = table.find('td', class_='tvnews_image')
            if td_image:
                img = td_image.find('img')
                if img:
                    image_url = img.get('src')
                    if not image_url.startswith('http'):
                        image_url = 'http' + image_url

            td_content = table.find('td', class_='tvnews_content')
            if td_content:
                content = td_content.get_text().strip()

            td_footer = table.find('td', class_='tvnews_footer')
            if td_footer:
                author = td_footer.get_text().strip()

            news.append({'title': title,
                         'link': link,
                         'show_title': show_title,
                         'image_url': image_url,
                         'content': content,
                         'author': author})
        return news
    return None


def main():
    news = getTvnews()

if __name__ == '__main__':
    main()
