from django.db import models
from utils.base_model import BaseModel


class Project_Mo(BaseModel):
    # 只要某一个字段中primary_key = True,那么Django就不会自动创建id字段，会使用自定义的
    id = models.AutoField(primary_key=True)  # primary=True，True的状态为唯一主键
    # 9.verbose_name:为个性化信息
    # 10.help_text帮助文本信息，在api接口文档平台和amdin后端站点中会用于提示，往往跟verbose_name一致
    # 11.unique用于指定唯一键，默认为False
    # 12.charField至少要指定一个max_length必传参数，代表此字段的最大长度，不能为负数
    name = models.CharField(max_length=200, verbose_name='项目名称', help_text='项目名称', unique=True)  # unique=True等于唯一的，max_length长度必须指定
    leader = models.CharField(max_length=50, verbose_name='项目负责人', help_text='项目负责人')
    tester = models.CharField(max_length=50, verbose_name='测试人员', help_text='测试人员')
    programmer = models.CharField(max_length=50, verbose_name='开发人员', help_text='开发人员')
    publish_app = models.CharField('发布应用', max_length=100, help_text='发布应用')
    # TextField没有长度限制
    desc = models.TextField(verbose_name='项目简介', help_text='项目简介',blank=True, default='XXX简介',null=True)
    # 13.null指定数据在保存时是否可以为空，默认不能为空秒如果null=True,那么可以为空值。
    # 14.blank指定前端用户在创建数据时，是否需要传递，默认需要传递，需要blank设置为True
    # 15.default为某一个字段指定默认值，往往会跟blank一起使用

    # 16.DateTimeField可以添加auto_now_add选项，django会自动添加创建记录时的时间
    # create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    # 17.DateTimeField可以添加auto_now选项，django会自动添加更新记录时的时间
    # update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    # 18.执行迁移脚本之后，生成的数据表名默认为子应用名_模型类名小写
    class Meta:
        # 19.可以在模型类下定义meta子类，meta子类名称固定
        # 20.可以使用db_table类属性，来指定表名
        # 21.指定表的个性化描述
        db_table = 'tb_project'
        verbose_name = '项目表'
        # managed = False  # 默认为True是可以进行创建表，如果为False的时候，这张表不进行操作

    def __str__(self):
        return f'<{self.name}>'