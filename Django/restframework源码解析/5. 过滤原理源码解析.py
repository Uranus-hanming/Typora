


class FilterMethod:
    def __init__(self, filter_instance):
        self.f = filter_instance

**2.1.3.1.1x
    def __call__(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        # 重点
        # 执行过滤器类中字段属性自定义的method方法
        return self.method(qs, self.f.field_name, value)

    @property
    def method(self):
        """
        Resolve the method on the parent filterset.
        """
        instance = self.f

        # noop if 'method' is a function
        if callable(instance.method):
            return instance.method

        # otherwise, method is the name of a method on the parent FilterSet.
        assert hasattr(instance, 'parent'), \
            "Filter '%s' must have a parent FilterSet to find '.%s()'" %  \
            (instance.field_name, instance.method)

        parent = instance.parent
        # 重点
        # 获取过滤器类中字段属性自定义的method方法
        method = getattr(parent, instance.method, None)

        assert callable(method), \
            "Expected parent FilterSet '%s.%s' to have a '.%s()' method." % \
            (parent.__class__.__module__, parent.__class__.__name__, instance.method)

        return method

class QuerySet:
    def _filter_or_exclude_inplace(self, negate, args, kwargs):
        # self: <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        # negate=False
        # args=()
        # kwargs={'description__icontains': 'a'}
        if negate:
            self._query.add_q(~Q(*args, **kwargs))
        else:
            self._query.add_q(Q(*args, **kwargs))

    def _chain(self, **kwargs):
        """
        克隆：Return a copy of the current QuerySet that's ready for another
        operation.
        """
        obj = self._clone()
        obj.__dict__.update(kwargs)
        return obj

    def _filter_or_exclude(self, negate, args, kwargs):
        # self: <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        # negate=False
        # args=()
        # kwargs={'description__icontains': 'a'}
        if args or kwargs:
            assert not self.query.is_sliced, \
                "Cannot filter a query once a slice has been taken."

        # <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        clone = self._chain()
        clone._filter_or_exclude_inplace(negate, args, kwargs)
        return clone

    def filter(self, *args, **kwargs):
        self._not_support_combined_queries('filter')
        return self._filter_or_exclude(False, args, kwargs)

############################# 过滤器各个字段对象所属的类 ##############################

class Filter:
**2.1.3.1.1.1.1x
    # 返回 QuerySet 的 filter方法，或 exclude方法
    def get_method(self, qs):
        # self: <django_filters.filters.ChoiceFilter object at 0x00000172CD963E20> 各个字段所属的类对象
        # qs: QuerySet <QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
        return qs.exclude if self.exclude else qs.filter

**2.1.3.1.1.1x
    def filter(self, qs, value):
        # self: <django_filters.filters.ChoiceFilter object at 0x00000172CD963E20> 各个字段所属的类对象
        # qs: QuerySet <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        # value: '1'  URL中所带参数的值，目的是根据 该字段等于该值 进行过滤
        if value in EMPTY_VALUES:
            # EMPTY_VALUES = ([], (), {}, "", None) value属于里面这些值时不需要进行过滤
            return qs
        if self.distinct:  # 目的是什么？？
            qs = qs.distinct()
        # 重点，构造对某个字段进行过滤的方式，可以在过滤器的字段属性中定义 lookup_expr="icontains"，但默认是 "exact"
        # lookup = 'description__icontains'
        lookup = "%s__%s" % (self.field_name, self.lookup_expr)
        
**2.1.3.1.1.1.1
        # 调用类 Filter 方法 get_method
        # {lookup: value} = {'description__icontains': 'a'}
        # self.get_method(qs)： 返回的是 QuerySet 的 filter方法，或 exclude方法，然后调用QuerySet对应的方法将参数传进去
        # 最后返回的是经过过滤后的 QuerySet 对象，对象中的属性 query 包含对数据库查询的sql语句。
        qs = self.get_method(qs)(**{lookup: value})
        return qs


class ChoiceFilter(Filter):
**2.1.3.1.1x
    def filter(self, qs, value):
        # self: <django_filters.filters.ChoiceFilter object at 0x00000172CD963E20>
        # qs: QuerySet <QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
        # value: '1'
        if value != self.null_value:
            
**2.1.3.1.1.1
            # 返回的是经过过滤后的 QuerySet 对象，对象中的属性 query 包含对数据库查询的sql语句。
            return super().filter(qs, value)

        qs = self.get_method(qs)(
            **{"%s__%s" % (self.field_name, self.lookup_expr): None}
        )
        return qs.distinct() if self.distinct else qs


class CharFilter(Filter):
    field_class = forms.CharField


############################# 过滤器各个字段对象所属的类 ##############################

class BaseFilterSet:
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS

** 2.1.1.3x
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        # self: <apps.viewsets.comments.CommentsFilter object at 0x000002F49BCFB280> 过滤器类CommentsFilter对象
        # data: <QueryDict: {'description': ['a']}>
        # queryset: <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        # request: <rest_framework.request.Request: GET '/app/comments/?description=a'>
        # prefix=None
        if queryset is None:
            queryset = self._meta.model._default_manager.all()
        model = queryset.model  # <class 'apps.models.Comments'>

        self.is_bound = data is not None  # True
        self.data = data or {}  # <QueryDict: {'description': ['a']}>
        self.queryset = queryset  # <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        self.request = request  # <rest_framework.request.Request: GET '/app/comments/?description=a'>
        self.form_prefix = prefix  # None

        # 获取表中所有字段信息，和其对象的字段对象
        # 重点代码，真正起到过滤的作用，但机制不理解？？ 会触发def qs(self)函数，是bug导致
        # 过滤器类CommentsFilter对象能获取到属性base_filters，可能是在创建过滤器类对象时赋值该属性，需要进一步验证？？
        # OrderedDict([('description', <django_filters.filters.CharFilter object at 0x0000023165E5B1F0>), ('commenter', <django_filters.filters.CharFilter object at 0x0000023165E598D0>), ('comment_time', <django_filters.filters.DateTimeFilter object at 0x0000023165E5B970>)])
        self.filters = copy.deepcopy(self.base_filters)

        # 目的是什么？？
        # propagate the model and filterset to the filters
        for filter_ in self.filters.values():
            filter_.model = model
            filter_.parent = self

**2.1.2x
    def is_valid(self):
        return self.is_bound and self.form.is_valid()

    @property
    def form(self):
        if not hasattr(self, "_form"):
            Form = self.get_form_class()
            if self.is_bound:
                self._form = Form(self.data, prefix=self.form_prefix)
            else:
                self._form = Form(prefix=self.form_prefix)
        # <CommentsFilterForm bound=True, valid=True, fields=(description;commenter;comment_time)>
        return self._form

**2.1.3.1x
    # 重点代码
    # 该方法可以在过滤器CommentsFilter类中被重写
    def filter_queryset(self, queryset):
        # self：<apps.viewsets.user_info.UserInfoFilter object at 0x0000017ADEC58B80> 过滤器类UserInfoFilter对象
        # queryset：QuerySet <QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
        
        # 重点：
        # 
        for name, value in self.form.cleaned_data.items():
            # name是字段名，value是字段对应的值
            # name = 'description'
            
**2.1.3.1.1
            # 重点：
            # 调用的是类方法 FilterMethod.__call__() ?? 如果字段属性定义了method方法，则self.filters[name].filter返回的是FilterMethod对象，什么时候生成的？？
            # self.filters[name].filter(): 调用各个字段对应对象的filter方法 ??
            # 返回的是经过过滤后的 QuerySet 对象，对象中的属性 query 包含对数据库查询的sql语句。
            queryset = self.filters[name].filter(queryset, value)
            # self： <apps.viewsets.user_info.UserInfoFilter object at 0x00000172CD961120> 过滤器类UserInfoFilter对象
            # 过滤器类UserInfoFilter对象能获取到filters属性，可能是在创建对象的时候就赋值的该属性，需要进一步验证。？？
            # self.filters： 包含所有字段，以及各字段对应的对象
                # OrderedDict([('level', <django_filters.filters.ChoiceFilter object at 0x00000172CD963E20>), 
                             # ('username', <django_filters.filters.CharFilter object at 0x00000172CD963B50>), 
                             # ('password', <django_filters.filters.CharFilter object at 0x00000172CD963B80>), 
                             # ('age', <django_filters.filters.NumberFilter object at 0x00000172CD961DE0>), 
                             # ('email', <django_filters.filters.CharFilter object at 0x00000172CD963D30>), 
                             # ('token', <django_filters.filters.CharFilter object at 0x00000172CD9633D0>), 
                             # ('depart', <django_filters.filters.ModelChoiceFilter object at 0x00000172CD962E00>), 
                             # ('roles', <django_filters.filters.ModelMultipleChoiceFilter object at 0x00000172CD963CD0>)])
            assert isinstance(
                queryset, models.QuerySet
            ), "Expected '%s.%s' to return a QuerySet, but got a %s instead." % (
                type(self).__name__,
                name,
                type(queryset).__name__,
            )
        # 返回的是经过过滤后的 QuerySet 对象，对象中的属性 query 包含对数据库查询的sql语句。
        return queryset

**2.1.3x
    # 返回过滤后的QuerySet
    @property
    def qs(self):
        # self： <apps.viewsets.user_info.UserInfoFilter object at 0x0000017ADF441C00> 过滤器类UserInfoFilter对象
        if not hasattr(self, "_qs"):
            qs = self.queryset.all()
            # <QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
            if self.is_bound:
                # ensure form validation before filtering
                self.errors
                
**2.1.3.1       
                # 重点
                # 关键代码，真正起到过滤作用
                # 返回的是经过过滤后的 QuerySet 对象，对象中的属性 query 包含对数据库查询的sql语句。
                qs = self.filter_queryset(qs)
            self._qs = qs
        return self._qs

class FilterSet(BaseFilterSet, metaclass=FilterSetMetaclass):
    pass

class DjangoFilterBackend:
** 2.1.1.1x
    # 获取过滤器类: <class 'apps.viewsets.comments.CommentsFilter'>
    def get_filterset_class(self, view, queryset=None):
        # self： <django_filters.rest_framework.backends.DjangoFilterBackend object at 0x000002F49AA61630> DjangoFilterBackend对象
        # view： <apps.viewsets.comments.CommentsViewSet object at 0x000002F49BD594E0> 视图类CommentsViewSet对象
        # queryset:<QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>

        # 获取视图类CommentsViewSet的属性filterset_class
        # <class 'apps.viewsets.comments.CommentsFilter'>
        filterset_class = getattr(view, "filterset_class", None)
        # 获取视图类CommentsViewSet的属性filterset_fields
        # None
        filterset_fields = getattr(view, "filterset_fields", None)  # 具体作用是什么？？

        if filterset_class:
            # <class 'apps.models.Comments'>
            filterset_model = filterset_class._meta.model
            # 返回过滤器类 <class 'apps.viewsets.comments.CommentsFilter'>
            return filterset_class

** 2.1.1.2x
    def get_filterset_kwargs(self, request, queryset, view):
        return {
            "data": request.query_params,  # <QueryDict: {'description': ['a']}>
            "queryset": queryset,  # <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>
            "request": request,  # <rest_framework.request.Request: GET '/app/comments/?description=a'>
        }

**2.1.1x
    # 对参数进行封装
    def get_filterset(self, request, queryset, view):
        # self： <django_filters.rest_framework.backends.DjangoFilterBackend object at 0x000002F49AA61630> DjangoFilterBackend对象
        # request: <rest_framework.request.Request: GET '/app/user/?level=1'>
        # queryset:<QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
        # view： <apps.viewsets.comments.CommentsViewSet object at 0x000002F49BD594E0> 视图类CommentsViewSet对象

** 2.1.1.1
        # 获取过滤器类: <class 'apps.viewsets.comments.CommentsFilter'>
        filterset_class = self.get_filterset_class(view, queryset)

** 2.1.1.2
        # 对参数进行封装
        # request： <rest_framework.request.Request: GET '/app/comments/?description=a'>
        # queryset： <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        # view： <apps.viewsets.comments.CommentsViewSet object at 0x000002F49BD594E0>
        # kwargs： {'data': <QueryDict: {'description': ['a']}>, 
                  # 'queryset': <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>, 
                  # 'request': <rest_framework.request.Request: GET '/app/comments/?description=a'>}
        kwargs = self.get_filterset_kwargs(request, queryset, view)

** 2.1.1.3
        # 初始化过滤器类CommentsFilter，执行 BaseFilterSet 类的初始化方法def __init__()
        # 重点：真正起到过滤的作用，构造sql查询语句，不是吧？？
        # 返回过滤器对象
        return filterset_class(**kwargs)

** 2.1x
    def filter_queryset(self, request, queryset, view):
        # self： <django_filters.rest_framework.backends.DjangoFilterBackend object at 0x000002F49AA61630> DjangoFilterBackend对象
        # request： <rest_framework.request.Request: GET '/app/comments/?description=a'>  drf的request对象
        # queryset： <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]> QuerySet对象
        # view： <apps.viewsets.comments.CommentsViewSet object at 0x000002F49BD594E0> 视图类CommentsViewSet对象

        # 返回filterset: <apps.viewsets.comments.CommentsFilter object at 0x000002F49BCFB280>
        # debug模式下，一查看filterset的值就会触发filterset.qs，让人很疑惑，是一个bug
**2.1.1
        # 返回过滤器类对象 <apps.viewsets.user_info.UserInfoFilter object at 0x0000017ADF441C00>
        filterset = self.get_filterset(request, queryset, view)
        if filterset is None:
            return queryset

**2.1.2
        # 调用BaseFilterSet类的is_valid方法，判断这段代码的含义？？
        if not filterset.is_valid() and self.raise_exception:
            raise utils.translate_validation(filterset.errors)

**2.1.3
        # 返回过滤后的QuerySet对象
        return filterset.qs

class GenericAPIView(views.APIView):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

** 1x
    def get_queryset(self):
        # 调用 CommentsViewSet 对象的 queryset 属性
        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

** 2x
    def filter_queryset(self, queryset):
        # self.filter_backends 是 CommentsViewSet 的属性 filter_backends ，或者是settings.py中配置的
        # REST_FRAMEWORK = {'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),}
        for backend in list(self.filter_backends):
            # 调用 DjangoFilterBackend 类的 filter_queryset 方法
            # self.request： <rest_framework.request.Request: GET '/app/comments/?description=a'>
            # queryset： <QuerySet [<Comments: Comments object (2)>, <Comments: Comments object (1)>]>  QuerySet对象
            # self： <apps.viewsets.comments.CommentsViewSet object at 0x000002F49BD592A0> CommentsViewSet对象
** 2.1      
            # 返回过滤后的QuerySet, QuerySet中有query的属性，是查询数据库的sql语句
            # backend()：实例化类DjangoFilterBackend，没有__init__() ??
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

class ListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        # self：<apps.viewsets.comments.CommentsViewSet object at 0x000001F5BFD4D330> CommentsViewSet对象
        # self.get_queryset 调用的是 GenericAPIView(views.APIView) 类的 get_queryset 方法
        # self.filter_queryset 调用的是 GenericAPIView(views.APIView) 类的 filter_queryset 方法
        # 过滤
** 1
** 2
        # 对数据进行过滤，返回经过过滤处理的QuerySet对象。
        queryset = self.filter_queryset(self.get_queryset())
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            # 序列化
            serializer = self.get_serializer(page, many=True)
            # 分页返回数据
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # serializer.data触发一系列操作
        return Response(serializer.data)

class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    pass

class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

########################## 视图类 ############################

class CommentsSerializers(serializers.ModelSerializer):
    issue_id = serializers.IntegerField()

    class Meta:
        model = Comments
        fields = "__all__"
        depth = 1

from django_filters import FilterSet
class CommentsFilter(django_filters.FilterSet):
    # 初始化CharFilter对象，设置Filter属性lookup_expr="icontains"，
    # 以便调用django_filters.filters.CharFilter的filter方法时，设置lookup='description__icontains'
    description = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Comments
        fields = "__all__"

from django_filters.rest_framework import DjangoFilterBackend
class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all().order_by("-id")
    serializer_class = CommentsSerializers
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentsFilter
    # authentication_classes = []
    # permission_classes = []

