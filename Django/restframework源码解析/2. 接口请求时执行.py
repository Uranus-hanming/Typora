# rest_framework/settings.py
DEFAULTS = {
    # Base API policies
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'rest_framework.negotiation.DefaultContentNegotiation',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': None,

    # Generic view behavior
    'DEFAULT_PAGINATION_CLASS': None,
    'DEFAULT_FILTER_BACKENDS': [],

    # Schema
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',

    # Throttling
    'DEFAULT_THROTTLE_RATES': {
        'user': None,
        'anon': None,
    },
    'NUM_PROXIES': None,

    # Pagination
    'PAGE_SIZE': None,

    # Filtering
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',

    # Versioning
    'DEFAULT_VERSION': None,
    'ALLOWED_VERSIONS': None,
    'VERSION_PARAM': 'version',

    # Authentication
    'UNAUTHENTICATED_USER': 'django.contrib.auth.models.AnonymousUser',
    'UNAUTHENTICATED_TOKEN': None,

    # View configuration
    'VIEW_NAME_FUNCTION': 'rest_framework.views.get_view_name',
    'VIEW_DESCRIPTION_FUNCTION': 'rest_framework.views.get_view_description',

    # Exception handling
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'NON_FIELD_ERRORS_KEY': 'non_field_errors',

    # Testing
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'multipart',

    # Hyperlink settings
    'URL_FORMAT_OVERRIDE': 'format',
    'FORMAT_SUFFIX_KWARG': 'format',
    'URL_FIELD_NAME': 'url',

    # Input and output formats
    'DATE_FORMAT': ISO_8601,
    'DATE_INPUT_FORMATS': [ISO_8601],

    'DATETIME_FORMAT': ISO_8601,
    'DATETIME_INPUT_FORMATS': [ISO_8601],

    'TIME_FORMAT': ISO_8601,
    'TIME_INPUT_FORMATS': [ISO_8601],

    # Encoding
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
    'STRICT_JSON': True,
    'COERCE_DECIMAL_TO_STRING': True,
    'UPLOADED_FILES_USE_URL': True,

    # Browseable API
    'HTML_SELECT_CUTOFF': 1000,
    'HTML_SELECT_CUTOFF_TEXT': "More than {count} items...",

    # Schemas
    'SCHEMA_COERCE_PATH_PK': True,
    'SCHEMA_COERCE_METHOD_NAMES': {
        'retrieve': 'read',
        'destroy': 'delete'
    },
}

IMPORT_STRINGS = [
    'DEFAULT_RENDERER_CLASSES',
    'DEFAULT_PARSER_CLASSES',
    'DEFAULT_AUTHENTICATION_CLASSES',
    'DEFAULT_PERMISSION_CLASSES',
    'DEFAULT_THROTTLE_CLASSES',
    'DEFAULT_CONTENT_NEGOTIATION_CLASS',
    'DEFAULT_METADATA_CLASS',
    'DEFAULT_VERSIONING_CLASS',
    'DEFAULT_PAGINATION_CLASS',
    'DEFAULT_FILTER_BACKENDS',
    'DEFAULT_SCHEMA_CLASS',
    'EXCEPTION_HANDLER',
    'TEST_REQUEST_RENDERER_CLASSES',
    'UNAUTHENTICATED_USER',
    'UNAUTHENTICATED_TOKEN',
    'VIEW_NAME_FUNCTION',
    'VIEW_DESCRIPTION_FUNCTION'
]

class APISettings:
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

	@property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'REST_FRAMEWORK', {})
        return self._user_settings

    def __getattr__(self, attr):
    	# attr = DEFAULT_PARSER_CLASSES

        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # DEFAULTS
            'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ]
            val = self.defaults[attr]

        # Coerce import strings into classes
        val = [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ]
        # attr = DEFAULT_PARSER_CLASSES
        if attr in self.import_strings:
        	# 以字符串的形式导入类
        	# val = [<class 'rest_framework.parsers.JSONParser'>, <class 'rest_framework.parsers.FormParser'>, <class 'rest_framework.parsers.MultiPartParser'>]
            val = perform_import(val, attr)

        # Cache the result 缓存结果
        self._cached_attrs.add(attr)
        # 设置属性DEFAULT_PARSER_CLASSES=[<class 'rest_framework.parsers.JSONParser'>, <class 'rest_framework.parsers.FormParser'>, <class 'rest_framework.parsers.MultiPartParser'>]
        setattr(self, attr, val)
        return val

api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


############################### 方法 ################################

class CreateModelMixin:
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

class ListModelMixin:
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


########################## 视图类 ####################################

class View:
	http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
