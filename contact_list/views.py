from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Contact, Group, Tag
from .forms import GroupForm, TagForm

# Create your views here.
class ContactListView(LoginRequiredMixin, ListView):
    model=Contact
    template_name = 'contact_list/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(phone__icontains=query) |
                Q(email__icontains=query) |
                Q(group__name__icontains=query)
            )
            groups = Group.objects.filter(name__icontains=query)
        return queryset


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'birthdate', 'group',]
    template_name = 'contact_list/contact_form.html'

    success_url = reverse_lazy('contact_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page']='Crear contacto'
        return context


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contact_list/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ContactEditView(LoginRequiredMixin, UpdateView):
    model = Contact
    fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'birthdate', 'group']
    template_name = 'contact_list/contact_form.html'
    success_url = reverse_lazy('contact_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page']='Editar contacto'
        return context


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('contact_list')


class GroupListView(LoginRequiredMixin, ListView):
    model=Group
    template_name = 'contact_list/contact_group_list.html'
    context_object_name = 'list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Grupos'
        context['form'] = GroupForm
        return context


class TagListView(LoginRequiredMixin, ListView):
    model=Tag
    template_name = 'contact_list/contact_tag_list.html'
    context_object_name = 'list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Etiquetas'
        context['form'] = TagForm
        return context


class GroupCreateView(CreateView):
    model=Group
    form_class = GroupForm
    success_url = reverse_lazy('group_list')

class TagCreateView(CreateView):
    model=Tag
    form_class = TagForm
    success_url = reverse_lazy('tag_list')


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'contact_list/contact_confirm_delete.html'
    success_url = reverse_lazy('group_list')


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'contact_list/contact_confirm_delete.html'
    success_url = reverse_lazy('tag_list')