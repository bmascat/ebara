import sqlite3

class DatabaseManager:
    def __init__(self, db_name="rag_responses.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        """Crea la tabla en la base de datos SQLite si no existe."""
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
        """Guarda la consulta, respuesta y contexto en SQLite."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO responses (query, response, context) VALUES (?, ?, ?)",
                       (query, response, "\n".join(context)))
        self.conn.commit()