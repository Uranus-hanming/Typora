
def is_simple_callable(obj):
    """
    True if the object is a callable that takes no arguments.
    """
    if not callable(obj):
        return False

    # Bail early since we cannot inspect built-in function signatures.
    if inspect.isbuiltin(obj):
        raise BuiltinSignatureError(
            'Built-in function signatures are not inspectable. '
            'Wrap the function call in a simple, pure Python function.')

    if not (inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, functools.partial)):
        return False

    sig = inspect.signature(obj)
    params = sig.parameters.values()
    return all(
        param.kind == param.VAR_POSITIONAL or
        param.kind == param.VAR_KEYWORD or
        param.default != param.empty
        for param in params
    )

class PrimaryKeyRelatedField(RelatedField):
    def to_representation(self, value):
        if self.pk_field is not None:
            return self.pk_field.to_representation(value.pk)
        return value.pk

class ManyRelatedField(Field):
    def to_representation(self, iterable):
        return [
            # 调用类PrimaryKeyRelatedField方法to_representation()
            self.child_relation.to_representation(value)
            for value in iterable
        ]

class DateTimeField(Field):
    def to_representation(self, value):
        # self: DateTimeField(label='评论时间', read_only=True)
        # value: datetime.datetime(2024, 7, 22, 18, 25, 40, tzinfo=<UTC>)
        if not value:
            return None
        # comment_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
        # 可以在序列化器中配置该字段的format，也可以在配置文件中全局配置DATETIME_FORMAT
        output_format = getattr(self, 'format', api_settings.DATETIME_FORMAT)

        if output_format is None or isinstance(value, str):
            return value

        value = self.enforce_timezone(value)

        if output_format.lower() == ISO_8601:
            value = value.isoformat()
            if value.endswith('+00:00'):
                value = value[:-6] + 'Z'
            return value
        # 将时间进行格式化
        return value.strftime(output_format)

class Model(metaclass=ModelBase):
    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choices_dict = dict(make_hashable(field.flatchoices))
        return force_str(choices_dict.get(make_hashable(value), value), strings_only=True)

# 重点代码
def is_simple_callable(obj):
    """
    True if the object is a callable that takes no arguments.
    """
    if not callable(obj):
        return False

    # Bail early since we cannot inspect built-in function signatures.
    if inspect.isbuiltin(obj):
        raise BuiltinSignatureError(
            'Built-in function signatures are not inspectable. '
            'Wrap the function call in a simple, pure Python function.')

    if not (inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, functools.partial)):
        return False

    sig = inspect.signature(obj)
    params = sig.parameters.values()
    return all(
        param.kind == param.VAR_POSITIONAL or
        param.kind == param.VAR_KEYWORD or
        param.default != param.empty
        for param in params
    )

# 重点代码
def get_attribute(instance, attrs):
    # <UserInfo: UserInfo object (2)>
    # ['get_level_display']
    # ["depart", "title", "xxx", "xxx"]
    for attr in attrs:
        if isinstance(instance, Mapping):
            instance = instance[attr]
        else:
            # 获取数据对象的字段属性值
            # 可以不断循环获取属性值，depart.title.xxx.xxx
            instance = getattr(instance, attr)  # 重点代码
        # 如果获取不到字段属性值就会走这个判断
        # 判断是否可调用：
        if is_simple_callable(instance): 
            # 调用的是类方法： Model._get_FIELD_display()
            instance = instance()
    return instance

class Field:
    # 该方法什么时候被调用？？
    def bind(self, field_name, parent):
        if self.source == '*':
            self.source_attrs = []
        else:
            self.source_attrs = self.source.split('.')  # 重点代码

    def get_attribute(self, instance):
        # self: 指的是字段对象
        # instance： 指的是整条数据对象
        # self.source_attrs： 获取字段名，是一个列表
        # 对模型类中的属性字段类对象中的source进行处理
        # 调用的是函数 def get_attribute(instance, attrs)
        return get_attribute(instance, self.source_attrs)  # 重点代码

