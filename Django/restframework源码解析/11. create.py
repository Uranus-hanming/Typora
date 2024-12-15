
############################### 各种字段类 ##################################

class Field:
	# 对字段进行各种校验？？
    def run_validators(self, value):
        errors = []
        for validator in self.validators:
            try:
                if getattr(validator, 'requires_context', False):
                    validator(value, self)
                else:
                    validator(value)
            except ValidationError as exc:
                # If the validation error contains a mapping of fields to
                # errors then simply raise it immediately rather than
                # attempting to accumulate a list of errors.
                if isinstance(exc.detail, dict):
                    raise
                errors.extend(exc.detail)
            except DjangoValidationError as exc:
                errors.extend(get_error_detail(exc))
        if errors:
            raise ValidationError(errors)

    def run_validation(self, data=empty):
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = self.to_internal_value(data)
        self.run_validators(value)
        return value
        

class CharField(Field):
    def run_validation(self, data=empty):
        if data == '' or (self.trim_whitespace and str(data).strip() == ''):
            if not self.allow_blank:
                self.fail('blank')
            return ''
        return super().run_validation(data)

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data)
        return value.strip() if self.trim_whitespace else value

    def to_representation(self, value):
        return str(value)


class IntegerField(Field):
    def to_representation(self, value):
        return int(value)


class SerializerMethodField(Field):
    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        # 重点，调用自定义的方法
        return method(value)


class DateTimeField(Field):
    def to_representation(self, value):
        if not value:
            return None

        # 重点，自定义时间格式
        output_format = getattr(self, 'format', api_settings.DATETIME_FORMAT)

        if output_format is None or isinstance(value, str):
            return value

        value = self.enforce_timezone(value)

        if output_format.lower() == ISO_8601:
            value = value.isoformat()
            if value.endswith('+00:00'):
                value = value[:-6] + 'Z'
            return value
        return value.strftime(output_format)


class ChoiceField(Field):
    def to_representation(self, value):
        if value in ('', None):
            return value
        return self.choice_strings_to_values.get(str(value), value)



################################# 序列化器类 #############################

class SerializerMetaclass(type):
	pass


class Field:
    def __init__(self, *, read_only=False, write_only=False,
                 required=None, default=empty, initial=empty, source=None,
                 label=None, help_text=None, style=None,
                 error_messages=None, validators=None, allow_null=False):
        self._creation_counter = Field._creation_counter
        Field._creation_counter += 1

        # If `required` is unset, then use `True` unless a default is provided.
        if required is None:
            required = default is empty and not read_only

        # Some combinations of keyword arguments do not make sense.
        assert not (read_only and write_only), NOT_READ_ONLY_WRITE_ONLY
        assert not (read_only and required), NOT_READ_ONLY_REQUIRED
        assert not (required and default is not empty), NOT_REQUIRED_DEFAULT
        assert not (read_only and self.__class__ == Field), USE_READONLYFIELD

        self.read_only = read_only  # False
        self.write_only = write_only  # False
        self.required = required  # True
        self.default = default  # <class 'rest_framework.fields.empty'>
        self.source = source  # None
        self.initial = self.initial if (initial is empty) else initial  # None
        self.label = label  # None
        self.help_text = help_text  # None
        self.style = {} if style is None else style  # {}
        self.allow_null = allow_null  # False

        if self.default_empty_html is not empty:
            if default is not empty:
                self.default_empty_html = default

        if validators is not None:
            self.validators = list(validators)

        # These are set up by `.bind()` when the field is added to a serializer.
        self.field_name = None
        self.parent = None

        # Collect default error message from self and parent classes
        # {'invalid': '无效数据。期待为字典类型，得到的是 {datatype} 。', 'null': '该字段不能为 null。', 'required': '该字段是必填项。'}
        messages = {}
        for cls in reversed(self.__class__.__mro__):
            messages.update(getattr(cls, 'default_error_messages', {}))
        messages.update(error_messages or {})
        self.error_messages = messages

    def __new__(cls, *args, **kwargs):
        # cls: <class 'bk_power.ecology.viewsets.bug_record.BugRecordSerializer'> 序列化器类

        # instance: <BugRecordSerializer instance at 0x1c03faa3d60> 序列化器类实例
        instance = super().__new__(cls)  # 将类进行实例，但是还没有进行初始化，所以还不是对象？？
        # 给实例赋值
        instance._args = args
        instance._kwargs = kwargs
        # 返回创建好的实例，即序列化器类实例
        return instance

    def validate_empty_values(self, data):
        if self.read_only:
            return (True, self.get_default())

        if data is empty:
            if getattr(self.root, 'partial', False):
                raise SkipField()
            if self.required:
                self.fail('required')
            return (True, self.get_default())

        if data is None:
            if not self.allow_null:
                self.fail('null')
            # Nullable `source='*'` fields should not be skipped when its named
            # field is given a null value. This is because `source='*'` means
            # the field is passed the entire object, which is not null.
            elif self.source == '*':
                return (False, None)
            return (True, None)

        return (False, data)

    def get_value(self, dictionary):
        """
        Given the *incoming* primitive data, return the value for this field
        that should be validated and transformed to a native value.
        """
        if html.is_html_input(dictionary):
            # HTML forms will represent empty fields as '', and cannot
            # represent None or False values directly.
            if self.field_name not in dictionary:
                if getattr(self.root, 'partial', False):
                    return empty
                return self.default_empty_html
            ret = dictionary[self.field_name]
            if ret == '' and self.allow_null:
                # If the field is blank, and null is a valid value then
                # determine if we should use null instead.
                return '' if getattr(self, 'allow_blank', False) else None
            elif ret == '' and not self.required:
                # If the field is blank, and emptiness is valid then
                # determine if we should use emptiness instead.
                return '' if getattr(self, 'allow_blank', False) else empty
            return ret
        # 返回json中对应字段的值
        return dictionary.get(self.field_name, empty)


