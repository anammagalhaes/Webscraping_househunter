from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    print(" Iniciando navegador...")

    options = Options()
    options.headless = False  # navegador visível
    options.add_argument("--start-maximized")

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(" Erro ao iniciar navegador:", e)
        return

    print(" Acessando o Idealista...")
    driver.get("https://www.idealista.pt/comprar-casas/lisboa/")

    # Tenta aceitar cookies
    try:
        agree_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
        )
        agree_btn.click()
        print(" Cookies aceitos.")
    except Exception as e:
        print(" Nenhum botão de cookies ou erro:", e)

    time.sleep(5)  # espera os imóveis carregarem

    artigos = driver.find_elements(By.CSS_SELECTOR, "article")
    print(f" {len(artigos)} imóveis encontrados.")

    imoveis = []

    for item in artigos:
        try:
            titulo = item.find_element(By.CSS_SELECTOR, "a.item-link").text
            preco = item.find_element(By.CSS_SELECTOR, ".item-price").text
            link = item.find_element(By.CSS_SELECTOR, "a.item-link").get_attribute("href")

            print(f" {titulo} | 💰 {preco}")
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
        df = pd.DataFrame(imoveis)
        df.to_csv("idealista_imoveis.csv", index=False)
        print(f"\n {len(imoveis)} imóveis salvos em idealista_imoveis.csv")
    else:
        print("⚠️ Nada salvo, nenhum imóvel coletado.")

scrape()
