import psycopg2


DBNAME = "news"


def write_question(file_name, question):
    with open(file_name,"a+") as f:
        f.write(str(question))
        f.write("\n")

def write_results(file_name, results):
    with open(file_name, "a+") as f:
        for result_i in results: 
            row_info = result_i[0] + "    " +  str(result_i[1])
            f.write(row_info)
            f.write("\n")
        f.write("\n")

def get_results(query):
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


question_1 = "The most popular three articles of all time:"

query_1 = ("SELECT articles.title, " 
           "COUNT(*) AS new FROM articles " 
           "left JOIN log on concat('/article/',articles.slug) = log.path " 
           "GROUP BY articles.title " 
           "ORDER BY new DESC " 
           "LIMIT 3")


question_2 = "The most popular article authors of all time:"

query_2 = ("SELECT authors.name, "
            "COUNT(*) as views " 
            "FROM articles, authors, log "
            "WHERE  concat('/article/',articles.slug) = log.path " 
            "AND articles.author = authors.id "  
            "GROUP BY authors.name " 
            "ORDER BY views DESC")


question_3 = "Days where more than 1% of requests lead to errors:"

query_3 = ("WITH date_percentage " 
           "AS (WITH date_status AS (SELECT to_char(time,'DD-MON-YYYY') AS date, status FROM log) " 
           "SELECT date, sum(case when status = '404 NOT FOUND' then 1.0 else 0 end)/count(date)*100 AS percent " 
           "FROM date_status GROUP BY date) " 
           "SELECT * FROM date_percentage " 
           "WHERE percent > '1.0'")

   
answer_1 = get_results(query_1)
answer_2 = get_results(query_2)
answer_3 = get_results(query_3)

write_question("output.txt", question_1)
write_results("output.txt", answer_1)
write_question("output.txt", question_2)
write_results("output.txt", answer_2)
write_question("output.txt", question_3)
write_results("output.txt", answer_3)



