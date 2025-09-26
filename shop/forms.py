from django import forms
from .models import Product
from .models import Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'stock_quantity', 'image', 'is_featured']
        widgets = {
        'category': forms.Select(attrs={'class': 'w-full ...'}), # Add Tailwind classes
        'name': forms.TextInput(attrs={'class': 'w-full ...'}),
        # Add classes for all fields
        }
        
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)], attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
        }