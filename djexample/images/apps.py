from django.apps import AppConfig


class ImagesConfig(AppConfig):
	name = 'images'
	verbose_name = 'Image Bookmars'

	def ready(self):
		import images.signals