from requests_html import HTMLSession
import time
import csv
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def create_table():
    
    commands = (
        """
        CREATE TABLE data (
        market TEXT, products TEXT,launch_stage TEXT,activity_level TEXT, activity_verified TEXT, pageviews TEXT, team_member TEXT, 
                founded_by TEXT,revenue_stage TEXT,revenue_through TEXT,twitter_followers TEXT, percentile TEXT, amount_raised TEXT,  company_website TEXT,
                description TEXT, name TEXT, founded TEXT, place TEXT, crunchbase_link TEXT, ranking TEXT
                )
        """,)
    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        print("successful")
    except:
        pass    

def scrapper():
    urls = [f"https://startuptracker.io/discover?filters%5B0%5D%5Bcc%5D%5Bq%5D=US&page={number}" for number in range(16)]
    for url in urls:
        session = HTMLSession()
        r = session.get(url)
        startups = r.html.xpath('//*[@class="_8vwxjw"]//a/@href')
        startups = [f"https://startuptracker.io{start}" for start in startups]
        session.close()
        for startup in startups:
            try:
                session = HTMLSession()
                r = session.get(startup)
                r.html.render(500)
                description = r.html.xpath('//*[@class="_qgzmqh"]/text()')
                description = str(description)
                description = description[1:-1]
                website = r.html.xpath('//*[@class="_e4x16a"]/a/@href')
                company_website = website[0]
                crunchbase_link = website[1]
                name = r.html.xpath('//*[@class="_1vj0t0j"]/text()')
                name = str(name)
                name = name[1:-1]
                print(name)
                activity = r.html.xpath('//*[@class="_1vmw3q2"]/text()')
                activity_level = activity[-3]
                activity_verified = str(activity[-1])
                first = r.html.xpath('//*[@class="_mm5zvh"]/text()')
                second =  r.html.xpath('//*[@class="_1jivuxq"]/text()')
                market = r.html.xpath('//*[@class="_16gr0n0l"]/text()')
                market = str(market)
                market = market[1:-1]
                products = r.html.xpath('//*[@class="_c4ithgh"]/text()')
                products = str(products)
                products = products[1:-1]
                revenue_through =  r.html.xpath('//*[@class="_11tz2hsj"]/text()')
                revenue_through = str(revenue_through)
                revenue_through = revenue_through[1:-1]            
                founded_by = r.html.xpath('//*[@class="_1gebkr1"]/text()')
                founded_by = str(founded_by)
                founded_by = founded_by[1:-1]
                founded  = str(f"{second[0]} {first[0]}")
                place =  f"{second[1]} {first[1]}"
                team_member = str(first[2])
                launch_stage = first[3]
                revenue_stage = first[4]
                amount_raised = first[5]
                twitter_followers = first[6]
                percentile = first[-1]
                if len(second[-2]) > 5:
                    pageviews = first[-2]
                else:
                    pageviews = 0 
                if second[-3] == 'global rank':
                    ranking = first[-3]
                else:
                    ranking= 0
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                cursor = conn.cursor()
                sql_insert_query = """ INSERT INTO data (market, products, launch_stage, activity_level, activity_verified, pageviews, team_member, founded_by, revenue_stage, revenue_through, twitter_followers, percentile, amount_raised, company_website, description, name, founded, place, crunchbase_link, ranking) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
                record_to_insert = (market, products, launch_stage, activity_level, activity_verified, pageviews, team_member, founded_by,revenue_stage,revenue_through,twitter_followers, percentile, amount_raised,  company_website, description, name, founded, place, crunchbase_link, ranking)
                cursor.execute(sql_insert_query, record_to_insert)            
                conn.commit()
                session.close()
                time.sleep(30)
            except:
                pass 



if __name__ == "__main__":
    print('started working')
    create_table()
    scrapper()
