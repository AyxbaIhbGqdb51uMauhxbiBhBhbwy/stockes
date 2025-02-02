from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

url = "https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22"

def remove_duplicate_items(arr):
    return list(set(arr))

def get_fruits(type_stock_element):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        fruit_names = []
        for element in soup.select(type_stock_element):
            fruit_name = element.find("big").find("b").find("a").get("title")
            if fruit_name:  # Check if fruit_name is not None
                fruit_names.append(fruit_name)

        print("Fruit names fetched:", fruit_names)  # Debugging output
        return remove_duplicate_items(fruit_names)
    except Exception as e:
        print(f"Error in get_fruits: {e}")
        return []

def get_price_fruits(type_stock_element):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        fruit_prices = []
        for element in soup.select(type_stock_element):
            price = element.find_all("span")[-1].text.strip()
            if price:  # Check if price is not empty
                fruit_prices.append(price)

        print("Fruit prices fetched:", fruit_prices)  # Debugging output
        return remove_duplicate_items(fruit_prices)
    except Exception as e:
        print(f"Error in get_price_fruits: {e}")
        return []

@app.route("/api/NormalStock", methods=["GET"])
def normal_stock():
    type_stock_element = "#mw-customcollapsible-current figure > figcaption > center"
    fruit_names = get_fruits(type_stock_element)
    fruit_prices = get_price_fruits(type_stock_element)

    fruits_json = []
    for i in range(len(fruit_names)):
        if i < len(fruit_prices):  # Make sure there are enough prices for each fruit
            fruits_json.append({
                "name": fruit_names[i],
                "price": int(fruit_prices[i].replace(",", ""))
            })

    print("Fruits JSON:", fruits_json)  # Debugging output

    return jsonify(fruits_json)

if __name__ == "__main__":
    app.run(debug=True)
