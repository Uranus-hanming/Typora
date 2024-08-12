
** 3.2.1x
def get_field_parts(model, field_name):
    # model：<class 'bk_power.ecology.models.bug_record.BugRecord'>
    # field_name：'label'

    # LOOKUP_SEP = '__'
    # parts = ['label']
    parts = field_name.split(LOOKUP_SEP)
    # <Options for BugRecord>
    opts = model._meta
    fields = []

    # walk relationships
    for name in parts:
        try:
** 3.2.1.1
            # field = <django.db.models.fields.CharField: label>
            field = opts.get_field(name)
        except FieldDoesNotExist:
            return None

        fields.append(field)
        if isinstance(field, RelatedField):
            opts = field.remote_field.model._meta
        elif isinstance(field, ForeignObjectRel):
            opts = field.related_model._meta

    return fields

** 3.2x
def get_model_field(model, field_name):
    # model: <class 'bk_power.ecology.models.bug_record.BugRecord'> 模型类
    # field_name: 'label' 过滤器类中定义的字段属性中的参数field_name自定义的值
** 3.2.1
    # fields = [<django.db.models.fields.CharField: label>]
    fields = get_field_parts(model, field_name)
    return fields[-1] if fields else None

** 3.1.1x
def get_all_model_fields(model):
    opts = model._meta

    return [
        f.name for f in sorted(opts.fields + opts.many_to_many)
        if not isinstance(f, models.AutoField) and
        not (getattr(f.remote_field, 'parent_link', False))
    ]

################################### 创建过滤器类BugRecordFilter ##############################

class FilterSetOptions:
** 2x
    def __init__(self, options=None):
        # <django_filters.filterset.FilterSetOptions object at 0x000001CEAFA93A90>
        # options: <class 'bk_power.ecology.viewsets.bug_record.BugRecordFilter.Meta'>

        # 模型类 <class 'bk_power.ecology.models.bug_record.BugRecord'>
        self.model = getattr(options, 'model', None)
        # ['label', 'bug_time', 'bug_level', 'phase', 'title']
        self.fields = getattr(options, 'fields', None)
        # None 可以使用exclude属性配置来排除字段
        self.exclude = getattr(options, 'exclude', None)
        # {}
        self.filter_overrides = getattr(options, 'filter_overrides', {})
        # <class 'django.forms.forms.Form'> ？？
        self.form = getattr(options, 'form', forms.Form)


class FilterSetMetaclass(type):

