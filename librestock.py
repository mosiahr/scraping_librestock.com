#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import time
import os
import csv
import sys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'http://librestock.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# NOT FOUND:
# http://fancycrave.com
# https://negativespace.co
# https://skitterphoto.com

# Not
# http://isorepublic.com/


try:
    SEARCH = ' '.join(sys.argv[1:])
except IndexError:
    SEARCH = None
    print('Enter the argument: \'search\' ')


def get_page(search):
    browser = webdriver.Firefox()
    browser.get(BASE_URL)

    elem = browser.find_element_by_name('query')
    elem.send_keys(search)
    elem.send_keys(Keys.RETURN)

    try:
        while browser.find_elements_by_tag_name('button')[0]:
            browser.find_elements_by_tag_name('button')[0].click()
            time.sleep(3)
    except:
        pass

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    class_overlay = soup.find_all(class_='overlay')
    images = [el.a['href'] for el in class_overlay]
    browser.quit()

    rez = {'search': search,
           'images': images}
    return rez


def save_page_to_file(file, pages):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for page in zip(pages):
            writer.writerow(page)


def get_domain(url):
    split_url = urlsplit(url)
    domain = '{}://{}'.format(split_url.scheme, split_url.netloc)
    return domain


def get_html(url):
    response = urlopen(url)
    return response.read().decode('utf-8')


def get_html_req(url):
    response = requests.get(url, headers=headers)
    return response.text


def get_src_pixabay(html):
    """ Getting a link from the site: www.pixabay.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', id='media_container')
    img = img.find('img')['src']
    return img


# def get_src_stock_tookapic(html):
#     """ Getting a link from the site: stock.tookapic.com """
#     soup = BeautifulSoup(html, 'html.parser')
#     img = soup.find('div', class_='c-stock-photo__image')
#     img = img.find('img')['data-src'].split('|')[0]
#     return img


def get_src_stocksnap(html):
    """ Getting a link from the site: https://stocksnap.io """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='img-col')
    img = img.find('img')['src']
    return img


def get_src_bossfight(url):
    """ Getting a link from the site: https://bossfight.co """
    browser = webdriver.Firefox()
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    img = soup.find('main', id='main')
    img = img.find('div', class_='entry-cover')['style']
    img = img.split('url')[1].lstrip('(\'').rstrip('\')')
    img = img.split('?')[0]
    browser.quit()
    return img


def get_src_picjumbo(html):
    """ Getting a link from the site: https://picjumbo.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='img_wrap single')
    img = img.find('img')['src'].lstrip('//').split('?')[0]
    img = 'http://{}'.format(img)
    return img

def get_src_jaymantri(html):
    """ Getting a link from the site: http://jaymantri.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='photo-wrapper-inner')
    img = img.find('img')['src']
    return img


def get_src_kaboompics(url):
    """ Getting a link from the site: http://kaboompics.com """
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        img = soup.find('div', class_='one')
        img = img.find('img')['src']
        browser.quit()
    except WebDriverException:
        img = None
        print("Message: Reached error page")
        browser.quit()
    return img


def get_src_libreshot(html):
    """ Getting a link from the site: http://libreshot.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('figure', class_='wp-caption aligncenter')
    img = img.find('a')['href']
    return img


def get_src_stock_tookapic(html):
    """ Getting a link from the site: http://stock.tookapic.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='c-stock-photo__image')
    img = img.find('img')['data-src']
    img = img.split('|')[0]
    return img


def get_src_pexels(url):
    """ Getting a link from the site: http://www.pexels.com"""
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        img = soup.find('div', class_='btn-primary btn--lg btn--splitted')
        img = img.a['href']
        browser.quit()
    except:
        img = None
        browser.quit()
    return img


def get_src_barnimages(html):
    """ Getting a link from the site: https://barnimages.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', id='buttonwrap')
    img = img.find('a')['href']
    return img


def get_src_freemagebank(html):
    """ Getting a link from the site: http://www.freemagebank.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('a', id='main_product_image')['href']
    return img


