
class QuerySet:
    def __getitem__(self, k):
        # self: <QuerySet [<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        # self对象中的属性query保存了sql语句
        # k: slice(0, 3, None)
        # self._result_cache: 查看sql语句查询的缓存
        if self._result_cache is not None:
            return self._result_cache[k]

        if isinstance(k, slice):
            qs = self._chain()
            if k.start is not None:
                start = int(k.start)
            else:
                start = None
            if k.stop is not None:
                stop = int(k.stop)
            else:
                stop = None
            qs.query.set_limits(start, stop)
            return list(qs)[::k.step] if k.step else qs

        qs = self._chain()
        qs.query.set_limits(k, k + 1)
        qs._fetch_all()
        return qs._result_cache[0]

    def __len__(self):
        # self: <QuerySet [<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        # self.query: SELECT `comments`.`id`, `comments`.`description`, `comments`.`commenter`, `comments`.`comment_time` FROM `comments` ORDER BY `comments`.`id` DESC LIMIT 3
        # ******** 关键地方，真正触发数据库查询的代码
        self._fetch_all()
        return len(self._result_cache)

** 1.2.4.3.1x
class Page(collections.abc.Sequence):
    def __init__(self, object_list, number, paginator):
    	# self: <Page instance at 0x1ff00a81030>
    	# object_list: 筛选一页数目的queryset对象
    	# number: 1
    	# paginator: <django.core.paginator.Paginator object at 0x000001FF00A83AF0>

        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __getitem__(self, index):
    	return self.object_list[index]

    def __len__(self):
        # self: <class 'django.core.paginator.Page'>
        # self.object_list: <QuerySet [<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        # 触发QuerySet类的__len__()
        return len(self.object_list)

class Paginator:

** 1.2.2x
    def __init__(self, object_list, per_page, orphans=0,
                 allow_empty_first_page=True):
        # self：<django.core.paginator.Paginator object at 0x000002BB11067DF0>
        # object_list： queryset对象 <QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
        # per_page： page_size每一页的条数
        # orphans=0
        # allow_empty_first_page=True

        self.object_list = object_list  # queryset对象中的属性query存的是sql查询语句，为后续从数据库查询数据做准备
        # 如果self.object_list没有进行排序就会警告
        self._check_object_list_is_ordered()
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page

** 1.2.4.1x
    def validate_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_('That page number is not an integer'))
        if number < 1:
            raise EmptyPage(_('That page number is less than 1'))
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage(_('That page contains no results'))
        return number

** 1.2.4.3x
    def _get_page(self, *args, **kwargs):
        # self: <django.core.paginator.Paginator object at 0x000002BB11067DF0>
        # args: ([<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>], 1, <django.core.paginator.Paginator object at 0x000002BB11067DF0>)
        # kwargs: {}

** 1.2.4.3.1
        # 实例化类Page
        # 返回对象： <Page 1 of 1>
        return Page(*args, **kwargs)

** 1.2.4.2x
    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        c = getattr(self.object_list, 'count', None)
        if callable(c) and not inspect.isbuiltin(c) and method_has_no_args(c):
            return c()
        # 返回查询数据的总长度
        return len(self.object_list)

** 1.2.4x
    def page(self, number):
        """Return a Page object for the given 1-based page number."""
        # self： <django.core.paginator.Paginator object at 0x000002BB11067DF0>
        # number： 1

** 1.2.4.1
        # 判断给的页码数是否符合要求
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page

** 1.2.4.2
        if top + self.orphans >= self.count:
            top = self.count
        # 触发QuerySet类的__getitem__()
        # QuerySet对象：<QuerySet [<Comments: Comments object (3)>, <Comments: Comments object (2)>, <Comments: Comments object (1)>]>
        self.object_list[bottom:top]

** 1.2.4.3
        # self： <django.core.paginator.Paginator object at 0x000001FF00A83AF0>
        # 重点代码，触发数据库查询，调用class QuerySet: def __getitem__(self, k)？？
        # 返回对象： <Page 1 of 1>
        return self._get_page(self.object_list[bottom:top], number, self)

    def _check_object_list_is_ordered(self):
        """
        Warn if self.object_list is unordered (typically a QuerySet).
        """
        ordered = getattr(self.object_list, 'ordered', None)
        if ordered is not None and not ordered:
            obj_list_repr = (
                '{} {}'.format(self.object_list.model, self.object_list.__class__.__name__)
                if hasattr(self.object_list, 'model')
                else '{!r}'.format(self.object_list)
            )
            # 实现告警信息
            import warnings
            warnings.warn(
                'Pagination may yield inconsistent results with an unordered '
                'object_list: {}.'.format(obj_list_repr),
                UnorderedObjectListWarning,
                stacklevel=3
            )