class BaseSerializer(Field):
    @property
    def data(self):  # 重点代码
        # self: <class 'rest_framework.serializers.ListSerializer'>
            # CommentsSerializers([<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>], 
            # context={'request': <rest_framework.request.Request: GET '/app/comments/'>, 'format': None, 
            # 'view': <apps.viewsets.comments.CommentsViewSet object>}, many=True):
            # id = IntegerField(label='ID', read_only=True)
            # description = CharField(allow_blank=True, allow_null=True, help_text='评论内容', label='评论内容', required=False, style={'base_template': 'textarea.html'})
            # commenter = CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)
            # comment_time = DateTimeField(label='评论时间', read_only=True)
        if not hasattr(self, '_data'):
            # self.instance: [<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>]
            if self.instance is not None and not getattr(self, '_errors', None):
                # 调用的是类方法： ListSerializer.to_representation()
                # 返回列表：
                    # [OrderedDict([('id', 3), ('description', 'ccc'), ('commenter', 'hjk'), ('comment_time', '2024-07-22 18:25:40')]), 
                    # OrderedDict([('id', 2), ('description', 'aaaa'), ('commenter', 'cvb'), ('comment_time', '2024-07-22 18:07:45')]), 
                    # OrderedDict([('id', 1), ('description', 'bbaadd'), ('commenter', 'sdf'), ('comment_time', '2024-07-22 18:07:24')])]
                self._data = self.to_representation(self.instance)
            elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.validated_data)
            else:
                self._data = self.get_initial()
        return self._data

class ReturnList(list):
    def __init__(self, *args, **kwargs):
        # self: []
        # args:
            # [OrderedDict([('id', 3), ('commenter', 'hjk'), ('comment_time', '2024-07-22 18:25:40')]), 
            # OrderedDict([('id', 2), ('commenter', 'cvb'), ('comment_time', '2024-07-22 18:07:45')]), 
            # OrderedDict([('id', 1), ('commenter', 'sdf'), ('comment_time', '2024-07-22 18:07:24')])]
        # kwargs:
            # {'serializer': CommentsSerializers([<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>], 
            # context={'request': <rest_framework.request.Request: GET '/app/comments/'>, 'format': None, 'view': <apps.viewsets.comments.CommentsViewSet object>}, many=True):
            # id = IntegerField(label='ID', read_only=True)
            # description = CharField(write_only=True)
            # commenter = CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)
            # comment_time = DateTimeField(label='评论时间', read_only=True)} 
        self.serializer = kwargs.pop('serializer')
        super().__init__(*args, **kwargs)

class ListSerializer(BaseSerializer):
    @property
    def data(self):
        # self: <class 'rest_framework.serializers.ListSerializer'>
            # CommentsSerializers([<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>], 
            # context={'request': <rest_framework.request.Request: GET '/app/comments/'>, 'format': None, 
            # 'view': <apps.viewsets.comments.CommentsViewSet object>}, many=True):
            # id = IntegerField(label='ID', read_only=True)
            # description = CharField(allow_blank=True, allow_null=True, help_text='评论内容', label='评论内容', required=False, style={'base_template': 'textarea.html'})
            # commenter = CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)
            # comment_time = DateTimeField(label='评论时间', read_only=True)
        # 返回列表：
            # [OrderedDict([('id', 3), ('description', 'ccc'), ('commenter', 'hjk'), ('comment_time', '2024-07-22 18:25:40')]), 
            # OrderedDict([('id', 2), ('description', 'aaaa'), ('commenter', 'cvb'), ('comment_time', '2024-07-22 18:07:45')]), 
            # OrderedDict([('id', 1), ('description', 'bbaadd'), ('commenter', 'sdf'), ('comment_time', '2024-07-22 18:07:24')])]
        # 调用类方法： BaseSerializer.data()
        ret = super().data
        # 实例化类：<class 'rest_framework.utils.serializer_helpers.ReturnList'>
        # 返回对象
            # [OrderedDict([('id', 3), ('description', 'ccc'), ('commenter', 'hjk'), ('comment_time', '2024-07-22 18:25:40')]), 
            # OrderedDict([('id', 2), ('description', 'aaaa'), ('commenter', 'cvb'), ('comment_time', '2024-07-22 18:07:45')]), 
            # OrderedDict([('id', 1), ('description', 'bbaadd'), ('commenter', 'sdf'), ('comment_time', '2024-07-22 18:07:24')])]
        return ReturnList(ret, serializer=self)

    def to_representation(self, data):  # 重点代码
        # data==iterable: [<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>]，实际含义是获取表中需要查询的所有数据对象
        # <Comments: Comments object (3)>：表示表Comments中id为3这条数据的对象
        iterable = data.all() if isinstance(data, models.Manager) else data

        return [
            # self: <class 'rest_framework.serializers.ListSerializer'>
            # self.child: <class 'apps.viewsets.comments.CommentsSerializers'>  # 这个属性在创建序列化器类的时候赋值？？
            # self.child.to_representation(item): 调用的是类方法 Serializer.to_representation()
            # 重点代码：遍历所有数据对象，返回每条数据中所有字段的值
            self.child.to_representation(item) for item in iterable
        ]

