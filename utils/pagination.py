from rest_framework.pagination import PageNumberPagination


# 重写父类:PageNumberPagination
class MyPagination(PageNumberPagination):
    page_size = 5  # 每页数字数量
    page_query_param = 'p'  # 指定前端页码的查询字符串key名称

    page_size_query_param = 's'  # 指定前端每一页数据条数的查询字符串key名称
    max_page_size = 50  # 最大数据显示
