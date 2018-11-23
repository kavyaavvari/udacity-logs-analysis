import psycopg2

DBNAME = "news"

def write_text(file_name, text):
    with open(file_name,"a+") as f:
        f.write(str(text))



question_1 = "The most popular three articles of all time:"

query_1 = ("SELECT articles.title" 
           "COUNT(*) AS new FROM articles" 
           "left JOIN log on concat('/article/',articles.slug) = log.path group" 
           "BY articles.title" 
           "ORDER BY new DESC" 
           "LIMIT 3")


question_2 = "The most popular article authors of all time:"

quergy_2 = ("SELECT authors.name"
            "COUNT(*) as views" 
            "FROM articles, authors, log"
            "WHERE  concat('/article/',articles.slug) = log.path" 
            "AND articles.author = authors.id"  
            "GROUP BY authors.name" 
            "ORDER BY views DESC")


question_3 = "Days where more than 1% of requests lead to errors:"

query_3 = ("WITH date_percentage" 
           "AS (WITH date_status AS (SELECT to_char(time,'DD-MON-YYYY') AS date, status FROM log)" 
           "SELECT date, sum(case when status = '404 NOT FOUND' then 1.0 else 0 end)/count(date)*100 AS percent" 
           "FROM date_status GROUP BY date)" 
           "SELECT * FROM date_percentage" 
           "WHERE percent > '1.0'")

def get_results(query):
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()

write_text("output.txt", results)