** 1x
    @classmethod
    def get_declared_filters(cls, bases, attrs):
        # cls: <class 'django_filters.filterset.FilterSetMetaclass'>
        # bases: (<class 'django_filters.filterset.FilterSet'>,)
        # attrs: 这里的属性参数包含了过滤器类属性和方法以及元类
                # {'__module__': 'bk_power.ecology.viewsets.bug_record', # 表名 db_table = "bug_record"
                # '__qualname__': 'BugRecordFilter', # 过滤器类名
                # 'title': <django_filters.filters.CharFilter object at 0x000001CEAF99FD00>, 
                # 'label': <django_filters.filters.CharFilter object at 0x000001CEAFB02680>, 
                # 'bug_time': <django_filters.filters.CharFilter object at 0x000001CEAFAB3850>, 
                # 'bug_level': <django_filters.filters.NumberFilter object at 0x000001CEAFAB3B80>, 
                # 'phase': <django_filters.filters.NumberFilter object at 0x000001CEAFAB3D00>, 
                # 'build_or_condition_query': <function BugRecordFilter.build_or_condition_query at 0x000001CEAFAD1240>, 
                # 'get_label': <function BugRecordFilter.get_label at 0x000001CEAFAD16C0>, 
                # 'get_bug_time': <function BugRecordFilter.get_bug_time at 0x000001CEAFA864D0>, 
                # 'get_bug_level': <function BugRecordFilter.get_bug_level at 0x000001CEAFAD1CF0>, 
                # 'get_phase': <function BugRecordFilter.get_phase at 0x000001CEAFAD1870>, 
                # 'Meta': <class 'bk_power.ecology.viewsets.bug_record.BugRecordFilter.Meta'>}

        filters = [
            (filter_name, attrs.pop(filter_name))
            for filter_name, obj in list(attrs.items())
            if isinstance(obj, Filter)
        ]
        # filters: 
                # [('title', <django_filters.filters.CharFilter object at 0x000001CEAF99FD00>), 
                # ('label', <django_filters.filters.CharFilter object at 0x000001CEAFB02680>), 
                # ('bug_time', <django_filters.filters.CharFilter object at 0x000001CEAFAB3850>), 
                # ('bug_level', <django_filters.filters.NumberFilter object at 0x000001CEAFAB3B80>), 
                # ('phase', <django_filters.filters.NumberFilter object at 0x000001CEAFAB3D00>)]

        # 如果定义字段时没有传field_name，则默认使用变量名
        for filter_name, f in filters:
            if getattr(f, 'field_name', None) is None:
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
            for base in bases if hasattr(base, 'declared_filters')
            for name, f in base.declared_filters.items() if name not in known
        ]
        # base_filters = []

        # 返回：
                # [('title', <django_filters.filters.CharFilter object at 0x000001CEAF99FD00>), 
                # ('label', <django_filters.filters.CharFilter object at 0x000001CEAFB02680>), 
                # ('bug_time', <django_filters.filters.CharFilter object at 0x000001CEAFAB3850>), 
                # ('bug_level', <django_filters.filters.NumberFilter object at 0x000001CEAFAB3B80>), 
                # ('phase', <django_filters.filters.NumberFilter object at 0x000001CEAFAB3D00>)]
        return OrderedDict(base_filters + filters)

    def __new__(cls, name, bases, attrs):
        # cls: <class 'django_filters.filterset.FilterSetMetaclass'>
        # name: 'BugRecordFilter'
        # bases: (<class 'django_filters.filterset.FilterSet'>,)
        # attrs: 这里的属性参数包含了过滤器类属性和方法以及元类
                # {'__module__': 'bk_power.ecology.viewsets.bug_record', # 表名 db_table = "bug_record"
                # '__qualname__': 'BugRecordFilter', # 过滤器类名
                # 'title': <django_filters.filters.CharFilter object at 0x000001CEAF99FD00>, 
                # 'label': <django_filters.filters.CharFilter object at 0x000001CEAFB02680>, 
                # 'bug_time': <django_filters.filters.CharFilter object at 0x000001CEAFAB3850>, 
                # 'bug_level': <django_filters.filters.NumberFilter object at 0x000001CEAFAB3B80>, 
                # 'phase': <django_filters.filters.NumberFilter object at 0x000001CEAFAB3D00>, 
                # 'build_or_condition_query': <function BugRecordFilter.build_or_condition_query at 0x000001CEAFAD1240>, 
                # 'get_label': <function BugRecordFilter.get_label at 0x000001CEAFAD16C0>, 
                # 'get_bug_time': <function BugRecordFilter.get_bug_time at 0x000001CEAFA864D0>, 
                # 'get_bug_level': <function BugRecordFilter.get_bug_level at 0x000001CEAFAD1CF0>, 
                # 'get_phase': <function BugRecordFilter.get_phase at 0x000001CEAFAD1870>, 
                # 'Meta': <class 'bk_power.ecology.viewsets.bug_record.BugRecordFilter.Meta'>}
** 1
        attrs['declared_filters'] = cls.get_declared_filters(bases, attrs)
        # attrs['declared_filters']：
            # [('title', <django_filters.filters.CharFilter object at 0x000001CEAF99FD00>), 
            # ('label', <django_filters.filters.CharFilter object at 0x000001CEAFB02680>), 
            # ('bug_time', <django_filters.filters.CharFilter object at 0x000001CEAFAB3850>), 
            # ('bug_level', <django_filters.filters.NumberFilter object at 0x000001CEAFAB3B80>), 
            # ('phase', <django_filters.filters.NumberFilter object at 0x000001CEAFAB3D00>)]

        new_class = super().__new__(cls, name, bases, attrs)
        # 新建对象： <class 'bk_power.ecology.viewsets.bug_record.BugRecordFilter'>

** 2    
        # 返回：<django_filters.filterset.FilterSetOptions object at 0x0000020E19DE72B0>
        new_class._meta = FilterSetOptions(getattr(new_class, 'Meta', None))

