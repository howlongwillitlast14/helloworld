from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyRegistrationForm(UserCreationForm):
	##which fields should be displayed in html? Very Convenient No need to make all the forms..and securing it
	email = forms.EmailField(required=True)##Emailfield is defioned in forms
	## 'Embedded class' that is defined within the scope of the form we created
	#simply to hold anything that is NOT a form Field : that is what the model is, what the fields are, what is the
	## what orderings.. Django tells!! This is the other info of the models other than the declared email field
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
    ## the save method below is almost a duplicate from that of
    #django.conrib.auth.forms' usercreationform class'
	def save(self, commit=True):
		user = super(MyRegistrationForm, self).save(commit=False)
		## If we make changes to models, we have to commit it by saving it
		#but because we are not finished yet, we do not commit it
		user.email = self.cleaned_data['email']
		## now we have added our custom field, lets commit it and save it
		
		if commit:
			user.save()

		return user



class ContactForm1(forms.Form):
	subject = forms.CharField(max_length=100)

class ContactForm2(forms.Form):
	sender = forms.EmailField()

class ContactForm3(forms.Form):
	message = forms.CharField(widget=forms.Textarea)