from django.shortcuts import render
from django.views.generic import View
from .forms import SignUpForm, LoginForm
from django.contrib.auth.views import LoginView
from django.views import generic
from .models import Question
from django.urls import reverse_lazy
import random
import uuid
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.sessions.models import Session


class HomeView(View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        expected_token = generate_token()
        request.session['expected_token'] = expected_token
        print(expected_token)
        context = {
                   'expected_token': expected_token
        }
        return render(request, self.template_name, context)
       

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")


def generate_token():
    return str(uuid.uuid4())


class KvizView(View):
    def get(self, request):
        session_token = request.session.get('expected_token')
        query_token = request.GET.get('token')
        if session_token != query_token:
            return render(request, "invalid_token.html")

        all_questions = list(Question.objects.all())
        questions = random.sample(all_questions, k=min(len(all_questions), 1))  # Adjust the number of questions as needed
        context = {'questions': questions
                   }

        return render(request, 'kviz.html', context)
    
    def post(self, request):
        question_ids = [int(key.split('_')[2]) for key in request.POST.keys() if key.startswith('user_answer_')]
        questions = Question.objects.filter(pk__in=question_ids)
        
        score = 0
        wrong = 0
        correct = 0
        total = 0
        
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
    

# def kviz(request):
#     if request.method == 'POST':
#         print(request.POST)
#         questions=Question.objects.all()
#         score=0
#         wrong=0
#         correct=0
#         total=0
#         for q in questions:
#             total+=1
#             print(request.POST.get(q.question))
#             print(q.ans)
#             print()
#             if q.ans ==  request.POST.get(q.question):
#                 score+=10
#                 correct+=1
#             else:
#                 wrong+=1
#         percent = score/(total*10) *100
#         context = {
#             'score':score,
#             'time': request.POST.get('timer'),
#             'correct':correct,
#             'wrong':wrong,
#             'percent':percent,
#             'total':total
#         }
#         return render(request,'result.html',context)
#     else:
#         questions=Question.objects.all()
#         context = {
#             'questions':questions
#         }
#         return render(request,'index.html',context)