
** 3.2.1x
def get_field_parts(model, field_name):
    parts = field_name.split(LOOKUP_SEP)
    opts = model._meta
    fields = []

    # walk relationships
    for name in parts:
        try:
            field = opts.get_field(name)
        except FieldDoesNotExist:
            return None

        fields.append(field)
        try:
            if isinstance(field, RelatedField):
                opts = field.remote_field.model._meta
            elif isinstance(field, ForeignObjectRel):
                opts = field.related_model._meta
        except AttributeError:
            # Lazy relationships are not resolved until registry is populated.
            raise RuntimeError(
                "Unable to resolve relationship `%s` for `%s`. Django is most "
                "likely not initialized, and its apps registry not populated. "
                "Ensure Django has finished setup before loading `FilterSet`s."
                % (field_name, model._meta.label)
            )

    return fields

** 3.2x
def get_model_field(model, field_name):

** 3.2.1
    fields = get_field_parts(model, field_name)
    return fields[-1] if fields else None

** 3.1.1x
def get_all_model_fields(model):
    # model: <class 'apps.models.UserInfo'>

    # <Options for UserInfo>
    opts = model._meta

    return [
        f.name
        for f in sorted(opts.fields + opts.many_to_many)
        if not isinstance(f, models.AutoField)
        and not (getattr(f.remote_field, "parent_link", False))
    ]

class BaseFilterSet:
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS

** 3.4x
    @classmethod
    def filter_for_field(cls, field, field_name, lookup_expr=None):
        # cls：<class 'apps.viewsets.user_info.UserInfoFilter'>
        # field： <django.db.models.fields.IntegerField: age>
        # field_name： 'age'
        # lookup_expr： 'exact'


        if lookup_expr is None:
            lookup_expr = settings.DEFAULT_LOOKUP_EXPR

** 3.4.1
        field, lookup_type = resolve_field(field, lookup_expr)

        default = {
            "field_name": field_name,
            "lookup_expr": lookup_expr,
        }

        filter_class, params = cls.filter_for_lookup(field, lookup_type)
        default.update(params)

        assert filter_class is not None, (
            "%s resolved field '%s' with '%s' lookup to an unrecognized field "
            "type %s. Try adding an override to 'Meta.filter_overrides'. See: "
            "https://django-filter.readthedocs.io/en/main/ref/filterset.html"
            "#customise-filter-generation-with-filter-overrides"
        ) % (cls.__name__, field_name, lookup_expr, field.__class__.__name__)

        return filter_class(**default)

** 3.3x
    @classmethod
    def get_filter_name(cls, field_name, lookup_expr):
        """
        Combine a field name and lookup expression into a usable filter name.
        Exact lookups are the implicit default, so "exact" is stripped from the
        end of the filter name.
        """
        # cls： <class 'apps.viewsets.user_info.UserInfoFilter'>
        # field_name： 'username'
        # lookup_expr： 'exact'

        # LOOKUP_SEP = '__'
        # 'username__exact'
        filter_name = LOOKUP_SEP.join([field_name, lookup_expr])

        # This also works with transformed exact lookups, such as 'date__exact'
        # '__exact'
        _default_expr = LOOKUP_SEP + settings.DEFAULT_LOOKUP_EXPR
        if filter_name.endswith(_default_expr):
            filter_name = filter_name[: -len(_default_expr)]

        return filter_name

** 3.1x
    @classmethod
    def get_fields(cls):
        # cls: <class 'apps.viewsets.user_info.UserInfoFilter'>

        # <class 'apps.models.UserInfo'>
        model = cls._meta.model
        # '__all__'
        fields = cls._meta.fields
        # None
        exclude = cls._meta.exclude

        assert not (fields is None and exclude is None), (
            "Setting 'Meta.model' without either 'Meta.fields' or 'Meta.exclude' "
            "has been deprecated since 0.15.0 and is now disallowed. Add an explicit "
            "'Meta.fields' or 'Meta.exclude' to the %s class." % cls.__name__
        )

        # Setting exclude with no fields implies all other fields.
        if exclude is not None and fields is None:
            # ALL_FIELDS = "__all__"
            fields = ALL_FIELDS

        # Resolve ALL_FIELDS into all fields for the filterset's model.
        if fields == ALL_FIELDS:
** 3.1.1    
            # ['level', 'username', 'password', 'age', 'email', 'token', 'depart', 'roles'] 获取模型类中的所有字段名
            fields = get_all_model_fields(model)

        # Remove excluded fields
        exclude = exclude or []
        if not isinstance(fields, dict):
            fields = [
                (f, [settings.DEFAULT_LOOKUP_EXPR]) for f in fields if f not in exclude
            ]
        else:
            fields = [(f, lookups) for f, lookups in fields.items() if f not in exclude]

        return OrderedDict(fields)


