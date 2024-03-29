from django.shortcuts import render, redirect
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
        context = {"context":"context"}

        # testing
        two_min_ago = tz.now() + timedelta(hours=1) - timedelta(minutes=4)
        print(f"now {tz.now()}, 2 mn ago {two_min_ago}")

        # time zone +1 hour
        twenty_four_hours_ago = tz.now() + timedelta(hours=1) - timedelta(hours=24)

        # change from two_min_ago to desired time
        recent_attempts = QuizResult.objects.filter(user=request.user.id, date_taken__gte=two_min_ago)
        last_quiz_taken = QuizResult.objects.filter(user=request.user.id, date_taken__gte=two_min_ago)
        print(last_quiz_taken)
        if last_quiz_taken:
            last_quiz_takenn = last_quiz_taken.order_by("-date_taken")
            js_time = last_quiz_takenn[0].time
            django_time = last_quiz_takenn[0].django_time
            subtraction = abs(django_time - js_time) 
            if subtraction > 10:
                context["timer_tamper_message"] = "Zablokovaný přístup na 24 hod. Zásah do časovače."

        if len(recent_attempts) < 2:
            expected_token = generate_token()
            request.session['expected_token'] = expected_token
            context['expected_token'] = expected_token
            return render(request, self.template_name, context)
        else:
            context["recent_attempts_message"] = "Počet pokusů za 24 hod přesáhl limit."
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

        quiz_result = QuizResult.objects.create(
            user=request.user,
            percent=0,
            score=0,
            time=0,
            django_time=0,
            date_taken=tz.now() + timedelta(hours=1)
        )
        request.session['quiz_result_id'] = quiz_result.id

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
        hint_button_clicked = request.POST.get("hintButtonClickCount")
        print(hint_button_clicked)
        time_taken_seconds = time_taken_seconds + int(hint_button_clicked)*5
        if (time_taken_seconds - 10) < int(context["time"]) < (time_taken_seconds + 10):
            if percent > 83:
                context["coords"] = coords
            else:
                # time zone +1 hour
                twenty_four_hours_ago = tz.now() + timedelta(hours=1) - timedelta(hours=24)
                recent_attempts = QuizResult.objects.filter(user=request.user.id, date_taken__gte=twenty_four_hours_ago)
                if len(recent_attempts) < 2:
                    expected_token = generate_token()
                    request.session['expected_token'] = expected_token
                    context['expected_token'] = expected_token
                else:
                    context["recent_attempts_message"] = "Počet pokusů za 24 hod přesáhl limit."
                    context["coords"] = ""
        else:
            time_now = datetime.now()
            time_now_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
            request.session['timer_tampering_attempt'] = time_now_str
            context["error_time_message"] = "Hodnota času serveru neodpovídá povolené odchylce časovače!"

        date_taken = tz.now() + timedelta(hours=1)

        quiz_result_id = request.session.get('quiz_result_id')
        quiz_result = QuizResult.objects.get(id=quiz_result_id)

        # Update the quiz result object with the actual quiz results
        quiz_result.percent = percent
        quiz_result.score = score  # Your logic to calculate score
        quiz_result.time = request.POST.get('timer')  # Assuming timer is submitted with the form
        quiz_result.django_time = time_taken_seconds  # Your logic to calculate Django time
        quiz_result.date_taken = tz.now() + timedelta(hours=1)  # Update the date taken

        # Save the updated quiz result object
        quiz_result.save()
        # quiz_result = QuizResult(
        #     user=request.user, 
        #     percent=percent, 
        #     score=score, 
        #     time=context["time"], 
        #     django_time=time_taken_seconds, 
        #     date_taken=date_taken)
        # quiz_result.save()

        session_key = request.GET.get('token')
        if session_key:
            try:
                session = Session.objects.get(session_key=session_key)
                session.delete()
                print("deleted")
            except Session.DoesNotExist:
                pass  # Session not found, no need to delete

        # expected_token = generate_token()
        # request.session['expected_token'] = expected_token
        # print(expected_token)
        # context['expected_token']=expected_token
        return render(request, 'result.html', context)


class InvalidateTokenView(View):
    def post(self, request):
        # Set expected_token session key to None
        request.session['expected_token'] = None
        
        # Return JSON response indicating successful token invalidation
        return JsonResponse({'status': 'success'})