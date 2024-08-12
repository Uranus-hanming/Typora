############################## 加载中间件 ################################


class WSGIHandler(base.BaseHandler):
    request_class = WSGIRequest

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_middleware()


class BaseHandler:
    _view_middleware = None
    _template_response_middleware = None
    _exception_middleware = None
    _middleware_chain = None

    def load_middleware(self, is_async=False):
        # self: <django.core.handlers.wsgi.WSGIHandler object at 0x0000017880CFFA90>

        self._view_middleware = []
        self._template_response_middleware = []
        self._exception_middleware = []
        # SyntaxError('invalid syntax', ('<string>', 1, 1, '<bound method BaseHandler._get_response of <django.core.handlers.wsgi.WSGIHandler object at 0x0000017880CFFA90>>', 1, 2))
        get_response = self._get_response_async if is_async else self._get_response
        # SyntaxError('invalid syntax', ('<string>', 1, 1, '<function BaseHandler._get_response at 0x0000017880E47370>', 1, 2))
        handler = convert_exception_to_response(get_response)
        handler_is_async = is_async

        # ['django.middleware.security.SecurityMiddleware', 
	        # 'django.contrib.sessions.middleware.SessionMiddleware', 
	        # 'django.middleware.common.CommonMiddleware', 
	        # 'django.middleware.csrf.CsrfViewMiddleware', 
	        # 'django.contrib.auth.middleware.AuthenticationMiddleware', 
	        # 'django.contrib.messages.middleware.MessageMiddleware', 
	        # 'django.middleware.clickjacking.XFrameOptionsMiddleware']
        for middleware_path in reversed(settings.MIDDLEWARE):
            middleware = import_string(middleware_path)
            middleware_can_sync = getattr(middleware, 'sync_capable', True)
            middleware_can_async = getattr(middleware, 'async_capable', False)
            try:
                # 
                adapted_handler = self.adapt_method_mode(
                    middleware_is_async, handler, handler_is_async,
                    debug=settings.DEBUG, name='middleware %s' % middleware_path,
                )
                # 
                mw_instance = middleware(adapted_handler)
            else:
            	# 
                handler = adapted_handler
            # 重点
            # mw_instance=<XFrameOptionsMiddleware get_response=BaseHandler._get_response>
            handler = convert_exception_to_response(mw_instance)  # 这个函数怎么理解？？
            handler_is_async = middleware_is_async

        # 
        handler = self.adapt_method_mode(is_async, handler, handler_is_async)
        # 
        self._middleware_chain = handler


#################################### 中间件类 ######################################

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


class SecurityMiddleware(MiddlewareMixin):
	def process_request(self, request):
        path = request.path.lstrip("/")
        if (self.redirect and not request.is_secure() and
                not any(pattern.search(path)
                        for pattern in self.redirect_exempt)):
            host = self.redirect_host or request.get_host()
            return HttpResponsePermanentRedirect(
                "https://%s%s" % (host, request.get_full_path())
            )

    def process_response(self, request, response):
    	pass

class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.SessionStore(session_key)

    def process_response(self, request, response):
    	pass

class CommonMiddleware(MiddlewareMixin):
	def process_request(self, request):
		pass

	def process_response(self, request, response):
        if response.status_code == 404 and self.should_redirect_with_slash(request):
            return self.response_redirect_class(self.get_full_path_with_slash(request))
        if not response.streaming and not response.has_header('Content-Length'):
            response.headers['Content-Length'] = str(len(response.content))
        return response


class CsrfViewMiddleware(MiddlewareMixin):
	def process_request(self, request):
        try:
            csrf_token = self._get_token(request)
        except InvalidTokenFormat:
            _add_new_csrf_cookie(request)
        else:
            if csrf_token is not None:
                # Use same token next time.
                request.META['CSRF_COOKIE'] = csrf_token

	def process_response(self, request, response):
        if request.META.get('CSRF_COOKIE_NEEDS_UPDATE'):
            self._set_csrf_cookie(request, response)
            request.META['CSRF_COOKIE_NEEDS_UPDATE'] = False

        return response


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'session'):
            raise ImproperlyConfigured(
                "The Django authentication middleware requires session "
                "middleware to be installed. Edit your MIDDLEWARE setting to "
                "insert "
                "'django.contrib.sessions.middleware.SessionMiddleware' before "
                "'django.contrib.auth.middleware.AuthenticationMiddleware'."
            )
        request.user = SimpleLazyObject(lambda: get_user(request))

class MessageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._messages = default_storage(request)

	def process_response(self, request, response):
        if hasattr(request, '_messages'):
            unstored_messages = request._messages.update(response)
            if unstored_messages and settings.DEBUG:
                raise ValueError('Not all temporary messages could be stored.')
        return response


