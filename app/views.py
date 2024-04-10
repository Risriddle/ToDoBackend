from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
#from django.http import HttpResponse
# Create your views here.
'''
#function based views
@api_view(['GET'])
def login(request):
    return Response("hello")

#class based views
class Login(APIView):
    def get(self,request):
        return Response("hellooooo")'''
    
#using viewset to create views (viewsets are classes that allow to handle all views in one class along with all CRUD opns)(types of viewset-ModelViewSet etc)
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from django.contrib.auth import authenticate  # Import authenticate function for user authentication
#from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


'''class MyModelViewSet(ModelViewSet):
    queryset = TodoUsers.objects.all()
    serializer_class = MyModelSerializer'''
    
class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserLogin(APIView):
    def post(self,request):
        
        # Extract username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User is authenticated
            # Create a token (if using token-based authentication)
            #token, created = Token.objects.get_or_create(user=user)
            token, _ = Token.objects.get_or_create(user=user)
            # Return a success response
            return Response({'token': token.key}, status=status.HTTP_200_OK)
            #return Response("logged in", status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response("Invalid username or password.", status=status.HTTP_401_UNAUTHORIZED)
        
        
class ToDoViewSet(ModelViewSet):
    queryset = TodoUsers.objects.all()
    serializer_class = TodoSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = TodoUsers.objects.filter(username=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    
    def create(self, request):
         # Assign the current user to the username field
        request.data['username'] = request.user.id

        # Pass the modified request data to the serializer
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request,**kwargs):
        pk = kwargs.get('pk')
        # Retrieve the existing todo instance
        todo_instance = get_object_or_404(TodoUsers, pk=pk)
        request.data['username'] = request.user.id

        # Update the fields with the new data from the request
        todo_instance.todo = request.data.get('todo', todo_instance.todo)
        
        # Serialize the updated todo instance
        serializer = self.serializer_class(todo_instance, data=request.data)
        
        if serializer.is_valid():
            # Save the updated todo instance
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        queryset = TodoUsers.objects.all()
        todo = get_object_or_404(queryset, pk=pk, username=request.user)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

class UserLogout(APIView):
    def post(self, request):
        # Get the token from the request headers
        authorization_header = request.headers.get('Authorization')
        print(request.user)
        if not authorization_header:
            return Response("Authorization header is required.", status=status.HTTP_400_BAD_REQUEST)

        # Extract the token value
        try:
            _, token_value = authorization_header.split()
        except ValueError:
            return Response("Invalid authorization header format.", status=status.HTTP_400_BAD_REQUEST)

        # Get the token object
        try:
            token = Token.objects.get(key=token_value)
        except Token.DoesNotExist:
            return Response("Invalid token.", status=status.HTTP_400_BAD_REQUEST)
        print(token.user,request.user)
        
        # Check if the token belongs to the current user
        '''if token.user != request.user:
        ##not working
            return Response("Unauthorized token.", status=status.HTTP_401_UNAUTHORIZED)'''

        # Delete the token
        token.delete()

        return Response("User logged out successfully.", status=status.HTTP_200_OK)
