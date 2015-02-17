from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from mvp_landing.forms import ContactForm1, ContactForm2, ContactForm3
from mvp_landing.views import ContactWizard
#casue admin system to look thorou all the models in our current django project
##so all the following urls could be done on admin

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    (r'^articles/', include('article.urls')),
    (r'^accounts/', include('userprofile.urls')),
    url(r'^thank-you/$', 'article.views.thankyou', name='thankyou'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^about-us/$', 'article.views.aboutus', name='aboutus'),
    url(r'^accounts/login/$', 'mvp_landing.views.login'),
    url(r'^accounts/logout/$', 'mvp_landing.views.logout'),
    url(r'^accounts/auth/$', 'mvp_landing.views.auth_view'),
    url(r'^accounts/loggedin/$', 'mvp_landing.views.loggedin'),
    url(r'^accounts/invalid/$', 'mvp_landing.views.invalid_login'),    
    url(r'^language/(?P<language>[a-z\-]+)/$', 'article.views.language'),
    url(r'^accounts/register/$', 'mvp_landing.views.register_user'),
    url(r'^accounts/register_success/$', 'mvp_landing.views.register_success'),
    url(r'^contact/$', ContactWizard.as_view([ContactForm1, ContactForm2, ContactForm3])),
    url(r'^search/', include('haystack.urls')),
)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, 
							document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, 
							document_root=settings.MEDIA_ROOT)