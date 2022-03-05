from django.shortcuts import render
from rest_framework.views import APIView
import jwt,datetime
import requests
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from user.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.admin.models import LogEntry

# Create your views here.
def home(request):
    LogEntry.objects.all().delete()
    return render(request,'login.html')

#to create a new user
class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
            
        else:
            return Response(serializer.errors)

def createUser(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username= request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('cfpassword')
        if pass1 == pass2:
            password = pass1
        data = {
            'name':name,
            'email':email,
            'username':username,
            'password':password,
        }
        headers = {'Content-Type': 'application/json'}
        read = requests.post('http://localhost:8000/api/registerView', json=data, headers=headers)        
        return render(request,'login.html')
    else:
        return render(request,'login.html')


#log in the existing users
class LoginView(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User Not Found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret', algorithm='HS256')
        
        response = Response()

        response.data = ({
            'username':username,
            'jwt':token

        })

        response.set_cookie(key='jwt', value=token, httponly=True)
        return response


def loginUser(request):
    allData = User.objects.all()

    data={
            "allData":allData
        }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
       
        data = {
            
            'username':username,
            'password':password,            
        }

        headers = {'Content-Type': 'application/json'}
        read = requests.post('http://localhost:8000/api/loginView', json=data, headers=headers)
        user = authenticate(username = username , password = password)
        
        if user:                    
                login(request,user) 
                allData = User.objects.all()

                data={
                "allData":allData
                    }           
                messages.success(request, 'Logged in successfully!')
                return render(request,'users.html',data)
    else:
        return render(request,'users.html',data)
    return HttpResponse('404 Not Found')


#logged out the existing users

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

def logoutUser(request):
    if request.method == "GET":
        read = requests.get('http://localhost:8000/api/logoutView')
        logout(request)
        messages.success(request, 'Logged out successfully!')
        return render(request,'login.html')
    else:
        return render(request,'register.html')
    return HttpResponse('404 Not Found')



def users(request):
    allData = User.objects.all()

    data={
            "allData":allData
         }           
    return render(request,'users.html',data)

def loginPage(request):
    return render(request,'login.html')

def registerPage(request):
    return render(request,'register.html')