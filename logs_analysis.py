import psycopg2

print('The most popular three articles of all time:')

db = psycopg2.connect("dbname=news")
cursor = db.cursor()
cursor.execute("SELECT articles.title, count(*) AS new FROM articles left JOIN log on concat('/article/',articles.slug) = log.path GROUP BY articles.title ORDER BY new DESC limit 3")
results = cursor.fetchall()
print(results)
db.close()


print('The most popular article authors of all time:')

cursor = db.cursor()
cursor.execute("SELECT authors.name, count(*) AS views FROM articles, authors, log WHERE  concat('/article/',articles.slug) = log.path AND articles.author = authors.id  GROUP BY authors.name ORDER BY views DESC")
results = cursor.fetchall()
print(results)


print('Days with more than 1% of requests leading to errors:')

cursor = db.cursor()
cursor.execute("WITH date_percentage AS (WITH date_status AS (SELECT to_char(time,'DD-MON-YYYY') AS date, status FROM log) SELECT date, sum(case when status = '404 NOT FOUND' then 1.0 else 0 end)/count(date)*100 AS percent FROM date_status GROUP BY date) SELECT * FROM date_percentage WHERE percent > '1.0'")
results = cursor.fetchall()
print(results)

db.close()
