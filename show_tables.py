# show_tables.py
import os
import django
from django.db import connection

# Set up Django environment (adjust the path to your own settings module)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')  # ← Change this to match your settings path
django.setup()

def show_tables_and_columns():
    """Display all database tables and their columns."""
    print("🔍 Database Tables and Columns:\n")

    with connection.cursor() as cursor:
        # Retrieve all table names
        tables = connection.introspection.table_names()

        for table in tables:
            print(f"🟢 Table: {table}")
            try:
                # Get detailed column information for each table
                columns = connection.introspection.get_table_description(cursor, table)
                for col in columns:
                    print(f"   - {col.name} ({col.type_code})")
            except Exception as e:
                print(f"   ⚠️  Failed to read columns: {e}")
            print()  # Blank line for spacing

if __name__ == "__main__":
    show_tables_and_columns()
