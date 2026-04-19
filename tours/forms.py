from django import forms
from .models import Tour

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        exclude = ['assigned_by', 'driver', 'status']
        # fields = '__all__'

        widgets = {
            'pickup_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'dropoff_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base_class = (
            'w-full px-3 py-2 border border-gray-300 '
            'rounded-md focus:outline-none focus:ring-2 '
            'focus:ring-blue-500 text-black bg-white'
        )

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': base_class,
                'placeholder': field.label
            })