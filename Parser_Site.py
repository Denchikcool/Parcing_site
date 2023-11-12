import json
import time
import requests
import os
from bs4 import BeautifulSoup
def get_page():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"
    }

    r = requests.get(url="https://coinmarketcap.com/", headers=headers)

    if not os.path.exists("pages"):
        os.mkdir("pages")

    with open("pages/page_1.html", "w", encoding="utf-8") as file:
        file.write(r.text)

    with open("pages/page_1.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    pages_count = int(soup.find("div", class_="sc-fd786ab3-0 bXSmUJ").find_all("a")[-2].text)
    for i in range(1, pages_count + 1):
        if i > 2:
            return i
        else:
            url = f"https://coinmarketcap.com/?page={i}"
            r = requests.get(url=url, headers=headers)

            with open(f"pages/page_{i}.html", "w", encoding="utf-8") as file:
                file.write(r.text)

            time.sleep(2)

def collect_data(pages_count):
    final_info = []
    parser_crip_data = []
    for page in range(1, pages_count):
        with open(f"pages/page_{page}.html", encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        table_crip = soup.select("tbody")

        for crip in table_crip:
            crip = crip.find_all("tr")
            for j in crip:
                try:
                    number = j.find("p", class_="sc-4984dd93-0 ihZPK").text
                    name = j.find("p", class_="sc-4984dd93-0 kKpPOn").text
                    symbol = j.find("p", class_="sc-4984dd93-0 iqdbQL coin-item-symbol").text
                    price = j.find("div", class_="sc-cadad039-0 clgqXO").find("span").text
                    market_cap = j.find("span", class_="sc-edc9a476-1 gqomIJ").text
                except Exception:
                    break
                parser_crip_data.append(
                    {
                        "Номер": number,
                        "Название криптовалюты": name,
                        "Символ криптовалюты": symbol,
                        "Цена": price,
                        "Рыночная капитализация": market_cap
                    }
                )
    final_info.append(parser_crip_data)
    with open("pages/tables_of_cryptocurrencies.json", "w", encoding="utf-8") as file:
        json.dump(final_info, file, indent=4, ensure_ascii=False)
    print("Pasing is done")

    return final_info

def find_crip(data_base, finding_crip):
    cryps = []
    for crip in data_base:
        for crypta in crip:
            if crypta["Название криптовалюты"].upper() == finding_crip.upper():
                cryps.append(crypta)
                return cryps

def main():
    data_base = []
    data_founded_crip = []
    pages_count = get_page()
    data_base = collect_data(pages_count=pages_count)

    data_founded_crip = find_crip(data_base, input("Enter the name of Cryptocurrency: "))
    if data_founded_crip:
        with open("pages/table_of_founded.json", "w", encoding="utf-8") as file:
            json.dump(data_founded_crip, file, indent=4, ensure_ascii=False)
    else:
        with open("pages/table_of_founded.json", "w", encoding="utf-8") as file:
            json.dump("Такая криптовалюта не найдена!", file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()