** 1.x
    def __init__(self, **kwargs):
        # cls: <class 'apps.viewsets.user_info.UserInfosViewSet'>
        # 对 CommentsViewSet 类初始化，调用的是类方法： View.__init__()
        # self = cls(**initkwargs)

        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x0000013EAEE31CF0>，这里的self是一个对象
        # 原因是在实例化类 CommentsViewSet 时，元类会先创建一个类对象，然后才在此对对象进行初始化
    	# kwargs = {'basename': 'comments', 'detail': False, 'suffix': 'List'}
        for key, value in kwargs.items():
        	# 给类对象UserInfosViewSet，添加basename、comments、suffix属性
            setattr(self, key, value)

** 2.2.1.1x
    def _allowed_methods(self):
        # 重点，获取对象支持的所有请求类型
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

** 2.1.1.4x
# rest_framework的Request类
class Request:
	# 如果项目工程settings.py中配置了REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": []},
	# 则覆盖rest_framework\settings.py中的'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ]

    # 对rest_framework的Request类对象进行初始化
    def __init__(self, request, parsers=None, authenticators=None,
                 negotiator=None, parser_context=None):
        assert isinstance(request, HttpRequest), (
            'The `request` argument must be an instance of '
            '`django.http.HttpRequest`, not `{}.{}`.'
            .format(request.__class__.__module__, request.__class__.__name__)
        )

        self._request = request
        self.parsers = parsers or ()
        # 为视图类对象赋值属性authenticators，该属性值是所有认证类对象列表，为后续调用对用户进行认证
        self.authenticators = authenticators or ()
        self.negotiator = negotiator or self._default_negotiator()
        self.parser_context = parser_context
        self._data = Empty
        self._files = Empty
        self._full_data = Empty
        self._content_type = Empty
        self._stream = Empty

        if self.parser_context is None:
            self.parser_context = {}
        self.parser_context['request'] = self
        self.parser_context['encoding'] = request.encoding or settings.DEFAULT_CHARSET

        force_user = getattr(request, '_force_auth_user', None)
        force_token = getattr(request, '_force_auth_token', None)
        if force_user is not None or force_token is not None:
            forced_auth = ForcedAuthentication(force_user, force_token)
            self.authenticators = (forced_auth,)

	self.authenticators = authenticators or ()

** 2.2.4.1x
	@property
    def user(self):
        if not hasattr(self, '_user'):
            with wrap_attributeerrors():  # 原理是什么？？
** 2.2.4.1.1
                # 重点代码入口，用户认证
                self._authenticate()
        return self._user

	@user.setter
    def user(self, value):
        self._user = value
        self._request.user = value

** 2.2.4.1.1x
    # 用户认证重点代码
    def _authenticate(self):
    	# 可在项目工程settings.py中配置了REST_FRAMEWORK = {"DEFAULT_AUTHENTICATION_CLASSES": []}
    	# 自定义多个认证类，继承BaseAuthentication并重写authenticate和authenticate_header方法
        for authenticator in self.authenticators:
            try:
                # 调用各个认证类的 authenticate 方法，执行具体的认证逻辑
                # 返回一个元组，分别是uer,auth
                user_auth_tuple = authenticator.authenticate(self)
            except exceptions.APIException:
                self._not_authenticated()
                raise

            if user_auth_tuple is not None:
                self._authenticator = authenticator
                # 给视图类对象分别设置属性 user auth
                self.user, self.auth = user_auth_tuple
                return
        # 如果没有认证时执行
        self._not_authenticated()

    def _not_authenticated(self):
        """
        Set authenticator, user & authtoken representing an unauthenticated request.

        Defaults are None, AnonymousUser & None.
        """
        self._authenticator = None

        # 默认配置： "UNAUTHENTICATED_USER": None
        if api_settings.UNAUTHENTICATED_USER:
            # 用户为None时执行自定义的业务逻辑
            self.user = api_settings.UNAUTHENTICATED_USER()
        else:
            self.user = None
        # 默认配置： "UNAUTHENTICATED_TOKEN": None
        if api_settings.UNAUTHENTICATED_TOKEN:
            # token为None时执行自定义的业务逻辑
            self.auth = api_settings.UNAUTHENTICATED_TOKEN()
        else:
            self.auth = None

class APISettings:
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            # 导入项目配置文件
            from django.conf import settings
            # 获取配置文件中键为'REST_FRAMEWORK'
            self._user_settings = getattr(settings, 'REST_FRAMEWORK', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            # 首先从项目配置文件中导入，没有则从默认配置中获取
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)

