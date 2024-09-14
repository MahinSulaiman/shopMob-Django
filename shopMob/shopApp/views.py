from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Mobiles
from .serializers import MobSerializer

# Create your views here.
class MobView(APIView):
    
    def post(self,request):
        # Pass JSON data from user POST request to serializer for validation
        serializedData=MobSerializer(data=request.data)

        # Check if  data passes validation checks from serializer
        if serializedData.is_valid():
            # If  data is valid, create a new todo item record in the database
            resp=serializedData.save()
            return Response(resp.id,status=201)

        return Response(serializedData.errors,status=400)
    
    def get(self,request,id=None):
        if id:
         # If an id is provided in the GET request, retrieve the item by that id
            try:
                mobData=Mobiles.objects.get(id=id)

            except Mobiles.DoesNotExist:
                # If the  item does not exist, return an error response
                return Response({'errors': 'This item does not exist.'},status=400)

            # Serialize the object to JSON formatted data
            serializedData=MobSerializer(mobData)

        else:
            # Get all todo items from the database using Django's model ORM 
            mobData=Mobiles.objects.all()

             # Serialize the object to JSON formatted data
            serializedData=MobSerializer(mobData,many=True)

        return Response(serializedData.data)

    def put(self,request,id=None):
        try:
             # If an id is provided in the PUT request, retrieve the item by that id
            mobData=Mobiles.objects.get(id=id)
        
        except Mobiles.DoesNotExist:
            # If the  item does not exist, return an error response
            return Response({'errors': 'This item does not exist.'},status=400)

        # If the  item does exists, use the serializer to validate the updated data
        serializedData=MobSerializer(mobData,data=request.data)

        # Check if  data passes validation checks from serializer
        if serializedData.is_valid():
            resp=serializedData.save()
            return Response(resp.id,status=200)

        # If the update data is not valid, return an error response
        return Response(serializedData.errors, status=400)

    def delete(self,request,id=None):
        try:
             # check whether the item exist
            mobData=Mobiles.objects.get(id=id)
        
        except Mobiles.DoesNotExist:
            # If the  item does not exist, return an error response
            return Response({'errors': 'This item does not exist.'},status=400)

       #delete item
        mobData.delete()
        return Response('deleted',status=204)




        
