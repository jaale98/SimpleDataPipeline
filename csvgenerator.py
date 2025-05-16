import os
import csv
import uuid
import random
from datetime import datetime, timedelta

OUTPUT_DIR = "output"
ROWS_PER_FILE = 1000

FIRST_NAMES = [
    "Alex", "Jamie", "Taylor", "Jordan", "Casey",
    "Morgan", "Riley", "Cameron", "Drew", "Robin"
]
LAST_NAMES = [
    "Smith", "Johnson", "Lee", "Brown", "Garcia",
    "Martinez", "Davis", "Rodriguez", "Lopez", "Wilson"
]
COUNTRIES = [
    "USA", "Canada", "UK", "Australia", "Germany",
    "France", "Japan", "Brazil", "India", "Mexico"
]
SUBSCRIPTION_TYPES = ["Free", "Basic", "Premium", "Enterprise"]
REFERRAL_SOURCES = ["Google", "Facebook", "Twitter", "Friend", "Other"]
EMAIL_DOMAINS = ["example.com", "mail.com", "test.org"]

def make_output_folder():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def next_available_filename(base_name):
    fname = f"{base_name}.csv"
    counter = 1
    while os.path.exists(os.path.join(OUTPUT_DIR, fname)):
        fname = f"{base_name}_{counter}.csv"
        counter += 1
    return fname

def random_date_within(days_back=365*5):
    return datetime.now() - timedelta(days=random.randint(0, days_back),
                                      seconds=random.randint(0, 86400))

def generate_row():
    signup = random_date_within()
    last_login = signup + timedelta(days=random.randint(0, (datetime.now() - signup).days),
                                    seconds=random.randint(0, 86400))
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return {
        "user_id": str(uuid.uuid4()),
        "first_name": first,
        "last_name": last,
        "email": f"{first.lower()}.{last.lower()}@{random.choice(EMAIL_DOMAINS)}",
        "signup_date": signup.strftime("%Y-%m-%d %H:%M:%S"),
        "last_login": last_login.strftime("%Y-%m-%d %H:%M:%S"),
        "age": random.randint(18, 80),
        "country": random.choice(COUNTRIES),
        "is_active": random.choice([True, False]),
        "account_balance": f"{random.uniform(0, 10000):.2f}",
        "num_logins": random.randint(1, 1000),
        "feedback_score": f"{random.uniform(1, 5):.1f}",
        "purchase_count": random.randint(0, 100),
        "subscription_type": random.choice(SUBSCRIPTION_TYPES),
        "referral_source": random.choice(REFERRAL_SOURCES),
    }

def main():
    make_output_folder()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"data_{ts}"
    filename = next_available_filename(base)
    path = os.path.join(OUTPUT_DIR, filename)
    
    columns = [
        "user_id", "first_name", "last_name", "email", "signup_date",
        "last_login", "age", "country", "is_active", "account_balance",
        "num_logins", "feedback_score", "purchase_count",
        "subscription_type", "referral_source"
    ]

    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for _ in range(ROWS_PER_FILE):
            writer.writerow(generate_row())

    print(f"Generated {ROWS_PER_FILE} rows → {path}")

if __name__ == "__main__":
    main()