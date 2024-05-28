class BaseSerializer(Field):
    @property
    def data(self):
        self._data = self.to_representation(self.validated_data)
        return self._data

class Serializer(BaseSerializer, metaclass=SerializerMetaclass):
    @property
    def data(self):
        ret = super().data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, instance):
    ret = OrderedDict()
    # [CharField字段对象，SerializerMethodField字段对象(method_name)，] # 内部会执行bind方法
    fields = self._readable_fields # 找到所有的字段，筛选出可以读取（可序列化） => read_only + 啥都没有 <=> 没有写write_only => 字段对象

    for field in fields:
        attribute = field.get_attribute(instance)   # CharFile字段对象.get_attribute()  instance.xxx.xxx.xxx SerializerMethodField字段对象(method_name).xxx -> None
        ret[field.field_name] = field.to_representation(attribute)

    return ret


class ModelSerializer(Serializer):
    pass


class NbModelSerializer(serializers.ModelSerializer):
    gender = SerializerMethodField()                        # get_attribute     to_representation
    name = serializers.CharField(source='xxx.xxx.xxx')      # get_attribute     to_representation
    class Meta:
        model = models.NbUserInfo
        fields = ["id", "name", "age", "gender"]
        extra_kwargs = {
            "id": {"read_only": True}
        }
    def get_gender(self, obj):
        return obj.get_gender_display()

ser = NbModelSerializer(instance=对象)
ser.data

ser = NbModelSerializer(data=request.data)
if ser.is_valid():
    ser.save()
    ser.data


class Field:
    def get_attribute(self, instance):
        # instance.字段名称.xxx.xxx.xxx
        return get_attribute(instance, self.source_attrs)

class CharField(Field):
    pass





class UusSerializer(serializers.ModelSerializer):
    v1 = serializers.SerializerMethodField() # 对象实例化后还没被调用

class SerializerMethodField(Field):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name # None v1 = serializers.SerializerMethodField()
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        # The method name defaults to `get_{field_name}`.
        if self.method_name is None:
            self.method_name = 'get_{field_name}'.format(field_name=field_name) # get_gender

        super().bind(field_name, parent)

    def to_representation(self, value):
        method = getattr(self.parent, self.method_name)
        return method(value)

class MyCharField(serializers.IntegerField):    # 注意这里继承的是IntegerField
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name # None
        super().__init__(**kwargs)
        
    def bind(self, field_name, parent):
        if self.method_name is None:
            self.method_name = 'xget_(field_name)'.format(field_name=field_name) # xget_gender
        super().bind(field_name, parent)
        
    def get_attribute(self, instance):
        method = getattr(self.parent, self.method_name)
        return str(value)
    
    def to_representation(self, value):
        return str(value)

序列化
    - 加载字段
    - 示例 ser=MyModelSerializer(...)
    - ser.data # 这一步才开始序列化