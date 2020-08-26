from django.db import models


class Interface_Mo(models.Model):

    # id = models.AutoField(primary_key=True)  # primary=True，True的状态为唯一主键
    name = models.CharField(verbose_name='接口名称', max_length=200, unique=True, help_text='接口名称')

    #related_name=父表引用从表的重命名
    projects = models.ForeignKey('project.Project_Mo', on_delete=models.CASCADE,
                                 verbose_name='所属项目', help_text='所属项目')#, related_name='interfaces'
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField(verbose_name='简要描述', max_length=200, null=True, blank=True, help_text='简要描述')

    class Meta:
        db_table = 't_Django_interface'
        verbose_name = '接口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name