class BaseSerializer(Field):
    def __init__(self, instance=None, data=empty, **kwargs):
    	# self: 序列化器类实例对象
    	# instance: None
    	# data: json数据
    	# kwargs： {'context': {'format': None, 'request': <rest_framework.request.Request: POST '/api/v1/bug_record/'>, 'view': <bk_power.ecology.viewsets.bug_record.BugRecordViewSet object at 0x000001C03F9B8340>}}

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

    def is_valid(self, *, raise_exception=False):
        assert hasattr(self, 'initial_data'), (
            'Cannot call `.is_valid()` as no `data=` keyword argument was '
            'passed when instantiating the serializer instance.'
        )

        if not hasattr(self, '_validated_data'):
            try:
            	# 重点
            	# self: 序列化器类对象？？
            	# self.initial_data: json数据
            	# 调用类方法：Serializer.run_validation()
            	# 返回： 
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}
                self._errors = exc.detail
            else:
                self._errors = {}

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)

	# 重点函数
	@property
    def data(self):
        if hasattr(self, 'initial_data') and not hasattr(self, '_validated_data'):
            msg = (
                'When a serializer is passed a `data` keyword argument you '
                'must call `.is_valid()` before attempting to access the '
                'serialized `.data` representation.\n'
                'You should either call `.is_valid()` first, '
                'or access `.initial_data` instead.'
            )
            raise AssertionError(msg)

        if not hasattr(self, '_data'):
            if self.instance is not None and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.instance)
            elif hasattr(self, '_validated_data') and not getattr(self, '_errors', None):
                self._data = self.to_representation(self.validated_data)
            else:
                self._data = self.get_initial()
        return self._data


def set_value(dictionary, keys, value):
    """
    Similar to Python's built in `dictionary[key] = value`,
    but takes a list of nested keys instead of a single key.

    set_value({'a': 1}, [], {'b': 2}) -> {'a': 1, 'b': 2}
    set_value({'a': 1}, ['x'], 2) -> {'a': 1, 'x': 2}
    set_value({'a': 1}, ['x', 'y'], 2) -> {'a': 1, 'x': {'y': 2}}
    """
    if not keys:
        dictionary.update(value)
        return

    for key in keys[:-1]:
        if key not in dictionary:
            dictionary[key] = {}
        dictionary = dictionary[key]

    dictionary[keys[-1]] = value


