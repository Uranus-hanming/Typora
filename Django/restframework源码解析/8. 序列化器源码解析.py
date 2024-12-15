
class SerializerMetaclass(type):
    pass

class Field:
    def __new__(cls, *args, **kwargs):
        # <CommentsSerializers instance at 0x235b63ce7a0> 这段代码怎么理解？
        instance = super().__new__(cls)
        # args: [<Comments: Comments object (11)>, <Comments: Comments object (10)>]
        # 为CommentsSerializers对象实例赋值
        instance._args = args
        # {'context': {'format': None, 'request': <rest_framework.request.Request: GET '/app/comments/'>, 'view': <apps.viewsets.comments.CommentsViewSet object at 0x00000235B639D5D0>}}
        # 为CommentsSerializers对象实例赋值
        instance._kwargs = kwargs
        # 返回序列化器类对象的实例
        return instance

class BaseSerializer(Field):
    def __init__(self, instance=None, data=empty, **kwargs):
        self.instance = instance
        if data is not empty:
            self.initial_data = data
        self.partial = kwargs.pop('partial', False)
        self._context = kwargs.pop('context', {})
        kwargs.pop('many', None)
        super().__init__(**kwargs)

    def __new__(cls, *args, **kwargs):
        # cls: <class 'apps.viewsets.comments.CommentsSerializers'>
        # args: [<Comments: Comments object (11)>, <Comments: Comments object (10)>]
        # kwargs: {'context': {'format': None, 'request': <rest_framework.request.Request: GET '/app/comments/'>, 
        #          'view': <apps.viewsets.comments.CommentsViewSet object at 0x000001FC1CAEB250>}, 'many': True}
        if kwargs.pop('many', False):
            # many为True时执行
            return cls.many_init(*args, **kwargs)
        # many默认为False
        # 调用父类Field的__new__()
        return super().__new__(cls, *args, **kwargs)

class ListSerializer(BaseSerializer):
    pass

LIST_SERIALIZER_KWARGS = (
    'read_only', 'write_only', 'required', 'default', 'initial', 'source',
    'label', 'help_text', 'style', 'error_messages', 'allow_empty',
    'instance', 'data', 'partial', 'context', 'allow_null',
    'max_length', 'min_length'
)
    @classmethod
    def many_init(cls, *args, **kwargs):
        # cls: <class 'apps.viewsets.comments.CommentsSerializers'>
        # args: [<Comments: Comments object (11)>, <Comments: Comments object (10)>]
        # kwargs: {'context': {'format': None, 'request': <rest_framework.request.Request: GET '/app/comments/'>, 
        #          'view': <apps.viewsets.comments.CommentsViewSet object at 0x000001FC1CAEB250>}, 'many': True}
        allow_empty = kwargs.pop('allow_empty', None)
        max_length = kwargs.pop('max_length', None)
        min_length = kwargs.pop('min_length', None)
        # 实例化序列化器类 CommentsSerializers <class 'apps.viewsets.comments.CommentsSerializers'>
        # 这次没有传many，默认many=False，调用BaseSerializer类的__new__()
        # 返回序列化器对象实例：CommentsSerializers([<Comments: Comments object (11)>, <Comments: Comments object (10)>], 
            #context={'request': <rest_framework.request.Request: GET '/app/comments/'>, 'format': None, 'view': <apps.viewsets.comments.CommentsViewSet object>}):
            # id = IntegerField(label='ID', read_only=True)
            # description = CharField(allow_blank=True, allow_null=True, help_text='评论内容', label='评论内容', required=False, style={'base_template': 'textarea.html'})
            # commenter = CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)
            # comment_time = DateTimeField(label='评论时间', read_only=True)
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {
            'child': child_serializer,
        }
        if allow_empty is not None:
            list_kwargs['allow_empty'] = allow_empty
        if max_length is not None:
            list_kwargs['max_length'] = max_length
        if min_length is not None:
            list_kwargs['min_length'] = min_length
        list_kwargs.update({
            key: value for key, value in kwargs.items()
            if key in LIST_SERIALIZER_KWARGS
        })
        # <class 'apps.viewsets.comments.CommentsSerializers.Meta'>
        meta = getattr(cls, 'Meta', None)
        # getattr(object, name[, default]) 尝试去获取CommentsSerializers.Meta对象的属性list_serializer_class，如果不存在则返回类ListSerializer
        list_serializer_class = getattr(meta, 'list_serializer_class', ListSerializer)
        # 实例化类：<class 'rest_framework.serializers.ListSerializer'>
        # 调用类BaseSerializer的__new__()
        # args: [<Comments: Comments object (11)>, <Comments: Comments object (10)>]
        # {'child': CommentsSerializers([<Comments: Comments object (11)>, <Comments: Comments object (10)>], 
            # context={'request': <rest_framework.request.Request: GET '/app/comments/'>, 'format': None, 'view': <apps.viewsets.comments.CommentsViewSet object>}):
            # id = IntegerField(label='ID', read_only=True)
            # description = CharField(allow_blank=True, allow_null=True, help_text='评论内容', label='评论内容', required=False, style={'base_template': 'textarea.html'})
            # commenter = CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)
            # comment_time = DateTimeField(label='评论时间', read_only=True), 'context': {'request': <rest_framework.request.Request: GET '/app/comments/'>, 'format': None, 'view': <apps.viewsets.comments.CommentsViewSet object at 0x00000235B639D810>}}
        return list_serializer_class(*args, **list_kwargs)

