from django.shortcuts import render
from django.http import HttpResponse
import random # Need To install Requre.txt
from django.db import connection
import pymysql.cursors # Need To install Requre.txt
from datetime import datetime as datetime_obj
from django.http import HttpRequest
import requests # Need To install Requre.txt
import json # Need To install Requre.txt
import os
from django.core.paginator import Paginator
import re # Need To install Requre.txt
import base64 # Need To install Requre.txt

def find_ip_address():
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()

    data = response.json()
    main_ip = data['ip']
    return main_ip
    # print(data['ip'])

def create_random_number():
    cap_number = random.randrange(11210,98990) # generate random Number For Captcha
    cap_str_number = cap_number
    return cap_str_number

def genrate_proper_string(a_sentence_or_word):
    a_sentence_or_word = a_sentence_or_word.replace("&#39;", "'").replace("&#34;", '"').replace("&#nl;", '\n').replace("&#rl;", '\r').replace("&#nl", '\n').replace("&#rl", '\r')
    return a_sentence_or_word
    
def insert_data_query_manage(query):
    try:
        mycursor = connection.cursor()
        mycursor.execute(query)
        connection.commit()
        return 'Done'
    except Exception as e:
        print(f"Error On insert_data_query_manage Function: {str(e)}")
        time.sleep(2)
        return 'Error'

def fetch_data_query_manage(query):
    mycursor = connection.cursor()
    mycursor.execute(query)
    fetch_data = mycursor.fetchall()
    return fetch_data

def home(request):
    return render(request, 'htmltemp/index.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['loginemail']
        password = request.POST['loginpass']
        print('Username: ',username)
        print('Password: ',password)
        user_data_found_or_not = fetch_data_query_manage(f"SELECT * FROM tbl_user WHERE email_id ='{str(username)}' AND user_password='{str(password)}'")
        if len(user_data_found_or_not) == 1:
            return HttpResponse("done")
        else:
            return HttpResponse("username or password invalid")
        
    return render(request, 'htmltemp/login_page.html')

def register_page(request):
    cap_str_number = create_random_number()
    fetch_country = fetch_data_query_manage("SELECT Country_Short_Code, Country_Name FROM tbl_region WHERE Country_Short_Code !='' ORDER BY Country_Name ASC")
    if request.method == 'POST':
        status = "3" # 3-Pending For Approval
        usertype = "NC" # NC- Not Client
        source = "web-reg-CONTRACTAWARD"
        reg_name = request.POST['reg_name']
        reg_email = request.POST['reg_email']
        reg_number = request.POST['reg_number']
        reginputcountry = request.POST['reginputcountry']
        ip_address = find_ip_address() # Find user public IP Address
        now = datetime_obj.now()
        registered_date = now.strftime('%Y-%m-%d %H:%M:%S')

        email_list = fetch_data_query_manage(f"SELECT * FROM tbl_user WHERE email_id ='{str(reg_email)}' AND source='{str(source)}'")
        if len(email_list) == 0:
            insert_query = f"INSERT INTO tbl_user(reg_date,country,mobile_no,contact_name,email_id,ip_address,status,user_type,source)VALUES('{registered_date}','{str(reginputcountry)}','{str(reg_number)}','{str(reg_name)}','{str(reg_email)}','{str(ip_address)}','{str(status)}','{str(usertype)}','{str(source)}')"
            data_condition = insert_data_query_manage(insert_query)
            if data_condition == 'Done':
                return HttpResponse("Data Register Successfully !!!")
            else:
                return HttpResponse("Something Went Wrong !!!")
        else:
            return HttpResponse("This Email Already Exist Please !!!")
        
    return render(request,"htmltemp/register_page.html",{"captcha_number": cap_str_number,"country_drop":fetch_country})

def conactus_page(request):
    cap_str_number = create_random_number()
    fetch_country = fetch_data_query_manage("SELECT Country_Short_Code, Country_Name FROM tbl_region WHERE Country_Short_Code !='' ORDER BY Country_Name ASC")
    if request.method == 'POST':
        source = "web-reg-CONTRACTAWARD"
        contact_name = request.POST['contact_name']
        contact_email = request.POST['contact_email']
        contact_number = request.POST['contact_number']
        user_contact_country = request.POST['user_contact_country']
        contact_user_message = request.POST['contact_user_message']
        current_url = request.POST['current_url']
        email_list = fetch_data_query_manage(f"SELECT * FROM tbl_contact WHERE email ='{str(contact_email)}'")
        if len(email_list) == 0:
            insert_query = f"INSERT INTO tbl_contact(username,email,mobile,message,country,source,url)VALUES('{str(contact_name)}','{str(contact_email)}','{str(contact_number)}','{str(contact_user_message)}','{str(user_contact_country)}','{str(source)}','{str(current_url)}')"
            data_condition = insert_data_query_manage(insert_query)
            if data_condition == 'Done':
                return HttpResponse("done")
            else:
                return HttpResponse("Something Went Wrong !!!")
        else:
            return HttpResponse("This Email Already Exist !!!")
        return HttpResponse("done")
    return render(request, 'htmltemp/contact_us.html',{"captcha_number": cap_str_number,"country_drop":fetch_country})

def Tenders_page(request):
    fetch_CA_data_tup = fetch_data_query_manage("""SELECT CA.id, CA.short_descp, CA.contract_val, CA.contract_currency, RE.Country_Name FROM contract_award CA 
                                                INNER JOIN tbl_region RE 
                                                ON CA.purch_country = RE.Country_Short_Code
                                                WHERE LENGTH(CA.short_descp) > 5
                                                ORDER BY CA.id DESC
                                                LIMIT 0,10""")
    main_data_list = []
    for i in fetch_CA_data_tup:
        a_list = list(i)
        title = genrate_proper_string(str(a_list[1].lower()))
        stop_words = ['a', 'an', 'as', 'at', 'before', 'but', 'by', 'for', 'from', 'is', 'in', 'into','like', 'of', 'off', 'on', 'onto', 'per', 'since', 'than', 'the', 'this', 'that', 'to', 'up','via', 'with']
        title_list = str(title).split()
        main_title_list = []
        [main_title_list.append(i) for i in title_list if i not in stop_words]
        main_title = " ".join(main_title_list) # list to string 
        clean_title = main_title[0:100].replace("<br/>","").replace("<br>","")
        title_replace_multispace = re.sub('\s+', ' ', str(clean_title)) # remove multiple spaces
        clean_title = re.sub('[^A-Za-z0-9 -]+', '', title_replace_multispace).replace(' ','-').strip()
        message_bytes = str(a_list[0]).encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_id = base64_bytes.decode('ascii')
        a_list.append(f"{str(clean_title.replace('---','-').replace('--','-').replace('--','-'))}-{str(base64_id)}")
        main_data_list.append(a_list)
    paginator = Paginator(main_data_list,10)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    posts = paginator.page(page)
    return render(request, 'htmltemp/tenders_page.html',{"posts":posts})

def view_tender_details(request,tender_title="none"):
    title_id_str_list = str(tender_title).split('-')
    encoded_tender_id = title_id_str_list[-1]
    base64_bytes = encoded_tender_id.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    decoded_tender_id = message_bytes.decode('ascii')
    fetch_tender_detail = fetch_data_query_manage(f"SELECT * FROM contract_award WHERE id='{str(decoded_tender_id)}'")
    fetch_tender_detail = dict(fetch_tender_detail)
    print(fetch_tender_detail)
    return render(request, 'htmltemp/tender_detail_page.html',{"fetch_tender_detail":fetch_tender_detail})