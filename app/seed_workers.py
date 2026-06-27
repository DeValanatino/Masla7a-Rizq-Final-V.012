import os
import uuid
from datetime import date, datetime, timedelta
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

def main():
    if not DATABASE_URL:
        print("[-] Error: DATABASE_URL environment variable is not set in the .env file.")
        print("Please add DATABASE_URL=\"your_postgres_connection_string\" to your .env file and try again.")
        print("\nAlternatively, you can run the script by passing the connection string manually:")
        db_url = input("Enter Postgres connection URL (or press Enter to exit): ").strip()
        if not db_url:
            return
        conn_string = db_url
    else:
        conn_string = DATABASE_URL

    print(f"[*] Connecting to database...")
    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cur = conn.cursor()
        print("[+] Connected successfully!")
        
        # Ensure users table exists
        print("[*] Ensuring 'users' table exists...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(255) PRIMARY KEY,
            phone_number VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            account_type VARCHAR(50) NOT NULL,
            subscription_expiry_date DATE NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_table_query)
        print("[+] 'users' table is ready.")

        # Dummy workers data (account_type = Craftsman)
        # Egyptian phone numbers: exactly 11 digits
        workers = [
            {
                "id": str(uuid.uuid4()),
                "phone_number": "01012345678",
                "name": "Ahmed Al-Herfi",
                "account_type": "Craftsman",
                "subscription_expiry_date": date.today() + timedelta(days=30),
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "phone_number": "01122334455",
                "name": "Mustafa Al-Sayegh",
                "account_type": "Craftsman",
                "subscription_expiry_date": date.today() + timedelta(days=30),
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "phone_number": "01234567890",
                "name": "Mohamed Al-Najar",
                "account_type": "Craftsman",
                "subscription_expiry_date": date.today() + timedelta(days=30),
                "created_at": datetime.utcnow()
            }
        ]

        print("[*] Seeding dummy workers...")
        inserted_count = 0
        for worker in workers:
            try:
                insert_query = """
                INSERT INTO users (id, phone_number, name, account_type, subscription_expiry_date, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (phone_number) DO UPDATE 
                SET name = EXCLUDED.name, account_type = EXCLUDED.account_type, 
                    subscription_expiry_date = EXCLUDED.subscription_expiry_date;
                """
                cur.execute(insert_query, (
                    worker["id"],
                    worker["phone_number"],
                    worker["name"],
                    worker["account_type"],
                    worker["subscription_expiry_date"],
                    worker["created_at"]
                ))
                print(f"[+] Seeded worker: {worker['name']} ({worker['phone_number']})")
                inserted_count += 1
            except Exception as e:
                print(f"[-] Failed to seed worker {worker['name']}: {e}")

        print(f"[+] Seeding complete! {inserted_count} workers seeded/updated.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"[-] Database error: {e}")

if __name__ == "__main__":
    main()
