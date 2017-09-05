#!/usr/bin/env python3

import psycopg2


def main():
    # Connect to an existing database
    conn = psycopg2.connect("dbname=news")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Question 1
    query1 = """
      SELECT article_view.title, article_view.view
      FROM article_view
      ORDER BY article_view.view DESC
      LIMIT 3;
    """
    cur.execute(query1)
    print("Most popular articles:")
    for (title, view) in cur.fetchall():
        print("{} - {} views".format(title, view))
    print(" ")  # Display line break for legibility

    # Question 2
    query2 = """
    SELECT article_view.name, SUM(article_view.view) AS author_view
    FROM article_view
    GROUP BY article_view.name
    ORDER BY author_view DESC;
    """
    cur.execute(query2)
    print("Most popular authors:")
    for (name, view) in cur.fetchall():
        print("{} - {} views".format(name, view))
    print(" ")  # Display line break for legibility

    # Question 3
    query3 = """
    SELECT *
    FROM error_rate
    WHERE error_rate.percentage > 1
    ORDER BY error_rate.percentage DESC;
    """
    cur.execute(query3)
    print("Days with more than 1% errors:")
    for (date, percentage) in cur.fetchall():
        print("{} - {}% errors".format(date, percentage))
    print(" ")  # Display line break for legibility

    # Close communication with the database
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
