from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from myPinterest.models import Pin


@registry.register_document
class PinDocument(Document):
    class Index:
        name = 'pins'  

    class Django:
        model = Pin
        fields = [
            'title',
            'category',
            'image_url',
        ]