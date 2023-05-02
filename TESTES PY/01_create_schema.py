import sqlite3

connection = sqlite3.connect("rui.db")

cursor = connection.cursor()
cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")

cursor.execute("""INSERT INTO fish (name, species, tank_number ) VALUES ('Sammy', 'shark', 1)""")
cursor.execute("""INSERT INTO fish (name, species, tank_number ) VALUES ('Le', 'hooker', 1)""")

connection.commit()

rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)

released_fish_name = "Sammy"
cursor.execute(
    "DELETE FROM fish WHERE name = ?",
    (released_fish_name,)
)

rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)


print(connection.total_changes)

connection.close()
