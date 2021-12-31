import requests
from bs4 import BeautifulSoup as bs
import datetime
import time
import os

def get_article_wraper_EN():
    wraper_url = 'https://kcnawatch.org/article/163/'
    response = requests.get(wraper_url)
    soup = bs(response.content, "html.parser")
    soup = soup.find("div", attrs={"id": "latest_article_wrapper"})
    return soup


def get_url_list(soup):
    url_list = soup.find_all("h4")
    return url_list


def parse_target_url(soup, iter_num):
    """ Get target URL (Article URL) from article wraper.
        iter_num required to maintain cosistancy across article url,
        date, title ect...

    """

    target_url = url_list[iter_num].find('a')['href']
    return target_url

def parse_target_title(soup, iter_num):
    """ Get target URL (Article URL) from article wraper.
        iter_num required to maintain cosistancy across article url,
        date, title ect...

    """

    target_title = url_list[iter_num].find('img')['alt']
    return target_title


def parse_target_date(soup, iter_num):
    """ Get target publish date from article wraper.
        iter_num required to maintain cosistancy across article url,
        date, title ect...

    """
    target_date = soup.find_all("p", attrs={"class": "articled-date"})
    target_date= target_date[iter_num].text
    return target_date

def convert_to_datetime(target_date):
    datetime_obj = datetime.datetime.strptime(target_date, ' %B %d, %Y')
    return datetime_obj

def get_target_article(target_url):
    """ Retrieve target article URL"""
    target_response = requests.get(target_url)
    target_soup = bs(target_response.content, "html.parser")

    return target_soup


def get_target_body(target_soup):
    """ Extract target article body"""

    target_body = target_soup.find("div", attrs={"class": "article-content"})
    target_body = target_body.text

    return target_body


today  = datetime.datetime.now()

date = today.date()

format_dir = today.strftime('%m-%d-%Y')

os.mkdir('data/'+format_dir)

timedelta = datetime.timedelta(1)

article_wraper = get_article_wraper_EN()

url_list = get_url_list(article_wraper)

iter_num = 0

for i in range(len(url_list)):

    target_datestring = parse_target_date(article_wraper, iter_num)
    target_datetime = convert_to_datetime(target_datestring)
    target_date = target_datetime.date()

    if date == target_date:

        try:
            target_url = parse_target_url(url_list,iter_num)
            target_title = parse_target_title(url_list,iter_num)
            target_article = get_target_article(target_url)
            target_body = get_target_body(target_article)
            lines = [target_datestring, target_body, target_url]
            with open('data/'+format_dir+'/'+target_title+'.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')
                    f.write('\n')
            print(target_title)
            print(target_url)

        except:
            target_url = parse_target_url(url_list,iter_num)
            target_title = url_list[iter_num].text
            target_article = get_target_article(target_url)
            target_body = get_target_body(target_article)
            lines = [target_datestring, target_body, target_url]
            with open('data/'+format_dir+'/'+target_title+'.txt', 'w') as f:
                for line in lines:
                    f.write(line)
                    f.write('\n')
                    f.write('\n')
            print(target_title)
            print(target_url)
            #print('You Failed')
            #pass

        iter_num+=1

    else:

        print('Date Out of Range')
        print(target_date)
        break

    time.sleep(5)
