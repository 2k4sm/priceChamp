import requests as rq
import bs4 as bs4


class Product:
    def __init__(self,product_name):
        self.product_name = str(product_name).replace(" ","+")
        
    
    def amazon_url(self):
        base_url = "https://www.amazon.in/s?k="
        
        return base_url + self.product_name
    
    def flipkart_url(self):
        base_url = "https://www.flipkart.com/search?q="
        
        return base_url + self.product_name
    
    def myntra_url(self):
        base_url = "https://www.myntra.com/"
        
        return base_url + self.product_name
    
    
    def product_urls(self):
        urls = {"amazon": self.amazon_url(),"flipkart" : self.flipkart_url(),"myntra" : self.myntra_url()}
        
        return urls


class Request:
    
    def __init__(self):
        self.custom_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'}
        self.urls = Product.product_urls()
    
    def make_request(self):
        pass
    
    def get_html(self):
        pass
    
        
        