** 3    # 返回：
            # OrderedDict([('label', <django_filters.filters.CharFilter object at 0x0000020E19DA88B0>), 
            #              ('bug_time', <django_filters.filters.CharFilter object at 0x0000020E19DA8C10>), 
            #              ('bug_level', <django_filters.filters.NumberFilter object at 0x0000020E19DA85E0>), 
            #              ('phase', <django_filters.filters.NumberFilter object at 0x0000020E19D888E0>), 
            #              ('title', <django_filters.filters.CharFilter object at 0x0000020E19DA8910>)])
        new_class.base_filters = new_class.get_filters()

        # TODO: remove assertion in 2.1
        assert not hasattr(new_class, 'filter_for_reverse_field'), (
            "`%(cls)s.filter_for_reverse_field` has been removed. "
            "`%(cls)s.filter_for_field` now generates filters for reverse fields. "
            "See: https://django-filter.readthedocs.io/en/master/guide/migration.html"
            % {'cls': new_class.__name__}
        )

        return new_class


class BaseFilterSet:
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        if queryset is None:
            queryset = self._meta.model._default_manager.all()
        model = queryset.model

        self.is_bound = data is not None
        self.data = data or {}
        self.queryset = queryset
        self.request = request
        self.form_prefix = prefix

        self.filters = copy.deepcopy(self.base_filters)

        # propagate the model and filterset to the filters
        for filter_ in self.filters.values():
            filter_.model = model
            filter_.parent = self

** 3.3x
    @classmethod
    def get_filter_name(cls, field_name, lookup_expr):
        # cls: <class 'bk_power.ecology.viewsets.bug_record.BugRecordFilter'>
        # field_name: 'label'
        # lookup_expr: 'exact'

        # filter_name = 'label__exact'
        filter_name = LOOKUP_SEP.join([field_name, lookup_expr])

        # _default_expr = '__exact'
        _default_expr = LOOKUP_SEP + settings.DEFAULT_LOOKUP_EXPR
        if filter_name.endswith(_default_expr):
            filter_name = filter_name[:-len(_default_expr)]
        # 返回：'label'
        return filter_name

** 3.1x
    @classmethod
    def get_fields(cls):
        # <class 'bk_power.ecology.viewsets.bug_record.BugRecordFilter'> 过滤器类

        # <class 'bk_power.ecology.models.bug_record.BugRecord'> 模型类
        model = cls._meta.model
        # ['label', 'bug_time', 'bug_level', 'phase', 'title']  过滤器类中定义的字段
        fields = cls._meta.fields
        # None 过滤器类中的元类Meta配置的exclude属性
        exclude = cls._meta.exclude

        assert not (fields is None and exclude is None), \
            "Setting 'Meta.model' without either 'Meta.fields' or 'Meta.exclude' " \
            "has been deprecated since 0.15.0 and is now disallowed. Add an explicit " \
            "'Meta.fields' or 'Meta.exclude' to the %s class." % cls.__name__

        # Setting exclude with no fields implies all other fields.
        if exclude is not None and fields is None:
            # 默认 ALL_FIELDS = '__all__'
            fields = ALL_FIELDS

** 3.1.1
        # Resolve ALL_FIELDS into all fields for the filterset's model.
        if fields == ALL_FIELDS:
            fields = get_all_model_fields(model)

        # Remove excluded fields
        # []
        exclude = exclude or []
        if not isinstance(fields, dict):
            # DEFAULT_LOOKUP_EXPR='exact'
            # fields = [('label', ['exact']), ('bug_time', ['exact']), ('bug_level', ['exact']), ('phase', ['exact']), ('title', ['exact'])]
            fields = [(f, [settings.DEFAULT_LOOKUP_EXPR]) for f in fields if f not in exclude]
        else:
            fields = [(f, lookups) for f, lookups in fields.items() if f not in exclude]

        return OrderedDict(fields)

** 3x
    @classmethod
    def get_filters(cls):
        # cls: <class 'bk_power.ecology.viewsets.bug_record.BugRecordFilter'>

        if not cls._meta.model:
            return cls.declared_filters.copy()

        # Determine the filters that should be included on the filterset.
        filters = OrderedDict()

** 3.1
        # 获取过滤器类中定义的所有字段，并给定默认的过滤类型exact
        # fields = OrderedDict([('label', ['exact']), ('bug_time', ['exact']), ('bug_level', ['exact']), ('phase', ['exact']), ('title', ['exact'])])
        fields = cls.get_fields()
        undefined = []

** 3.2
        for field_name, lookups in fields.items():
            # field = <django.db.models.fields.CharField: label>
            field = get_model_field(cls._meta.model, field_name)

            # warn if the field doesn't exist.
            if field is None:
                undefined.append(field_name)

