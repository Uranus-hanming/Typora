
class Field:
	creation_counter = 0

    default_error_messages = {
        'required': _('This field is required.'),
        'null': _('This field may not be null.')
    }
    default_validators = []
    default_empty_html = empty
    initial = None

** 1.3x
    # 初始化类对象，目的是给对象添加初始的属性值
    # 了解配置这些属性的含义？？
    def __init__(self, *, read_only=False, write_only=False,
                 required=None, default=empty, initial=empty, source=None,
                 label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False):
    	# self: CharField()
    	# 做计数标记，方便后续使用
        self._creation_counter = Field._creation_counter
        Field._creation_counter += 1

        # If `required` is unset, then use `True` unless a default is provided.
        # required没有配置则默认是True
        if required is None:
            required = default is empty and not read_only

        # Some combinations of keyword arguments do not make sense.
        # 两个不能同时配置，做冲突判断处理
        assert not (read_only and write_only), NOT_READ_ONLY_WRITE_ONLY
        assert not (read_only and required), NOT_READ_ONLY_REQUIRED
        assert not (required and default is not empty), NOT_REQUIRED_DEFAULT
        assert not (read_only and self.__class__ == Field), USE_READONLYFIELD

        # 为对象赋值属性
        self.read_only = read_only  # read_only: 序列化时才对该字段进行处理
        self.write_only = write_only  # write_only: 只在反序列化时才使用该字段
        self.required = required  # required: 要求在反序列化时是否需要给该字段传值
        self.default = default  # default: 设置默认值？？
        self.source = source  # source: ??
        self.initial = self.initial if (initial is empty) else initial
        self.label = label
        self.help_text = help_text
        self.style = {} if style is None else style
        self.allow_null = allow_null  # allow_null: 允许在反序列化时该字段是否为空？？

        if self.default_empty_html is not empty:
            if default is not empty:
                self.default_empty_html = default

        if validators is not None:  # validators: ??
            self.validators = list(validators)

        # These are set up by `.bind()` when the field is added to a serializer.
        self.field_name = None
        self.parent = None

        # Collect default error message from self and parent classes
        messages = {}  # 配置报错信息??
        # {'required': 'This field is required.', 'null': 'This field may not be null.', 
         # 'invalid': 'Not a valid string.', 'blank': 'This field may not be blank.', 
         # 'max_length': 'Ensure this field has no more than {max_length} characters.', 
         # 'min_length': 'Ensure this field has at least {min_length} characters.'}
        for cls in reversed(self.__class__.__mro__):
            messages.update(getattr(cls, 'default_error_messages', {}))
        messages.update(error_messages or {})
        self.error_messages = messages

** 1.1
    def __new__(cls, *args, **kwargs):
        """
        When a field is instantiated, we store the arguments that were used,
        so that we can present a helpful representation of the object.
        """
        # <class 'rest_framework.fields.CharField'>
        # args: ()
        # kwargs: {'write_only': True}

        # 创建实例对象：<CharField instance at 0x1707adc86d0>
        # 实例对象拥有的属性： 类CharField属性 + 类Field属性 + 传来的参数args/kwargs
        instance = super().__new__(cls)
        # 为实例对象赋值属性
        # ()
        instance._args = args
        # 为实例对象复制属性
        # {}
        instance._kwargs = kwargs
        # 返回实例对象
        return instance

class CharField(Field):
** 1.2
    # 初始化类对象，目的是给对象添加初始的属性值
    def __init__(self, **kwargs):  # 了解这些属性的作用？？
    	# self: <CharField instance at 0x1707adc86d0> CharField类对象
        # kwargs: {'write_only': True}
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        self.max_length = kwargs.pop('max_length', None)
        self.min_length = kwargs.pop('min_length', None)
** 1.3
        # 调用父类 Field 方法 __init__()
        super().__init__(**kwargs)
        if self.max_length is not None:
            message = lazy_format(self.error_messages['max_length'], max_length=self.max_length)
            self.validators.append(
                MaxLengthValidator(self.max_length, message=message))
        if self.min_length is not None:
            message = lazy_format(self.error_messages['min_length'], min_length=self.min_length)
            self.validators.append(
                MinLengthValidator(self.min_length, message=message))
        # 目的是什么？？
        self.validators.append(ProhibitNullCharactersValidator())
        self.validators.append(ProhibitSurrogateCharactersValidator())

