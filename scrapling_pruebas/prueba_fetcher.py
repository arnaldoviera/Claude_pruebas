from scrapling.fetchers import Fetcher
from scrapling.parser import Selector

# 1) Fetcher HTTP (curl_cffi, imita huellas TLS de navegador)
page = Fetcher.get("https://quotes.toscrape.com/", impersonate="chrome")
print("status:", page.status)
for q in page.css(".quote")[:3]:
    print("-", q.css(".text::text").get(), "—", q.css(".author::text").get())
print("tags (xpath):", page.xpath("//div[contains(@class,'tags-box')]//a/text()").getall()[:5])
print("siguiente:", page.css("li.next a::attr(href)").get())
print("buscar por texto:", page.find_by_text("Albert Einstein", first_match=True))

# 2) Adaptive: guarda la huella del elemento y lo reencuentra si el HTML cambia
v1 = '<div class="lista"><div class="producto"><h2>Mate</h2><span class="precio" id="p1">$100</span></div></div>'
v2 = '<div class="grilla"><article class="item"><h2>Mate</h2><span class="price-tag" id="p1">$100</span></article></div>'  # rediseño: cambian clases y tags
s1 = Selector(v1, url="demo.local", adaptive=True)
s1.css(".precio", auto_save=True)
s2 = Selector(v2, url="demo.local", adaptive=True)
print("selector viejo en HTML nuevo:", s2.css(".precio"))
print("con adaptive=True:", s2.css(".precio", adaptive=True))

# 3) find_similar: a partir de un elemento, encuentra los "hermanos" con la misma estructura
primera = page.find_by_text("Albert Einstein", first_match=True).find_ancestor(lambda e: e.has_class("quote"))
print("citas similares a la primera:", len(primera.find_similar()))
