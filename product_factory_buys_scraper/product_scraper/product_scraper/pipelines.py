# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ProductScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

        # Convert new price to float
        new_price = adapter.get('price_now')
        new_price = new_price.replace('$', '').replace(',','')
        adapter['price_now'] = float(new_price)

        # Proccess old price and convert to float
        old_price = adapter.get('price_old')
        if old_price:
            old_price_list = old_price.split()
            price = old_price_list[1]
            price = price.replace('$', '')
            price_list = price.split(")")
            price_final = price_list[0].replace(",", "")
            adapter['price_old'] = float(price_final)



        return item

import mysql.connector

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'C0st1n2203',
            database = 'factory_buys_products'
        )

        #create cursor, used to execute commands
        self.cur = self.conn.cursor()

        #create products table if not exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id int NOT NULL auto_increment,
            name VARCHAR(255),
            url VARCHAR(255),
            collection VARCHAR(255),
            price_now DECIMAL(10,2),
            price_old DECIMAL(10,2),
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        # Define insert statement
        self.cur.execute("""
        insert into products(
            name,
            url,
            collection,
            price_now,
            price_old
        ) values (
            %s,%s,%s,%s,%s
        )""", (
            item["name"],
            item["url"],
            item["collection"],
            item["price_now"],
            item["price_old"]
        ))

        #Execute insert of data into database
        self.conn.commit()
        return item

    def cloase_spider(self, spider):
        #close cursor and connection to database
        self.cur.close()
        self.conn.close()
