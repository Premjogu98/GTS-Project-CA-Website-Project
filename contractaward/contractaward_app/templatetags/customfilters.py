from django import template
from django.db import connection
import html
import base64 # Need To install Requre.txt
import re # Need To install Requre.txt
register = template.Library()

def fetch_data_query_manage(query):
    mycursor = connection.cursor()
    mycursor.execute(query)
    query_result = [ dict(line) for line in [zip([ column[0] for column in mycursor.description], row) for row in mycursor.fetchall()] ]
    return query_result

@register.filter(name='change_tag')
def change_tag(value):
    """Removes all values of arg from the given string"""
    value = html.unescape(value).replace('\n','').replace('&lt;br&gt;','<br>').replace('<BR>','<br>')
    print(value)
    return value

@register.filter(name='fetch_region_data')
def fetch_region_data(value,arg):
    if value == "region":
        data = fetch_data_query_manage(f"SELECT region_name FROM `tbl_region` GROUP BY region_name")
    else:
        arg1 = str(arg).partition("&")[2]
        arg2 = str(arg).partition("&")[0]
        data = fetch_data_query_manage(f"SELECT {str(arg2)} FROM tbl_region WHERE {str(arg1)}='{str(value)}' GROUP BY {str(arg2)}")
    # print(data)
    return data
@register.filter(name='custom_url')
def custom_url(value,arg):
    title = value.lower()
    stop_words = ['a', 'an', 'as', 'at', 'before', 'but', 'by', 'for', 'from', 'is', 'in', 'into','like', 'of', 'off', 'on', 'onto', 'per', 'since', 'than', 'the', 'this', 'that', 'to', 'up','via', 'with']
    title_list = str(title).lower().split()
    main_title_list = []
    [main_title_list.append(i) for i in title_list if i not in stop_words]
    main_title = " ".join(main_title_list) # list to string 
    clean_title = main_title[0:100].replace("<br/>","").replace("<br>","")
    title_replace_multispace = re.sub('\s+', ' ', str(clean_title)) # remove multiple spaces
    clean_title = re.sub('[^A-Za-z0-9 -]+', '', title_replace_multispace).replace(' ','-').strip()
    message_bytes = str(arg).encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_id = base64_bytes.decode('ascii')
    main_url = f"{str(clean_title.replace('---','-').replace('----','-').replace('--','-'))}-{str(base64_id)}"
    return main_url

@register.filter(name='regions_url_pattern')
def regions_url_pattern(value):
    custom_region = str(value).lower().strip().replace(' ','-')
    return custom_region