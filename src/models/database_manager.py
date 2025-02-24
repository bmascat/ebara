import sqlite3

class DatabaseManager:
    def __init__(self, db_name="rag_responses.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        """Creates the table in the SQLite database if it does not exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            response TEXT,
            context TEXT
        )
        """)
        self.conn.commit()
    
    def save_to_db(self, query: str, response: str, context: list):
        """Saves the query, response and context in SQLite."""
        # Convert each dictionary in context to a string
        context_str = "\n".join([f"Title: {item['title']}, Abstract: {item['abstract']}" for item in context])
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO responses (query, response, context) VALUES (?, ?, ?)",
                       (query, response, context_str))
        self.conn.commit()