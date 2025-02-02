from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

url = "https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22"

# Menghapus elemen yang duplikat
def remove_duplicate_items(arr):
    return list(set(arr))

# Mengambil daftar nama buah
def get_fruits(type_stock_element):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        fruit_names = []
        for element in soup.select(type_stock_element):
            fruit_name = element.find("big").find("b").find("a").get("title")
            fruit_names.append(fruit_name)

        return remove_duplicate_items(fruit_names)
    except Exception as e:
        print(f"Error: {e}")
        return []

# Mengambil harga buah
def get_price_fruits(type_stock_element):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        fruit_prices = []
        for element in soup.select(type_stock_element):
            price = element.find_all("span")[-1].text.strip()
            fruit_prices.append(price)

        return remove_duplicate_items(fruit_prices)
    except Exception as e:
        print(f"Error: {e}")
        return []

# Endpoint NormalStock
@app.route("/api/NormalStock", methods=["GET"])
def normal_stock():
    # Selector untuk elemen stock buah saat ini
    type_stock_element = "#mw-customcollapsible-current figure > figcaption > center"
    
    fruit_names = get_fruits(type_stock_element)
    fruit_prices = get_price_fruits(type_stock_element)

    fruits_json = []
    for i in range(len(fruit_names)):
        fruits_json.append({
            "name": fruit_names[i],
            "price": int(fruit_prices[i].replace(",", ""))  # Mengkonversi harga ke integer
        })

    return jsonify(fruits_json)  # Mengirimkan data dalam format JSON

if __name__ == "__main__":
    app.run(debug=True)
