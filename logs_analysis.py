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


print('Days with more than 1% of requests leading to errors:')

cursor = db.cursor()
cursor.execute("with date_percentage as (with date_status as (select to_char(time,'DD-MON-YYYY') as date, status from log) select date, sum(case when status = '404 NOT FOUND' then 1.0 else 0 end)/count(date)*100 as percent from date_status group by date) select * from date_percentage where percent > '1.0'")
results = cursor.fetchall()
print(results)

db.close()
