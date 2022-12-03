from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import base64
from django.views.decorators.csrf import csrf_exempt
from . import DDS_SQL 
import base64
import re
import string
import random
import glob
import os
from prediction.predict import predict as pred
def decode_base64(data, altchars='+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub('[^a-zA-Z0-9%s]+' % altchars, '', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += '='* (4 - missing_padding)
    return base64.b64decode(data, altchars)


import os
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data["email"]
        password=  data["password"]
        print(email)
        print(password)
        #ret = DDS_SQL.login(email, password)

        return HttpResponse("hi")

        if ret == None:
            return HttpResponse("FAIL")
        else:
            return JsonResponse({"user": ret[0]})
        

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        firstname = json_data["firstname"]
        lastname = json_data["lastname"]
        email = json_data["email"]
        password=  json_data["password"]

        print(firstname)

        try:
            #DDS_SQL.add_user(firstname, lastname, email, password, "test", "test", "123")
            return HttpResponse("OK")
        except:
            return HttpResponse("FAIL")

@csrf_exempt
def url_check(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        url = json_data["url"]
        ret = DDS_SQL.url_check(url)
        #url does not exist in database
        if ret == None:
            return HttpResponse("FAIL")
        else:
            #server if flagged
            if ret[0] == 1:
                return HttpResponse("TRUE")
            else:
                return HttpResponse("FALSE")

@csrf_exempt
def report(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        type_report = json_data["type"]
        uid = json_data["uid"]
        url = json_data["url"]
        try:
            DDS_SQL.add_reports(uid, url, 1 if type_report == "add" else -1)
            return HttpResponse("OK")
        except:
            return HttpResponse("FAIL")

letters = string.ascii_lowercase

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        
        json_data = json.loads(request.body)

        imagedata = json_data["picture"]
        filetype, imagedata = imagedata.split(";base64,")
        filetype = filetype.split("/")[1]
        
        imagedata = decode_base64(imagedata)

        if filetype == "png":
            filename = 'temp/'+''.join(random.choice(letters) for i in range(10))+".png"
        else: # if filetype == "jpeg"
            filename = 'temp/'+''.join(random.choice(letters) for i in range(10))+".jpg"


        with open(filename, 'wb') as f:
            f.write(imagedata)

        p = pred(filename)

        prediction = {"prediction" : p}

        # Flush temp/
        files = glob.glob("temp/*")
        for f in files:
            os.remove(f)

        return JsonResponse(prediction)


@csrf_exempt
def add_website(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        url = data["url"]
        name=  data["name"]
        ret = DDS_SQL.add_website(url, name)

@csrf_exempt
def add_contains(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        pic = data["pic"]
        prediction=  data["prediction"]
        url = data["url"]
        ret = DDS_SQL.add_contains(pic, prediction, url)

