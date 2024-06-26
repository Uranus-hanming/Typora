
django/conf/__init__.py
	class Settings:
		def __init__(self, settings_module):  # 'first_django.settings'
			# 先从 global_settings 导入属性，然后再从 first_django.settings 属性，如果属性名相同的会覆盖global_settings中的属性，
			# 因此给用户的感觉是配置会优先从first_django.settings中查找，找不到时才去global_settings中查找
			for setting in dir(global_settings):
	            if setting.isupper():
	                # self指的是Settings对象，这里的含义是将global_settings属性值赋给Settings对象
	                setattr(self, setting, getattr(global_settings, setting))
	        
	        self.SETTINGS_MODULE = settings_module
	        # 导入first_django.settings
	        mod = importlib.import_module(self.SETTINGS_MODULE)

	        for setting in dir(mod):
	            if setting.isupper():
	                setting_value = getattr(mod, setting)
	                setattr(self, setting, setting_value)

	class LazySettings(LazyObject):
		def _setup(self, name=None):
			# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "first_django.settings")  # manage.py文件中的配置
			# ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
			settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
			self._wrapped = Settings(settings_module)

		def __getattr__(self, name):
	        if self._wrapped is empty:
	            self._setup(name)
	        # self._wrapped是 Settings 对象，因此是去获取Settings对象中的属性
	        val = getattr(self._wrapped, name)
	        # 添加缓存，懒加载，获取属性的时候，会首先从__dict__里面获取。如果该属性存在就输出其值，如果不存在则会去找_getatrr_方法。
	        self.__dict__[name] = val
	        return val

		settings = LazySettings()

from django.conf import settings
# 获取数据库配置信息
settings.DATABASES  # 调用的是LazySettings对象的__getattr__方法
