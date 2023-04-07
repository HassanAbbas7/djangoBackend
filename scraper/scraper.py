import csv
import os
from urllib.parse import urljoin, urlparse

import requests
from fake_useragent import FakeUserAgent
from selectolax.parser import HTMLParser

from .models import Data


class CrawlWebsite(object):
    def __init__(self, website_link) -> None:
        self.website_link = website_link
        self.url_hostname = urlparse(website_link).hostname
        while True:
            try: self.user_agent = FakeUserAgent(); break
            except : pass

    def find_all_urls_on_page(self):
        """
        Finds all links referenced by a particular URL.
        :param url:
        :param use_callback:
        :return:
        """
        found_urls = []
        r = requests.get(self.website_link, headers={'user-agent': self.user_agent.random})

        # Only operate on pages with a content-type header
        if r.headers.get('content-type') is None:
            return found_urls

        # Only handle HTML files
        if "text/html" not in r.headers.get('content-type'):
            return found_urls

        tree = HTMLParser(r.text)
        for a in tree.body.css("a"):
            a_href = a.attrs.get("href")

            # Skip empty urls
            if a_href is None or len(a_href) == 0:
                continue

            # If the url is relative, make it absolute
            if a_href[0] == '/':
                a_href = urljoin(self.website_link, a_href)

            if a_href[:a_href.find(":")] not in ("http", "https"):
                continue

            # Clean the url
            url_parts = urlparse(a_href)
            a_href = url_parts.scheme + '://' + url_parts.netloc + url_parts.path

            if url_parts.query:
                a_href += "?" + url_parts.query

            # If its an external url, skip it
            if not self.is_internal_url(a_href):
                continue

            if a_href == self.website_link : continue

            found_urls.append(a_href)

        return list(set(found_urls))

    def is_internal_url(self, url):
        """
        Checks if a URL is internal or external pointing.
        :param url:
        :return:
        """
        return self.url_hostname in url


def get_text_selectolax(tree):
    if tree.body is None:
        return None
    for tag in tree.css('script'):
        tag.decompose()
    for tag in tree.css('style'):
        tag.decompose()
    text = tree.body.text(strip=True).strip()
    return text


def clean_url(website_link, a_href):
    # Skip empty urls
    if a_href is None or len(a_href) == 0:
        return

    # If the url is relative, make it absolute
    if a_href[0] == '/':
        a_href = urljoin(website_link, a_href)

    if a_href[:a_href.find(":")] not in ("http", "https"):
        return

    # Clean the url
    url_parts = urlparse(a_href)
    a_href = url_parts.scheme + '://' + url_parts.netloc + url_parts.path

    if url_parts.query:
        a_href += "?" + url_parts.query

    return a_href


def scrape_url(target_website, url, user_agent):
    headers = {
        'user-agent': user_agent,
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'accept': '*/*',
        'sec-ch-ua-platform': '"Windows"',
    }
    try:
        r = requests.get(url, headers=headers, timeout=25)
    except:
        r = requests.get(url, headers=headers, timeout=25)
    if r.status_code != 200:
        return
    tree = HTMLParser(r.text)
    title = tree.css_first('title')
    if title: title = title.text(strip=True)
    else : title = '-'
    description = tree.css_first('meta[name="description"]')
    if description: description = description.attributes.get('content')
    else : description = '-'
    keywords = tree.css_first('meta[name="keywords"]')
    if keywords: keywords = keywords.attributes.get('content')
    else : keywords = '-'
    text = get_text_selectolax(tree)
    if not text : text = '-'
    links = tree.css('body a[href]')
    if len(links):
        links = [link.attributes.get('href') for link in links]
    real_links = []
    for link in links:
        if link == '/' or link == '#': continue
        link = clean_url(url, link)
        if link: real_links.append(link)
    real_links = list(set(real_links))
    if not len(real_links) : real_links = ['-']

    images = tree.css('body img[src]')
    if len(images): images = list(set([img.attributes.get('src') for img in images]))
    else :images = ['-']
    videos = tree.css('a[href*="//youtu."]')
    if len(videos): videos = list(set([vid.attributes.get('href') for vid in videos]))
    else : videos = ['-']

    d = Data(Target_website=target_website, URL=url, Title=title, Description=description, Keywords=keywords, Text=text, Links=', '.join(real_links), Images=', '.join(images), Videos=', '.join(videos))
    d.save()
    return {'Target Website': target_website, 'URL': url, 'Title': title, 'Description': description, 'Keywords': keywords, 'Text': text, 'Links': ', '.join(real_links), 'Images': ', '.join(images), 'Videos': ', '.join(videos)}

def main_scraper(target_website):
    while True:
        try: user_agents = FakeUserAgent(); break
        except : pass
    fieldnames=['Target Website', 'URL', 'Title', 'Description', 'Keywords', 'Text', 'Links', 'Images', 'Videos']
    out_put = 'Django_Scraper_Data.csv'
    if os.path.exists(out_put):
        f = open(out_put, 'a', encoding='utf-8-sig', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    else:
        f = open(out_put, 'w', encoding='utf-8-sig', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
    crawler = CrawlWebsite(target_website)
    for url in crawler.find_all_urls_on_page():
        print(url)
        try:
            data = scrape_url(target_website, url, user_agents.random)
            if data:
                csv_writer.writerow(data)
        except  Exception as e: print(e)
    f.close()
    print('Finished scraping')