class Serializer(BaseSerializer, metaclass=SerializerMetaclass):
    pass

class ModelSerializer(Serializer):
    pass

class GenericAPIView(views.APIView):
    def get_serializer_class(self):
        # 调用视图类CommentsViewSet属性serializer_class，返回序列化器类CommentsSerializers
        return self.serializer_class

    def get_serializer_context(self):
        # self.request： <rest_framework.request.Request: GET '/app/comments/'>
        # 'format': None
        # view: <apps.viewsets.comments.CommentsViewSet object at 0x000002B4375E20E0>
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        # self: <apps.viewsets.comments.CommentsViewSet object at 0x000002B4375E20E0>
        # args: [<Comments: Comments object (11)>, <Comments: Comments object (10)>]
        # kwargs: many=True
        # 返回<class 'apps.viewsets.comments.CommentsSerializers'>
        serializer_class = self.get_serializer_class()
        # self.get_serializer_context()返回{'format': None, 'request': <rest_framework.request.Request: GET '/app/comments/'>, 'view': <apps.viewsets.comments.CommentsViewSet object at 0x000001FC1CAEB070>}
        kwargs.setdefault('context', self.get_serializer_context())
        # 实例化序列化器类CommentsSerializers，首先执行的是BaseSerializer类的__new__()
        # 返回<class 'rest_framework.serializers.ListSerializer'>
        return serializer_class(*args, **kwargs)

class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            # self: <apps.viewsets.comments.CommentsViewSet object at 0x000002B4375E20E0>
            # self.get_serializer: <bound method GenericAPIView.get_serializer of <apps.viewsets.comments.CommentsViewSet object at 0x000002B4375E20E0>>
            # page: [<Comments: Comments object (11)>, <Comments: Comments object (10)>]
            # 返回<class 'rest_framework.serializers.ListSerializer'>
                # CommentsSerializers([<Comments: Comments object (11)>, <Comments: Comments object (10)>>, 
                # <Comments: Comments object (2)>], context={'request': <rest_framework.request.Request: GET '/app/comments/'>, 'format': None, 'view': <apps.viewsets.comments.CommentsViewSet object>}, many=True):
                # id = IntegerField(label='ID', read_only=True)
                # description = CharField(allow_blank=True, allow_null=True, help_text='评论内容', label='评论内容', required=False, style={'base_template': 'textarea.html'})
                # commenter = CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)
                # comment_time = DateTimeField(label='评论时间', read_only=True)
            # serializer: 返回类<class 'rest_framework.serializers.ListSerializer'>
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


##################################### 视图类 ################################

from rest_framework import serializers
class CommentsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = "__all__"

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all().order_by("-id")
    serializer_class = CommentsSerializers
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend, CustomSearchFilter]
    filterset_class = CommentsFilter
    # 根据keyword过滤搜索
    search_fields = [i.name for i in Comments._meta.fields]
