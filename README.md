# Site Log Analysis and Reporting Tool
The project is to build an internal reporting tool based on a news site log database with 1.6 million records. Design complex SQL query plans to analyze the data and provide business insights.

## Questions
1. **What are the most popular three articles of all time?** Which articles have been accessed the most?
  Present this information as a sorted list with the most popular article at the top.
2. **Who are the most popular article authors of all time?** That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.
3. **On which days did more than 1% of requests lead to errors?** The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.

You can open output_example.txt to see an example of the expected output after running Log_Analysis.py.

## Setup
### Software
Make sure the software listed beneath is installed on your computer.
[Python 3.6.x](https://www.python.org/downloads/)
[PostgreSQL 9.6.x](https://www.postgresql.org/download/)
### Virtual Machine
Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/)
### Test Data
Download and unzip [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).

## How to run
1. Place the Log_Analysis.py file within the same directory as the vm and sql file.
2. `vagrant up` command to run the vagrant on vm
3. `vagrant ssh` to login into vm
4. `cd` into the `vagrant` directory
5. Load the data onto the database `psql -d news -f newsdata.sql`
6. Connect to the database `psql -d news`
7. Create views
8. Use command `python Logs_Analysis.py` to run the program

## Create Views
```sql
CREATE VIEW author_article AS
SELECT authors.name, articles.title, article.slug
FROM authors, articles
WHERE articles.author = authors.id
ORDER BY authors.name;
```

```sql
CREATE VIEW path_view AS
SELECT path, COUNT(*) AS views
FROM log
GROUP BY path
ORDER BY views DESC;
```

```sql
CREATE VIEW article_view AS
SELECT author_article.name, author_article.title, path_view.views
FROM author_article, path_view
WHERE path_view.path = CONCAT('/article/', author_article.slug)
ORDER BY author_article.name;
```

```sql
CREATE VIEW total_request AS
SELECT date(time), COUNT(*) AS total
FROM log
GROUP BY date(time)
ORDER BY total DESC;
```

```sql
CREATE VIEW error_request AS
SELECT date(time), COUNT(*) AS errors
WHERE status!='200 OK'
GROUP BY date(time)
ORDER BY errors DESC;
```

```sql
CREATE VIEW error_rate AS
SELECT total_request.date, (100.0*error_request.errors/total_request.total) AS percentage
FROM total_request, error_request
WHERE total_request.date = error_request.date
ORDER BY total_request.date;
```