from scrapling.fetchers import Fetcher, DynamicFetcher
import os

# Chromium del sistema (opcional): evita depender de `scrapling install`
CHROMIUM = os.environ.get("CHROMIUM_PATH")
extra = {"executable_path": CHROMIUM} if CHROMIUM else {}

URL = "https://quotes.toscrape.com/js/"  # las citas se generan con JavaScript

estatico = Fetcher.get(URL)
print("Fetcher (HTTP):", len(estatico.css(".quote")), "citas")

dinamico = DynamicFetcher.fetch(URL, headless=True, network_idle=True, **extra)
citas = dinamico.css(".quote")
print("DynamicFetcher (Chromium):", len(citas), "citas")
print("primera:", citas[0].css(".author::text").get())
