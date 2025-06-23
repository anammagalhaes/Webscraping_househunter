from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

SITE_URLS = {
    "idealista": "https://www.idealista.pt/comprar-casas/lisboa/",
    "casasapo": "https://www.casaso.pt/comprar-casas/lisboa/",
    "olx": "https://www.olx.pt/ads/q-venda-casas/",
    "imovirtual": "https://www.imovirtual.com/pt/resultados/comprar/apartamento/lisboa/lisboa?viewType=listing"
}

def scrape(site):
    if site not in SITE_URLS:
        print(f" Site '{site}' não reconhecido.")
        return

    url = SITE_URLS[site]
    print(f"🌍 Scraping do site: {site} | URL: {url}")

    options = Options()
    options.headless = False
    options.add_argument("--start-maximized")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(" Erro ao iniciar navegador:", e)
        return

    driver.get(url)

    # Tenta clicar em cookies (caso seja o idealista)
    if site == "idealista":
        try:
            agree_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            agree_btn.click()
            print(" Cookies aceitos.")
        except:
            print("⚠️ Nenhum botão de cookies ou não necessário.")

    time.sleep(5)

    artigos = driver.find_elements(By.CSS_SELECTOR, "article")
    print(f" {len(artigos)} imóveis encontrados.")

    imoveis = []

    for item in artigos:
        try:
            titulo = item.find_element(By.CSS_SELECTOR, "a.item-link").text
            preco = item.find_element(By.CSS_SELECTOR, ".item-price").text
            link = item.find_element(By.CSS_SELECTOR, "a.item-link").get_attribute("href")

            print(f"🏠 {titulo} | 💰 {preco}")
            imoveis.append({
                "Título": titulo,
                "Preço": preco,
                "Link": link
            })
        except Exception as e:
            print(" Erro em um item:", e)
            continue

    driver.quit()

    if imoveis:
        filename = f"{site}_imoveis.csv"
        pd.DataFrame(imoveis).to_csv(filename, index=False)
        print(f"\n {len(imoveis)} imóveis salvos em {filename}")
    else:
        print(" Nada salvo, nenhum imóvel coletado.")

#scrape("idealista")
#scrape("casasapo")
scrape("imovirtual")
