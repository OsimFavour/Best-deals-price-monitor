import requests
from bs4 import BeautifulSoup
from pony import orm
from datetime import datetime
from requests_html import HTMLSession
import http.client


AMAZON_URL = "https://www.amazon.com/dp/B09JQSLL92/"
BESTBUY_URL = "https://www.bestbuy.com/pricing/v1/price/item?allFinanceOffers=true&catalog=bby&context=offer-list&includeOpenboxPrice=true&paidMemberSkuInCart=false&salesChannel=LargeView&skuId=6450856&useCabo=true&usePriceWithCart=true&visitorId=09e0ebb8-6987-11ed-a0ab-1217a82b487f"
EBAY_URL = "https://www.ebay.com/p/13050304310"
WALMART_URL = "walmart.com/ip/Apple-MacBook-Pro-14-inch-Apple-M1-Pro-chip-with-8-core-CPU-and-14-core-GPU-16GB-RAM-512GB-SSD-Space-Gray/861122204"
TODAY = datetime.now().strftime("%Y-%m-%d")
PRODUCT_NAME = "Apple MacBook Pro (14-inch, Apple M1 Pro chip with 8-core CPU and 14-core GPU, 16GB RAM, 512GB SSD) - Space Gray"


db = orm.Database()
db.bind(provider='sqlite', filename='tracker.db', create_db=True)


class Product(db.Entity):
    product = orm.Required(str)
    ecommerce_site = orm.Required(str)
    current_price = orm.Required(float)
    created_date = orm.Required(datetime)


db.generate_mapping(create_tables=True)


def amazon():
    session = HTMLSession()
    response = session.get(AMAZON_URL)
    response.html.render(sleep=6)
    data = (
        "Amazon",
        float(response.html.xpath('//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[1]', first=True).text.replace("$", "").replace(",", "").strip())
   )
    return data



