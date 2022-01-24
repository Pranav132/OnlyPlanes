from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


# Form for all the sorting and filtering options on product page and search page
class FilterForm(forms.Form):

    # Setting choices for users to choose from for each kind of input

    CHOICES = [
        ('low2high', 'Price: Low to High'),
        ('high2low', 'Price: High to Low')
    ]

    RANGES = [
        ('zero', 'No price filter'),
        ('point', 'below ₹1000'),
        ('one', '₹1000 - ₹9999'),
        ('ten', '₹10,000 - ₹19,999'),
        ('twenty', '₹20,000 - ₹29,999'),
        ('thirty', '₹30,000 - ₹39,999'),
        ('fourty', '₹40,000 - ₹49,999'),
        ('fifty', '₹50,000 - ₹59,999'),
        ('sixty', '₹60,000 - ₹69,999'),
        ('seventy', '₹70,000 - ₹79,999'),
        ('eighty', '₹80,000 and above'),
    ]

    RATING = [
        ('none', 'no rating filter'),
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
