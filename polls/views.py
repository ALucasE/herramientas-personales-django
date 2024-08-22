from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages


from .forms import PollForm, ChoiceForm
from .models import Poll, Choice, Vote


class IndexView(LoginRequiredMixin, generic.ListView):
    model = Poll
    template_name = 'polls/polls.html'
    ordering = ['pub_date']
    context_object_name = 'polls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PollForm
        context['accion'] = 'Crear una encuesta'
        return context


@login_required
def poll_crerate(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.creator = request.user
            if Poll.objects.filter(title=poll.title, creator=poll.creator).exists():
                form.add_error('title', 'Ya tienes una encuesta con este título.')
            else:
                poll.save()
                # url_choice_create = reverse('choice_create', args=[poll.id])
                messages.add_message(
                    request, messages.SUCCESS, 'Se creo la nueva encuesta con exito!', extra_tags='success'
                )
                return redirect('polls')
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Error al crear la tarea. Por favor, revisa el formulario.',
                extra_tags='danger',
            )
    else:
        form = PollForm()

    contexto = {'form': form, 'accion': 'Crear una encuesta'}
    return render(request, 'polls/polls_form.html', contexto)


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Poll
    template_name = 'polls/poll_detail.html'
    context_object_name = 'poll'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.get_object()
        has_voted = poll.choice_set.filter(voters=self.request.user).exists()
        context['has_voted'] = has_voted
        context['form'] = ChoiceForm
        context['accion'] = 'Agregar una opción'
        return context


@login_required
def choice_create(request, pk):
    if request.method == 'POST':
        poll = Poll.objects.get(pk=pk)
        form = ChoiceForm(request.POST)
        choice = form.save(commit=False)
        choice.question_id = poll.id
        if form.is_valid():
            form.save()
            url_poll_detail = reverse('poll_detail', args=[pk])
            messages.add_message(
                request, messages.SUCCESS, 'Se creo la nueva encuesta con exito!', extra_tags='success'
            )
            return redirect(url_poll_detail)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Error al crear la tarea. Por favor, revisa el formulario.',
                extra_tags='danger',
            )
    else:
        form = ChoiceForm()
    contexto = {
        'form': form,
        'accion': 'Crear una opcion',
    }
    return render(request, 'polls/polls_form.html', contexto)



class VoteView(LoginRequiredMixin, View):
    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, pk=poll_id)
        choice_id = request.POST.get('choice')
        url_poll_detail = reverse('poll_detail', args=[poll_id])
        if not choice_id:
            messages.add_message(request, messages.ERROR, 'Debes seleccionar una opción antes de votar.', extra_tags='danger')
            return redirect(url_poll_detail)
        choice = get_object_or_404(Choice, pk=choice_id, question=poll)
        if Vote.objects.filter(user=request.user, choice__question=poll).exists():
            messages.add_message(request, messages.ERROR, 'Usted ya voto!', extra_tags='danger')
        else:
            choice.add_vote(request.user)
            messages.add_message(request, messages.SUCCESS, 'Su voto se guardo con exito!', extra_tags='success')
        return redirect(url_poll_detail)
    

class PollDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Poll
    success_url = reverse_lazy('polls')