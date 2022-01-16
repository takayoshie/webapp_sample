#!/usr/bin/python3
# -*- coding: UTF-8 -*-

def get_http_resp(url, param):
    import json, requests
    import xmltodict
    res = requests.get(url)
    return xmltodict.parse(res.text)

def get_data(field):
    import re
    if field is None:
        return ''
    p = re.compile(r"<[^>]*?>")
    return p.sub("", field).replace('\u3000', '').replace('\n', '')

def national_lib(keyword):
    url = "https://iss.ndl.go.jp/api/sru?operation=searchRetrieve&query=title=\"" + keyword + "\" AND mediatype=1 AND sortBy=\"issued_date/sort.descending\""
    param = {"title": "\"" + keyword +"\""}
    response = get_http_resp(url, param)
    books = []
    for record in response["searchRetrieveResponse"]["records"]["record"]:
        import xmltodict
        recordData = xmltodict.parse(record["recordData"])
        e = {}
        e["title"] = get_data(recordData["srw_dc:dc"]["dc:title"])
        books.append(e)
    return books

def doorkeeper(keywords):
    url = "https://api.doorkeeper.jp/events?"
    param = {"q": ','.join(keywords)}
    response = get_http_resp(url, param)
    events = []
    for event in response:
        e = {}
        e["url"] = get_data(event["event"]["public_url"])
        e["title"] = get_data(event["event"]["title"])
        e["start"] = get_data(event["event"]["starts_at"])
        e["address"] = get_data(event["event"]["address"])
        e["description"] = get_data(event["event"]["description"])
        events.append(e)
    return events

def print_header():
    print("<head>")
    print("<link rel=\"stylesheet\" href=\"https://cdn.datatables.net/t/bs-3.3.6/jqc-1.12.0,dt-1.10.11/datatables.min.css\"/>")
    print("<script src=\"https://cdn.datatables.net/t/bs-3.3.6/jqc-1.12.0,dt-1.10.11/datatables.min.js\"></script>")
    print("<script>")
    print("    jQuery(function($){$(\"#res-table\").DataTable();});")
    print("</script>")
    print("<title>Event search results</title>")
    print("</head>")

def save_db(ipaddr, pref, keyword):
    import sqlite3
    from contextlib import closing
    
    dbname = '../db/access.db'
    
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        create_table = '''create table if not exists access (id integer primary key, ipaddr varchar(16), pref varchar(50), keyword varchar(100), updated datetime)'''
        c.execute(create_table)
        sql = 'insert into access (ipaddr, pref, keyword, updated) values (?,?,?,?)'
        access = (ipaddr, ','.join(pref), ','.join(keyword), datetime.datetime.now())
        c.execute(sql, access)
        conn.commit()
        conn.close()

import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if ( os.environ['REQUEST_METHOD'] == "POST" ):
    import requests, urllib
    form = urllib.parse.parse_qs(sys.stdin.read())
    keywords = form['keyword'] if 'keyword' in form else []
    results = national_lib(keywords[0])
    import datetime
    print('Content-Type:text/html\n')
    print("<html lang=\"ja\">")
    print("<meta charset=\"utf-8\"/>")
    print_header()
    print("<body>")
    print("<table id=\"res-table\"  class=\"table table-bordered\">")
    print("<thead><tr><th>#</th><th>名称</th></tr></thead>")
    print("<tbody>")
    cnt = 0
    for result in results:
        cnt += 1
        print("<tr><td>%s</td><td>%s</td></tr>" % (cnt, result['title']))
    print("</tbody></table>")
    print("</body></html>") 
    save_db(os.environ['REMOTE_ADDR'], keywords)

