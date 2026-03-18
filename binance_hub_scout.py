import json
import requests
import uuid

USER_AGENT_WEB3 = "binance-web3/1.4 (Skill)"
USER_AGENT_ALPHA = "binance-alpha/1.0.0 (Skill)"

def get_binance_alpha():
    """Uses the 'alpha' skill logic."""
    url = "https://www.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/cex/alpha/all/token/list"
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT_ALPHA}, timeout=10).json()
        if resp.get("success"):
            # Filter for high score Alpha tokens
            return [t for t in resp["data"] if int(t.get("score", 0)) >= 50][:3]
    except: pass
    return []

def get_meme_rush_migrated():
    """Uses the 'meme-rush' skill logic for Migrated tokens."""
    url = "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list"
    data = {"chainId": "56", "rankType": 30, "limit": 5} # BSC Migrated
    try:
        resp = requests.post(url, headers={"User-Agent": "binance-web3/1.0 (Skill)"}, json=data, timeout=10).json()
        return resp.get("data", [])[:3]
    except: pass
    return []

def get_trending_hype():
    """Uses 'crypto-market-rank' logic for Social Hype."""
    url = "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/social/hype/rank/leaderboard?chainId=56&sentiment=Positive&socialLanguage=ALL&targetLanguage=en&timeRange=1"
    try:
        resp = requests.get(url, headers={"User-Agent": "binance-web3/2.0 (Skill)"}, timeout=10).json()
        return resp.get("data", {}).get("leaderBoardList", [])[:3]
    except: pass
    return []

def audit_token(chain_id, contract_address):
    """Uses the 'query-token-audit' skill logic."""
    url = "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/security/token/audit"
    data = {
        "binanceChainId": chain_id,
        "contractAddress": contract_address,
        "requestId": str(uuid.uuid4())
    }
    try:
        resp = requests.post(url, headers={"User-Agent": "binance-web3/1.4 (Skill)"}, json=data, timeout=10).json()
        if resp.get("success") and resp.get("data"):
            return {
                "risk": resp["data"].get("riskLevelEnum") or "LOW",
                "score": resp["data"].get("riskLevel") if resp["data"].get("riskLevel") is not None else 0,
                "verified": resp["data"].get("extraInfo", {}).get("isVerified", False)
            }
    except: pass
    return {"risk": "UNKNOWN", "score": "N/A", "verified": False}

def generate_report():
    alpha = get_binance_alpha()
    meme = get_meme_rush_migrated()
    hype = get_trending_hype()
    
    # Audit found tokens
    for t in alpha:
        t["audit"] = audit_token(t["chainId"], t["contractAddress"])
    for t in meme:
        t["audit"] = audit_token(t["chainId"], t["contractAddress"])
        
    report = {
        "alpha_picks": alpha,
        "meme_rush": meme,
        "social_hype": hype
    }
    return report

if __name__ == "__main__":
    print(json.dumps(generate_report()))
