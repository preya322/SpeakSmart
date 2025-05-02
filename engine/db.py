import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# def remove_words(input_string, words_to_remove):
#     # Split the input string into words
#     words = input_string.split()

#     # Remove unwanted words
#     filtered_words = [word for word in words if word.lower() not in words_to_remove]

#     # Join the remaining words back into a string
#     result_string = ' '.join(filtered_words)
    # return result_string

# ASSISTANT_NAME = "jarvis"

def CreateTableSys():
    # Create a table sya_command
    query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
    cursor.execute(query)

def InsertSysCommand(name: str, path: str):
    query = f"INSERT INTO sys_command (name, path) VALUES (?, ?)"
    cursor.execute(query, (name, path))
    con.commit()

def CreateTableWeb():
    query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
    cursor.execute(query)

def InsertWebCommand(name: str, path: str):
    query = f"INSERT INTO web_command (name, path) VALUES (?, ?)"
    cursor.execute(query, (name, path))
    con.commit()

def update():
    cursor.execute("UPDATE sys_command SET name='powerpoint' WHERE name='power point'")
    con.commit()
    con.close()

def delete():
    cursor.execute("DROP TABLE telegram")
    con.commit()
    con.close()

def CreateTableTelegram():
    query = "CREATE TABLE IF NOT EXISTS telegram(id integer primary key, name VARCHAR(100), api_id integer, api_hash integer)"
    cursor.execute(query)

def InsertTelegramId(name, api, hash):
    query = f"INSERT INTO telegram (name, api_id, api_hash) VALUES (?, ?, ?)"
    cursor.execute(query, (name, api, hash))
    con.commit()

contacts = {
    "preya": [6764597107, -2372861768764682316],
    "nisarg": [1823014468, -3800926344296716025],
    "krish": [7285691291, -7487924970872153528],
    "kushal": [7133621138, 2946859940038011968], 
    "astha": [5042506181, -3614361498485050840],
    "dron": [8180894005, -3520734637596481458]
}

# def findContact(query):
#     query = query.lower()
#     words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
#     query = remove_words(query, words_to_remove)
#     query = query.strip().lower()
#     cursor.execute("SELECT api_id, api_hash FROM telegram WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#     results = cursor.fetchall()
#     print(results[0])
    


if __name__ == "__main__":
    InsertTelegramId("rajvi", 1139490002, 8148986698858288002)