class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            # self: <apps.viewsets.comments.CommentsViewSet object at 0x0000024AEA9127D0>
            # self.get_serializer: <bound method GenericAPIView.get_serializer of <apps.viewsets.comments.CommentsViewSet object at 0x0000024AEA9127D0>>
            # page: [<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>]
            # 返回CommentsSerializers([<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>], 
                # context={'request': <rest_framework.request.Request: GET '/app/comments/'>, 'format': None, 'view': <apps.viewsets.comments.CommentsViewSet object>}, many=True):
                # id = IntegerField(label='ID', read_only=True)
                # description = CharField(allow_blank=True, allow_null=True, help_text='评论内容', label='评论内容', required=False, style={'base_template': 'textarea.html'})
                # commenter = CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)
                # comment_time = DateTimeField(label='评论时间', read_only=True)
            # serializer: 返回类<class 'rest_framework.serializers.ListSerializer'>
            serializer = self.get_serializer(page, many=True)

            # 调用的是类 ListSerializer.data()
            # serializer.data： 返回类<class 'rest_framework.utils.serializer_helpers.ReturnList'>
                # [OrderedDict([('id', 3), ('description', 'ccc'), ('commenter', 'hjk'), ('comment_time', '2024-07-22 18:25:40')]), 
                # OrderedDict([('id', 2), ('description', 'aaaa'), ('commenter', 'cvb'), ('comment_time', '2024-07-22 18:07:45')]), 
                # OrderedDict([('id', 1), ('description', 'bbaadd'), ('commenter', 'sdf'), ('comment_time', '2024-07-22 18:07:24')])]
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


##################################### 视图类 ################################

class PKOnlyObject:
    def __init__(self, pk):
        self.pk = pk

    def __str__(self):
        return "%s" % self.pk

class OrderedDict(dict):
    pass