def best_buy():
    headers = {
    'authority': 'www.bestbuy.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'CTT=eb7cf39e5ce04fee72b3029873611224; oid=1094554225; vt=09e0ebb8-6987-11ed-a0ab-1217a82b487f; __gads=ID=248c0b2d9a41b385:T=1669026442:S=ALNI_MZdV4_K5-Pz97FSIMaa44nw-Ml0lw; s_ecid=MCMID%7C25122470040933118614091273757687944481; __gsas=ID=761c23bc48b4a916:T=1669026569:S=ALNI_MYxlW4LUO50TY7ERiSIb8rslmm0Fg; aam_uuid=31704918058267613033595435902937873411; _gcl_au=1.1.1454209105.1669026702; locDestZip=00820; locStoreId=1118; sc-location-v2=%7B%22meta%22%3A%7B%22CreatedAt%22%3A%222022-11-21T10%3A31%3A44.250Z%22%2C%22ModifiedAt%22%3A%222022-11-21T10%3A31%3A47.568Z%22%2C%22ExpiresAt%22%3A%222023-11-21T10%3A31%3A47.568Z%22%7D%2C%22value%22%3A%22%7B%5C%22physical%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2200820%5C%22%2C%5C%22source%5C%22%3A%5C%22A%5C%22%2C%5C%22captureTime%5C%22%3A%5C%222022-11-21T10%3A31%3A44.249Z%5C%22%7D%2C%5C%22destination%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2200820%5C%22%7D%2C%5C%22store%5C%22%3A%7B%5C%22storeId%5C%22%3A1118%2C%5C%22zipCode%5C%22%3A%5C%2200918%5C%22%2C%5C%22storeHydratedCaptureTime%5C%22%3A%5C%222022-11-21T10%3A31%3A47.566Z%5C%22%7D%7D%22%7D; _cs_c=1; intl_splash=false; intl_splash=false; bby_rdp=l; SID=140a671d-38f2-429a-81b4-7d37bf99303f; bm_sz=D1130D140AE7ED3A9934CD2B3DA6B218~YAAQhdN6XIMgms2EAQAAZ3487BLobZP9zU1s6DdUGtVB+60k5tDKJKfC7ufQUPXPWiCVq1ZuFtrKull2TaI0KSvv/YJt+t1kk8SpAY7Pspw8nyThIf9DmVKJPPAONp8fXQ9GVbor2G8A5f4qZ+LnlwsF/Fcbbs/k/OwVQNh1wq4bwp9r7OfEf04nWQ10eMvdVJPAUfeS0G0X3SuEpXGIKg48GVg2RzTF/Kxe4v1EQRJqoOBeaWk4z73cnhNgDa70zJLjH9c6vnV/45SyTHnICjSbMtDBVxY2Jl6mAKQ/KXExii0ztuc6ml7iqE3OKp8T5VF7lQWh6fMSxDtW+Up9Br0VNltdPGc14QcQcGF0d0o3ofa9LdGBlO2HRV9dY4vYxVBjSJ8pp4OPiMbegCPm0RjXtg==~4473412~4605509; _abck=50ACDF3A9C803195A0EC0B135E05879A~0~YAAQhdN6XIIgms2EAQAAZ3487Am+NGMMnCYXmkg5fbo3yhZyfglPT+IILvm7XjjccxXc9C/yC/GbfeV5tgjon7/tF5vN+pGO9cd5JngeKTqfkV1t1bg/FRD+3KFFAhlZakXueXBCdBXW6IqWfl4Q/n7f4lMTPkG7UruBgnqMYooxFwoyqVRm72vdwbhmPUbe0gUKYL2PotfHFhr9jYR5iafzSjRo7OHNiA/BtIMM5z6RD+UvjOS30Vkz1bD+C6IxeESzhHmtnSEskonuV2rrPH+5NneSiwUNfLIIaiN0WolEvs2xb8RZQFg6+UbmBuG8ketwJPaSJNynPxeHTQf741Xp357GNpWFY1W+DLMFOhSsl+1DlTTXSnETT8qmSkZdyU1tlSmzLl1Lt5xmXd6opUfN1idpF+a2lOsLjCPWSv9l9e1yIJlT+ySJxUHmQhbP~-1~-1~-1; rxVisitor=1670410847000MB7D42FQ4896UGP22T81UU0EGLPGIVCD; COM_TEST_FIX=2022-12-07T11%3A02%3A00.228Z; dtCookie=v_4_srv_2_sn_99UB3CL3VUHLGPR4MNH4JUAPFDFS8AJ5_app-3Aea7c4b59f27d43eb_1_app-3A1b02c17e3de73d2a_1_ol_0_perc_100000_mul_1; __gpi=UID=00000b23efe4d3fe:T=1669026442:RT=1670410799:S=ALNI_MY5I8hCoy0rw4Gh5QcjinJgH0elBg; surveyDisabled=true; AMCVS_F6301253512D2BDB0A490D45%40AdobeOrg=1; AMCV_F6301253512D2BDB0A490D45%40AdobeOrg=1585540135%7CMCMID%7C25122470040933118614091273757687944481%7CMCAAMLH-1671015747%7C6%7CMCAAMB-1671015747%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1670418148s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-247786330%7CvVersion%7C4.4.0; _cs_mk=0.2265404984285826_1670410948116; s_cc=true; s_sq=%5B%5BB%5D%5D; c2=Product%20Detail%20Page; dtSa=-; cto_bundle=mnauRF9LZnUlMkJyOVVCNUZYdWx3UFJrQWJydFlxaWQ2cGZJZnp1OTFtWVVEa0glMkYlMkZoJTJCSnBTYlprbGJvNiUyQm42R2pYdXZETGF3MnFxRDZsOTlrcENMb2xJM3FLdiUyQkw0Rm1VTFBvOSUyRlElMkZsbnYlMkZvJTJGY0pjVVplN3h5eXA5blE0dTBxTnY0QTdNcWQybU5JenFhcExKJTJCaE5Odm9IR0VBJTNEJTNE; _cs_id=c4896e38-0606-a694-fb70-3f296144623c.1669026708.19.1670413927.1670413804.1645469968.1703190708422; _cs_s=3.0.0.1670415728258; ltc=%20; bby_cbc_lb=p-browse-e; dtPC=2$15588424_670h1vWLFSUGNSKCBNHPPMQPSUCMKFBUGRVKPJ-0e0; dtLatC=424; rxvt=1670417388516|1670413692271; _abck=50ACDF3A9C803195A0EC0B135E05879A~-1~YAAQbo57XGU2vISEAQAAy9KS7Am+XV1wiBz7laYS85oxgJw0NlO3+4zVMQVK57oJ7EW9KFQy76LNYmJTMQqktM9n8YfBNMKc6vUpVT3YZMTVew6Wn28kaZR+lfAI84JjzxjIYZIWfF6bROR6+zDjfGQP/ayJgOJ5IZRe5j4/iTn/OWKMlcOLYFmv3hBV1RZoWD3CoqcmT83PwpcScfsrhJjZhX7N0HAKr+HhZcZ3f8sY/Y4BgvT18ijf+arpx57IrfCewGUVPTiMXcxrGZifRUuYxHTVV4VaDtw+KFWUeF6EJc4qlVBijHiGf185wQCEZdghuZCjH8IgxExaW8lk5XDFR2iI2/5immpmd5FDllaoU/7mckp8ErlHkn++FRNa7V2DMCybAERJe8dSC4iXfZh0WUdvpTXx5mkdzdkFwS6ifzhv39voL0N06b76XGsH~0~-1~-1; bby_prc_lb=p-prc-e',
    'referer': 'https://www.bestbuy.com/site/macbook-pro-14-laptop-apple-m1-pro-chip-16gb-memory-512gb-ssd-latest-model-silver/6450856.p?skuId=6450856&intl=nosplash',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'x-client-id': 'lib-price-browser'
    }
    response = requests.request("GET", BESTBUY_URL, headers=headers).json()

    data = (
        "Bestbuy",
        float(response['currentPrice'])
    )
    return data
    

def ebay():
    response = requests.get(EBAY_URL).text
    soup = BeautifulSoup(response, "html.parser")
    data = (
        "Ebay",
        float(soup.find("div", {"class": "display-price"}).text.replace("$", "").replace(",", ""))
    )
  
    return data


def walmart():
    conn = http.client.HTTPSConnection("api.scrapingant.com")
    conn.request("GET", f"https://api.scrapingant.com/v2/general?url=https%3A%2F%2F{WALMART_URL}&browser=false&x-api-key=25faca642b9045e59d1cbcc54eae09bf")
    res = conn.getresponse()
    parsed_data = res.read()
    decoded_text = parsed_data.decode("utf-8")
    soup = BeautifulSoup(decoded_text, "html.parser")
    data = (
        "Walmart",
        float(soup.find("span", {"itemprop": "price"}).text.replace("$", "").replace(",", "").strip())
    )
    return data
    


def main():

    data = [
        amazon(),
        best_buy(),
        ebay(),
        walmart() 
    ]

    # print(data)

    with orm.db_session:
        for item in data:
            Product(product=PRODUCT_NAME, ecommerce_site=item[0], current_price=item[1], created_date=TODAY)

     


if __name__ == '__main__':
    main()
