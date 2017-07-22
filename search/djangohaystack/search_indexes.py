
import datetime
from haystack import indexes
from models import Person
#from models import Note
import search_utils

from django.template import loader, Context


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare(self,obj):
        data = super(PersonIndex,self).prepare(obj)
        try:
            file_obj = obj.file_upload.open()

            extracted_data = self.backend.extract_file_contents(file_obj)
            #extracted_data = search_utils.parse_to_string(obj.file_upload.path)
            #print extracted_data
        except:
            extracted_data = None
        t = loader.select_template(('../templates/search/indexes/djangohaystack/person_text.txt',))
        data['text'] = t.render(Context({'object': obj, 'extracted' :extracted_data}))
        return data
