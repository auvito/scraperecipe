import scrapy
from ..items import Makanan, Bahan, Langkah


class MainSpider(scrapy.Spider):
    # command: scrapy crawl main -O ayam-daging.json -a category=ayam-daging
    name = 'main'
    allowed_domains = ['resepkoki.id']
    # start_urls = [
    #     'https://resepkoki.id/category/ayam-daging/',
    #     # 'https://resepkoki.id/category/ikan-seafood/',
    #     # 'https://resepkoki.id/category/tahu-tempe-telur/',
    #     # 'https://resepkoki.id/category/sayur/',
    #     # 'https://resepkoki.id/category/sambal/',
    #     # 'https://resepkoki.id/category/nasi-mie-pasta/',
    #     # 'https://resepkoki.id/category/sop-soto-bakso/',
    #     # 'https://resepkoki.id/category/kue-roti/',
    #     # 'https://resepkoki.id/category/jajanan-pasar/',
    #     # 'https://resepkoki.id/category/puding-jeli/',
    #     # 'https://resepkoki.id/category/keripik-kerupuk/',
    #     # 'https://resepkoki.id/category/buah-minuman/',
    # ]
    def start_requests(self):
        url = 'https://resepkoki.id/category/'
        category = getattr(self, 'category', None)
        if category is not None:
            url = url + category
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        food_links = response.css('.archive-item-media a::attr(href)').getall()
        yield from response.follow_all(food_links, self.parse_food)

        next_page = response.css('.nextpostslink::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_food(self, response):
        makanan = Makanan()

        makanan['nama'] = response.css('.single-title h1::text').get()
        makanan['waktu'] = response.css('li.single-meta-cooking-time span::text').get()
        makanan['porsi'] = response.css('.servings-adjuster-control input::attr(value)').get()
        makanan['kesulitan'] = response.css('.single-meta-difficulty span::text').get()
        makanan['likes'] = response.css('.osetin-vote-count::text').get()

        list_bahan = []
        namabahan = response.css('span.ingredient-name::text').getall()
        banyakbahan = response.css('span.ingredient-amount::text').getall()
        for itemnama, itembanyak in zip(namabahan, banyakbahan):
            bahan = Bahan()

            bahan['nama'] = itemnama
            bahan['banyak'] = itembanyak

            list_bahan.append(bahan)

        list_langkah = []
        urutanlangkah = response.css('.single-step-number-value::text').getall()
        deskripsilangkah = response.css('.single-step-description-i p::text').getall()
        for itemurutan, itemdeskripsi in zip(urutanlangkah, deskripsilangkah):
            langkah = Langkah()

            langkah['urutan'] = itemurutan
            langkah['deskripsi'] = itemdeskripsi

            list_langkah.append(langkah)

        makanan['bahan'] = list_bahan
        makanan['langkah'] = list_langkah

        yield makanan
