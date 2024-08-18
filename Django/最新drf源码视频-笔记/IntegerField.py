def get_attribute(instance, attrs):
	["depart", "title", "xxx", "xxx"]
	for attr in attrs:
		if isinstance(instance, Mapping):
			instance = instance[attr]
	    else:
	        instance = getattr(instance, attr)	# 循环赋值，可以不断.下去，source="depart.title"
	    if is_simple_callable(instance):
	        instance = instance()	# source="get_gender_display"
    return instance

class Field:
	_creation_counter = 0

	def __init__(self, *, source，...):
		self._creation_counter = Field._creation_counter
		self.source = source
        Field._creation_counter += 1

    def bind(self, field_name, parent):
        if self.source == '*':
            self.source_attrs = []
        else:
            self.source_attrs = self.source.split('.')

    def get_attribute(self, instance):
    	return get_attribute(instance, self.source_attrs) # ["depart", "title"] # instance.depart.title
 
class IntegerField(Field):
	def __init__(self, **kwargs):
		...
		self.max_value = 111
		super().__init__(**kwargs)

    def to_representation(self, value):
    return int(value)

class CharField(Field):
	def __init__(self, **kwargs):
		self.allow_blank = False
		super().__init__(**kwargs)

    def to_representation(self, value):
    return str(value)


id = serializers.IntegerField() 	# {max_value:111,     _creation_counter:0, source="id"}
title = serializers.CharField() 	# {allow_blank:False, _creation_counter:1, source="title"}
order = serializers.IntegerField()  # {max_value:111,     _creation_counter:2, source="order"}



class SerializerMetaclass(type):
    @classmethod
    def _get_declared_fields(cls, bases, attrs):
    	# fields = [("id", 对象), ("title", 对象), ("count", 对象)]
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, Field)]

        # 自己类中字段对象 排序 [("id", 对象), ("title", 对象), ("count", 对象)]
        fields.sort(key=lambda x: x[1]._creation_counter)
        # Ensures a base class field doesn't override cls attrs, and maintains
        # field precedence when inheriting multiple parents. e.g. if there is a
        # class C(A, B), and A and B both define 'field', use 'field' from A.
        known = set(attrs) # 解决字段重复问题

        def visit(name):
            known.add(name)
            return name

        base_fields = [
            (visit(name), f)
            for base in bases if hasattr(base, '_declared_fields') # 找父类中的字段对象
            for name, f in base._declared_fields.items() if name not in known
        ]
        # [(xx, 对象)] + [("id", 对象), ("title", 对象), ("count", 对象)]
        return OrderedDict(base_fields + fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs) # {自己的字段对象 + 父类字段对象}
        # 创建类
        return super().__new__(cls, name, bases, attrs)

class BaseSerializer(Field):
    def __init__(self, instance=None, data=empty, **kwargs):
    self.instance = instance
    ...

    def __new__(cls, *args, **kwargs):
	    # We override this method in order to automatically create
	    # `ListSerializer` classes instead when `many=True` is set.
	    if kwargs.pop('many', False):
	        return cls.many_init(*args, **kwargs)
	    return super().__new__(cls, *args, **kwargs) # -> 当前类的对象

	@classmethod
    def many_init(cls, *args, **kwargs):
    	# cls表示当前类UserSerializer，括号()表示实例化
    	child_serializer = cls(*args, **kwargs) # obj = UserSerializer()
    	list_kwargs = {
            'child': child_serializer,
        }
    	meta = getattr(cls, 'Meta', None)
        list_serializer_class = getattr(meta, 'list_serializer_class', ListSerializer)
        return list_serializer_class(*args, **list_kwargs)  # 实例化 ListSerializer( obj = UserSerializer() )

    @property
    def data(self):
        if not hasattr(self, '_data'):
            if self.instance is not None and not getattr(self, '_errors', None):

            	# 序列化功能
                self._data = self.to_representation(self.instance)
            elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.validated_data)
            else:
                self._data = self.get_initial()
        return self._data

class Serializer(BaseSerializer, metaclass=SerializerMetaclass):
	@property
    def data(self):
        ret = super().data
        return ReturnDict(ret, serializer=self)

    @cached_property
    def fields(self):
        fields = BindingDict(self)
        # self.get_fields()返回所有的字段：InfoSerializer._declared_fields + Meta里面fileds字段创建对象
        for key, value in self.get_fields().items():
            fields[key] = value
        return fields

    @property
    def _readable_fields(self):
        for field in self.fields.values():
            if not field.write_only:
                yield field

    def to_representation(self, instance):
	    """
	    Object instance -> Dict of primitive datatypes.
	    """
	    ret = OrderedDict()
	    # 获取所有的字段：InfoSerializer._declared_fields + Meta里面fileds字段创建对象
	    fields = self._readable_fields

	    # 循环所有的字段对象，
	    for field in fields:
            attribute = field.get_attribute(instance) # 获取数据库中字段原始的值
            """
            ctime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
            class DateTimeField(Field):
            	def to_representation(self, value):
            		# 可以在setting.py中全局配置：REST_FRAMEWORK = {'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S"}
            		output_format = getattr(self, 'format', api_settings.DATETIME_FORMAT)
            """
            ret[field.field_name] = field.to_representation(attribute)

	    return ret

class ModelSerializer(Serializer):
	def get_fields(self):
		# 获取在类变量中定义的那些字段对象
        declared_fields = copy.deepcopy(self._declared_fields)

        # 数据库表=类 model = models.UserInfo
        model = getattr(self.Meta, 'model')
        # depth = getattr(self.Meta, 'depth', 0)

        # if depth is not None:
        #     assert depth >= 0, "'depth' may not be negative."
        #     assert depth <= 10, "'depth' may not be greater than 10."

        # Retrieve metadata about fields & relationships on the model class.
        info = model_meta.get_field_info(model)
        field_names = self.get_field_names(declared_fields, info)

        # Determine any extra field arguments and hidden fields that
        # should be included
        extra_kwargs = self.get_extra_kwargs()
        extra_kwargs, hidden_fields = self.get_uniqueness_extra_kwargs(
            field_names, declared_fields, extra_kwargs
        )

        # Determine the fields that should be included on the serializer.
        fields = OrderedDict()

        for field_name in field_names:

            # Determine the serializer field class and keyword arguments.
            field_class, field_kwargs = self.build_field(
                source, info, model, depth
            )

            # Create the serializer field.
            fields[field_name] = field_class(**field_kwargs)

        # Add in any hidden fields.
        fields.update(hidden_fields)

        return fields

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
	    model = Depart
	    fields = "__all__"