def get_src_splitshire(url):
    """ Getting a link from the site: https://www.splitshire.com """
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        img = soup.find('div', class_='post-content').find('img')['src']
        browser.quit()
    except:
        img = None
        browser.quit()
    return img


def get_src_foodiesfeed(html):
    """ Getting a link from the site: http://foodiesfeed.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='entry').find('img')['srcset']
    img = img.split(',')[0].split()[0]
    return img


def get_src_finda_photo(html):
    """ Getting a link from the site: http://finda.photo """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='image-detail-image-container').find('img')['src']
    return img


def get_src_freestocks(html):
    """ Getting a link from the site: http://freestocks.org """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='img-wrap')
    img = img.find('img')['srcset'].split(',')[0]
    img = img.split()[0]
    return img


def get_src_freelyphotos(html):
    """ Getting a link from the site: http://freelyphotos.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_="featured-media")
    img = img.find('img')['src']
    return img


def get_src_streetwill(html):
    """ Getting a link from the site: http://streetwill.co"""
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='image-wrapper')
    img = img.find('img')['src']
    img = 'http://streetwill.co{}'.format(img)
    return img


def get_src_travelcoffeebook(html):
    """ Getting a link from the site: http://travelcoffeebook.com"""
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='media')
    img = img.find('img')['src']
    return img


def get_src_lookingglassfreephotos(html):
    """ Getting a link from the site: https://lookingglassfreephotos.tumblr.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='photo__wrapper')
    img = img.find('img')['src']
    return img


def get_src_nomad_pictures(html):
    """ Getting a link from the site: https://nomad.pictures """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='entry-content')
    img = img.find('img')['src']
    return img


def get_src_mystock_photos(html):
    """ Getting a link from the site: http://mystock.photos """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='entry-content')
    img = img.find('img')['src']
    return img


def get_src_goodstock_photos(html):
    """ Getting a link from the site: https://goodstock.photos """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='entry-content')
    img = img.find('img')['src']
    return img


def get_src_alana(html):
    """ Getting a link from the site: http://alana.io """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', id='product_images')
    img = img.find('img')['src']
    return img


def get_src_minimography(html):
    """ Getting a link from the site: http://minimography.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='entry-content')
    img = img.find('img')['src']
    return img


def get_src_picalls(html):
    """ Getting a link from the site: http://picalls.com"""
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='single-izquierda')
    img = img.find('img')['src']
    return img


def get_src_pickleja(html):
    """ Getting a link from the site: http://www.picklejar.in """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('article', class_='gallery-item full')
    img = img.find('img')['src']
    return img


def get_src_publicdomainarchive(html):
    """ Getting a link from the site: http://publicdomainarchive.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='entry-content')
    img = img.find('img')['src']
    return img


def get_src_realisticshots(html):
    """ Getting a link from the site: http://realisticshots.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', class_='photo')
    img = img.find('img')['src']
    return img


def get_src_designerspics(html):
    """ Getting a link from the site: http://www.designerspics.com """
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('div', id='content')
    img = img.find('img')['src']
    return img