#################### 序列化器类 ######################

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
        # We override this method in order to automatically create
        # `ListSerializer` classes instead when `many=True` is set.
        if kwargs.pop('many', False):
            return cls.many_init(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)

class SerializerMetaclass(type):
    @classmethod
    def _get_declared_fields(cls, bases, attrs):
    	# cls: <class 'rest_framework.serializers.SerializerMetaclass'>
    	# bases: (<class 'rest_framework.serializers.ModelSerializer'>,)
    	# attrs: field_name, attrs
    		# {'__module__': 'apps.viewsets.user_info',  # 代码所在文件路径
    		# '__qualname__': 'UserInfoSerializers',     # 序列化器类
    		# 'username': CharField(), 
    		# 'level': CharField(read_only=True, source='get_level_display'), 
    		# 'depart': CharField(read_only=True, source='depart.title'), 
    		# 'Meta': <class 'apps.viewsets.user_info.UserInfoSerializers.Meta'>}  # 序列化器类中的Meta类
        
    	# 收集所有父类是继承了Field类的属性，即序列化器类中定义的所有字段属性
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, Field)]
        # 可以改写为：
        fields = []
        # 这里list(attrs.items())，目的是为了拷贝一份字典
        for field_name, obj in list(attrs.items()):
            if isinstance(obj, Field):
                fields.append((field_name, attrs.pop(field_name)))

        # 排序  
        fields.sort(key=lambda x: x[1]._creation_counter)

        # Ensures a base class field doesn't override cls attrs, and maintains
        # field precedence when inheriting multiple parents. e.g. if there is a
        # class C(A, B), and A and B both define 'field', use 'field' from A.
        # 去重
        known = set(attrs)

        def visit(name):
            known.add(name)
            return name
        # 重点代码
        # 
        base_fields = [
            (visit(name), f)
            for base in bases if hasattr(base, '_declared_fields')
            for name, f in base._declared_fields.items() if name not in known
        ]
        # 可以改写为：
        base_fields = []
        for base in bases:
            if hasattr(base, '_declared_fields'):
                for name, f in base._declared_fields.items():
                    if name not in known:
                        base_fields.append((visit(name), f))

        return OrderedDict(base_fields + fields)

** 2x
    def __new__(cls, name, bases, attrs):
    	# cls: <class 'rest_framework.serializers.SerializerMetaclass'>
    	# name: 'UserInfoSerializers'
    	# bases: (<class 'rest_framework.serializers.ModelSerializer'>,)
    	# attrs: 包含序列化器类UserInfoSerializers所有属性，包括Meta类（Meta类也可以看成属于序列化器类UserInfoSerializers的一个属性）
    		# {'__module__': 'apps.viewsets.user_info',  # 代码所在文件路径
    		# '__qualname__': 'UserInfoSerializers',     # 序列化器类
    		# 'username': CharField(), 
    		# 'level': CharField(read_only=True, source='get_level_display'), 
    		# 'depart': CharField(read_only=True, source='depart.title'), 
    		# 'Meta': <class 'apps.viewsets.user_info.UserInfoSerializers.Meta'>}  # 序列化器类中的Meta类
** 2.1
        # 调用元类 SerializerMetaclass 的方法 _get_declared_fields()
        attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs)
        # 返回创建好的序列化器类对象：<class 'apps.viewsets.user_info.UserInfoSerializers'>
        return super().__new__(cls, name, bases, attrs)


##################### 序列化器 ###################

class SerializerMetaclass(type):
    pass

# 创建类时，先调用元类的__new__()
class Serializer(BaseSerializer, metaclass=SerializerMetaclass):
	default_error_messages = {'invalid': _('Invalid data. Expected a dictionary, but got {datatype}.')}

class ModelSerializer(Serializer):
	pass

** 2
# 创建序列化器类对象，调用元类 SerializerMetaclass 方法 __new__()
class UserInfoSerializers(serializers.ModelSerializer):
** 1
    # 实例化类 CharField，先调用父类 Field 的 __new__()，再调用类 CharField 的 __init__()
    username = serializers.CharField(write_only=True)
    level = serializers.CharField(source="get_level_display", read_only=True)
    depart = serializers.CharField(source="depart.title", read_only=True)

    class Meta:
        model = UserInfo
        fields = "__all__"
        # depth = 1

实例化对象分两步
    1. 第一步，先创建对象本身，一般调用元类的 __new__()
    2. 第二步，初始化对象，目的是给对象配置一些初始的属性值，调用的是类方法 __init__()

