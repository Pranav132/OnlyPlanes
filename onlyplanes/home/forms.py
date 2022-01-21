from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


# Form for all the sorting and filtering options on product page and search page
class FilterForm(forms.Form):

    # Setting choices for users to choose from for each kind of input

    CHOICES = [
        ('popularity', 'Popularity'),
        ('low2high', 'Price: Low to High'),
        ('high2low', 'Price: High to Low')
    ]

    RANGES = [
        ('zero', 'No price filter'),
        ('five', 'Below ₹500'),
        ('ten', 'Below ₹1000'),
        ('twenty', 'Below ₹2000'),
        ('thirty', 'Below ₹3000'),
        ('fourty', 'Below ₹4000'),
        ('fifty', 'Below ₹5000'),
        ('sixty', 'Below ₹6000'),
        ('seventy', 'Below ₹7000'),
        ('eighty', 'Below ₹8000'),
    ]

    RATING = [
        ('five', '5-star'),
        ('four', '4-star and above'),
        ('three', '3-star and above'),
        ('two', '2-star and above'),
        ('one', '1-star and above'),
    ]

    # Setting inputs and types of inputs

    name = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect(
            attrs={'class': 'dropdown-item'}
        ))

    price = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect(attrs={'class': 'dropdown-item'}), choices=RANGES)

    rating = forms.MultipleChoiceField(
        required=False, widget=forms.RadioSelect(attrs={'class': 'dropdown-item'}), choices=RATING)