class APIView(View):
	# 在实例化对象时调用
	from rest_framework.settings import api_settings
	# 调用的是APISettings对象的__getattr__(self, attr)
	# parser_classes = [<class 'rest_framework.parsers.JSONParser'>, 
                       # <class 'rest_framework.parsers.FormParser'>, 
                       # <class 'rest_framework.parsers.MultiPartParser'>]
	parser_classes = api_settings.DEFAULT_PARSER_CLASSES

	# [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ]
    # 用户认证配置
    # 调用类方法：APISettings.__getattr__() 获取属性
	authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    
    # 默认配置： ['rest_framework.authentication.SessionAuthentication', 'rest_framework.authentication.BasicAuthentication']
    content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS

	# 用户权限配置
    # 默认配置： 'rest_framework.permissions.AllowAny'
	permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES

    # 请求限流配置
    # 默认配置： []
    throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES

** 2.2.1x
    @property
    def allowed_methods(self):
** 2.2.1.1
        # 调用类方法： View._allowed_methods()
        return self._allowed_methods()

** 2.2x
    @property
    def default_response_headers(self):
        headers = {
** 2.2.1
            'Allow': ', '.join(self.allowed_methods),
        }
        if len(self.renderer_classes) > 1:
            headers['Vary'] = 'Accept'
        return headers

** 2.1.1.1x
    def get_parser_context(self, http_request):
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {})
        }

** 2.2.4x
    # 认证
    # 
    def perform_authentication(self, request):
** 2.2.4.1
    	# 调用Request类的user()方法
        # user函数被装饰器@property装饰，可以对用户进行赋值更改用户信息
        request.user

** 2.2.5.1x
    # 获取权限类对象列表
    def get_permissions(self):
        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x0000018B7415ADD0>
    	# 可在项目工程settings.py中配置了REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": []}
        # 优先从视图类的属性 permission_classes 中获取自定义认证类
    	# 自定义多个认证类，继承 BasePermission 并重写has_permission和has_object_permission方法
        # 默认：'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny', ]
        # 获取所有认证类实例化对象列表
        return [permission() for permission in self.permission_classes]

** 2.2.5.3x
    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message, code=code)

** 2.2.5x
    # 用户权限校验重点代码
    def check_permissions(self, request):
        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x0000018B7415ADD0>
        # request: <rest_framework.request.Request: GET '/app/user/'>
** 2.2.5.1
        for permission in self.get_permissions():
            # 调用自定义认证类的 has_permission()
** 2.2.5.2
            # 重点
            # 执行权限类对象的 has_permission 方法，执行具体的权限认证业务逻辑
            if not permission.has_permission(request, self):
** 2.2.5.3
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )

    def get_throttles(self):
        # 限流
        """
        Instantiates and returns the list of throttles that this view uses.
        """
        return [throttle() for throttle in self.throttle_classes]

    # 限流重点代码
    def check_throttles(self, request):
        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x0000018B7415ADD0>
        # request: <rest_framework.request.Request: GET '/app/user/'>
        throttle_durations = []
        for throttle in self.get_throttles():
            if not throttle.allow_request(request, self):
                throttle_durations.append(throttle.wait())

        if throttle_durations:
            # Filter out `None` values which may happen in case of config / rate
            # changes, see #1438
            durations = [
                duration for duration in throttle_durations
                if duration is not None
            ]

            duration = max(durations, default=None)
            self.throttled(request, duration)

** 2.1.1.1x
	def get_parsers(self):
        # 实例化对象，返回列表中包含的对象实例object：
            # [<rest_framework.parsers.JSONParser object at 0x000001DDF16FB1C0>, 
            #  <rest_framework.parsers.FormParser object at 0x000001DDF16FB430>,
            #  <rest_framework.parsers.MultiPartParser object at 0x000001DDF1799360>]
        # 列表中包含类class：self.parser_classes = [<class 'rest_framework.parsers.JSONParser'>, <class 'rest_framework.parsers.FormParser'>, <class 'rest_framework.parsers.MultiPartParser'>]
        return [parser() for parser in self.parser_classes]

** 2.1.1.2
    # 返回所有认证类对象列表
	def get_authenticators(self):
        # 重点，用户认证配置获取入口
        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x0000013EAEE31CF0>
        # 可调用视图类UserInfosViewSet的属性 authentication_classes
        # 也可以在配置文件中配置：DEFAULT_AUTHENTICATION_CLASSES
        # 默认：
            # ([<rest_framework.authentication.SessionAuthentication object at 0x0000018B74159E70>, 
            #   <rest_framework.authentication.BasicAuthentication object at 0x0000018B7415AEF0>],)
		# 调用所有的认证类，并实例化
        return [auth() for auth in self.authentication_classes]

