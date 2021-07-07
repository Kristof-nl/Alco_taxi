import sqlite3
import os.path

#Add products to datebase
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "alco_taxi.db")


products = [(1, "Bear in can", 1.20, "A89456RT678P", "/static/beer_can.png"),(2, "Beer in bootle", 1.35, "W89356XW378Z","/static/beer_bottle.png"),
            (3, "Beer case", 15.00, "I12353PL378V", "/static/beer_case.png"),(4, "Red wine", 7.35, "Q89322AW318K", "/static/red_wine.png"),
            (5, "White wine", 6.90, "WW9351XX318Y", "/static/white_wine.png"), (6, "Rose wine", 7.75, "B894356XW374E", "/static/rose_wine.png"),
            (7, "Vodka", 17.95, "Z89316XW171O", "/static/vodka.png"), (8, "Gin", 22.40, "X81326MW318F", "/static/gin.png"), 
            (9, "Whisky", 31.25, "J89251XW171R", "/static/whisky2.png")]

def add_products(products_list):
    conn = sqlite3.connect(db_path)
    sql_statement = 'INSERT INTO product VALUES (?, ?, ?, ?, ?)'
    cur = conn.cursor()
    cur.executemany(sql_statement, products_list)
    conn.commit()
    conn.close()



add_products(products)