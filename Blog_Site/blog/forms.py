from .models import Post,Comment
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','text']

        widgets ={
            'title':forms.TextInput(attrs={'class':'form-control form-control-custom','id':'form-control-custom',
                                           'placeholder':'Enter blog title'}),
            'text':forms.Textarea(attrs={'class':'form-control form-control-custom update-text','id':'form-control-custom-text',
                                         'placeholder':'Type your blog content','rows':10,'cols':800}),

        }

    def __init__(self, *args, **kwargs):


        self.request = kwargs.pop("request", None)  # Pop the request off the passed in kwargs.
        super(PostForm, self).__init__(*args, **kwargs)
        self.data=""
        if 'data' in kwargs:
            self.data = kwargs['data']

    def clean(self):

        if 'publish' in self.data:
            self.publish = True
        else:
            self.publish = False

    def save(self,*args,**kwargs):
        post = super(PostForm,self).save(*args,**kwargs)
        if self.publish:
            post.published_date = timezone.now()
            post.save()

        return post



class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment
        fields = ('text',)
        #exclude = ['comment']
        widgets = {
            'author':forms.TextInput(attrs={'class':'form-control comment-author form-control-custom',
                                            'id': 'form-control-custom',
                                            'placeholder':'Enter your Name'},),
            'text':forms.Textarea(attrs={'class':'form-control comment-text form-control-custom',
                                         'id': 'form-control-custom',
                                         'placeholder':'Type your comment',
                                         'rows':3}),
        }

class RegistrationForm(forms.ModelForm):
    #password = forms.CharField()
    confirm_password = forms.CharField(widget=forms.PasswordInput,required=True)
    confirm_password.widget = forms.PasswordInput(attrs={'class': 'form-control  form-control-custom signup-form-input',
                                                   'id': 'form-control-custom-cfm-pwd',
                                                   'placeholder': 'Re-enter Password'})
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password')

        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control  form-control-custom signup-form-input',
                                            'id': 'form-control-custom',
                                            'placeholder':'Enter Username for your account'},),

            'email' : forms.EmailInput(attrs={'class':'form-control  form-control-custom signup-form-input',
                                            'id': 'form-control-custom',
                                            'placeholder':'Enter a valid Mail ID'},),

            'first_name' :  forms.TextInput(attrs={'class':'form-control  form-control-custom signup-form-input',
                                            'id': 'form-control-custom',
                                            'placeholder':'Enter First Name'},),

            'last_name': forms.TextInput(attrs={'class': 'form-control  form-control-custom signup-form-input',
                                                 'id': 'form-control-custom',
                                                 'placeholder': 'Enter Last Name'},),

            'password' : forms.PasswordInput(attrs={'class': 'form-control  form-control-custom signup-form-input',
                                                 'id': 'form-control-custom',
                                                 'placeholder': 'Enter Password'},),


        }

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")


        if len(password)<8:
            raise forms.ValidationError(
                "Your password must contain at least 8 characters"
            )
        elif password != confirm_password:
            raise forms.ValidationError(
                "Password mismatch"
            )