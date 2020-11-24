from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.generics import CreateAPIView


# class UserView(CreateAPIView):
#     def post(self, request, *args, **kwargs):  # 用户注册的功能
#         serializer = RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserView(CreateAPIView):
    serializer_class = RegisterSerializer



class UsernameIsExistedView(APIView):

    def get(self, request, username):  # 要查询的字段username
        count = User.objects.filter(
            username=username).count()  # 调用自带django.contrib.auth.models的auth_user数据库，查询从前端传入的用户名存不存在于数据库
        one_dict = {
            'username': username,
            'count': count
        }
        return Response(one_dict)


class EmailIsExistedView(APIView):

    def get(self, request, email):  # 要查询的字段email
        count = User.objects.filter(
            email=email).count()  # 调用自带django.contrib.auth.models的auth_user数据库，查询从前端传入的用户名存不存在于数据库
        one_dict = {
            'email': email,
            'count': count
        }
        return Response(one_dict)


class SloganView(APIView):

    def get(self, request):
        url = "http://www.yogapi.com/api/getPresentQuote.php"
        data = requests.get(url).json()['quote']
        dict = {
            'data': data
        }
        return Response(dict)
