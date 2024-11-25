
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
import os
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator


from .models import Mobiles
from .serializers import MobSerializer,UserRegistrationSerializer,UserLoginSerializer

# Create your views here.
class MobView(APIView):
    permission_classes= [IsAuthenticated]

    @method_decorator(permission_required('shopApp.add_mobiles',raise_exception=True))
    def post(self,request):

        # Pass JSON data from user POST request to serializer for validation
        serializedData=MobSerializer(data=request.data)

        # Check if  data passes validation checks from serializer
        if serializedData.is_valid():

            # Handle image file upload
            image = request.FILES.get('image')  # Get the image file from the request

            if image:
                #saving image to media/mob_images directory
                file_path=os.path.join('mob_images', image.name)
                #check whether the file already exists
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT, file_path)):
                    default_storage.save(file_path, image)

                #generate image url
                image_url=f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}{file_path}"

                 # Save the image url in the database
                serializedData.validated_data['image_url'] = image_url

            # If  data is valid, create a new  record in the database
            resp=serializedData.save()
            return Response({
                'message':"mobile created"
            },status.HTTP_201_CREATED)

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

    @method_decorator(permission_required('shopApp.change_mobiles',raise_exception=True))
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

    @method_decorator(permission_required('shopApp.delete_mobiles',raise_exception=True))
    def delete(self,request,id=None):
        try:
             # check whether the item exist
            mobData=Mobiles.objects.get(id=id)
        
        except Mobiles.DoesNotExist:
            # If the  item does not exist, return an error response
            return Response({'errors': 'This item does not exist.'},status=400)

       #delete item

        # Get the image URL from the record
        image_url = mobData.image_url

         # Get the relative file path
        relative_image_path = image_url[len(request.scheme + "://" + request.get_host() + settings.MEDIA_URL):]
        # Build the full path to the image file
        image_path = os.path.join(settings.MEDIA_ROOT, relative_image_path)

        # Check if the file exists and delete it
        if os.path.exists(image_path):
            os.remove(image_path)
        else:
            return Response({"message": "Image file not found"}, status=status.HTTP_404_NOT_FOUND)

        mobData.delete()
        return Response('deleted',status=204)

#views for user management
class UserManagement(APIView):
    permission_classes=[AllowAny]   #Anyone can access this endpoind
    def post(self,request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({
                'message': 'User created successfully.',
                'user': serializer.data ,
            },status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=400)

#view for login
class UserLogin(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user=authenticate(username=username,password=password)
            if user:
                # Generate JWT token 
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({
                    'access_token': access_token,
                    'refresh_token': str(refresh),
                    'message': "success"
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'message': "invalid credentials",   
                },status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )

#view for Logout
class UserLogout(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            # Get the user's refresh token from the request
            print(request)
            refresh_token = request.data.get('refresh_token')

             # Revoke the refresh token by blacklisting it
            token=RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
            

        





        
