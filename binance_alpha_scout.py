import json
import requests

def get_alpha_tokens():
    url = "https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/cex/alpha/all/token/list"
    headers = {"User-Agent": "binance-alpha/1.0.0 (Skill)"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def scout_alpha():
    data = get_alpha_tokens()
    if not data.get("success") or not data.get("data"):
        return []
    
    tokens = data["data"]
    scouted = []
    
    for t in tokens:
        # Convert values to float for comparison
        try:
            change = float(t.get("percentChange24h", 0))
            volume = float(t.get("volume24h", 0))
            mcap = float(t.get("marketCap", 0))
            score = int(t.get("score", 0))
        except:
            continue
            
        # Filter: 24h gain > 2%, or high score, or high volume
        if change > 2 or score >= 50 or volume > 100000:
            scouted.append({
                "name": t.get("name"),
                "symbol": t.get("symbol"),
                "chain": t.get("chainName"),
                "price": t.get("price"),
                "change": change,
                "volume": volume,
                "mcap": mcap,
                "score": score,
                "listing": "Binance CEX" if t.get("listingCex") else "Alpha Trade",
                "alphaId": t.get("alphaId")
            })
            
    # Sort by score then by change
    scouted.sort(key=lambda x: (x['score'], x['change']), reverse=True)
    return scouted[:10] # Top 10

if __name__ == "__main__":
    results = scout_alpha()
    print(json.dumps(results))
