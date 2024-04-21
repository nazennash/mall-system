from django import forms
from .models import Order, Feedback, ForumPost, ForumComment, UserProfile, Advertisement

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = "__all__"
        exclude = ['participants']

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['delivery_address']

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['name', 'image', 'link', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