class PageNumberPagination(BasePagination):
	from django.core.paginator import Paginator as DjangoPaginator
	django_paginator_class = DjangoPaginator
	page_query_param = 'page'
    last_page_strings = ('last',)

** 1.2x
	def paginate_queryset(self, queryset, request, view=None):
		# self: <apps.utils.pagination.Pagination object at 0x000001FF00A824A0>
		# queryset: queryset对象 <QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
		# request: <rest_framework.request.Request: GET '/app/comments/'>
		# view: <apps.viewsets.comments.CommentsViewSet object at 0x000001FF00A83250> 视图类

** 1.2.1
		# 调用的是 自定义分页器 Pagination 对象的 get_page_size()，返回Pagination对象属性值：page_size
		page_size = self.get_page_size(request)

** 1.2.2
		# 实例化类 DjangoPaginator(即类Paginator)，返回对象 <django.core.paginator.Paginator object at 0x000001FF00A83AF0>
		paginator = self.django_paginator_class(queryset, page_size)

** 1.2.3
		# 调用PageNumberPagination类方法get_page_number，获取当前所在页
		page_number = self.get_page_number(request, paginator)

** 1.2.4
		# 重点代码，调用Paginator对象的page()，返回对象 <class 'django.core.paginator.Page'>
        # ****** 此处已经触发sql语句到数据库查询？？没有，如果走的是缓存就有数据，如果没有走缓存，object_list.query保存的sql语句如下：
        # SELECT `comments`.`id`, `comments`.`description`, `comments`.`commenter`, `comments`.`comment_time` FROM `comments` ORDER BY `comments`.`id` DESC LIMIT 3
        # 返回对象 <Page 1 of 1>
		self.page = paginator.page(page_number)

		# <rest_framework.request.Request: GET '/app/user/'>
		self.request = request

** 1.2.5
        # 重点
		# 触发 Page 对象的 __len__()，返回的是包含一页数据的数据库表对象的列表
        # 如果不走缓存，则会触发数据库查询？？
        # 返回什么？？
        # 返回所查询页的所有数据对象列表
        return list(self.page)

** 1.2.1.1x
    def get_page_size(self, request):
        # self: <apps.utils.pagination.Pagination object at 0x000002BB11066FB0>
        # request: <rest_framework.request.Request: GET '/app/user/'>

        # 获取分页器的自定义属性 page_size_query_param
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        # 返回分页器的自定义属性 page_size
        return self.page_size

** 1.2.3x
    def get_page_number(self, request, paginator):
        # self： <apps.utils.pagination.Pagination object at 0x000002BB11066FB0>
        # request： <rest_framework.request.Request: GET '/app/user/'>
        # paginator：<django.core.paginator.Paginator object at 0x000002BB11067DF0>

        # self.page_query_param = 'page'
        # 从请求url参数中获取用户想要查询的页码
        page_number = request.query_params.get(self.page_query_param, 1)
        # self.last_page_strings = ('last',)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        # 返回当前的页码数
        return page_number

** 2.1.1x
    def get_next_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

** 2.1.2x
    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

