from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Mobiles
from .serializers import MobSerializer

# Create your views here.
class MobView(APIView):
    
    def post(self,request):
        serializedData=MobSerializer(data=request.data)
        if serializedData.is_valid():
            resp=serializedData.save()
            return Response(resp.id,status=201)

        return Response(serializedData.errors,status=400)
    
    def get(self,request,id=None):
        if id:
         # If an id is provided in the GET request, retrieve the item by that id
            try:
                mobData=Mobiles.objects.get(id=id)

            except Mobiles.DoesNotExist:
                return Response({'errors': 'This item does not exist.'},status=400)

            # Serialize the object to JSON formatted data
            serializedData=MobSerializer(mobData)

        else:
            # Get all todo items from the database using Django's model ORM 
            mobData=Mobiles.objects.all()

             # Serialize the object to JSON formatted data
            serializedData=MobSerializer(mobData,many=True)

        return Response(serializedData.data)



        
