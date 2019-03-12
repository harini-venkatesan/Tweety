from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
class ElasticSearchappConfig(AppConfig):
    name = 'elasticsearchapp'

    def ready(self):
        import elasticsearch.signals