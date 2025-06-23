from scrapers import idealista, idealista_selenium

def main():
    print("Scraping Idealista")
    idealista.scrape()
    
    # print("Scraping noticias")
    # noticias.scrape()
    
if __name__ == "__main__":
    main()
    
    