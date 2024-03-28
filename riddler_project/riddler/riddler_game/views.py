from django.shortcuts import render
from django.views.generic import View
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import SetPasswordForm
from django.views import generic
from .models import Question, QuizResult
from django.urls import reverse_lazy
import random
import uuid
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.sessions.models import Session
from django.utils import timezone as tz
from django.contrib.auth.forms import PasswordResetForm
from datetime import datetime, timedelta, timezone



class HomeView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        expected_token = generate_token()
        request.session['expected_token'] = expected_token
        print(expected_token)
        context = {'expected_token': expected_token}
        return render(request, self.template_name, context)
       

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"
    

def generate_token():
    return str(uuid.uuid4())


class KvizView(View):
    def get(self, request):
        session_token = request.session.get('expected_token')
        query_token = request.GET.get('token')
        if session_token != query_token:
            return render(request, "invalid_token.html")
        
        start_time = datetime.now()
        my_timezone = timezone(timedelta(hours=1))
        start_time = start_time.astimezone(my_timezone)

        # start_timezone = timezone.now()
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
        a = request.session['quiz_start_time'] = start_time_str
        print(a)

        all_questions = list(Question.objects.all())
        questions = random.sample(all_questions, k=min(len(all_questions), 2))  # Adjust the number of questions as needed
        context = {'questions': questions}

        expected_token = generate_token()
        request.session['expected_token'] = expected_token

        return render(request, 'kviz.html', context)
    
    def post(self, request):
        start_time_str = request.session.get('quiz_start_time')
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.now()
        duration = end_time - start_time
        time_taken_seconds = duration.total_seconds()
        del request.session['quiz_start_time']
        
        question_ids = [int(key.split('_')[2]) for key in request.POST.keys() if key.startswith('user_answer_')]
        questions = Question.objects.filter(pk__in=question_ids)
        
        score = 0
        wrong = 0
        correct = 0
        total = 0
        coords = "Uff, to bylo něco že? Tady je tvá odměna 49° 10.007 16° 35.214"
        
        for q in questions:
            total += 1
            user_answer = request.POST.get('user_answer_' + str(q.id), "").lower()
            correct_answer = q.answer.lower()
            print(f"user {user_answer}, q.question {q.id}, correct {correct_answer}")

            if correct_answer == user_answer:
                score += 10
                correct += 1
            else:
                wrong += 1
        
        

        percent = score / (total * 10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
            }
        
        if (time_taken_seconds - 10) < int(context["time"]) < (time_taken_seconds + 10):
            if percent > 83:
                context["coords"] = coords
            else:
                context["coords"] = ""
        else:
            context["error_time_message"] = "Hodnota času serveru neodpovídá povolené odchylce časovače!"

        date_taken = tz.now() + timedelta(hours=1)
        quiz_result = QuizResult(
            user=request.user, 
            percent=percent, 
            score=score, 
            time=context["time"], 
            django_time=time_taken_seconds, 
            date_taken=date_taken)
        quiz_result.save()

        session_key = request.GET.get('token')
        if session_key:
            try:
                session = Session.objects.get(session_key=session_key)
                session.delete()
                print("deleted")
            except Session.DoesNotExist:
                pass  # Session not found, no need to delete

        expected_token = generate_token()
        request.session['expected_token'] = expected_token
        print(expected_token)
        context['expected_token']=expected_token
        return render(request, 'result.html', context)


class InvalidateTokenView(View):
    def post(self, request):
        # Set expected_token session key to None
        request.session['expected_token'] = None
        
        # Return JSON response indicating successful token invalidation
        return JsonResponse({'status': 'success'})