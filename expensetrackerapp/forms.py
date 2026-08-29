from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            'amount',
            'category',
            'description',
            'date',
        ]

        widgets = {
            'amount': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter amount'
                }
            ),

            'description': forms.TextInput(
                attrs={
                    'placeholder': 'What did you spend money on?'
                }
            ),

            'date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }