import psycopg2

print('The most popular three articles of all time:')

db = psycopg2.connect("dbname=news")
cursor = db.cursor()
cursor.execute("select articles.title, count(*) as new from articles left join log on concat('/article/',articles.slug) = log.path group by articles.title order by new desc limit 3")
results = cursor.fetchall()
print(results)
db.close()


print('The most popular article authors of all time:')

cursor = db.cursor()
cursor.execute("select authors.name, count(*) as views from articles, authors, log where  concat('/article/',articles.slug) = log.path and articles.author = authors.id  group by authors.name order by views desc")
results = cursor.fetchall()
print(results)

db.close()
