#python first
#3django second
#your apps

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.core.context_processors import csrf
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from haystack.query import SearchQuerySet
from django.utils import timezone
from django.template import RequestContext
''' Create your views here.
##if you need to start using things like messages, we have to use 
Requestcontext  : recognize the things that are passed from one page
 to the another (the text that is capable of doing that can parser 
up those messages is request context)
#3rendertoresponse   only template and arguments(basic context object)'''
from django.contrib import messages

def articles(request):
	language = 'en-gb'
	session_language = 'en-gb'
	
	if 'lang' in request.COOKIES:
			language = request.COOKIES['lang']
	if 'lang' in request.session:
		session_language = request.session['lang']

	args = {}
	args.update(csrf(request))
	args['articles'] = Article.objects.all()
	args['language'] = language
	args['session_language'] = session_language

	return render_to_response('articles.html/', args)

def article(request, article_id):
	return render_to_response('article.html/', {'article': Article.objects.get(id=article_id)},
								context_instance=RequestContext(request))
	#return render('article.html', {'article': Article.objects.get(id=article_id)})

def thankyou(request):

	return render_to_response("thankyou.html", locals(),
						context_instance=RequestContext(request))

def aboutus(request):

	return render_to_response("aboutus.html", locals(),
						context_instance=RequestContext(request))


def language(request, language='en-gb'):

	response = HttpResponse("setting language to %s" % language)

	response.set_cookie('lang', language)

	request.session['lang'] = language
	return response

def create(request):
	if request.POST:
		form = ArticleForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, "Your Article was added")
			return HttpResponseRedirect('/articles/all')
	else:
		form = ArticleForm()
	args = {}
	args.update(csrf(request))

	args['form'] = form
	return render_to_response('create_article.html', args)

def like_article(request, article_id):
	if article_id:
		a = Article.objects.get(id=article_id)##Updating 	the database record!
		count = a.likes
		count +=1
		a.likes = count
		a.save()## when saving, updating a record always remeber!!

	return HttpResponseRedirect('/articles/get/%s' % article_id)

def add_comment(request, article_id):
	a = Article.objects.get(id=article_id)

	if request.method == "POST":
			f = CommentForm(request.POST)
			if f.is_valid():
				c = f.save(commit=False)
				c.pub_date = timezone.now()
				c.article = a
				c.save()##success message is already built in so you can use the shortcut like the below

				messages.success(request, "Your comment was added")

				return HttpResponseRedirect('/articles/get/%s' % article_id)
	else:
		f = CommentForm()

	args = {}
	args.update(csrf(request))
	args['article'] = a
	args['form'] = f

	return render_to_response('add_comment.html', args)

def delete_comment(request, comment_id):
	c = Comment.objects.get(id=comment_id)

	article_id = c.article.id

	c.delete()
	messages.add_message(request,
						settings.DELETE_MESSAGE,
						"Your comment was deleted")
	return HttpResponseRedirect("/articles/get/%s" % article_id)

def search_titles(request):

	articles = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_text', ''))

	return render_to_response('ajax_search.html', {'articles' : articles})