def save_img(src, name):
    dir_img = '{}/{}_img'.format(BASE_DIR, SEARCH.replace(' ', '_'))
    if not os.path.exists(dir_img):
        os.mkdir(dir_img)

    try:
        r = requests.get(src, headers=headers)
        if r.status_code == 200:
            with open("{}/{}.jpg".format(dir_img, name), 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            print('Status code:', r.status_code)
    except ConnectionError as err:
        print(err)


def parse(url):
    src = name = None
    try:
        split_url = urlsplit(url)
        print(split_url)
        if '.jpg' in split_url.path:
            try:
                src = url
                name = split_url.path.strip('/').split('/')[-1].rstrip('.jpg')
                name = '{}_{}'.format(split_url.netloc, name)
            except:
                pass
        elif split_url.netloc == 'www.pixabay.com':
            try:
                src = get_src_pixabay(get_html(url))
                name = split_url.path.strip('/').split('/')[1]
                name = 'pixabay_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'stock.tookapic.com':
            try:
                src = get_src_stock_tookapic(get_html(url))
                name = src.split('/')[-1].split('?')[0].rstrip('.jpg')
                name = 'stock_tookapic_{}'.format(name)
                print(src)
                print(name)
            except:
                pass
        elif split_url.netloc == 'www.stocksnap.io':
            try:
                src = get_src_stocksnap(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'stocksnap_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'bossfight.co':
            try:
                src = get_src_bossfight(url)
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'bossfight_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'picjumbo.com':
            try:
                src = get_src_picjumbo(get_html(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'picjumbo_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'jaymantri.com':
            try:
                src = get_src_jaymantri(get_html(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'jaymantri_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'kaboompics.com':
            try:
                src = get_src_kaboompics(url)
                name = src.split('/')[-1].rstrip('_min.jpg')
                name = 'kaboompics_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'libreshot.com':
            try:
                src = get_src_libreshot(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'libreshot_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'www.pexels.com':
            try:
                src = get_src_pexels(url)
                name = src.split('/')[-2].rstrip('.jpg')
                name = 'pexels_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'barnimages.com':
            try:
                src = get_src_barnimages(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'barnimages_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'www.freemagebank.com':
            try:
                src = get_src_freemagebank(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'freemagebank_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'www.splitshire.com':
            try:
                src = get_src_splitshire(url)
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'splitshire_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'foodiesfeed.com':
            try:
                src = get_src_foodiesfeed(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'foodiesfeed_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'www.finda.photo':
            try:
                src = get_src_finda_photo(get_html_req(url))
                src = 'http://finda.photo{}'.format(src)
                name = src.split('/')[4]
                name = 'finda_photo_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'freestocks.org':
            try:
                src = get_src_freestocks(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'freestocks_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'freelyphotos.com':
            try:
                src = get_src_freelyphotos(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'freelyphotos_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'streetwill.co':
            try:
                src = get_src_streetwill(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'streetwill_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'travelcoffeebook.com':
            try:
                src = get_src_travelcoffeebook(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'travelcoffeebook_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'lookingglassfreephotos.tumblr.com':
            try:
                src = get_src_lookingglassfreephotos(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'lookingglassfreephotos_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'nomad.pictures':
            try:
                src = get_src_nomad_pictures(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'nomad.pictures_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'mystock.photos':
            try:
                src = get_src_mystock_photos(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'mystock.photos_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'goodstock.photos':
            try:
                src = get_src_mystock_photos(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'goodstock.photos_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'alana.io':
            try:
                src = get_src_alana(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'alana.io_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'minimography.com':
            try:
                src = get_src_minimography(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'minimography.com_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'picalls.com':
            try:
                src = get_src_picalls(get_html_req(url))
                name = src.split('/')[-1].split('.')[0]
                name = 'picalls.com_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'www.picklejar.in':
            try:
                src = get_src_pickleja(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'picklejar.in.com_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'publicdomainarchive.com':
            try:
                src = get_src_publicdomainarchive(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'publicdomainarchive.com_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'realisticshots.com':
            try:
                src = get_src_realisticshots(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'realisticshots.com_{}'.format(name)
            except:
                pass
        elif split_url.netloc == 'www.designerspics.com':
            try:
                src = get_src_designerspics(get_html_req(url))
                name = src.split('/')[-1].rstrip('.jpg')
                name = 'designerspics.com_{}'.format(name)
            except:
                pass

        else:
            src = None
            name = None


        if src and name:
            save_img(src, name)
        else:
            print("Not found")

    except HTTPError as err:
        if err.code == 404:
                print("Not Found. The URL:'{}' you requested could not be found.".format(url))
        else:
            raise


def main():
    print('Scrape START')
    print('-------------------------------')
    count = 0
    page_search = get_page(SEARCH)
    print("Found %s pages" % len(page_search['images']))
    pages = page_search['images']
    file_search = '.'.join((page_search['search'].replace(' ', '_'), 'csv'))
    save_page_to_file(file_search, pages)

    with open(file_search) as csvfile:
        reader = csv.reader(csvfile)

        r_list = [el for el in reader]
        print(r_list)
        for url in r_list:
            count += 1
            print(url[0])
            parse(url[0])
            print('Scrape: %d%%' % (count/len(page_search['images'])*100))


if __name__ == '__main__':
    main()
