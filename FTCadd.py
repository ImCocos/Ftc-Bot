import sqlite3

con = sqlite3.connect('users.db')
cur = con.cursor()
ImCocosKingId = 2021855860
value = int(input("How many do you want to add/delete: "))

cur_balance = cur.execute(f'SELECT balance FROM users WHERE id = "{ImCocosKingId}"').fetchone()[0]

cur.execute(f'UPDATE users SET balance = "{cur_balance + value}" WHERE id = "{ImCocosKingId}"')
con.commit()