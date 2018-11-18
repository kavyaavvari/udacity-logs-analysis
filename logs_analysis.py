import psycopg2

print('The most popular three articles of all time:')

db = psycopg2.connect("dbname=news")
cursor = db.cursor()
cursor.execute("select articles.title, count(*) as new from articles left join log on concat('/article/',articles.slug) = log.path group by articles.title order by new desc limit 3")
results = cursor.fetchall()
print(results)
db.close()
