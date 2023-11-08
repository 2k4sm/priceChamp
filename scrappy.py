import requests as rq
import bs4 as bs4
import random
import prettytable as pt

class Product:
    """
    Provides functions for creating product specific search urls.
    """
    def __init__(self,product_name):
        self.product_name = str(product_name).replace(" ","+")
        
    
    def amazon_url(self):
        """
        Creates amazon url using product name and base url and returns it.
        """
        amazon_url = f"https://www.amazon.in/s?k={self.product_name}"
        
        return amazon_url
    
    def flipkart_url(self):
        """
        Creates flipkart url using product name and base url and returns it.
        """
        
        flipkart_url = f"https://www.flipkart.com/search?q={self.product_name}&marketplace=FLIPKART"
        
        return flipkart_url
    
    def product_urls(self):
        """
        returns an dictionary of product urls.
        """
        urls = {"amazon": self.amazon_url(),"flipkart" : self.flipkart_url()}
        
        return urls


class Request:
    
    """
    Provides functions for making request and processing response into useful fields.
    """
    
    def __init__(self,Product):
        
        self.custom_headers_list = [{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"},
                                    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"},
                                    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15',"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"},
                                    ]
        self.urls = Product.product_urls()
        self.htmls = self.get_htmls()
    
    def make_request(self):
        """
        Creates an get request to the product urls and returns the response content along with the status code as an response dictionary.
        """
        stat_codes = {}
        resp = {}
        
        for url in self.urls:
            req = rq.get(self.urls[url],headers = self.custom_headers_list[random.randint(0,2)])
            resp[url] = req.content
            stat_codes[url] = req.status_code
        
        response = {"status" : stat_codes,"response" : resp}
        
        return response
            
            
    
    def get_htmls(self):
        """
        Creates a html object using the response content and returns it.
        """
        self.htmls = {}
        response = self.make_request()["response"]
        
        for pf in response:
            html = bs4.BeautifulSoup(response[pf],"lxml")
            self.htmls[pf] = html
        
        return self.htmls
    
    def clean_html_tags(self,obj):
        """Removes Html tags and returns the output as string"""
        
        
        for i in range(len(obj)):
            obj[i] = obj[i].string
    
    def get_names(self):
        """
        Extract the Specified fields using custom css properties and returns the extracted product names as a dictionary of product list.
        """
        names = {}
        
        for html in self.htmls:
            name = []
            if (html == 'amazon'):
                name = self.htmls[html].select('div.puisg-col-inner span.a-size-medium.a-color-base.a-text-normal')
                name.extend(self.htmls[html].select('div.puisg-col-inner span.a-size-base-plus.a-color-base.a-text-normal'))
                self.clean_html_tags(name)
                # strips extended lines.
                for i in range(len(name)):
                    if len(name[i]) > 50:
                        name[i] = name[i][:51]+"..."
                    
                names[html] = name
            elif (html == 'flipkart'):
                name = self.htmls[html].find_all('div',{'class':'_4rR01T'})
                name.extend(self.htmls[html].find_all('a',{'class' : 's1Q9rs'}))
                name.extend(self.htmls[html].find_all('a',{'class' : 'IRpwTa'}))
                self.clean_html_tags(name)
                names[html] = name
        
        return names
    
    def get_prices(self):
        """
        Extract the Specified fields using custom css properties and returns the extracted product names as a dictionary of product list.
        """
        prices = {}
        
        for html in self.htmls:
            price = []
            if (html == 'amazon'):
                price = self.htmls[html].select('div.puisg-col-inner span.a-price-whole')
                self.clean_html_tags(price)
                # adds ₹ syblom in front of price and for none prices change them to PNA(product not found.)
                for i in range(len(price)):
                    if price[i] != None:
                        price[i] = "₹"+str(price[i])
                    else:
                        price[i] = "PNA"
                prices[html] = price
            elif (html == 'flipkart'):
                price = self.htmls[html].find_all('div',{'class':'_30jeq3'})
                self.clean_html_tags(price)
                prices[html] = price
        
        return prices
    
    
class Presentation:
    """
    Contains functions to Present the response data in a clean and meaningful table.
    """
    
    def print_table(product_website):
        """
        Uses the get_name and get_prices functions to get the product details and then displays them in a table.
        """
        
        names = Request(p1).get_names()[product_website]
        prices = Request(p1).get_prices()[product_website]

        table = pt.PrettyTable(align='l')

        table.field_names = ["S.NO",f"                  {product_website} Product Name", "Price (INR)"]
        no = 1
        for name, price in zip(names,prices):
            table.add_row([no,name, price])
            no+=1

        print(table)
    
    
    
# Driver Code.
if __name__ == "__main__":
    product_name = str(input("Enter Product name to search for: "))

    p1 = Product(product_name)

    Presentation.print_table("flipkart")
    Presentation.print_table("amazon")


