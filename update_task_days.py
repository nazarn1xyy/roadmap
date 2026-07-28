#!/usr/bin/env python3
import urllib.request
import json
from datetime import datetime, timedelta

SUPABASE_URL = "https://iiksxgmckztwptwcftok.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlpa3N4Z21ja3p0d3B0d2NmdG9rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ1NDA2MDksImV4cCI6MjEwMDExNjYwOX0.hzh4npHyquBhnrsKmraiJYESmzQ_Xb1m0iARQGmNwDQ"

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

def format_day(date_obj):
    days_ua = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    return f"{days_ua[date_obj.weekday()]}, {date_obj.strftime('%d.%m')}"

def main():
    print("Fetching current state from Supabase...")
    state = get_current_state()
    
    if "frontend" not in state:
        print("No frontend data found.")
        return

    # Base dates for each week (Year 2026 for July/August)
    # 20.07.2026 is Monday
    week_starts = {
        1: datetime(2026, 7, 20),
        2: datetime(2026, 7, 27),
        3: datetime(2026, 8, 3),
        4: datetime(2026, 8, 10),
        5: datetime(2026, 8, 17)
    }

    for week in state["frontend"]:
        w_id = week.get("week")
        if w_id in week_starts:
            current_date = week_starts[w_id]
            for task in week.get("tasks", []):
                new_day_str = format_day(current_date)
                
                # Replace the old day string at the beginning of the text
                # We simply update task["day"]
                task["day"] = new_day_str
                
                # Increment by 1 day
                current_date += timedelta(days=1)
                
    update_state(state)
    print("Done! Task days updated in Supabase.")

if __name__ == "__main__":
    main()
