from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.db.models import Q
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .forms import RecipeForm, QualityForm, IngredientForm, UnitForm
from .models import Recipe, Quality

# Create your views here.


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    paginate_by = 10
    context_object_name = 'recipes'
    template_name = 'cookbook/cookbook_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recetas'
        return context

    def get_queryset(self):
        queryset = super().get_queryset().all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
        return queryset


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    context_object_name = 'recipe'


@login_required
def create_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            pk = recipe.id
            url = reverse('detail_recipe', args=[pk])
            return redirect(url)
    else:
        recipe_form = RecipeForm()
    return render(request, 'cookbook/cookbooks_form.html', {'form': recipe_form, 'title_page': 'Agregar una receta'})


class RecipeEditView(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['title', 'description', 'instructions', 'image', 'category']
    template_name = 'cookbook/cookbooks_form.html'
    success_url = reverse_lazy('cookbook')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("No tienes permiso para editar este post.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Editar receta'
        context['volver_detalle'] = True
        return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = 'cookbook/cookbook_confirm_delete.html'
    success_url = reverse_lazy('cookbook')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("No tienes permiso para editar este post.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['volver_detalle'] = True
        return context


# DETALLLE DE INGREDIENTES


@login_required
def ingredient_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden()
    all_ingredients = Quality.objects.filter(recipe=recipe)
    form = QualityForm()
    form_ingredient = IngredientForm()
    form_unit = UnitForm()
    if request.method == 'POST' and 'form_type' in request.POST:
        form_type = request.POST['form_type']
        if form_type == 'form':
            form = QualityForm(request.POST)
            if form.is_valid():
                quality = form.save(commit=False)
                quality.recipe = recipe
                quality.save()
                messages.add_message(
                    request, messages.SUCCESS, f'Se agrego el nuevo ingrediente a {recipe.title}', extra_tags='success'
                )
                url = reverse('ingredient_detail', args=[pk])
                return redirect(url)
            else:
                messages.add_message(request, messages.ERROR, 'Corrige los datos del formulario', extra_tags='danger')
        elif form_type == 'form_ingredient':
            form_ingredient = IngredientForm(request.POST)
            if form_ingredient.is_valid():
                form_ingredient.save()
                messages.add_message(request, messages.SUCCESS, 'Se agrego el nuevo ingrediente', extra_tags='success')
                url = reverse('ingredient_detail', args=[pk])
                return redirect(url)
            else:
                messages.add_message(request, messages.ERROR, 'Corrige los datos del formulario', extra_tags='danger')
        elif form_type == 'form_unit':
            form_unit = UnitForm(request.POST)
            if form_unit.is_valid():
                form_unit.save()
                messages.add_message(
                    request, messages.SUCCESS, 'Se agrego la nueva unidad de medida', extra_tags='success'
                )
                url = reverse('ingredient_detail', args=[pk])
                return redirect(url)
            else:
                messages.add_message(request, messages.ERROR, 'Corrige los datos del formulario', extra_tags='danger')
    contexto = {
        'all_ingredients': all_ingredients,
        'form': form,
        'form_ingredient': form_ingredient,
        'form_unit': form_unit,
        'recipe': recipe,
    }
    return render(request, 'cookbook/ingredients_detail.html', contexto)


class IngredientDetailEditView(LoginRequiredMixin, UpdateView):
    model = Quality
    fields = ['ingredient', 'unit', 'quantity', 'notes']
    template_name = 'cookbook/ingredients_detail_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.recipe.author != self.request.user:
            raise Http404("No tienes permiso para editar este post.")
        return obj

    def get_success_url(self):
        return reverse_lazy('ingredient_detail', kwargs={'pk': self.object.recipe.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Editar Ingredientes'
        context['volver_detalle'] = True
        print(context)
        return context


class IngredientDetailDeleteView(LoginRequiredMixin, DeleteView):
    model = Quality
    template_name = 'cookbook/cookbook_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.recipe.author != self.request.user:
            raise Http404("No tienes permiso para editar este post.")
        return obj

    def get_success_url(self):
        return reverse_lazy('ingredient_detail', kwargs={'pk': self.object.recipe.pk})