** 2.1.1.3
    def get_content_negotiator(self):
        if not getattr(self, '_negotiator', None):
            # 默认配置： ['rest_framework.authentication.SessionAuthentication', 'rest_framework.authentication.BasicAuthentication']
            # content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
            self._negotiator = self.content_negotiation_class()
        return self._negotiator

** 2.1.1x
    # 对原生django的request进行封装，返回drf自己的request对象
	def initialize_request(self, request, *args, **kwargs):
        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x0000013EAEE31CF0>
        # request: WSGIRequestduixiang <WSGIRequest: GET '/app/user/'>
        # parser_context={'args': (), 'kwargs': {}, 
                        # 'view': <apps.viewsets.comments.CommentsViewSet object at 0x00000212577E7EE0>}
** 2.1.1.1
        parser_context = self.get_parser_context(request)

        # 重点代码，实例化类Request，对原生django的request进行封装
** 2.1.1.4
        return Request(  # from rest_framework.request import Request
            request,
            # ([<rest_framework.parsers.JSONParser object at 0x0000018B7415BA90>, 
                # <rest_framework.parsers.FormParser object at 0x0000018B74159EA0>, 
                # <rest_framework.parsers.MultiPartParser object at 0x0000018B7415B2E0>],)
** 2.1.1.1
            # 调用的时类 APIView(View) 方法 get_parsers
            parsers=self.get_parsers(),

** 2.1.1.2
            # 调用的时类 APIView(View) 方法 get_authenticators
            # 返回所有认证类对象列表
            # 默认：
                # ([<rest_framework.authentication.SessionAuthentication object at 0x0000018B74159E70>, 
                #   <rest_framework.authentication.BasicAuthentication object at 0x0000018B7415AEF0>],)
            authenticators=self.get_authenticators(),

** 2.1.1.3
            # 调用的时类 APIView(View) 方法 get_content_negotiator
            # (<rest_framework.negotiation.DefaultContentNegotiation object at 0x0000018B7415B7C0>,)
            negotiator=self.get_content_negotiator(),  # 作用是什么？？

            # {'args': (), 'kwargs': {}, 'view': <apps.viewsets.user_info.UserInfosViewSet object at 0x0000018B7415ADD0>}
            parser_context=parser_context
        )

    def get_format_suffix(self, **kwargs):
        """
        Determine if the request includes a '.json' style format suffix
        """
        if self.settings.FORMAT_SUFFIX_KWARG:
            return kwargs.get(self.settings.FORMAT_SUFFIX_KWARG)

    def perform_content_negotiation(self, request, force=False):
        # 解析器
        renderers = self.get_renderers()
        conneg = self.get_content_negotiator()

        try:
            return conneg.select_renderer(request, renderers, self.format_kwarg)
        except Exception:
            if force:
                return (renderers[0], renderers[0].media_type)
            raise

    def determine_version(self, request, *args, **kwargs):
        # 版本校验
        if self.versioning_class is None:
            return (None, None)
        scheme = self.versioning_class()
        return (scheme.determine_version(request, *args, **kwargs), scheme)

** 2.2x
    # 重点函数
    def initial(self, request, *args, **kwargs):
        # self： <apps.viewsets.user_info.UserInfosViewSet object at 0x0000018B7415ADD0>
        # request: <rest_framework.request.Request: GET '/app/user/'>
        # args: ()
        # kwargs: {}

** 2.2.1
        # None 作用是什么？？
        self.format_kwarg = self.get_format_suffix(**kwargs)

** 2.2.2
        # 解析器？？
        # (<rest_framework.renderers.JSONRenderer object at 0x0000018B7415A920>, 'application/json')
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

** 2.2.3
        # 版本校验
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

** 2.2.4
    	# 认证，是在这里对用户进行认证
        # 调用 APIView(View)类方法 perform_authentication
        self.perform_authentication(request)

** 2.2.5
        # 权限
        # 调用 APIView(View)类方法 perform_authentication
        self.check_permissions(request)

** 2.2.6
        # 限流
        self.check_throttles(request)

** 2.x
    # 重点代码
    def dispatch(self, request, *args, **kwargs):
        # self: <apps.viewsets.user_info.UserInfosViewSet object at 0x0000013EAEE31CF0>
    	# request = <WSGIRequest: GET '/app/comments/'> WSGIRequest对象
    	# args = ()
    	# kwargs = {}
        self.args = args
        self.kwargs = kwargs

