#!/usr/bin/env python3
import urllib.request
import json

SUPABASE_URL = "https://iiksxgmckztwptwcftok.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlpa3N4Z21ja3p0d3B0d2NmdG9rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ1NDA2MDksImV4cCI6MjEwMDExNjYwOX0.hzh4npHyquBhnrsKmraiJYESmzQ_Xb1m0iARQGmNwDQ"

ORIGINAL_DATES = {
    1: "20 лип. — 26 лип.",
    2: "27 лип. — 02 серп.",
    3: "03 серп. — 09 серп.",
    4: "10 серп. — 16 серп.",
    5: "17 серп. — 25 серп.",
}

def get_current_state():
    url = f"{SUPABASE_URL}/rest/v1/tasks_state?id=eq.1&select=state"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    })
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    return data[0]["state"] if data else {}

def update_state(state):
    body = json.dumps({"state": state}).encode("utf-8")
    url = f"{SUPABASE_URL}/rest/v1/tasks_state?id=eq.1"
    req = urllib.request.Request(
        url, data=body, method="PATCH",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }
    )
    with urllib.request.urlopen(req) as resp:
        print(f"HTTP {resp.status} — Updated!")

def main():
    print("Fetching current state from Supabase...")
    state = get_current_state()
    
    if "frontend" in state:
        print("Reverting frontend dates...")
        for week in state["frontend"]:
            week_num = week.get("week")
            if week_num in ORIGINAL_DATES:
                week["dates"] = ORIGINAL_DATES[week_num]
                
    if "backend" in state:
        print("Reverting backend dates...")
        for week in state["backend"]:
            week_num = week.get("week")
            if week_num in ORIGINAL_DATES:
                week["dates"] = ORIGINAL_DATES[week_num]
                
    update_state(state)
    print("Done! Dates reverted in Supabase without modifying tasks.")

if __name__ == "__main__":
    main()