class XFrameOptionsMiddleware(MiddlewareMixin):
	def process_response(self, request, response):
        # Don't set it if it's already in the response
        if response.get('X-Frame-Options') is not None:
            return response

        # Don't set it if they used @xframe_options_exempt
        if getattr(response, 'xframe_options_exempt', False):
            return response

        response.headers['X-Frame-Options'] = self.get_xframe_options_value(
            request,
            response,
        )
        return response


################################ 中间件源码 ###########################################


def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # <XFrameOptionsMiddleware get_response=BaseHandler._get_response>
    # <MessageMiddleware get_response=convert_exception_to_response.<locals>.inner>
    # <AuthenticationMiddleware get_response=convert_exception_to_response.<locals>.inner>
    # <CsrfViewMiddleware get_response=convert_exception_to_response.<locals>.inner>
    # <CommonMiddleware get_response=convert_exception_to_response.<locals>.inner>
    # <SessionMiddleware get_response=convert_exception_to_response.<locals>.inner>
    # <SecurityMiddleware get_response=convert_exception_to_response.<locals>.inner>
    return wrapper

def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)


def convert_exception_to_response(get_response):
    # 重点
    @wraps(get_response)
    def inner(request):
        try:
** 5
			# 
            response = get_response(request)
        except Exception as exc:
            response = response_for_exception(request, exc)
        return response
    return inner

class MiddlewareMixin:
	# 重点、
** 6
	# 所有的中间件都需要继承 MiddlewareMixin 类，然后实现自己的方法 process_request、process_response
	def __call__(self, request):
        if asyncio.iscoroutinefunction(self.get_response):
            return self.__acall__(request)
        response = None
        if hasattr(self, 'process_request'):
** 7		# <SecurityMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <SessionMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <CommonMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <CsrfViewMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <AuthenticationMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <MessageMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <XFrameOptionsMiddleware get_response=BaseHandler._get_response>
            response = self.process_request(request)
** 8
		# 关键代码
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
** 9
			# <XFrameOptionsMiddleware get_response=BaseHandler._get_response>
			# <MessageMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <AuthenticationMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <CsrfViewMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <CommonMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <SessionMiddleware get_response=convert_exception_to_response.<locals>.inner>
			# <SecurityMiddleware get_response=convert_exception_to_response.<locals>.inner>
            response = self.process_response(request, response)
        return response


class WSGIHandler(base.BaseHandler):
	def __call__(self, environ, start_response):
** 3
		# self: <django.core.handlers.wsgi.WSGIHandler object at 0x000002D6F7461B10>
		# request: <WSGIRequest: GET '/books/test/'>
		response = self.get_response(request)


class StaticFilesHandler(StaticFilesHandlerMixin, WSGIHandler):
	def __call__(self, environ, start_response):
        if not self._should_handle(get_path_info(environ)):
** 2
            return self.application(environ, start_response)
        return super().__call__(environ, start_response)

class BaseHandler:
	def get_response(self, request):
		set_urlconf(settings.ROOT_URLCONF)
** 4
		# self._middleware_chain: <function convert_exception_to_response.<locals>.inner at 0x0000016AD4BA0EE0>
        response = self._middleware_chain(request)

	def run(self, application):
        self.setup_environ()
