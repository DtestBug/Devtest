from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token  # 登录类视图

from user import views


urlpatterns = [
    path('login/', obtain_jwt_token),  # 登录 drf自带登录系统obtain_jwt_token
    path('register/', views.UserView.as_view()),
    path('slogan/', views.SloganView.as_view()),


    # 用户名正则和邮箱正则阔以百度搜索
    re_path(r'^(?P<username>\w{6,20})/count/$', views.UsernameIsExistedView.as_view()),  # 正则：地址以^开头，$/结尾、字母数字下划线长度6--20
    re_path(r'^(?P<email>[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)/count/$', views.EmailIsExistedView.as_view()),  # 正则：地址以^开头，$/结尾、字母数字下划线长度6--20

]