** 3.3
            for lookup_expr in lookups:
                # 返回：'label'
                filter_name = cls.get_filter_name(field_name, lookup_expr)

                # If the filter is explicitly declared on the class, skip generation
                if filter_name in cls.declared_filters:
                    filters[filter_name] = cls.declared_filters[filter_name]
                    continue

                if field is not None:
                    filters[filter_name] = cls.filter_for_field(field, field_name, lookup_expr)

        # Allow Meta.fields to contain declared filters *only* when a list/tuple
        if isinstance(cls._meta.fields, (list, tuple)):
            undefined = [f for f in undefined if f not in cls.declared_filters]

        if undefined:
            raise TypeError(
                "'Meta.fields' must not contain non-model field names: %s"
                % ', '.join(undefined)
            )

        # Add in declared filters. This is necessary since we don't enforce adding
        # declared filters to the 'Meta.fields' option
        filters.update(cls.declared_filters)
        # 返回：
            # OrderedDict([('label', <django_filters.filters.CharFilter object at 0x0000020E19DA88B0>), 
            #              ('bug_time', <django_filters.filters.CharFilter object at 0x0000020E19DA8C10>), 
            #              ('bug_level', <django_filters.filters.NumberFilter object at 0x0000020E19DA85E0>), 
            #              ('phase', <django_filters.filters.NumberFilter object at 0x0000020E19D888E0>), 
            #              ('title', <django_filters.filters.CharFilter object at 0x0000020E19DA8910>)])
        return filters


class FilterSet(BaseFilterSet, metaclass=FilterSetMetaclass):
    pass


class BugRecordFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    label = django_filters.CharFilter(method="get_label")
    bug_time = django_filters.CharFilter(method="get_bug_time")
    bug_level = django_filters.NumberFilter(method="get_bug_level")
    phase = django_filters.NumberFilter(method="get_phase")

    def build_or_condition_query(self, field, values, lookup_expr="icontains"):
        """构造 "or" 查询条件"""
        query = Q()
        query.connector = Q.OR
        [query.children.append((f"{field}__{lookup_expr}", value)) for value in values]
        return query

    def get_label(self, queryset, name, value):
        values = self.request.query_params.getlist('label')
        return queryset.filter(self.build_or_condition_query(name, values))

    def get_bug_time(self, queryset, name, value):
        values = self.request.query_params.getlist('bug_time')
        return queryset.filter(self.build_or_condition_query(name, values))

    def get_bug_level(self, queryset, name, value):
        values = self.request.query_params.getlist('bug_level')
        return queryset.filter(self.build_or_condition_query(name, values))

    def get_phase(self, queryset, name, value):
        values = self.request.query_params.getlist('phase')
        return queryset.filter(self.build_or_condition_query(name, values))

    class Meta:
        model = BugRecord
        fields = ["label", "bug_time", "bug_level", "phase"]


################################### 创建过滤器类BugRecordFilter中自定义的字段属性 ##############################

class Filter:
    creation_counter = 0
    field_class = forms.Field

    def __init__(self, field_name=None, lookup_expr=None, *, label=None,
                 method=None, distinct=False, exclude=False, **kwargs):
        # self: <django_filters.filters.CharFilter object at 0x000002BBCDD34400>
        # field_name='title'
        # lookup_expr='icontains'
        # label=None ??
        # method='get_title' ??
        # distinct=False ??
        # exclude=False ??
        # kwargs={}

        if lookup_expr is None:
            # 'DEFAULT_LOOKUP_EXPR': 'exact',
            lookup_expr = settings.DEFAULT_LOOKUP_EXPR
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.label = label
        self.method = method
        self.distinct = distinct
        self.exclude = exclude

        self.extra = kwargs
        # {'required': False}
        self.extra.setdefault('required', False)

        self.creation_counter = Filter.creation_counter
        Filter.creation_counter += 1

class CharFilter(Filter):
    field_class = forms.CharField

class BugRecordFilter(django_filters.FilterSet):
    # 调用类方法 Filter.__init__()
    title = django_filters.CharFilter(field_name="title", method="get_title", lookup_expr="icontains")
    label = django_filters.CharFilter(method="get_label")
    bug_time = django_filters.CharFilter(method="get_bug_time")
    bug_level = django_filters.NumberFilter(method="get_bug_level")
    phase = django_filters.NumberFilter(method="get_phase")