** 2.1
    def get_paginated_response(self, data):
        # self: <apps.utils.pagination.Pagination object at 0x00000250288EA2C0> 分页器类
        # data: [OrderedDict([('id', 1), ('level', '普通会员'), ('depart', '开发部门'), ('password', '123456'), ('age', 22), ('email', '123456qq.com'), ('token', 'lsadfklklsdf'), ('roles', [1, 2])]), OrderedDict([('id', 2), ('level', 'VIP'), ('depart', '测试部门'), ('password', '123456'), ('age', 25), ('email', '123456qq.com'), ('token', 'j;lskjdfksgas'), ('roles', [2])]), OrderedDict([('id', 3), ('level', 'SVIP'), ('depart', '经理部门'), ('password', '123456'), ('age', 29), ('email', '123456qq.com'), ('token', 'sakdfjals;jlskdk'), ('roles', [1])])]
        return Response(OrderedDict([
            ('code', 200),
            ('count', self.page.paginator.count),
** 2.1.1
            ('next', self.get_next_link()),
** 2.1.2
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

class GenericAPIView(views.APIView):

** 1.1x
    @property
    def paginator(self):
** 1.1.1
    	# 实例化分页器，调用CommentsViewSet的属性pagination_class，并实例化Pagination对象
        self._paginator = self.pagination_class()
        # <apps.utils.pagination.Pagination object at 0x000001FF00A83040>
        return self._paginator

** 1x
    def paginate_queryset(self, queryset):
    	# 实例化分页器，并调用分页器对象方法 paginate_queryset()
    	# self: <apps.viewsets.comments.CommentsViewSet object at 0x000001FF00A82440>
    	# queryset: queryset对象

** 1.1 self.paginator
** 1.2 self.paginator.paginate_queryset
    	# self.paginator： <apps.utils.pagination.Pagination object at 0x000001FF00A824A0> 自定义分页器
    	# 最后调用的是 PageNumberPagination 类的 paginate_queryset()
        # 返回所查询页的所有数据对象列表
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

** 2.1x
    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x00000250288EA050>
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                # pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
                self._paginator = self.pagination_class()
        # 返回视图类中的属性类 pagination_class
        return self._paginator

** 2x
    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x00000250288EA050>
        # data: [OrderedDict([('id', 1), ('level', '普通会员'), ('depart', '开发部门'), ('password', '123456'), ('age', 22), ('email', '123456qq.com'), ('token', 'lsadfklklsdf'), ('roles', [1, 2])]), OrderedDict([('id', 2), ('level', 'VIP'), ('depart', '测试部门'), ('password', '123456'), ('age', 25), ('email', '123456qq.com'), ('token', 'j;lskjdfksgas'), ('roles', [2])]), OrderedDict([('id', 3), ('level', 'SVIP'), ('depart', '经理部门'), ('password', '123456'), ('age', 29), ('email', '123456qq.com'), ('token', 'sakdfjals;jlskdk'), ('roles', [1])])]
        assert self.paginator is not None
** 2.1
        # self.paginator： 返回分页类
        # 最后调用的是类方法： GenericAPIView.get_paginated_response()
        return self.paginator.get_paginated_response(data)

class ListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        # self：<apps.viewsets.comments.CommentsViewSet object at 0x000001F5BFD4D330> 视图类
        # self.get_queryset调用的是 GenericAPIView(views.APIView) 类的 get_queryset 方法

        # self.filter_queryset调用的是 GenericAPIView(views.APIView )类的 filter_queryset 方法
        # 过滤
        # 返回的是queryset对象，此时还没有从数据库查询数据，该对象中的属性query保存的是sql语句：SELECT `comments`.`id`, `comments`.`description`, `comments`.`commenter`, `comments`.`comment_time` FROM `comments` ORDER BY `comments`.`id` DESC
        # <QuerySet [<UserInfo: UserInfo object (1)>, <UserInfo: UserInfo object (2)>, <UserInfo: UserInfo object (3)>]>
        queryset = self.filter_queryset(self.get_queryset())

** 1
        # 分页，调用的是 GenericAPIView 类的 paginate_queryset 方法
        # 最终返回的是包含一页数据对象的列表
        # 模型类Comments对象列表： [<Comments: Comments object (11)>, <Comments: Comments object (10)>]，其中已经触发数据库查询？？哪一步触发的？？
        page = self.paginate_queryset(queryset)
        if page is not None:
            # 序列化
            serializer = self.get_serializer(page, many=True)
** 2
            # 分页返回数据
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # serializer.data触发一系列操作
        return Response(serializer.data)


########################## 视图类 ############################

from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
RETURN_ALL = "-1"  # page_size=-1表示不分页，获取所有值

** 1.1.1
class Pagination(PageNumberPagination):
    """分页"""
    page_size = 10  # 配置单页条目
    page_size_query_param = "page_size"  # URL配置每页条目名称
    page_query_param = 'page'  # 配置页数名称

** 1.2.1x
    def get_page_size(self, request):
        # self: <apps.utils.pagination.Pagination object at 0x000002BB11066FB0>
        # request: <rest_framework.request.Request: GET '/app/user/'>

        if request.query_params.get(self.page_size_query_param) == RETURN_ALL:
            return None
** 1.2.1.1
        # 返回分页器的自定义属性 page_size
        # 调用的是 PageNumberPagination(BasePagination) 类的 get_page_size()
        return super(Pagination, self).get_page_size(request)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('code', 200),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

from django_filters.rest_framework import DjangoFilterBackend
from apps.utils.pagination import Pagination
class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all().order_by("-id")
    serializer_class = CommentsSerializers
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentsFilter
    # authentication_classes = []
    # permission_classes = []