class Serializer(BaseSerializer, metaclass=SerializerMetaclass):

	@property
    def _writable_fields(self):
        for field in self.fields.values():
            if not field.read_only:
                yield field

    def to_internal_value(self, data):
        ret = OrderedDict()
        errors = OrderedDict()
        fields = self._writable_fields
        # 重点
        for field in fields:
        	# 获取方法： validate_字段名
            validate_method = getattr(self, 'validate_' + field.field_name, None)
            # 调用类方法： Field.get_value()
            # 返回： 获取json中对应字段的值
            primitive_value = field.get_value(data)
            try:
            	# 重点: 校验的核心逻辑代码入口
            	# 调用字段对象对应类的方法，如： CharField.run_validation() IntegerField DateTimeField ...
            	# 返回： 对初始值进行校验，返回校验后的值
                validated_value = field.run_validation(primitive_value)
                if validate_method is not None:
                	# 重点： 执行自定义的 validate_字段名 方法
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                errors[field.field_name] = exc.detail
            except DjangoValidationError as exc:
                errors[field.field_name] = get_error_detail(exc)
            except SkipField:
                pass
            else:
            	# ret: OrderedDict()
            	# field.source_attrs: ['platform'] 对应的字段名列表
            	# validated_value: '1,2,3' 校验后的有效值
                set_value(ret, field.source_attrs, validated_value)

        if errors:
            raise ValidationError(errors)
        # OrderedDict([('platform', '1,2,3'), ('manufacturer', '中电金信'), ('project', '合作888'), ('title', '事故01'), ('bug_time', datetime.datetime(2022, 7, 30, 0, 0)), ('bug_level', 3), ('phase', 2), ('during', 56), ('affect', '10000'), ('option_to', '无舆论'), ('economic', '6666'), ('deal', ''), ('analysis', ''), ('refer_to', '1'), ('summary', ''), ('image', 'xxx.png'), ('label', '1,4')])
        return ret

    def run_validators(self, value):
        """
        Add read_only fields with defaults to value before running validators.
        """
        if isinstance(value, dict):
            to_validate = self._read_only_defaults()
            to_validate.update(value)
        else:
            to_validate = value
        super().run_validators(to_validate)

    def run_validation(self, data=empty):
        # self: 序列化器类对象？？
        # data: json数据
        # 调用类方法： Field.validate_empty_values()
        # is_empty_value=False
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        # 调用类方法： Serializer.to_internal_value()
        # 返回： OrderedDict([('platform', '1,2,3'), ('manufacturer', '中电金信'), ('project', '合作888'), ('title', '事故01'), ('bug_time', datetime.datetime(2022, 7, 30, 0, 0)), ('bug_level', 3), ('phase', 2), ('during', 56), ('affect', '10000'), ('option_to', '无舆论'), ('economic', '6666'), ('deal', ''), ('analysis', ''), ('refer_to', '1'), ('summary', ''), ('image', 'xxx.png'), ('label', '1,4')])
        value = self.to_internal_value(data)
        try:
            self.run_validators(value)
            value = self.validate(value)
            assert value is not None, '.validate() should return the validated data'
        except (ValidationError, DjangoValidationError) as exc:
            raise ValidationError(detail=as_serializer_error(exc))

        return value

    # 最重要的函数
    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
            	# 重点
            	# 调用各种字段类的 to_representation()
                ret[field.field_name] = field.to_representation(attribute)

        return ret


	@property
    def data(self):
        ret = super().data
        return ReturnDict(ret, serializer=self)


class ModelSerializer(Serializer):
	pass


class BugRecordSerializer(serializers.ModelSerializer):
    bug_level_info = serializers.CharField(source="get_bug_level_display", read_only=True)
    phase_info = serializers.CharField(source="get_phase_display", read_only=True)
    during = serializers.CharField()
    platform_info = serializers.SerializerMethodField()
    label_info = serializers.SerializerMethodField()
    refer_info = serializers.SerializerMethodField()
    during_info = serializers.SerializerMethodField()


#################################### 视图类 ###############################


class GenericAPIView(views.APIView):

    def get_serializer_class(self):
    	# self: <bk_power.ecology.viewsets.bug_record.BugRecordViewSet object at 0x000001C03F9B8340>
    	# 返回视图类BugRecordViewSet属性serializer_class，即序列化器类
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
    	# self:<bk_power.ecology.viewsets.bug_record.BugRecordViewSet object at 0x000001C03F9B8340>
    	# args:()
    	# kwargs:前端传来的json数据

    	# 获取序列化器类
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        # 实例化序列化器，先调用类方法 BaseSerializer.__new__() 再调用 Field.__new__() 创建序列化器类对象
        # 最后调用类方法 BaseSerializer.__init__() 和 Field.__init__() 对实例进行初始化
        return serializer_class(*args, **kwargs)


class CreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
    	# type(self): <class 'bk_power.ecology.viewsets.bug_record.BugRecordViewSet'>
    	# self: <bk_power.ecology.viewsets.bug_record.BugRecordViewSet object at 0x000001C03F9BB490> 序列化器类对象
    	# request: <rest_framework.request.Request: POST '/api/v1/bug_record/'>
    	# args: ()
    	# kwargs: {}

    	# request.data: 前端传来的json数据
    	# self.get_serializer 是方法: <bound method GenericAPIView.get_serializer of <bk_power.ecology.viewsets.bug_record.BugRecordViewSet object at 0x000001C03F9BB490>>
        # type(serializer): <class 'bk_power.ecology.viewsets.bug_record.BugRecordSerializer'>
        # serializer: 是什么？？也是对象？？
        	# BugRecordSerializer(context={'request': <rest_framework.request.Request: POST '/api/v1/bug_record/'>, 'format': None, 'view': <bk_power.ecology.viewsets.bug_record.BugRecordViewSet object>}, data={'label': '1,4', 'bug_time': '2022-07-30 00:00:00', 'bug_level': 3, 'phase': 2, 'platform': '1,2,3', 'manufacturer': '中电金信', 'project': '合作888', 'title': '事故01', 'during': 56, 'affect': '10000', 'option_to': '无舆论', 'economic': '6666', 'deal': '', 'analysis': '', 'refer_to': 1, 'summary': '', 'image': 'xxx.png'}):
			    # id = IntegerField(label='ID', read_only=True)
			    # platform = CharField(allow_blank=True, allow_null=True, help_text='影响平台', label='影响平台', max_length=128, required=False)
			    # platform_info = SerializerMethodField()
			    # created_by = CharField(allow_blank=True, label='创建者', max_length=64, required=False)
			    # created_at = DateTimeField(allow_null=True, label='创建时间', read_only=True)
			    # updated_by = CharField(allow_blank=True, label='更新者', max_length=64, required=False)
			    # updated_at = DateTimeField(label='更新时间', read_only=True)
			    # manufacturer = CharField(allow_blank=True, allow_null=True, help_text='厂商', label='厂商', max_length=128, required=False)
			    # project = CharField(allow_blank=True, allow_null=True, help_text='项目', label='项目', max_length=128, required=False)
			    # title = CharField(allow_blank=True, allow_null=True, help_text='标题', label='标题', max_length=128, required=False)
			    # bug_time = DateTimeField(allow_null=True, help_text='bug时间', label='Bug时间', required=False)
			    # bug_level_info = CharField(read_only=True, source='get_bug_level_display')
			    # bug_level = ChoiceField(choices=((1, '一级事故'), (2, '二级事故'), (3, '三级事故'), (4, '致命BUG'), (5, '严重BUG'), (6, '一般BUG')), help_text='bug等级', label='Bug等级', required=False, validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
			    # phase = ChoiceField(choices=((1, '小范围测试'), (2, '一测'), (3, '二测'), (4, '三测'), (5, '公测')), help_text='发生阶段', label='发生阶段', required=False, validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
			    # phase_info = CharField(read_only=True, source='get_phase_display')
			    # during = CharField()
			    # during_info = SerializerMethodField()
			    # affect = CharField(allow_blank=True, allow_null=True, help_text='影响用户数', label='影响用户数', max_length=128, required=False)
			    # option_to = CharField(allow_blank=True, allow_null=True, help_text='舆论导向', label='舆论导向', max_length=128, required=False)
			    # economic = CharField(allow_blank=True, allow_null=True, help_text='经济损失', label='经济损失', max_length=128, required=False)
			    # deal = CharField(allow_blank=True, allow_null=True, help_text='处理过程', label='处理过程', required=False, style={'base_template': 'textarea.html'})
			    # analysis = CharField(allow_blank=True, allow_null=True, help_text='成因分析', label='成因分析', required=False, style={'base_template': 'textarea.html'})
			    # refer_to = CharField(allow_blank=True, allow_null=True, help_text='涉及职能', label='涉及职能', max_length=128, required=False)
			    # refer_info = SerializerMethodField()
			    # summary = CharField(allow_blank=True, allow_null=True, help_text='bug总结', label='Bug总结', required=False, style={'base_template': 'textarea.html'})
			    # image = CharField(allow_blank=True, allow_null=True, label='头像', max_length=2048, required=False)
			    # label = CharField(allow_blank=True, allow_null=True, help_text='标签', label='标签', max_length=128, required=False)
			    # label_info = SerializerMethodField()
			    # permission = ChoiceField(choices=((1, '仅厂商内可见'), (2, '外部可见（简略信息）'), (3, '外部可见（详细信息）')), help_text='用户权限', label='用户权限', required=False, validators=[<django.core.validators.MinValueValidator object>, <django.core.validators.MaxValueValidator object>])
			    # company_id = ReadOnlyField()

        serializer = self.get_serializer(data=request.data)

        # 调用类方法: BaseSerializer.is_valid()
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # 调用类方法 Serializer.data()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