class Serializer(BaseSerializer, metaclass=SerializerMetaclass):
    @cached_property
    def fields(self):
        fields = BindingDict(self)
        # self.get_fields().items()： odict_items([('id', IntegerField(label='ID', read_only=True)), ('description', CharField(write_only=True)), 
            # ('commenter', CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)), 
            # ('comment_time', DateTimeField(label='评论时间', read_only=True))])
        # 实际含义是获取所有的字段对象信息
        # self.get_fields调用的是ModelSerializer.get_fields()
        for key, value in self.get_fields().items():
            fields[key] = value
        return fields

    @property
    def _readable_fields(self):  # 重点代码，读取可用的字段（根据字段对象属性值write_only进行过滤）
        # self: <class 'apps.viewsets.comments.CommentsSerializers'> 序列化器对象
        # self.fields: 
            # {'id': IntegerField(label='ID', read_only=True), 
            # 'description': CharField(write_only=True), 
            # 'commenter': CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False), 
            # 'comment_time': DateTimeField(label='评论时间', read_only=True)}
        # 不能跟代码进去，而是直接返回，原因是什么？？
        # 获取对象属性fields，应该是序列化器在初始化时，该属性fields已经保存了所有字段对象信息？？
        self.fields
        # 调用的是类方法 Mapping(Collection).values()
        # ValuesView({'id': IntegerField(label='ID', read_only=True), 'description': CharField(write_only=True), 'commenter': CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False), 'comment_time': DateTimeField(label='评论时间', read_only=True)})
        self.fields.values()
        for field in self.fields.values():
            # 如果description = serializers.CharField(write_only=True)配置了write_only=True才会返回，默认write_only=False，一开始在哪里设置了该属性值？？
            if not field.write_only:
                yield field

    # 重点代码业务逻辑
    def to_representation(self, instance):
        # self: <class 'apps.viewsets.comments.CommentsSerializers'> 类实例对象
        # instance: <Comments: Comments object (3)> 表Comments中一条数据对象，一条数据对象
        ret = OrderedDict() # 实例化类OrderedDict，是一个有序字典
        # 返回一个迭代器对象 <generator object Serializer._readable_fields at 0x0000028F811E00B0>
        # 获取的是数据库表中的字段对象
        # 获取所有的字段： CommentsSerializers._declared_fields + Meta里面fileds字段创建对象？？
        fields = self._readable_fields  # 此处不加()，原因是加了装饰器@property，但原理是什么？？

        # 遍历表中所有的字段，获取一条数据对象中所有字段对应的值
        for field in fields:
            # field：指的是每一个字段对象
            # IntegerField(label='ID', read_only=True)
            # CharField(allow_blank=True, allow_null=True, help_text='评论人名称', label='评论人名称', max_length=255, required=False)
            # DateTimeField(label='评论时间', read_only=True)
            # ChoiceField(choices=((1, '普通会员'), (2, 'VIP'), (3, 'SVIP')), label='级别', required=False, validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
            # CharField(read_only=True, source='get_level_display')
            # NestedSerializer(read_only=True):
                # 一般情况下：
                    # id = IntegerField(label='ID', read_only=True)
                    # title = CharField(label='名称', max_length=32)
                # 序列化器中配置了depth=1:
                    # NestedSerializer(read_only=True): id = IntegerField(label='ID', read_only=True) title = CharField(label='名称', max_length=32)
                    # NestedSerializer(many=True, read_only=True): id = IntegerField(label='ID', read_only=True) title = CharField(label='名称', max_length=32)
            try:
                # 获取field(数据库表中字段对象)的属性值(即数据库表中的一条数据对象对应字段的值)
                # 调用的是类方法： Field.get_attribute()
                # 当instance是外键时：
                    # PrimaryKeyRelatedField(label='部门', queryset=Department.objects.all())
                    # ManyRelatedField(allow_empty=False, child_relation=PrimaryKeyRelatedField(allow_empty=False, label='角色', queryset=Role.objects.all()), label='角色')
                # 获取对用类的 get_attribute 方法
                attribute = field.get_attribute(instance)  # 重点代码
            except SkipField:
                continue

            # 重点代码，如果没有对外键进行额外的配置，默认返回的是关联对象的id
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                # 调用字段类型对应的 to_representation()
                # class IntegerField(Field): return int(value)
                # class CharField(Field): return str(value)
                # class DateTimeField(Field): 查看对应to_representation方法
                # class PrimaryKeyRelatedField(RelatedField): return value.pk
                # class ManyRelatedField(Field): 查看多对多关系to_representation()
                # 如果是外键字段，调用的还是当前方法to_representation()
                    # 如果是外键是多对多关系，则调用类ListSerializer的to_representation()
                ret[field.field_name] = field.to_representation(attribute)

        return ret

