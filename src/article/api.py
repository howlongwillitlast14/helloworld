from tastypie.resources import ModelResource
from tastypie.constants import ALL
from .models import Article

class ArticleResource(ModelResource):
	class Meta:
		queryset = Article.objects.all()
		resource_name = "article"  ##when it is called on our urls...
		filtering = { "title" : ALL }
