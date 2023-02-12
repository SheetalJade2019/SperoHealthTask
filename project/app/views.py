from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from project.settings import BASE_DIR
from .models import *
from django.db.models import Q





@csrf_exempt
@api_view(["POST"])
def upload_file(request):
    """
    API that takes excel file as input and saves it to file system storage and also to database file header collection and upload collection
    """
    try:
        if request.FILES['upload']:
            upload = request.FILES['upload']
            fss=FileSystemStorage()
            file=fss.save(upload.name,upload)
            file_url = fss.url(file)
            print(BASE_DIR)
            df = pd.read_excel(f"{BASE_DIR}/{file_url}")
            # print(df)
            file = FileHeader.objects.create(file_name=upload.name,file_url=file_url)
            for index,row in df.iterrows():
                print(type(row),row["Name"],row["Age"],row["District"],row["Std"],row["Date"])
                Uploads.objects.create(file_id=file, name=row["Name"],age=row["Age"],district=row["District"],std=row["Std"],date=row["Date"])
            return Response({"file_url":file_url,"message":"File Uploaded Successfully..!"},status=status.HTTP_200_OK)
        return Response({"message":"File not sent..!"},status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print("Exception : ",str(e))
        return Response({"message":f"Something went wrong. {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(["GET"])
def get_file_data(request):
    """
    API that reads file data from database and returns to frontend
    """
    try:
        file_id = request.GET['file_id']
        if not file_id:
            return Response({"message":"File id not sent..!"},status=status.HTTP_403_FORBIDDEN)
        else:
            file_id=int(file_id)
        
        returnDict={}
        file = FileHeader.objects.get(file_id=file_id)
        returnDict["filename"]=file.file_name
        returnDict["file_id"]=file.file_id
        returnDict["rows"]=[]
        data = Uploads.objects.filter(file_id=file)

        for obj in data:
            returnDict["rows"].append({str(obj.row_id):{"name":obj.name,"age":obj.age,"district":obj.district,"std":obj.std,"date":obj.date}})

        return Response({"data":returnDict,"message":"File data fetched Successfully..!"},status=status.HTTP_200_OK)
    except Exception as e:
        print("Exception : ",str(e))
        return Response({"message":f"Something went wrong. {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["GET"])
def get_searched_data(request):
    """
    API that searches for the input word and returns result
    """
    try:
        query = request.GET['query']
        if not query:
            return Response({"message":"Input missing"},status=status.HTTP_403_FORBIDDEN)
        results=None

        if 48 <= ord(query[0]) <= 57:
            results = Uploads.objects.filter(Q(std=int(query)) | Q(age=int(query))).distinct()
        else:
            results = Uploads.objects.filter(Q(name__icontains=query) | Q(district__icontains=query) | Q(date__icontains=query) ).distinct()

        returnDict=[]
        for obj in results:
            returnDict.append({str(obj.row_id):{"name":obj.name,"age":obj.age,"district":obj.district,"std":obj.std,"date":obj.date}})

        return Response({"data":returnDict,"message":"File data fetched Successfully..!"},status=status.HTTP_200_OK)
    except Exception as e:
        print("Exception : ",str(e))
        return Response({"message":f"Something went wrong. {e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
