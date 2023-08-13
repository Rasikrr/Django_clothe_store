from django import forms


class ProductFilterForm(forms.Form):
    SIZE_CHOICES = [
        ('', 'All'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ("2XL", "2XL")
    ]
    SORT_CHOICES = [
        ("Ascending Price", "Ascending Price"),
        ("Descending Price", "Descending Price"),
    ]
    size = forms.ChoiceField(choices=SIZE_CHOICES, required=False)
    sort = forms.ChoiceField(choices=SORT_CHOICES, required=False)


class OutwearFilterForm(ProductFilterForm):
    TYPE = [
        ("Jacket", "Jacket"),
        ("Coat", "Coat"),
    ]

    type_of_outwear = forms.MultipleChoiceField(choices=TYPE, required=False)