class ModelSerializer(Serializer):

    # 重点代码
    def get_fields(self):
        """
        Return the dict of field names -> field instances that should be
        used for `self.fields` when instantiating the serializer.
        """
        # self: 序列化器实例对象 <UserInfoSerializers instance at 0x207e437fd30>
        if self.url_field_name is None:
            self.url_field_name = api_settings.URL_FIELD_NAME

        assert hasattr(self, 'Meta'), (
            'Class {serializer_class} missing "Meta" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        assert hasattr(self.Meta, 'model'), (
            'Class {serializer_class} missing "Meta.model" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        if model_meta.is_abstract_model(self.Meta.model):
            raise ValueError(
                'Cannot use ModelSerializer with Abstract Models.'
            )
        # 获取序列化器类变量中定义的那些字段对象
        # self._declared_fields 该属性在创建序列化器类时赋值
        # OrderedDict([('username', CharField()), 
                    #  ('level', CharField(read_only=True, source='get_level_display')), 
                    #  ('depart', CharField(read_only=True, source='depart.title'))])
        declared_fields = copy.deepcopy(self._declared_fields)
        # 获取模型类： <class 'apps.models.UserInfo'>
        model = getattr(self.Meta, 'model')
        # 序列化器类的Meta类中配置
        depth = getattr(self.Meta, 'depth', 0)

        if depth is not None:
            assert depth >= 0, "'depth' may not be negative."
            assert depth <= 10, "'depth' may not be greater than 10."

        # Retrieve metadata about fields & relationships on the model class.
        # from rest_framework.utils.model_meta import get_field_info
        info = model_meta.get_field_info(model)
        # 获取所有需要序列化的字段名
        field_names = self.get_field_names(declared_fields, info)

        # 对字段进行校验
        # 可以在序列化器类的Meta类中配置 extra_kwargs
        extra_kwargs = self.get_extra_kwargs()
        extra_kwargs, hidden_fields = self.get_uniqueness_extra_kwargs(
            field_names, declared_fields, extra_kwargs
        )

        # Determine the fields that should be included on the serializer.
        fields = OrderedDict()

        # 重点重点重点
        for field_name in field_names:
            # If the field is explicitly declared on the class then use that.
            if field_name in declared_fields:
                fields[field_name] = declared_fields[field_name]
                continue

            extra_field_kwargs = extra_kwargs.get(field_name, {})
            source = extra_field_kwargs.get('source', '*')
            if source == '*':
                source = field_name

            # Determine the serializer field class and keyword arguments.
            field_class, field_kwargs = self.build_field(
                source, info, model, depth
            )

            # Include any kwargs defined in `Meta.extra_kwargs`
            field_kwargs = self.include_extra_kwargs(
                field_kwargs, extra_field_kwargs
            )

            # Create the serializer field.
            fields[field_name] = field_class(**field_kwargs)

        # Add in any hidden fields.
        fields.update(hidden_fields)

        return fields

    # 重点
    def get_field_names(self, declared_fields, info):
        # declared_fields： OrderedDict([('username', CharField()), 
                                       # ('level', CharField(read_only=True, source='get_level_display')), 
                                       # ('depart', CharField(read_only=True, source='depart.title'))])
        # info：
            FieldResult(
                pk=<django.db.models.fields.BigAutoField: id>, 
                fields=OrderedDict([('level', <django.db.models.fields.IntegerField: level>), 
                    ('username', <django.db.models.fields.CharField: username>), 
                    ('password', <django.db.models.fields.CharField: password>), 
                    ('age', <django.db.models.fields.IntegerField: age>), 
                    ('email', <django.db.models.fields.CharField: email>), 
                    ('token', <django.db.models.fields.CharField: token>)]), 
                forward_relations=OrderedDict([
                    ('depart', RelationInfo(
                        model_field=<django.db.models.fields.related.ForeignKey: depart>, 
                        related_model=<class 'apps.models.Department'>, to_many=False, to_field=None, has_through_model=False, reverse=False)), 
                    ('roles', RelationInfo(
                        model_field=<django.db.models.fields.related.ManyToManyField: roles>, 
                        related_model=<class 'apps.models.Role'>, to_many=True, to_field=None, has_through_model=False, reverse=False))]), 
                reverse_relations=OrderedDict(), 
                fields_and_pk=OrderedDict([
                    ('pk', <django.db.models.fields.BigAutoField: id>), 
                    ('id', <django.db.models.fields.BigAutoField: id>), ('level', <django.db.models.fields.IntegerField: level>), 
                    ('username', <django.db.models.fields.CharField: username>), 
                    ('password', <django.db.models.fields.CharField: password>), 
                    ('age', <django.db.models.fields.IntegerField: age>), 
                    ('email', <django.db.models.fields.CharField: email>), 
                    ('token', <django.db.models.fields.CharField: token>)]), 
                relations=OrderedDict([
                    ('depart', RelationInfo(
                        model_field=<django.db.models.fields.related.ForeignKey: depart>, 
                        related_model=<class 'apps.models.Department'>, to_many=False, to_field=None, has_through_model=False, reverse=False)), 
                    ('roles', RelationInfo(
                        model_field=<django.db.models.fields.related.ManyToManyField: roles>, 
                        related_model=<class 'apps.models.Role'>, to_many=True, to_field=None, has_through_model=False, reverse=False))]))
        
        fields = getattr(self.Meta, 'fields', None)
        exclude = getattr(self.Meta, 'exclude', None)
        # ['id', 'username', 'level', 'depart', 'level', 'username', 'password', 'age', 'email', 'token', 'depart', 'roles']
        # 可以在序列化器类的Meta类中配置fields、exclude来规定哪些字段需要序列化
        fields = self.get_default_field_names(declared_fields, info)
        return fields

    def get_default_field_names(self, declared_fields, model_info):
        # 获取所有的字段键值信息
        return (
            [model_info.pk.name] +               # id值
            list(declared_fields) +              # 序列化器类中定义的字段
            list(model_info.fields) +            # 模型类中定义的字段（不包含外键）
            list(model_info.forward_relations)   # 模型类中定义的外键字段
        )

    def get_extra_kwargs(self):
        # 对序列化器类的Meta类中配置的 extra_kwargs 进行校验
        extra_kwargs = copy.deepcopy(getattr(self.Meta, 'extra_kwargs', {}))

        read_only_fields = getattr(self.Meta, 'read_only_fields', None)
        if read_only_fields is not None:
            if not isinstance(read_only_fields, (list, tuple)):
                raise TypeError(
                    'The `read_only_fields` option must be a list or tuple. '
                    'Got %s.' % type(read_only_fields).__name__
                )
            for field_name in read_only_fields:
                kwargs = extra_kwargs.get(field_name, {})
                kwargs['read_only'] = True
                extra_kwargs[field_name] = kwargs

        else:
            # Guard against the possible misspelling `readonly_fields` (used
            # by the Django admin and others).
            assert not hasattr(self.Meta, 'readonly_fields'), (
                'Serializer `%s.%s` has field `readonly_fields`; '
                'the correct spelling for the option is `read_only_fields`.' %
                (self.__class__.__module__, self.__class__.__name__)
            )

        return extra_kwargs
    # 重点代码
    def get_uniqueness_extra_kwargs(self, field_names, declared_fields, extra_kwargs):
        """
        Return any additional field options that need to be included as a
        result of uniqueness constraints on the model. This is returned as
        a two-tuple of:

        ('dict of updated extra kwargs', 'mapping of hidden fields')
        """
        if getattr(self.Meta, 'validators', None) is not None:
            return (extra_kwargs, {})

        model = getattr(self.Meta, 'model')
        model_fields = self._get_model_fields(
            field_names, declared_fields, extra_kwargs
        )

        # Determine if we need any additional `HiddenField` or extra keyword
        # arguments to deal with `unique_for` dates that are required to
        # be in the input data in order to validate it.
        unique_constraint_names = set()

        for model_field in model_fields.values():
            # Include each of the `unique_for_*` field names.
            unique_constraint_names |= {model_field.unique_for_date, model_field.unique_for_month,
                                        model_field.unique_for_year}

        unique_constraint_names -= {None}

        # Include each of the `unique_together` field names,
        # so long as all the field names are included on the serializer.
        for parent_class in [model] + list(model._meta.parents):
            for unique_together_list in parent_class._meta.unique_together:
                if set(field_names).issuperset(unique_together_list):
                    unique_constraint_names |= set(unique_together_list)

        # Now we have all the field names that have uniqueness constraints
        # applied, we can add the extra 'required=...' or 'default=...'
        # arguments that are appropriate to these fields, or add a `HiddenField` for it.
        hidden_fields = {}
        uniqueness_extra_kwargs = {}

        for unique_constraint_name in unique_constraint_names:
            # Get the model field that is referred too.
            unique_constraint_field = model._meta.get_field(unique_constraint_name)

            if getattr(unique_constraint_field, 'auto_now_add', None):
                default = CreateOnlyDefault(timezone.now)
            elif getattr(unique_constraint_field, 'auto_now', None):
                default = timezone.now
            elif unique_constraint_field.has_default():
                default = unique_constraint_field.default
            else:
                default = empty

            if unique_constraint_name in model_fields:
                # The corresponding field is present in the serializer
                if default is empty:
                    uniqueness_extra_kwargs[unique_constraint_name] = {'required': True}
                else:
                    uniqueness_extra_kwargs[unique_constraint_name] = {'default': default}
            elif default is not empty:
                # The corresponding field is not present in the
                # serializer. We have a default to use for it, so
                # add in a hidden field that populates it.
                hidden_fields[unique_constraint_name] = HiddenField(default=default)

        # Update `extra_kwargs` with any new options.
        for key, value in uniqueness_extra_kwargs.items():
            if key in extra_kwargs:
                value.update(extra_kwargs[key])
            extra_kwargs[key] = value

        return extra_kwargs, hidden_fields

    def build_field(self, field_name, info, model_class, nested_depth):
        """
        Return a two tuple of (cls, kwargs) to build a serializer field with.
        """
        if field_name in info.fields_and_pk:
            model_field = info.fields_and_pk[field_name]
            return self.build_standard_field(field_name, model_field)

        elif field_name in info.relations:
            relation_info = info.relations[field_name]
            if not nested_depth:
                return self.build_relational_field(field_name, relation_info)
            else:
                return self.build_nested_field(field_name, relation_info, nested_depth)

        elif hasattr(model_class, field_name):
            return self.build_property_field(field_name, model_class)

        elif field_name == self.url_field_name:
            return self.build_url_field(field_name, model_class)

        return self.build_unknown_field(field_name, model_class)

    def include_extra_kwargs(self, kwargs, extra_kwargs):
        """
        Include any 'extra_kwargs' that have been included for this field,
        possibly removing any incompatible existing keyword arguments.
        """
        if extra_kwargs.get('read_only', False):
            for attr in [
                'required', 'default', 'allow_blank', 'min_length',
                'max_length', 'min_value', 'max_value', 'validators', 'queryset'
            ]:
                kwargs.pop(attr, None)

        if extra_kwargs.get('default') and kwargs.get('required') is False:
            kwargs.pop('required')

        if extra_kwargs.get('read_only', kwargs.get('read_only', False)):
            extra_kwargs.pop('required', None)  # Read only fields should always omit the 'required' argument.

        kwargs.update(extra_kwargs)

        return kwargs

def _get_pk(opts):
    pk = opts.pk
    rel = pk.remote_field

    while rel and rel.parent_link:
        # If model is a child via multi-table inheritance, use parent's pk.
        pk = pk.remote_field.model._meta.pk
        rel = pk.remote_field

    return pk

def _get_fields(opts):
    fields = OrderedDict()
    for field in [field for field in opts.fields if field.serialize and not field.remote_field]:
        fields[field.name] = field

    return fields

def _get_forward_relationships(opts):
    """
    Returns an `OrderedDict` of field names to `RelationInfo`.
    """
    forward_relations = OrderedDict()
    for field in [field for field in opts.fields if field.serialize and field.remote_field]:
        forward_relations[field.name] = RelationInfo(
            model_field=field,
            related_model=field.remote_field.model,
            to_many=False,
            to_field=_get_to_field(field),
            has_through_model=False,
            reverse=False
        )

    # Deal with forward many-to-many relationships.
    for field in [field for field in opts.many_to_many if field.serialize]:
        forward_relations[field.name] = RelationInfo(
            model_field=field,
            related_model=field.remote_field.model,
            to_many=True,
            # manytomany do not have to_fields
            to_field=None,
            has_through_model=(
                not field.remote_field.through._meta.auto_created
            ),
            reverse=False
        )

    return forward_relations

def _get_reverse_relationships(opts):
    """
    Returns an `OrderedDict` of field names to `RelationInfo`.
    """
    reverse_relations = OrderedDict()
    all_related_objects = [r for r in opts.related_objects if not r.field.many_to_many]
    for relation in all_related_objects:
        accessor_name = relation.get_accessor_name()
        reverse_relations[accessor_name] = RelationInfo(
            model_field=None,
            related_model=relation.related_model,
            to_many=relation.field.remote_field.multiple,
            to_field=_get_to_field(relation.field),
            has_through_model=False,
            reverse=True
        )

    # Deal with reverse many-to-many relationships.
    all_related_many_to_many_objects = [r for r in opts.related_objects if r.field.many_to_many]
    for relation in all_related_many_to_many_objects:
        accessor_name = relation.get_accessor_name()
        reverse_relations[accessor_name] = RelationInfo(
            model_field=None,
            related_model=relation.related_model,
            to_many=True,
            # manytomany do not have to_fields
            to_field=None,
            has_through_model=(
                (getattr(relation.field.remote_field, 'through', None) is not None) and
                not relation.field.remote_field.through._meta.auto_created
            ),
            reverse=True
        )

    return reverse_relations

def _merge_fields_and_pk(pk, fields):
    fields_and_pk = OrderedDict()
    fields_and_pk['pk'] = pk
    fields_and_pk[pk.name] = pk
    fields_and_pk.update(fields)

    return fields_and_pk

def _merge_relationships(forward_relations, reverse_relations):
    return OrderedDict(
        list(forward_relations.items()) +
        list(reverse_relations.items())
    )

def get_field_info(model):
    # model: <class 'apps.models.UserInfo'>
    # opts: <Options for UserInfo>
    opts = model._meta.concrete_model._meta
    # <django.db.models.fields.BigAutoField: id>
    pk = _get_pk(opts)
    # OrderedDict([('level', <django.db.models.fields.IntegerField: level>), 
                #  ('username', <django.db.models.fields.CharField: username>), 
                #  ('password', <django.db.models.fields.CharField: password>), 
                #  ('age', <django.db.models.fields.IntegerField: age>), 
                #  ('email', <django.db.models.fields.CharField: email>), 
                #  ('token', <django.db.models.fields.CharField: token>)])
    fields = _get_fields(opts)
    # OrderedDict([('depart', RelationInfo(model_field=<django.db.models.fields.related.ForeignKey: depart>, 
                        # related_model=<class 'apps.models.Department'>, to_many=False, to_field=None, has_through_model=False, reverse=False)), 
                 # ('roles', RelationInfo(model_field=<django.db.models.fields.related.ManyToManyField: roles>, 
                        # related_model=<class 'apps.models.Role'>, to_many=True, to_field=None, has_through_model=False, reverse=False))])
    forward_relations = _get_forward_relationships(opts)
    # OrderedDict()
    reverse_relations = _get_reverse_relationships(opts)
    # OrderedDict([('pk', <django.db.models.fields.BigAutoField: id>), 
                #  ('id', <django.db.models.fields.BigAutoField: id>), 
                #  ('level', <django.db.models.fields.IntegerField: level>), 
                #  ('username', <django.db.models.fields.CharField: username>), 
                #  ('password', <django.db.models.fields.CharField: password>), 
                #  ('age', <django.db.models.fields.IntegerField: age>), 
                #  ('email', <django.db.models.fields.CharField: email>), 
                #  ('token', <django.db.models.fields.CharField: token>)])
    fields_and_pk = _merge_fields_and_pk(pk, fields)
    # OrderedDict([('depart', RelationInfo(model_field=<django.db.models.fields.related.ForeignKey: depart>, 
                        # related_model=<class 'apps.models.Department'>, to_many=False, to_field=None, has_through_model=False, reverse=False)), 
                 # ('roles', RelationInfo(model_field=<django.db.models.fields.related.ManyToManyField: roles>, 
                        # related_model=<class 'apps.models.Role'>, to_many=True, to_field=None, has_through_model=False, reverse=False))])
    relationships = _merge_relationships(forward_relations, reverse_relations)

    return FieldInfo(pk, fields, forward_relations, reverse_relations,
                     fields_and_pk, relationships)

from rest_framework import serializers
class CommentsSerializers(serializers.ModelSerializer):
    level = serializers.CharField(source="get_level_display", read_only=True)
    depart = serializers.CharField(source="depart.title", read_only=True)

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


1. source="get_level_display" 源码的实现原理
2. 配置depth = 1生效的源码原理
