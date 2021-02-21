from django import template
from django.db import connection
import html
register = template.Library()

def fetch_data_query_manage(query):
    mycursor = connection.cursor()
    mycursor.execute(query)
    query_result = [ dict(line) for line in [zip([ column[0] for column in mycursor.description], row) for row in mycursor.fetchall()] ]
    return query_result

@register.filter(name='change_tag')
def change_tag(value):
    """Removes all values of arg from the given string"""
    value = html.unescape(value).replace('\n','')
    print(value)
    return value

@register.filter(name='fetch_region_data')
def fetch_region_data(value,arg):
    arg1 = str(arg).partition("&")[2]
    arg2 = str(arg).partition("&")[0]
    data = fetch_data_query_manage(f"SELECT {str(arg2)} FROM tbl_region WHERE {str(arg1)}='{str(value)}' GROUP BY {str(arg2)}")

    return data