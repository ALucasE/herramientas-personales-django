from django import forms
from .models import Recipe, Quality, Ingredient, Unit

class QualityForm(forms.ModelForm):
    class Meta:
        model = Quality
        fields = ('ingredient', 'unit', 'quantity', 'notes')
        

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title','description', 'instructions', 'image', 'category')

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Seleccione una categoría'


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name',)

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('name',)