** 1	
		# 返回：<HttpResponse status_code=200, "text/plain">
		# self: <django.core.servers.basehttp.ServerHandler object at 0x000002D6F752D0F0>
		# application: <django.contrib.staticfiles.handlers.StaticFilesHandler object at 0x000002D6F74AA4D0>
		# self.environ: {'ALLUSERSPROFILE': 'C:\\ProgramData', 'APPDATA': 'C:\\Users\\hanming.qin\\AppData\\Roaming', 'CHOCOLATEYINSTALL': 'C:\\ProgramData\\chocolatey', 'CHOCOLATEYLASTPATHUPDATE': '133494389561011580', 'CHROME_CRASHPAD_PIPE_NAME': '\\\\.\\pipe\\crashpad_13580_MTDQIJDLPHEAKXIE', 'COMMONPROGRAMFILES': 'C:\\Program Files\\Common Files', 'COMMONPROGRAMFILES(X86)': 'C:\\Program Files (x86)\\Common Files', 'COMMONPROGRAMW6432': 'C:\\Program Files\\Common Files', 'COMPUTERNAME': 'HANMING-QIN', 'COMSPEC': 'C:\\Windows\\system32\\cmd.exe', 'DRIVERDATA': 'C:\\Windows\\System32\\Drivers\\DriverData', 'FPS_BROWSER_APP_PROFILE_STRING': 'Internet Explorer', 'FPS_BROWSER_USER_PROFILE_STRING': 'Default', 'HOMEDRIVE': 'C:', 'HOMEPATH': '\\Users\\hanming.qin', 'LOCALAPPDATA': 'C:\\Users\\hanming.qin\\AppData\\Local', 'LOGONSERVER': '\\\\PACTERA-TGSC-AD', 'NUMBER_OF_PROCESSORS': '8', 'NVM_HOME': 'C:\\Users\\hanming.qin\\AppData\\Roaming\\nvm', 'NVM_SYMLINK': 'C:\\Program Files\\nodejs', 'ONEDRIVE': 'C:\\Users\\hanming.qin\\OneDrive', 'ORIGINAL_XDG_CURRENT_DESKTOP': 'undefined', 'OS': 'Windows_NT', 'PATH': 'c:\\Users\\hanming.qin\\.vscode\\extensions\\ms-python.python-2024.12.2-win32-x64\\python_files\\deactivate\\powershell;D:\\typora\\env/Scripts;c:\\Users\\hanming.qin\\.vscode\\extensions\\ms-python.python-2024.12.2-win32-x64\\python_files\\deactivate\\powershell;D:\\typora\\env/Scripts;C:\\Windows\\system32;C:\\Windows;C:\\Windows\\System32\\Wbem;C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\;C:\\Windows\\System32\\OpenSSH\\;VN\\bin;D:\\svnclient\\bin;C:\\ProgramData\\chocolatey\\bin;D:\\Android\\platform-tools;C:\\Program Files\\dotnet\\;C:\\Program Files\\Docker\\Docker\\resources\\bin;C:\\Users\\hanming.qin\\AppData\\Roaming\\nvm;C:\\Program Files\\nodejs;D:\\wxdevelop\\微信web开发者工具\\dll;;;D:\\软件安装\\Git\\cmd;C:\\Users\\hanming.qin\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\;C:\\Users\\hanming.qin\\AppData\\Local\\Programs\\Python\\Python310\\;C:\\Users\\hanming.qin\\AppData\\Local\\Microsoft\\WindowsApps;D:\\软件安装\\PyCharm Community Edition 2024.1.1\\bin;;C:\\Program Files\\JetBrains\\PyCharm 2023.2.3\\bin;;D:\\软件安装\\Microsoft VS Code\\bin;C:\\Users\\hanming.qin\\AppData\\Roaming\\nvm;C:\\Program Files\\nodejs', 'PATHEXT': '.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL', 'PROCESSOR_ARCHITECTURE': 'AMD64', 'PROCESSOR_IDENTIFIER': 'Intel64 Family 6 Model 158 Stepping 9, GenuineIntel', 'PROCESSOR_LEVEL': '6', 'PROCESSOR_REVISION': '9e09', 'PROGRAMDATA': 'C:\\ProgramData', 'PROGRAMFILES': 'C:\\Program Files', 'PROGRAMFILES(X86)': 'C:\\Program Files (x86)', 'PROGRAMW6432': 'C:\\Program Files', 'PSMODULEPATH': 'C:\\Users\\hanming.qin\\Documents\\WindowsPowerShell\\Modules;C:\\Program Files\\WindowsPowerShell\\Modules;C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\Modules;D:\\SVN\\PowerShellModules', 'PUBLIC': 'C:\\Users\\Public', 'PYCHARM': 'C:\\Program Files\\JetBrains\\PyCharm 2023.2.3\\bin;', 'PYCHARM COMMUNITY EDITION': 'D:\\软件安装\\PyCharm Community Edition 2024.1.1\\bin;', 'SESSIONNAME': 'Console', 'SYSTEMDRIVE': 'C:', 'SYSTEMROOT': 'C:\\Windows', 'TEMP': 'C:\\Users\\hanming.qin\\AppData\\Local\\Temp', 'TMP': 'C:\\Users\\hanming.qin\\AppData\\Local\\Temp', 'USERDNSDOMAIN': 'PACTERA_TGSC.CN', 'USERDOMAIN': 'PACTERA_TGSC', 'USERDOMAIN_ROAMINGPROFILE': 'PACTERA_TGSC', 'USERNAME': 'hanming.qin', 'USERPROFILE': 'C:\\Users\\hanming.qin', 'VISUALSVN_SERVER': 'D:\\SVN\\', 'WINDIR': 'C:\\Windows', 'TERM_PROGRAM': 'vscode', 'TERM_PROGRAM_VERSION': '1.92.1', 'LANG': 'zh_CN.UTF-8', 'COLORTERM': 'truecolor', 'GIT_ASKPASS': 'd:\\软件安装\\Microsoft VS Code\\resources\\app\\extensions\\git\\dist\\askpass.sh', 'VSCODE_GIT_ASKPASS_NODE': 'D:\\软件安装\\Microsoft VS Code\\Code.exe', 'VSCODE_GIT_ASKPASS_EXTRA_ARGS': '', 'VSCODE_GIT_ASKPASS_MAIN': 'd:\\软件安装\\Microsoft VS Code\\resources\\app\\extensions\\git\\dist\\askpass-main.js', 'VSCODE_GIT_IPC_HANDLE': '\\\\.\\pipe\\vscode-git-e04f6e83c8-sock', 'VIRTUAL_ENV': 'D:\\typora\\env', ...}
        # self.start_response: 
        self.result = application(self.environ, self.start_response)
        self.finish_response()

