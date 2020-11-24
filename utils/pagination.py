from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPagination(PageNumberPagination):
    page_size = 10  # 默认每页1条数据
    page_query_param = 'page'  # 查询字符串的key值 p=2

    page_size_query_param = 'size'  #
    max_page_size = 50  # 最多每一页显示50条

    page_query_description = '每页几条'
    page_size_query_description = '第几页'

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)  # 重写父类

        response.data['current_pages'] = self.page.number
        response.data['total_pages'] = self.page.paginator.num_pages
        return response
