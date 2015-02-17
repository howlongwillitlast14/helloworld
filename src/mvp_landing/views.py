from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth   ##check username, password
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
##Actually we dont need the above one anymore.. since we customized it
from .forms import MyRegistrationForm
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail


def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('accounts/login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')## if we dont get username because it doesnt exist, it will just return blank
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	##if it finds a match, it will return to us a User Object
	##if not, return NONe

	if user is not None:
		##actually log him in
		 auth.login(request, user)
		 return HttpResponseRedirect('/accounts/loggedin')
	else:
		return HttpResponseRedirect('/accounts/invalid')

## we need update our database
##user authentication system creates a new table in a database 
## that deal with users that stores..

def loggedin(request):
	return render_to_response('accounts/loggedin.html')

def invalid_login(request):
	return render_to_response('accounts/invalid.html')

def logout(request):
	auth.logout(request)
	return render_to_response('accounts/logout.html', {'full_name': request.user.username})

def register_user(request):
	if request.method == 'POST':#not activated at the first time
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register_success')

##When user visits the register page for the firsttime
	args = {}
	args.update(csrf(request))

	args['form'] = MyRegistrationForm() ## blank user creation form that has no info


	return render_to_response('accounts/register.html', args)



def register_success(request):
	return render_to_response('accounts/register_success.html')


##class based view

class ContactWizard(SessionWizardView):
	template_name = "contact_form.html"

	def done(self, form_list, **kwargs):
		form_data = process_form_data(form_list)

		return render_to_response('done.html', {'form_data' : form_data})

def process_form_data(form_list):
	form_data = [form.cleaned_data for form in form_list]

	send_mail(form_data[0]['subject'],
			form_data[2]['message'], form_data[1]['sender'],
			['howlongwillitlast14@gmail.com'], fail_silently=False)

	return form_data





