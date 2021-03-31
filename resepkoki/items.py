# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Makanan(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nama = scrapy.Field()
    waktu = scrapy.Field()
    porsi = scrapy.Field()
    kesulitan = scrapy.Field()
    likes = scrapy.Field()
    bahan = scrapy.Field()
    langkah = scrapy.Field()

class Bahan(Makanan):
    nama = scrapy.Field()
    banyak = scrapy.Field()

class Langkah(Makanan):
    urutan = scrapy.Field()
    deskripsi = scrapy.Field()