** 3x
    # 重点代码
    @classmethod
    def get_filters(cls):
        # cls: <class 'apps.viewsets.user_info.UserInfoFilter'>
        if not cls._meta.model:
            return cls.declared_filters.copy()

        # OrderedDict()
        filters = OrderedDict()

** 3.1
        # OrderedDict([('level', ['exact']), ('username', ['exact']), ('password', ['exact']), ('age', ['exact']), ('email', ['exact']), ('token', ['exact']), ('depart', ['exact']), ('roles', ['exact'])])
        fields = cls.get_fields()
        undefined = []

        for field_name, lookups in fields.items():
        	# field_name: 'username'
        	# lookups: ['exact']

** 3.2
        	# <django.db.models.fields.IntegerField: level>
            field = get_model_field(cls._meta.model, field_name)

            # warn if the field doesn't exist.
            if field is None:
                undefined.append(field_name)

            for lookup_expr in lookups:

** 3.3          
                # 'username'
                filter_name = cls.get_filter_name(field_name, lookup_expr)

                # If the filter is explicitly declared on the class, skip generation
                # OrderedDict([('username', <django_filters.filters.CharFilter object at 0x000001AA4D2166E0>)])
                if filter_name in cls.declared_filters:
                    filters[filter_name] = cls.declared_filters[filter_name]
                    continue

                if field is not None:

** 3.4
                    filters[filter_name] = cls.filter_for_field(
                        field, field_name, lookup_expr
                    )

        # Allow Meta.fields to contain declared filters *only* when a list/tuple
        if isinstance(cls._meta.fields, (list, tuple)):
            undefined = [f for f in undefined if f not in cls.declared_filters]

        if undefined:
            raise TypeError(
                "'Meta.fields' must not contain non-model field names: %s"
                % ", ".join(undefined)
            )

        # Add in declared filters. This is necessary since we don't enforce adding
        # declared filters to the 'Meta.fields' option
        filters.update(cls.declared_filters)
        return filters

	@classmethod
    def filter_for_lookup(cls, field, lookup_type):
        DEFAULTS = dict(cls.FILTER_DEFAULTS)
        if hasattr(cls, "_meta"):
            DEFAULTS.update(cls._meta.filter_overrides)

        data = try_dbfield(DEFAULTS.get, field.__class__) or {}
        filter_class = data.get("filter_class")
        params = data.get("extra", lambda field: {})(field)

        # if there is no filter class, exit early
        if not filter_class:
            return None, {}

        # perform lookup specific checks
        if lookup_type == "exact" and getattr(field, "choices", None):
            return ChoiceFilter, {"choices": field.choices}

        if lookup_type == "isnull":
            data = try_dbfield(DEFAULTS.get, models.BooleanField)

            filter_class = data.get("filter_class")
            params = data.get("extra", lambda field: {})(field)
            return filter_class, params

        if lookup_type == "in":

            class ConcreteInFilter(BaseInFilter, filter_class):
                pass

            ConcreteInFilter.__name__ = cls._csv_filter_class_name(
                filter_class, lookup_type
            )

            return ConcreteInFilter, params

        if lookup_type == "range":

            class ConcreteRangeFilter(BaseRangeFilter, filter_class):
                pass

            ConcreteRangeFilter.__name__ = cls._csv_filter_class_name(
                filter_class, lookup_type
            )

            return ConcreteRangeFilter, params

        return filter_class, params


class Filter:
    creation_counter = 0
    field_class = forms.Field

    def __init__(
        self,  # <django_filters.filters.CharFilter object at 0x000001D8544F8580>
        field_name=None,  # ??
        lookup_expr=None,  # 设置过滤规则
        *,
        label=None,  # ？？
        method=None,  # 'get_file_name'
        distinct=False,  # ？？
        exclude=False,  # ？？
        **kwargs  # {}
    ):
        if lookup_expr is None:
        	# 默认 lookup_expr = "exact"
            lookup_expr = settings.DEFAULT_LOOKUP_EXPR
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.label = label
        self.method = method
        self.distinct = distinct
        self.exclude = exclude

        self.extra = kwargs
        self.extra.setdefault("required", False)

        self.creation_counter = Filter.creation_counter
        Filter.creation_counter += 1


