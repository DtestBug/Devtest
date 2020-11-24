from django.db import models
# 多表内重复的字段


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    # 避免单独创建数据表
    class Meta:
        abstract = True  # 将abstract设置为True，指定在迁移时不创建表

