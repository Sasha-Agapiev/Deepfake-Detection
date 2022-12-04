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
import uuid

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

        #ret = DDS_SQL.login(email, password)
        ret = 1
        if ret == None:
            return HttpResponse("FAIL")
        else:
            return JsonResponse({"userid": 1234})
        

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        firstname = json_data["firstname"]
        lastname = json_data["lastname"]
        email = json_data["email"]
        password=  json_data["password"]
        #generate unique userid
        uid = uuid.uuid4()

        try:
            #DDS_SQL.add_user(uid, firstname, lastname, email, password)
            return HttpResponse("OK")
        except:
            return HttpResponse("FAIL")

@csrf_exempt
def domainname_check(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        domainname = json_data["domainname"]
        ret = DDS_SQL.domainname_check(domainname)
        #domainname does not exist in database
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

        type_report = json_data["type"] #flag or false flag
        userid = json_data["userid"]
        domainname = json_data["domainname"]
        exists = DDS_SQL.exists_website(domainname)
        if exists == None:
            DDS_SQL.add_website(domainname)
        #flag website or false flag report 
        try:
            if type_report == "flag" or type_report == "false_flag":
                DDS_SQL.add_reports(userid, domainname, 1 if type_report == "flag" else -1)
            else:
                DDS_SQL.revoke_report(userid, domainname)
            return HttpResponse("OK")
        except:
            return HttpResponse("FAIL")


letters = string.ascii_lowercase

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        
        json_data = json.loads(request.body)

        imagedata = json_data["picture"]
        userid = json_data["userid"]

        """
        subscription = DDS.SQL.check_subscription(userid)
        if subscription == 0:
            num_predictions = DDS.SQL.check_predictions(userid)
            if num_predictions == 0:
                return HttpResponse("No predictions left")
        """
        
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

        #DDS_SQL.update_predictions(userid)

        return JsonResponse(prediction)



