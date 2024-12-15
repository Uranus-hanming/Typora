





** 1.1.1.1x
def _get_queryset(klass):
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass

** 1.1.1x
def get_object_or_404(klass, *args, **kwargs):
	# klass: 过滤后的QuerySet对象
	# args=()
	# kwargs={'pk': '109'}
** 1.1.1.1
    queryset = _get_queryset(klass)

    # 重点
    # 调用类方法 QuerySet.get()
    # 返回模型类 BugRecord 第109条数据的对象
    return queryset.get(*args, **kwargs)

** 1.1x
def get_object_or_404(queryset, *filter_args, **filter_kwargs):
	# queryset：过滤后的QuerySet对象
	# filter_args=()
	# filter_kwargs={'pk': '109'}
** 1.1.1
    return _get_object_or_404(queryset, *filter_args, **filter_kwargs)


class APIView(View):
    def get_permissions(self):
    	# self.permission_classes: 获取视图类的属性permission_classes
        return [permission() for permission in self.permission_classes]

** 1.2x
    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            # 查询单例时权限校验了两次，一次是在dispatch时调用permission.has_permission()进行校验，这里是调用permission.has_object_permission()
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )


class GenericAPIView(views.APIView):

** 1x
    def get_object(self):
    	# self: <bk_power.ecology.viewsets.bug_record.BugRecordViewSet object at 0x000002BB4EC55450>

    	# 和list一样，返回过滤后的QuerySet对象
        queryset = self.filter_queryset(self.get_queryset())
        # 从视图类BugRecordViewSet对象中分别查询属性lookup_url_kwarg和lookup_field
        # lookup_url_kwarg=pk
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        # self.kwargs={'pk': '109'}
        # filter_kwargs={'pk': '109'}
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
** 1.1
        # <BugRecord: BugRecord object (109)> 返回模型类 BugRecord 第109条数据的对象
        obj = get_object_or_404(queryset, **filter_kwargs)
** 1.2
        # 权限校验
        self.check_object_permissions(self.request, obj)

        return obj



################################# 视图类 ################################

class ViewSetMixin:
	pass

class GenericViewSet(ViewSetMixin, generics.GenericAPIView):
    pass


class RetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
    	# self: <bk_power.ecology.viewsets.bug_record.BugRecordViewSet object at 0x000002BB4E96ADD0> 视图类对象
    	# request: <rest_framework.request.Request: GET '/api/v1/bug_record/109/'>
    	# args: ()
    	# kwargs: {'pk': '109'}

** 1
        instance = self.get_object()

** 2
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ModelViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

class BugRecordViewSet(viewsets.ModelViewSet):
    queryset = BugRecord.objects.all().order_by("-created_at")
    serializer_class = BugRecordSerializer
    pagination_class = BugRecordPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BugRecordFilter
    permission_classes = []

