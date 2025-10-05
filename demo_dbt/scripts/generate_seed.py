import csv
import random
from datetime import datetime, timedelta
import uuid
import os

os.makedirs("seeds", exist_ok=True)
OUT = "seeds/unterwerk_bills.csv"

random.seed(42)

unterwerks = [f"Unterwerk_{chr(65+i)}" for i in range(8)]  # A..H

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 10, 1)

def random_dates_for_month(year, month, prob_no_bills=0.2):
    if random.random() < prob_no_bills:
        return []
    n = random.choice([1, 1, 2, 3])  # اغلب 1 یا 2 تا قبض در ماه
    return sorted(
        {datetime(year, month, random.randint(1, 28)) for _ in range(n)}
    )

rows = []
cur = start_date
while cur <= end_date:
    year, month = cur.year, cur.month
    for u in unterwerks:
        for d in random_dates_for_month(year, month):
            rows.append({
                "unterwerk": u,
                "bill_date": d.strftime("%Y-%m-%d"),
                "bill_id": str(uuid.uuid4())[:8]
            })
    cur += timedelta(days=32)
    cur = cur.replace(day=1)

with open(OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["unterwerk", "bill_date", "bill_id"])
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ Generated {len(rows)} rows -> {OUT}")
