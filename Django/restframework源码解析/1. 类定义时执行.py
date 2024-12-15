####################### 框架处理代码 #############################
class BaseRouter:
    def __init__(self):
        # [‘comments’, <viewsets.CommentsViewSet>, basename=None]
        self.registry = []
    
    def register(self, prefix, viewset, basename=None):
    	"""
    	前缀：prefix="comments"
    	viewset: apps.viewsets.CommentsViewSet类
    	"""
        if basename is None:
            basename = self.get_default_basename(viewset)  # 'comments'
        self.registry.append((prefix, viewset, basename))

	@property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls


class SimpleRouter(BaseRouter):
	routes = [
        # List route.
        # Route = namedtuple('Route', ['url', 'mapping', 'name', 'detail', 'initkwargs'])
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]

    def __init__(self, trailing_slash=True):
    	# self.trailing_slash = ‘/’
        self.trailing_slash = '/' if trailing_slash else ''
        super().__init__()

    def get_default_basename(self, viewset):
    	# 获取CommentsViewSet类的属性queryset
    	# queryset = Comments.objects.all().order_by("-id")
        queryset = getattr(viewset, 'queryset', None)
        # 获取模型类类名
        return queryset.model._meta.object_name.lower()

    def get_lookup_regex(self, viewset, lookup_prefix=''):
        base_regex = '(?P<{lookup_prefix}{lookup_url_kwarg}>{lookup_value})'
        # lookup_field = 'pk'
        lookup_field = getattr(viewset, 'lookup_field', 'pk')
        lookup_url_kwarg = getattr(viewset, 'lookup_url_kwarg', None) or lookup_field
        lookup_value = getattr(viewset, 'lookup_value_regex', '[^/.]+')
        return base_regex.format(
            lookup_prefix=lookup_prefix,
            lookup_url_kwarg=lookup_url_kwarg,
            lookup_value=lookup_value
        )

    def get_routes(self, viewset):
        known_actions = list(flatten([route.mapping.values() for route in self.routes if isinstance(route, Route)]))
        extra_actions = viewset.get_extra_actions()
        # partition detail and list actions
        detail_actions = [action for action in extra_actions if action.detail]
        list_actions = [action for action in extra_actions if not action.detail]
        routes = []
        for route in self.routes:
            if isinstance(route, DynamicRoute) and route.detail:
                routes += [self._get_dynamic_route(route, action) for action in detail_actions]
            elif isinstance(route, DynamicRoute) and not route.detail:
                routes += [self._get_dynamic_route(route, action) for action in list_actions]
            else:
                routes.append(route)
        return routes

    def get_urls(self):
        # self.registry = [‘comments’, <viewsets.CommentsViewSet>, basename=None]
        ret = []

        for prefix, viewset, basename in self.registry:
            # prefix: ‘comments’
            # viewset: <viewsets.CommentsViewSet>
            # basename: 'comments'

        	# lookup = '(?P<pk>[^/.]+)'
            lookup = self.get_lookup_regex(viewset)
            
            # routes = [Route(url='^{prefix}{trailing_slash}$', mapping={'get': 'list', 'post': 'create'}, name='{basename}-list', detail=False, initkwargs={'suffix': 'List'}), 
                      # Route(url='^{prefix}/{lookup}{trailing_slash}$', mapping={'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}, name='{basename}-detail', detail=True, initkwargs={'suffix': 'Instance'})]
            routes = self.get_routes(viewset)    

            for route in routes:

                # mapping = {'get': 'list', 'post': 'create'}
                mapping = self.get_method_map(viewset, route.mapping)

                # Build the url pattern
                # regex = '^comments/$'
                regex = route.url.format(
                    prefix=prefix,
                    lookup=lookup,
                    trailing_slash=self.trailing_slash
                )

                if not prefix and regex[:2] == '^/':
                    regex = '^' + regex[2:]
                # initkwargs = {'suffix': 'List'}
                initkwargs = route.initkwargs.copy()
                # initkwargs = {'basename': 'comments', 'detail': False, 'suffix': 'List'}
                initkwargs.update({
                    'basename': basename,
                    'detail': route.detail,
                })
                # 重点，实例化类 CommentsViewSet
                # 调用ViewSetMixin类的as_view方法，返回内部函数def view(request, *args, **kwargs):
                view = viewset.as_view(mapping, **initkwargs)
                name = route.name.format(basename=basename)
                # re_path(regex, view, name=name)？？
                ret.append(re_path(regex, view, name=name))
        # ret = [<URLPattern '^comments/$' [name='comments-list']>, 
               # <URLPattern '^comments/(?P<pk>[^/.]+)/$' [name='comments-detail']>]
        return ret

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = self.get_urls()
        return self._urls

################### 父类 ####################

class ViewSetMixin:
    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            self.action_map = actions
            for method, action in actions.items():
                handler = getattr(self, action)
                setattr(self, method, handler)
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)
    # 免除csrf校验
    return csrf_exempt(view)

class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    pass

class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

########################## 本地代码 #######################

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all().order_by("-id")
    serializer_class = CommentsSerializers
    pagination_class = Pagination
    filterset_class = CommentsFilter


# 实例化SimpleRouter(BaseRouter)类，调用__init__()
router = SimpleRouter()

# 调用SimpleRouter(BaseRouter)类对象的 register 方法
# 路由请求时，调用 ViewSetMixin 类的 as_view 方法的内部函数view，
# 原因是 router.urls 会执行 view = viewset.as_view(mapping, **initkwargs)，然后返回内部函数 def view(request, *args, **kwargs)
router.register(r"comments", viewsets.CommentsViewSet)

urlpatterns = []
# 调用 SimpleRouter 类对象的 urls 方法，返回正则匹配的路由列表
# [<URLPattern '^comments/$' [name='comments-list']>, 
# <URLPattern '^comments/(?P<pk>[^/.]+)/$' [name='comments-detail']>]
urlpatterns += router.urls
