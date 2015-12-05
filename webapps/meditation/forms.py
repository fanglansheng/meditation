from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm

from meditation.models import *

from djangular.forms import NgModelFormMixin, NgForm, NgModelForm, NgFormValidationMixin
from mimetypes import guess_type


# Override AuthenticationForm and add more widgets
class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=20,
                               label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username',
                                                             'html_name': 'login_username',
                                                             'ng-model': 'login_username'}))
    password = forms.CharField(max_length=200,
                               label='Password',
                               required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password',
                                                                 'html_name': 'login_password',
                                                                 'ng-model': 'login_password'}))


# Override UserCreationForm and add more widgets
class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=254,
                               label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username',
                                                             'ng-model': 'register_username'}))
    email = forms.EmailField(max_length=254,
                             label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email',
                                                           'ng-model': 'register_email'}))
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Password',
                                                                  'ng-model': 'register_password1'}))
    password2 = forms.CharField(max_length=200,
                                label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Confirm Password',
                                           'ng-model': 'register_password2'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password1'],
                                        email=self.cleaned_data['email'])
        user.save()
        return user


# Set new password for sending email authentication
class MyPasswordResetForm(NgModelFormMixin, NgForm):
    scope_prefix = 'reset_password_data'
    form_name = 'reset_password_form'

    username = forms.CharField(max_length=254,
                               label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Username'}))
    new_password1 = forms.CharField(max_length=200,
                                    label='New Password',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': 'New Password'}))
    new_password2 = forms.CharField(max_length=200,
                                    label='Confirm New Password',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': 'Confirm New Password'}))

    def clean(self):
        cleaned_data = super(MyPasswordResetForm, self).clean()
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        try:
            User.objects.get(username__exact=username)
        except:
            raise forms.ValidationError('No such user in database.')

        if password1 != password2:
            raise forms.ValidationError('Passwords are not equal.')

        return cleaned_data


# Change password inside webapp without sending email
class MyPasswordChangeForm(PasswordChangeForm):
    scope_prefix = 'change_password_data'

    old_password = forms.CharField(max_length=200,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(max_length=200,
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(max_length=200,
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}))


class ProfileForm(NgModelFormMixin, NgFormValidationMixin, NgModelForm):
    scope_prefix = 'profile_data'
    form_name = 'profile_form'

    image = forms.ImageField(max_length=200,
                             label='Image',
                             required=False,
                             widget=forms.FileInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Image', 'ngf-select': ''}))

    class Meta:
        model = Profile
        exclude = ['user', 'favorites']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Biography', 'rows': '5'}),
        }

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        image = cleaned_data.get('image')

        if image is None:
            raise forms.ValidationError("The thing you uploaded is not an image.")

        image_type = guess_type(image.name)[0]
        if 'image' not in image_type:
            raise forms.ValidationError("The thing you uploaded is not an image.")
        return cleaned_data


class AddCommentForm(NgModelFormMixin, NgFormValidationMixin, NgModelForm):
    scope_prefix = 'comment_creation_data'
    form_name = 'create_comment_form'

    name = forms.CharField(max_length=200,
                           label='Comment Content',
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment Content'}))

    class Meta:
        model = Comment
        fields = ['content']


class CreateAlbumForm(NgModelFormMixin, NgFormValidationMixin, NgModelForm):
    scope_prefix = 'album_creation_data'
    form_name = 'create_album_form'

    name = forms.CharField(max_length=42,
                           label='Album Name',
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Album Name'}))

    image = forms.ImageField(max_length=200,
                             label='Image',
                             required=False,
                             widget=forms.FileInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Image', 'ngf-select': ''}))

    description = forms.CharField(max_length=200,
                           label='Description',
                           required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description of Album'}))
    class Meta:
        model = Album
        fields = ['name', 'image', 'description']

    def clean(self):
        cleaned_data = super(CreateAlbumForm, self).clean()
        image = cleaned_data.get('image')

        if image is None:
            raise forms.ValidationError("The thing you uploaded is not an image.")

        image_type = guess_type(image.name)[0]

        if 'image' not in image_type:
            raise forms.ValidationError("The thing you uploaded is not an image.")
        return cleaned_data


class CreateSoundForm(NgModelFormMixin, NgFormValidationMixin, NgModelForm):
    scope_prefix = 'sound_creation_data'
    form_name = 'create_sound_form'

    name = forms.CharField(max_length=42,
                           label='Sound Name',
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sound Name'}))

    url = forms.URLField(max_length=200,
                         label='Url',
                         required=False,
                         widget=forms.TextInput(
                             attrs={'class': 'form-control', 'placeholder': 'Paste a youtube media url here.'}))

    content = forms.FileField(max_length=200,
                              label='Content',
                              required=False,
                              widget=forms.FileInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Upload video or audio here',
                                         'ngf-select': ''}))

    image = forms.ImageField(max_length=200,
                             label='Image',
                             required=False,
                             widget=forms.FileInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Image', 'ngf-select': ''}))

    class Meta:
        model = Sound
        fields = ['name', 'url', 'content', 'image']

    def clean(self):
        cleaned_data = super(CreateSoundForm, self).clean()
        url = cleaned_data.get('url')
        image = cleaned_data.get('image')
        if image is None:
            raise forms.ValidationError("The image you uploaded is not an image.")
        image_type = guess_type(image.name)[0]
        if 'image' not in image_type:
            raise forms.ValidationError("The image you uploaded is not an image.")

        flag = [False, False]

        content = cleaned_data.get('content')
        if content is not None:
            content_type = guess_type(content.name)[0]
            print content_type
            if 'video' in content_type or 'audio' in content_type:
                flag[0] = True

        if url and 'https://www.youtube.com/watch?v=' in url:
            flag[1] = True

        if not any(flag):
            raise forms.ValidationError('Neither url nor content is valid, or they are not provided.')

        return cleaned_data


class CreateMusicForm(NgModelFormMixin, NgFormValidationMixin, NgModelForm):
    scope_prefix = 'music_creation_data'
    form_name = 'create_music_form'

    name = forms.CharField(max_length=42,
                           label='Music Name',
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Music Name'}))

    url = forms.URLField(max_length=200,
                         label='Url',
                         required=True,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL'}))

    class Meta:
        model = Music
        fields = ['name', 'url']

    def clean(self):
        cleaned_data = super(CreateMusicForm, self).clean()
        url = cleaned_data.get('url')

        if not url or 'https://www.youtube.com/watch?v=' not in url:
            raise forms.ValidationError('This page seems no music media. You can paste a youtube media url here.')

        return cleaned_data
