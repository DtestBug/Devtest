from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import ReportsModelSerializer
from .models import Reports
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action  # 导入装饰器
from django.conf import settings  # 需要配置settings下 REPORT_DIR = os.path.join(BASE_DIR, 'reports')
from django.http.response import StreamingHttpResponse  # 操作文件流需要
from .utils import get_file_content
import os
from django.utils.encoding import escape_uri_path  # django处理文件乱码


class ReportsViewSet(mixins.ListModelMixin,  # 查询list
                     mixins.RetrieveModelMixin,  # 查询单个
                     mixins.DestroyModelMixin,  # 删除数据
                     GenericViewSet):  # 必须继承

    queryset = Reports.objects.all()  # 查询集
    serializer_class = ReportsModelSerializer  # 序列化
    permission_classes = [permissions.IsAuthenticated]  # 用户权限
    ordering_fields = ['id', 'name']

    # def retrieve(self, request, *args, **kwargs):
    #     pass

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        # 获取html源码
        instance = self.get_object()
        html = instance.html
        name = instance.name

        # 获取测试报告所属目录路径
        reports_dir = settings.REPORT_DIR

        # 生成html文件，存放在reports目录下
        reports_full_dir = os.path.join(reports_dir, name) + 'html'
        if not os.path.exists(reports_full_dir):  # 如果文件不存在，则下载新文件
            with open(reports_full_dir, 'w', encoding='utf-8') as file:
                file.write(html)

        # 获取文件流，返回给前端
        # 创建一个生成器，获取文件流，每次获取的是文件字节数据，可以提升下载速度
        response = StreamingHttpResponse(get_file_content(reports_full_dir))

        # django处理文件乱码
        html_file_name = escape_uri_path(name + 'html')
        # 添加响应头
        # 直接使用Response对象['响应头名称'] = '值'
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachement; filename*=UTF-8'' {html_file_name}"
        return response

