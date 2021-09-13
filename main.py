import urllib
import urllib.request

from docx import Document
from bs4 import BeautifulSoup as bSoup
from lxml import html

base_url = 'https://dilemaveche.ro'


def get_soup(html_content):
    return bSoup(html_content, "html.parser")


def get_soup_for_link(given_link):
    header = {'User-Agent': 'Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}
    req = urllib.request.Request(url=given_link, headers=header)
    page = urllib.request.urlopen(req).read()
    return get_soup(page)


def get_article_links_from_page(url):
    page_soup = get_soup_for_link(url)
    articles = page_soup.findAll('h2', {'class': 'title'})
    link_list = []
    for i in range(0, len(articles)):
        link_html_soup = get_soup(str(articles[i]))
        iterable_obj = iter(link_html_soup.children)
        while True:
            try:
                item = next(iterable_obj)
                link_list.append(base_url + get_soup(str(item)).find('a')['href'])
            except StopIteration:
                break
    return link_list


def get_text_from_article_url(article_link):
    article_div_paragraphs = get_soup_for_link(article_link).findAll('p')
    p_list_to_string = ''
    for i in range(0, len(article_div_paragraphs) - 1):
        p_list_to_string += str(article_div_paragraphs[i])
    tree = html.fromstring(p_list_to_string)
    return tree.text_content().strip()


def create_docx(file_name, content):
    base_path = 'C:\\Users\\Rares\\Desktop\\articole'
    doc = Document()
    doc.add_paragraph(content)
    doc.save(base_path + '\\' + file_name + '.docx')


def get_article_title(link):
    soup = get_soup_for_link(link)
    title = str(soup.findAll('h1', {'class': 'article-title'})[0])
    title_soup = get_soup(title).getText()
    return title_soup


if __name__ == '__main__':
    for i in range(1, 48):
        url = f'https://dilemaveche.ro/autor/rodica-zafiu?page={i}'
        links = get_article_links_from_page(url)
        for link in links:
            article_text = get_text_from_article_url(link)
            article_title = get_article_title(link)
            create_docx(article_title, article_text)

