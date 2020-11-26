from django.db import models
from utils.base_model import BaseModel


class Debugtalks(BaseModel):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('debugtalks文件名称', max_length=200, default='debugtablk.py', help_text='debugtalks文件名称')
    debugtalk = models.TextField(null=True, default='#debugtalk.py', help_text='debugtalk.py')

    project = models.OneToOneField('project.Project_Mo', on_delete=models.CASCADE,
                                related_name='debugtalks', help_text='所属项目')
    class Meta:
        db_table = 'tb_debugtalks'
        verbose_name = 'debugtalks.py文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name