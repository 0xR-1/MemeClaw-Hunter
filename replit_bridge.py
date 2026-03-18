import json
import requests
from binance_hub_scout import generate_report

REPLIT_API_URL = "https://meme-claw-dashboard--0xr1.replit.app/api"

def main():
    report = generate_report()
    payloads = []

    # Process Alpha Picks
    for t in report.get("alpha_picks", []):
        payloads.append({
            "coinName": t.get("name", ""),
            "symbol": t.get("symbol", ""),
            "price": t.get("lastPrice", 0),
            "marketCap": t.get("marketCap", 0),
            "liquidity": t.get("liquidity", 0),
            "riskLevel": t.get("audit", {}).get("risk", "UNKNOWN")
        })

    # Process Meme Rush Migrations
    for t in report.get("meme_rush", []):
        payloads.append({
            "coinName": t.get("name", ""),
            "symbol": t.get("symbol", ""),
            "price": t.get("price", 0),
            "marketCap": t.get("marketCap", 0),
            "liquidity": t.get("liquidity", 0),
            "riskLevel": t.get("audit", {}).get("risk", "UNKNOWN")
        })

    # Send data to Replit
    if payloads:
        try:
            # Wrap in a root object if needed, or send as list
            response = requests.post(REPLIT_API_URL, json={"data": payloads}, timeout=15)
            print(f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending data to Replit: {e}")
    else:
        print("No tokens found to send.")

if __name__ == "__main__":
    main()