** 2.1
        # 重点
        # 调用 ViewSetMixin 类的 initialize_request 方法，对原生django的request进行封装
        # 此处已经对用户进行过认证校验
        request = self.initialize_request(request, *args, **kwargs)

        # 将封装后的request替换原来的request
        self.request = request

** 2.2
        # 调用的时类 APIView(View) 方法 default_response_headers
        # {'Allow': 'GET, POST, HEAD, OPTIONS', 'Vary': 'Accept'}
        # 这里判断请求类型是否允许
        self.headers = self.default_response_headers

** 2.2
        # 初始化（重点）
        # 认证、权限、限流、版本、解析器
        self.initial(request, *args, **kwargs)

        # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
        # request.method：http请求类型
        # 此处可以配置请求类型，判断请求是否被允许访问
        if request.method.lower() in self.http_method_names:
        	# 获取属性值，返回最终要执行的函数，此时的函数并没有被调用
            # 这是在前面代码中已经设置属性和函数方法的映射关系，此处只是去获取方法
            handler = getattr(self, request.method.lower(),
                              self.http_method_not_allowed)
        else:
            # 否则放回请求不被允许
            handler = self.http_method_not_allowed
** 2.3
        # 调用函数(加了括号就是函数被调用)，执行最终要实现的业务逻辑函数
        response = handler(request, *args, **kwargs)
        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

#################### 本地代码 #################

class GenericAPIView(views.APIView):
	pass

class ViewSetMixin:
	@classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        def view(request, *args, **kwargs):
        	# request = <WSGIRequest: GET '/app/comments/'> WSGIRequest对象需要进一步深入理解？？
            # args = ()
            # initkwargs={'basename': 'comments', 'detail': False, 'suffix': 'List'}
            # cls: <class 'apps.viewsets.user_info.UserInfosViewSet'>

** 1
        	# 对CommentsViewSet类初始化，调用的是类方法： View.__init__()
            # 初始化的目的： 给类对象UserInfosViewSet，添加basename、comments、suffix属性
            # 返回self = CommentsViewSet类对象
            self = cls(**initkwargs)

            # actions = {'get': 'list', 'head': 'list', 'post': 'create'} 怎么来？？
            self.action_map = actions
            # 重点代码： 将不同的请求方法和对应的函数进行对应
            for method, action in actions.items():
            	# 设置CommentsViewSet类对象属性get、head、post，分别对应ListModelMixin.list()，CreateModelMixin.create()
                # <bound method ListModelMixin.list of <apps.viewsets.user_info.UserInfosViewSet object at 0x000001C61FF933D0>>
                handler = getattr(self, action)  # 获取CommentsViewSet类对象的属性或方法
                # 为CommentsViewSet类对象设置不同请求类型对应的方法
                setattr(self, method, handler)
            self.request = request
            self.args = args
            self.kwargs = kwargs
            # 调用 APIView(View) 的dispatch方法
** 2
            return self.dispatch(request, *args, **kwargs)
        # cls: CommentsViewSet类
        view.cls = cls
        view.initkwargs = initkwargs
        view.actions = actions
        return csrf_exempt(view)

** 2.1x
    # 对原生django的request进行封装，返回drf自己的request对象
    def initialize_request(self, request, *args, **kwargs):

** 2.1.1
        # 对原生django的request进行封装，返回drf自己的request对象
        # 调用父类 APIView(View) 的 initialize_request 方法
        request = super().initialize_request(request, *args, **kwargs)

        # 获取请求方法
        method = request.method.lower()
        if method == 'options':
            # This is a special case as we always provide handling for the
            # options method in the base `View` class.
            # Unlike the other explicitly defined actions, 'metadata' is implicit.
            self.action = 'metadata'
        else:
        	# actions = {'get': 'list', 'head': 'list', 'post': 'create'} method = 'get'
        	# self.action = 'list'
            self.action = self.action_map.get(method)
        return request

class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
	pass

class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all().order_by("-id")
    serializer_class = CommentsSerializers
    pagination_class = Pagination
    filterset_class = CommentsFilter
    # 自定义配置哪些请求可以访问
    http_method_names = ['get', 'post', 'put', 'delete']
    # authentication_classes = []
    # permission_classes = []

** 主入口
# 请求进来直接进的是类方法 ViewSetMixin.as_view() 内部的 def view(request, *args, **kwargs)
# 原因是 router.urls 会执行 view = viewset.as_view(mapping, **initkwargs)，然后返回内部函数 def view(request, *args, **kwargs)
# CBV的原理其实和FBV是一样的，请求进来都是映射到函数，然后执行函数
router.register(r"comments", viewsets.CommentsViewSet)
urlpatterns += router.urls

说明白这段代码做了哪些事情？
