from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///enterprise.db")

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                product TEXT,
                region TEXT,
                amount INTEGER,
                customer_id INTEGER
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                city TEXT
            )
        """))
        result = conn.execute(text("SELECT COUNT(*) FROM sales")).fetchone()
        if result[0] == 0:
            conn.execute(text("""
                INSERT INTO customers VALUES
                (1,'Amit','Pune'),
                (2,'Neha','Mumbai'),
                (3,'Raj','Delhi')
            """))
            conn.execute(text("""
                INSERT INTO sales VALUES
                (1,'Laptop','Maharashtra',50000,1),
                (2,'Phone','Maharashtra',30000,2),
                (3,'Tablet','Delhi',20000,3)
            """))
        conn.commit()