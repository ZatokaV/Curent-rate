import requests
from bs4 import BeautifulSoup

from urls import url


def get_bank_data(soup: BeautifulSoup) -> list:
    bank_name = soup.find_all('a', class_='mfm-black-link')
    return [bank.text.strip() for bank in bank_name if 'mfm-bank-icon' in str(bank)]


def get_rate_data(soup: BeautifulSoup) -> list:
    current_rate = soup.find_all('td', class_='responsive-hide mfm-text-left mfm-pl0')
    return [rate.text.strip() for rate in current_rate if rate.get('data-title') == "У касах банків"]


def clean_data(data) -> list:
    return data.strip()


def format_rate(rate) -> str or None:
    try:
        return f"{float(rate):.2f}"
    except ValueError:
        return None


def fetch_data(url: str) -> BeautifulSoup:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except requests.exceptions.RequestException:
        print("Помилка під час отримання даних")
        exit()


def main():
    soup = fetch_data(url)

    bank_names = get_bank_data(soup)
    bank_rates = get_rate_data(soup)

    paired = list(zip(bank_names, bank_rates))

    filtered_list = [pair for pair in paired if pair[1] and pair[1] != '0.000 ']
    cleaned_list = [(clean_data(bank), clean_data(rate)) for bank, rate in filtered_list]
    formatted_list = [(bank, format_rate(rate)) for bank, rate in cleaned_list if format_rate(rate)]
    sorted_list = sorted(formatted_list, key=lambda x: x[1])

    for top_bank in (sorted_list):
        print(top_bank)


if __name__ == '__main__':
    main()
