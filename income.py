import json
import requests

API_BASE_URL = "https://api.ataix.kz"
API_KEY = "key"
ORDERS_FILE = "orders.json"


def load_orders():
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)
    print("Orders saved.")


def send_request(endpoint, method="GET"):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }

    try:
        response = requests.request(method, url, headers=headers)
        if response.ok:
            return response.json()
        else:
            print(f"API error {response.status_code}: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Connection error: {e}")
        return None


def update_and_calculate_profit():
    orders = load_orders()
    updated_orders = []
    total_profit = 0.0

    for order in orders:
        order_id = order.get("orderID")
        if not order_id:
            continue

        print(f"\nChecking order {order_id}...")

        response = send_request(f"/api/orders/{order_id}")
        if not response or "result" not in response:
            updated_orders.append(order)
            continue

        result = response["result"]
        status = result.get("status")

        if status == "filled":
            order["status"] = "filled"
            order["cumQuoteQuantity"] = float(result.get("cumQuoteQuantity", 0) or 0)
            order["cumCommission"] = float(result.get("cumCommission", 0) or 0)

            linked_id = order.get("linkedTo")
            buy_order = next((o for o in orders if o.get("orderID") == linked_id), None)

            if not buy_order:
                print(f"Buy order not found for sell order {order_id}. Skipping profit calc.")
                updated_orders.append(order)
                continue

            buy_sum = float(buy_order.get("cumQuoteQuantity", 0) or 0)
            buy_fee = float(buy_order.get("cumCommission", 0) or 0)
            sell_sum = order["cumQuoteQuantity"]
            sell_fee = order["cumCommission"]

            print(f"Buy sum: {buy_sum}, Buy fee: {buy_fee}")
            print(f"Sell sum: {sell_sum}, Sell fee: {sell_fee}")

            if buy_sum == 0:
                print(f"Zero buy sum for order {linked_id}, cannot calculate profit.")
                updated_orders.append(order)
                continue

            profit = sell_sum - sell_fee - buy_sum - buy_fee
            profit_percent = (profit / (buy_sum + buy_fee)) * 100 if (buy_sum + buy_fee) > 0 else 0

            order["netProfitUSDT"] = round(profit, 4)
            order["netProfitPercent"] = round(profit_percent, 2)

            total_profit += profit

            print(f"Order {order_id} profit: {profit:.4f} USDT ({profit_percent:.2f}%)")
        else:
            print(f"Order {order_id} is not filled (status = {status})")

        updated_orders.append(order)

    print(f"\nTotal net profit: {total_profit:.4f} USDT")
    save_orders(updated_orders)


if __name__ == "__main__":
    update_and_calculate_profit()
