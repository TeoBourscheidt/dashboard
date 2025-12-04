import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

def scrape_price(asset: str) -> float:
    """
    Scrape le prix actuel d’un actif depuis Investing.com (version moderne du site).
    
    Parameters
    ----------
    asset : str
        Slug de l’actif dans l’URL (ex : 'cac-40', 's-p-500', 'bitcoin').
    
    Returns
    -------
    float
        Le prix actuel, ou NaN si erreur.
    """

    # Exemple d’URL Investing.com (indices)
    url = f"https://www.investing.com/indices/{asset}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Le prix est dans une div avec un data-test très stable
        price_tag = soup.find("div", attrs={"data-test": "instrument-price-last"})

        if price_tag is None:
            raise ValueError("Impossible de trouver le prix (data-test='instrument-price-last').")

        # Nettoyage de la valeur
        price_str = price_tag.text.strip().replace(",", "")

        return float(price_str)

    except Exception as e:
        print(f"Erreur dans scrape_price : {e}")
        return float("nan")


#essayer de voir pour faire le scraping sur une periode de temps, j' n'ai pas reussi 