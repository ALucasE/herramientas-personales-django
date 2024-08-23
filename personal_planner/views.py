from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Event
from .forms import EventForm


# Create your views here.
class EventJSONList(LoginRequiredMixin, View):
    def get(self, request):
        events = Event.objects.filter(user=self.request.user)
        event_list = [{'title': event.title, 'start': event.start_date, 'end': event.end_date} for event in events]
        return JsonResponse(event_list, safe=False)
    
    
def full_calendar(request):
    return render(request, 'personal_planner/personal_planner_full_calendar.html')


class EventList(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'personal_planner/personal_planner_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(title__icontains=query))
        return queryset


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'personal_planner/personal_planner_form.html'
    form_class = EventForm
    success_url = reverse_lazy('personal_planner')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, '¡El evento creado con éxito!', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, '¡Revisa los errores en el formulario!', extra_tags='warning')
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Crear evento'
        return context


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'personal_planner/personal_planner_detail.html'


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'start_date', 'end_date', 'location', 'is_public']
    template_name = 'personal_planner/personal_planner_form.html'

    def get_success_url(self):
        return reverse_lazy('personal_planner_detail', kwargs={'slug': self.object.slug})
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, '¡El evento guardado con éxito!', extra_tags='success')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, '¡Revisa los errores en el formulario!', extra_tags='warning')
        return super().form_invalid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("No tienes permiso para editar este post.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = 'Editar evento'
        context['return_edit'] = True
        return context


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'personal_planner/personal_planner_confirm_delete.html'
    success_url = reverse_lazy('personal_planner')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, '¡El evento fue eliminado!', extra_tags='success')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("No tienes permiso para editar este post.")
        return obj
