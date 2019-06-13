import requests
from cookiespool.config import *
from lxml import etree
import pymongo


def zlhunt(page):

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['zlhunt']
    cookies = {
        'cookies': requests.get("http://0.0.0.0:5000/zlhunt/random").text
    }
    headers = {
        'User-Agent':'Mozilla / 5.0(Windows NT 6.1; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    for i in page:
        url = URL + i
        response = requests.get(url, header=headers, cookies=cookies)
        html = etree.parse(response.text, etree.HTMLParser())
        job_title = html.xpath("//div[@class='contentpile__content__wrapper clearfix']//span[@class='contentpile__content__wrapper__item__info__box__jobname__title']/@title")
        job_price = html.xpath("//div[@class='contentpile__content__wrapper clearfix']//p/text()")
        job_place = html.xpath("//div[@class='contentpile__content__wrapper clearfix']//li[@class='contentpile__content__wrapper__item__info__box__job__demand__item'][1]/text()")
        job_time = html.xpath("//div[@class='contentpile__content__wrapper clearfix']//li[@class='contentpile__content__wrapper__item__info__box__job__demand__item'][2]/text()")
        job_request = html.xpath("//div[@class='contentpile__content__wrapper clearfix']//li[@class='contentpile__content__wrapper__item__info__box__job__demand__item'][3]/text()")
        job_url = html.xpath("//div[@class='contentpile__content__wrapper__item clearfix']/a/@href")
        job = {
            'job_title': job_title,
            'job_price': job_price,
            'job_place': job_place,
            'job_time': job_time,
            'job_request': job_request,
            'job_url': job_url
        }
        db['zlhunt'].insert(job)


if __name__ == "__main__":
    zlhunt(200)