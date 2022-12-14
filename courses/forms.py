from django import forms
from .widgets import CustomClearableFileInput
from .models import Course, Category, CourseReview


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class CourseReviewForm(forms.ModelForm):
    """
    Adding the course review
    """
    class Meta:
        model = CourseReview
        fields = ('title', 'content',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated labels
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'title': 'Write a review title here',
            'content': 'Write your review here',
        }

        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False