** 8.1x
	def resolve_request(self, request):
		# <URLResolver 'first_django.urls' (None:None) '^/'>
        resolver = get_resolver()
        # request.path_info='/books/test/'
        # 调用类方法: URLResolver.resolve()
        # 返回: ResolverMatch(func=books.views.view, args=(), kwargs={}, url_name=None, app_names=[], namespaces=[], route='books/test/')
** 8.1.1
        resolver_match = resolver.resolve(request.path_info)
        request.resolver_match = resolver_match
        return resolver_match

** 8x
	def _get_response(self, request):
		# callback: SyntaxError('invalid syntax', ('<string>', 1, 1, '<function View.as_view.<locals>.view at 0x0000016AD4AC8550>', 1, 2))
		# callback_args: ()
		# callback_kwargs: {}
** 8.1
		callback, callback_args, callback_kwargs = self.resolve_request(request)

		# 什么都没做，直接返回 callback
		# SyntaxError('invalid syntax', ('<string>', 1, 1, '<function View.as_view.<locals>.view at 0x0000016AD4AC8550>', 1, 2))
** 8.2
		wrapped_callback = self.make_view_atomic(callback)
		# 调用视图类 View.as_view() 的内部函数 def view()
** 8.3
		response = wrapped_callback(request, *callback_args, **callback_kwargs)
        return response

** 8.2x
	def make_view_atomic(self, view):
        non_atomic_requests = getattr(view, '_non_atomic_requests', set())
        # 数据库连接？？
        for db in connections.all():
            if db.settings_dict['ATOMIC_REQUESTS'] and db.alias not in non_atomic_requests:
                if asyncio.iscoroutinefunction(view):
                    raise RuntimeError(
                        'You cannot use ATOMIC_REQUESTS with async views.'
                    )
                view = transaction.atomic(using=db.alias)(view)
        return view


############################ 视图类 ######################################

class URLResolver:

** 8.1.1x
	# 重点，路由匹配
	def resolve(self, path):
        path = str(path)  # path may be a reverse_lazy object
        tried = []
        match = self.pattern.match(path)
        if match:
            new_path, args, kwargs = match
            for pattern in self.url_patterns:
                try:
                    sub_match = pattern.resolve(new_path)
                except Resolver404 as e:
                    self._extend_tried(tried, pattern, e.args[0].get('tried'))
                else:
                    if sub_match:
                        # Merge captured arguments in match with submatch
                        sub_match_dict = {**kwargs, **self.default_kwargs}
                        # Update the sub_match_dict with the kwargs from the sub_match.
                        sub_match_dict.update(sub_match.kwargs)
                        # If there are *any* named groups, ignore all non-named groups.
                        # Otherwise, pass all non-named arguments as positional arguments.
                        sub_match_args = sub_match.args
                        if not sub_match_dict:
                            sub_match_args = args + sub_match.args
                        current_route = '' if isinstance(pattern, URLPattern) else str(pattern.pattern)
                        self._extend_tried(tried, pattern, sub_match.tried)
                        return ResolverMatch(
                            sub_match.func,
                            sub_match_args,
                            sub_match_dict,
                            sub_match.url_name,
                            [self.app_name] + sub_match.app_names,
                            [self.namespace] + sub_match.namespaces,
                            self._join_route(current_route, sub_match.route),
                            tried,
                        )
                    tried.append([pattern])
            raise Resolver404({'tried': tried, 'path': new_path})
        raise Resolver404({'path': path})

class View:
	@classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError(
                    'The method name %s is not accepted as a keyword argument '
                    'to %s().' % (key, cls.__name__)
                )
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

** 8.3x
        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            self.setup(request, *args, **kwargs)
            if not hasattr(self, 'request'):
                raise AttributeError(
                    "%s instance has no 'request' attribute. Did you override "
                    "setup() and forget to call super()?" % cls.__name__
                )
            return self.dispatch(request, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # __name__ and __qualname__ are intentionally left unchanged as
        # view_class should be used to robustly determine the name of the view
        # instead.
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        view.__annotations__ = cls.dispatch.__annotations__
        # Copy possible attributes set by decorators, e.g. @csrf_exempt, from
        # the dispatch method.
        view.__dict__.update(cls.dispatch.__dict__)

        return view


