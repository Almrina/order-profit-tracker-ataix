# sell-order-profit-checker

A Python script that reads sell orders from a JSON file, checks their status via the ATAIX exchange API, and calculates net profit in USDT for filled orders. It also updates the order file accordingly.

## Features

- Loads sell orders from a local JSON file  
- Verifies order status using ATAIX API (`/api/orders/{orderID}`)  
- Calculates net profit for filled orders based on:
  - `cumQuoteQuantity` (total value)
  - `cumCommission` (exchange commission)  
- Matches each sell order with its corresponding buy order using `linkedTo` field  
- Updates order status and prints profit results to console  

## Requirements

- Python 3.7+
- `requests` library


## The script will:

- Check each order's status via API;
- For filled sell orders, find the related buy order;
- Calculate and print the net profit;
- Update the orders.json with the latest status.

## Example Output

```
- Checking order TRX-USDT-532395-1744268137866...
Found linked buy order: TRX-USDT-532392-1744268137122
Buy total: 1.0000 USDT, Sell total: 1.0200 USDT
Buy commission: 0.0006 USDT, Sell commission: 0.0006 USDT
Net profit: 0.0188 USDT (1.88%)

Total net profit: 0.0188 USDT
Orders saved.
```
