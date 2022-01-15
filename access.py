#!/usr/bin/python3
# -*- coding: UTF-8 -*-

def print_header():
    print("<head>")
    print("<meta charset="utf-8"/>")
    print("<link rel=\"stylesheet\" href=\"https://cdn.datatables.net/t/bs-3.3.6/jqc-1.12.0,dt-1.10.11/datatables.min.css\"/>")
    print("<script src=\"https://cdn.datatables.net/t/bs-3.3.6/jqc-1.12.0,dt-1.10.11/datatables.min.js\"></script>")
    print("<script>")
    print("    jQuery(function($){$(\"#res-table\").DataTable();});")
    print("</script>")
    print("<title>Event search results</title>")
    print("</head>")

def select_db():
    import sqlite3
    from contextlib import closing
    
    dbname = '../db/access.db'

    rows = []
    
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = 'select * from access'
        for row in c.execute(select_sql):
            rows.append(row)
        conn.close()
    return rows

import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

rows = select_db()

print('Content-Type:text/html\n')
print("<html lang=\"ja\">")
print_header()
print("<body>")
print("<table id=\"res-table\"  class=\"table table-bordered\">")
print("<thead><tr><th>#</th><th>Timestamp</th><th>指定地域</th><th>キーワード</th><th>IP Address</th></tr></thead>")
print("<tbody>")
cnt = 0
for row in rows:
    cnt += 1
    print("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (cnt, row[4][:19], row[2], row[3], row[1]))
print("</tbody></table>")
print("</body></html>") 
