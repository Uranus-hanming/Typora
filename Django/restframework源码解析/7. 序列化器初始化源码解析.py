
class ListSerializer(BaseSerializer):
	pass

class Field:
    def __new__(cls, *args, **kwargs):
        # cls: 类UserInfoSerializers <class 'apps.viewsets.user_info.UserInfoSerializers'>
        # 重点，这段代码的含义是什么？？ 对类UserInfoSerializers进行实例化
        instance = super().__new__(cls)
        # ([<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>],)
        instance._args = args
        # {'context': {'format': None, 'request': <rest_framework.request.Request: GET '/app/user/'>, 'view': <apps.viewsets.user_info.UserInfosViewSet object at 0x0000017E2240BC10>}}
        instance._kwargs = kwargs
        # instance： UserInfoSerializers([<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>], 
        	# context={'request': <rest_framework.request.Request: GET '/app/user/'>, 'format': None, 'view': <apps.viewsets.user_info.UserInfosViewSet object>}):
		    # id = IntegerField(label='ID', read_only=True)
		    # level = CharField(read_only=True, source='get_level_display')
		    # username = CharField(label='用户名', max_length=32)
		    # password = CharField(label='密码', max_length=64)
		    # age = IntegerField(label='年龄', max_value=2147483647, min_value=-2147483648, required=False)
		    # email = CharField(label='邮箱', max_length=64)
		    # token = CharField(allow_blank=True, allow_null=True, label='TOKEN', max_length=64, required=False)
		    # depart = PrimaryKeyRelatedField(label='部门', queryset=Department.objects.all())
		    # roles = PrimaryKeyRelatedField(allow_empty=False, label='角色', many=True, queryset=Role.objects.all())
        return instance

class BaseSerializer(Field):
	@classmethod
    def many_init(cls, *args, **kwargs):  # 重点代码
    	# cls: <class 'apps.viewsets.user_info.UserInfoSerializers'>
    	# args: 所有数据对象信息 ([<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>],)
    	# kwargs: 请求接口 + 视图类对象
    	# kwargs: {'context': {'format': None, 
    			 # 'request': <rest_framework.request.Request: GET '/app/user/'>, 
    		     # 'view': <apps.viewsets.user_info.UserInfosViewSet object at 0x0000017E2240BC10>}}
        allow_empty = kwargs.pop('allow_empty', None)
        max_length = kwargs.pop('max_length', None)
        min_length = kwargs.pop('min_length', None)
        # 实例化类UserInfoSerializers，many为空，调用类方法BaseSerializer.__new__()
        # 返回类UserInfoSerializers实例对象
        # child_serializer = UserInfoSerializers([<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>], 
        	# context={'request': <rest_framework.request.Request: GET '/app/user/'>, 'format': None, 'view': <apps.viewsets.user_info.UserInfosViewSet object>}):
		    # id = IntegerField(label='ID', read_only=True)
		    # level = CharField(read_only=True, source='get_level_display')
		    # username = CharField(label='用户名', max_length=32)
		    # password = CharField(label='密码', max_length=64)
		    # age = IntegerField(label='年龄', max_value=2147483647, min_value=-2147483648, required=False)
		    # email = CharField(label='邮箱', max_length=64)
		    # token = CharField(allow_blank=True, allow_null=True, label='TOKEN', max_length=64, required=False)
		    # depart = PrimaryKeyRelatedField(label='部门', queryset=Department.objects.all())
		    # roles = PrimaryKeyRelatedField(allow_empty=False, label='角色', many=True, queryset=Role.objects.all())
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

        LIST_SERIALIZER_KWARGS = ('read_only', 'write_only', 'required', 'default', 'initial', 'source', 'label', 'help_text', 
        	'style', 'error_messages', 'allow_empty', 'instance', 'data', 'partial', 'context', 'allow_null', 'max_length', 'min_length')

        list_kwargs.update({
            key: value for key, value in kwargs.items()
            if key in LIST_SERIALIZER_KWARGS
        })
        meta = getattr(cls, 'Meta', None)
        list_serializer_class = getattr(meta, 'list_serializer_class', ListSerializer)
        # 实例化类ListSerializer，调用的是 BaseSerializer.__new__()
        # 返回的是ListSerializer对象
        return list_serializer_class(*args, **list_kwargs)

    def __new__(cls, *args, **kwargs):
    	# cls: <class 'apps.viewsets.user_info.UserInfoSerializers'>
    	# args: 所有数据对象信息 ([<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>],)
    	# kwargs: 请求接口 + 视图类对象
    	# kwargs: {'context': {'format': None, 'request': <rest_framework.request.Request: GET '/app/user/'>, 'view': <apps.viewsets.user_info.UserInfosViewSet object at 0x0000017E2240BC10>}}
        if kwargs.pop('many', False):
            return cls.many_init(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

class type(object):
	pass

class SerializerMetaclass(type):


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
        # args: ([<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>],)
        # kwargs: many=True
        # 返回类CommentsSerializers <class 'apps.viewsets.comments.CommentsSerializers'>
        serializer_class = self.get_serializer_class()
        # self.get_serializer_context()返回{'format': None, 'request': <rest_framework.request.Request: GET '/app/comments/'>, 'view': <apps.viewsets.comments.CommentsViewSet object at 0x000001FC1CAEB070>}
        kwargs.setdefault('context', self.get_serializer_context())
        # 实例化序列化器类 UserInfoSerializers ，首先执行的是BaseSerializer类的__new__()
        # many=True时返回<class 'rest_framework.serializers.ListSerializer'>
        return serializer_class(*args, **kwargs)  # 重点入口

class ListModelMixin:
    def list(self, request, *args, **kwargs):
    	# self: CommentsViewSet对象 <apps.viewsets.comments.CommentsViewSet object at 0x000002B4375E20E0>
    	# 调用类方法：GenericAPIView.get_serializer()
    	# many=True时返回类<class 'rest_framework.serializers.ListSerializer'>
    	serializer = self.get_serializer(page, many=True)

##################################### 视图类 ################################

class View:
	pass

class APIView(View):
	pass

class GenericAPIView(views.APIView):
	pass

class ViewSetMixin:
	pass

class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
	pass

class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
	pass

from rest_framework import serializers
class UserInfoSerializers(serializers.ModelSerializer):
    level = serializers.CharField(source="get_level_display", read_only=True)

    class Meta:
        model = UserInfo
        fields = "__all__"
        # depth = 1

class UserInfosViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializers
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserInfoFilter
    # authentication_classes = []
    # permission_classes = []