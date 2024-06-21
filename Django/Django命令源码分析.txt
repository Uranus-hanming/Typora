django\core\management\templates.py
	class TemplateCommand(BaseCommand):
		# 最终执行具体的业务逻辑的方法
		def handle(self, app_or_project, name, target=None, **options):
			pass

django\core\management\commands\startproject.py
	class Command(TemplateCommand):
		def handle(self, **options):
			# 执行的是父类 TemplateCommand 中的 handle()
			super().handle('project', project_name, target, **options)

django\core\management\base.py
	class BaseCommand:
		def execute(self, *args, **options):def execute(self, *args, **options):
			# self指的是django.core.management.commands.startproject.Command 对象
			# 执行的是Command类中的 handle 方法
			output = self.handle(*args, **options)

		def run_from_argv(self, argv):
			# self指的是django.core.management.commands.startproject.Command 对象
			# Command类中没有定义execute方法，就找父类 TemplateCommand，父类 TemplateCommand 也没有实现execute()，
			# 所以最终执行的是BaseCommand类中的execute()
			self.execute(*args, **cmd_options)

django\core\management\__init__.py
	class ManagementUtility:
		def load_command_class(app_name, name):
			# 以字符串的方式导入模块
		    module = import_module("%s.management.commands.%s" % (app_name, name))
		    # 实例化的是django\core\management\commands\startproject路径下的Command
		    return module.Command()

		def fetch_command(self, subcommand):
			# subcommand='startproject'
			# app_name='django.core'
			app_name = commands[subcommand]
			klass = load_command_class(app_name, subcommand)
			return klass  # 返回的是django.core.management.commands.startproject.Command 对象

		def execute(self):
			# 即子命令，本例子中为：startproject
			subcommand = self.argv[1]
			# 执行的实际是django.core.management.commands.startproject.Command对象run_from_argv()
			self.fetch_command(subcommand).run_from_argv(self.argv)

	def execute_from_command_line(argv=None):
		# argv=None
	    utility = ManagementUtility(argv)  # 实例化ManagementUtility
	    utility.execute()  # 执行ManagementUtility类的execute()

django-admin.py
执行命令：django-admin.py startproject second_django

	from django.core.management import execute_from_command_line
	sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
	sys.exit(execute_from_command_line())