** 2x
class FilterSetOptions:
    def __init__(self, options=None):
    	# self： <django_filters.filterset.FilterSetOptions object at 0x000001AA4C439660>
    	# options： <class 'apps.viewsets.user_info.UserInfoFilter.Meta'> 过滤器类中的元类

    	# <class 'apps.models.UserInfo'>  模型类
        self.model = getattr(options, "model", None)
        # '__all__'
        self.fields = getattr(options, "fields", None)
        # None
        self.exclude = getattr(options, "exclude", None)
        # {}
        self.filter_overrides = getattr(options, "filter_overrides", {})
        # <class 'django.forms.forms.Form'>
        self.form = getattr(options, "form", forms.Form)

class FilterSetMetaclass(type):

** 1x
    @classmethod
    def get_declared_filters(cls, bases, attrs):
        # cls： <class 'django_filters.filterset.FilterSetMetaclass'>
        # bases：(<class 'django_filters.filterset.FilterSet'>,)
        # attrs： {'__module__': 'apps.viewsets.user_info', 
                # '__qualname__': 'UserInfoFilter', 
                # 'username': <django_filters.filters.CharFilter object at 0x000001D8544F8580>, 
                # 'get_username': <function UserInfoFilter.get_username at 0x000001D854515A20>, 
                # 'Meta': <class 'apps.viewsets.user_info.UserInfoFilter.Meta'>}

        # 将父类继承了Filter的对象筛选出来
        filters = [
            (filter_name, attrs.pop(filter_name))
            for filter_name, obj in list(attrs.items())
            if isinstance(obj, Filter)
        ]
        # filters: [('username', <django_filters.filters.CharFilter object at 0x0000019DA4132650>)]

        # 如果字段属性没有配置field_name，则默认为字段变量名
        for filter_name, f in filters:
            if getattr(f, "field_name", None) is None:
                f.field_name = filter_name

        filters.sort(key=lambda x: x[1].creation_counter)

        # Ensures a base class field doesn't override cls attrs, and maintains
        # field precedence when inheriting multiple parents. e.g. if there is a
        # class C(A, B), and A and B both define 'field', use 'field' from A.
        known = set(attrs)

        def visit(name):
            known.add(name)
            return name

        base_filters = [
            (visit(name), f)
            for base in bases
            if hasattr(base, "declared_filters")
            for name, f in base.declared_filters.items()
            if name not in known
        ]

        # 返回：OrderedDict([('username', <django_filters.filters.CharFilter object at 0x0000019DA4132650>)])
        return OrderedDict(base_filters + filters)


    def __new__(cls, name, bases, attrs):
    	# cls: <class 'django_filters.filterset.FilterSetMetaclass'> 元类
    	# name: 'UserInfoFilter'
    	# bases: (<class 'django_filters.filterset.FilterSet'>,) 怎么来的？？
    	# attrs: {'__module__': 'apps.viewsets.user_info', '__qualname__': 'UserInfoFilter', 
    			# 'username': <django_filters.filters.CharFilter object at 0x000001D8544F8580>, 
    			# 'get_username': <function UserInfoFilter.get_username at 0x000001D854515A20>, 
    			# 'Meta': <class 'apps.viewsets.user_info.UserInfoFilter.Meta'>}

** 1
        # 添加声明字段，即过滤器类中自定义的字段属性，包含字段名和对应的对象（name: object）
        # 返回： OrderedDict([('username', <django_filters.filters.CharFilter object at 0x0000019DA4132650>)])
        attrs["declared_filters"] = cls.get_declared_filters(bases, attrs)

        # <class 'apps.viewsets.user_info.UserInfoFilter'>
        # 调用元类创建对象，创建对象就是划定一块内存空间，给这块空间进行命名和提供属性？？
        new_class = super().__new__(cls, name, bases, attrs)
        
** 2    
        # 将元类中的所有属性赋值给对象的_meta属性
        new_class._meta = FilterSetOptions(getattr(new_class, "Meta", None))

** 3
        new_class.base_filters = new_class.get_filters()

        return new_class


class FilterSet(BaseFilterSet, metaclass=FilterSetMetaclass):
    pass

class CharFilter(Filter):
    field_class = forms.CharField

# 调用元类 FilterSetMetaclass.__new__() 创建过滤器类UserInfoFilter对象
class UserInfoFilter(django_filters.FilterSet):
	# 初始化类CharFilter对象，调用 Filter.__init__()
    username = django_filters.CharFilter(method="get_file_name")

    def get_username(self, queryset, name, value):
        return queryset

    class Meta:
        model = UserInfo
        fields = "__all__"
