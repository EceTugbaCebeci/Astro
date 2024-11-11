import datetime
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .forms import RelativeForm, AskAstroQuestionForm, UpdateProfileForm, UpdateProfileForm, UpdatePasswordForm
from .models import Relative, PlanetaryPosition, PersonalizedProbability, ProbabilitiesComments, AskAstroQuestion, AstroFunContent
from .utils import calculate_natal_chart, get_coordinates, calculate_compatibility, get_ai_response
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin


SIGN_MAP = {
    'Aqu': 'aquarius',
    'Pis': 'pisces',
    'Ari': 'aries',
    'Tau': 'taurus',
    'Gem': 'gemini',
    'Can': 'cancer',
    'Leo': 'leo',
    'Vir': 'virgo',
    'Lib': 'libra',
    'Sco': 'scorpio',
    'Sag': 'sagittarius',
    'Cap': 'capricorn'
}


class HomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        birth_date = user.birth_date
        birth_hour = user.birth_hour
        birth_place = user.birth_place

        if not (user.birth_date and user.birth_hour and user.birth_place):
            messages.error(request, 'Birth information is missing.')
            return render(request, 'home.html', {'error_message': 'Birth information is missing.'})

        try:
            natal_chart_data = calculate_natal_chart(user.username, birth_date, birth_hour, birth_place)
            return render(request, 'home.html', {
                'natal_chart_data': natal_chart_data
            })

        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'home.html', {'error_message': str(e)})
        

class CompatibilityAnalysisView(LoginRequiredMixin, View):
    def get(self, request):
        relatives = request.user.relatives.all()
        form = RelativeForm()
        compatibility_comments = []

        user_data = calculate_natal_chart(request.user.username, request.user.birth_date, request.user.birth_hour, request.user.birth_place)
        for relative in relatives:
            relative_data = calculate_natal_chart(relative.first_name, relative.birth_date, relative.birth_hour, relative.birth_place)
            comment = calculate_compatibility(user_data, relative_data)
            compatibility_comments.append((relative, comment))

        return render(request, 'compatibility_analysis.html', {'relatives': relatives, 'form': form, 'compatibility_comments': compatibility_comments})

    def post(self, request):
        form = RelativeForm(request.POST)
        if form.is_valid():
            relative = form.save(commit=False)
            relative.user = request.user
            relative.save()
        else:
            messages.error(request, 'There was an error adding the relative.')
        return redirect('compatibility_analysis')


class PersonalizedProbabilityView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        try:
            personalized_prob = PersonalizedProbability.objects.get(user=user)
            
            sun_sign = SIGN_MAP.get(personalized_prob.probabilities_comments.sun_sign, personalized_prob.probabilities_comments.sun_sign.lower())
            ascendant_sign = SIGN_MAP.get(personalized_prob.probabilities_comments.ascendant_sign, personalized_prob.probabilities_comments.ascendant_sign.lower())

            probabilities_comments = ProbabilitiesComments.objects.get(sun_sign=sun_sign, ascendant_sign=ascendant_sign)

            # For update
            personalized_prob.daily_comment = probabilities_comments.daily_comment
            personalized_prob.weekly_comment = probabilities_comments.weekly_comment
            personalized_prob.monthly_comment = probabilities_comments.monthly_comment
            personalized_prob.yearly_comment = probabilities_comments.yearly_comment
            personalized_prob.save()

        except PersonalizedProbability.DoesNotExist:
            natal_chart_data = calculate_natal_chart(user.username, user.birth_date, user.birth_hour, user.birth_place)
            
            sun_sign = SIGN_MAP.get(natal_chart_data['sun'], natal_chart_data['sun'].lower())
            ascendant_sign = SIGN_MAP.get(natal_chart_data['ascendant'], natal_chart_data['ascendant'].lower())

            try:
                probabilities_comments = ProbabilitiesComments.objects.get(sun_sign=sun_sign, ascendant_sign=ascendant_sign)
            except ProbabilitiesComments.DoesNotExist:
                return HttpResponse("Comments for the given sun sign and ascendant sign combination do not exist.")
            personalized_prob = PersonalizedProbability.objects.create(
                user=user,
                probabilities_comments=probabilities_comments,
                daily_comment=probabilities_comments.daily_comment,
                weekly_comment=probabilities_comments.weekly_comment,
                monthly_comment=probabilities_comments.monthly_comment,
                yearly_comment=probabilities_comments.yearly_comment
            )
            personalized_prob.save() 

        return render(request, 'personalized_probabilities.html', {'personalized_prob': personalized_prob})


class AstroFunView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        natal_chart_data = calculate_natal_chart(user.username, user.birth_date, user.birth_hour, user.birth_place)
        
        sun_sign = SIGN_MAP.get(natal_chart_data['sun'], natal_chart_data['sun'].lower())
        ascendant_sign = SIGN_MAP.get(natal_chart_data['ascendant'], natal_chart_data['ascendant'].lower())
        
        try:
            astrofun_content = AstroFunContent.objects.get(sun_sign=sun_sign, ascendant_sign=ascendant_sign)
        except AstroFunContent.DoesNotExist:
            return render(request, 'astrofun.html', {'error_message': 'AstroFun content not found for your combination.'})

        return render(request, 'astrofun.html', {'astrofun_content': astrofun_content})
    

class AskAstroView(LoginRequiredMixin, View):
    def get(self, request):
        today = datetime.datetime.now().date()
        questions_today = AskAstroQuestion.objects.filter(user=request.user, created_at__date__lte=today)
        form = AskAstroQuestionForm()
        return render(request, 'ask_astro.html', {'form': form, 'questions': questions_today})

    def post(self, request):
        today = datetime.datetime.now().date()
        questions_today = AskAstroQuestion.objects.filter(user=request.user, created_at__date=today)

        if questions_today.count() >= 3:
            return render(request, 'ask_astro.html', {'form': AskAstroQuestionForm(), 'questions': questions_today, 'error_message': 'Your quota for today is exhausted. See you tomorrow!'})

        form = AskAstroQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()

            natal_chart_data = calculate_natal_chart(request.user.username, request.user.birth_date, request.user.birth_hour, request.user.birth_place)
            answer = get_ai_response(natal_chart_data, question.question)

            if "An error occurred" in answer:
                return render(request, 'ask_astro.html', {'form': form, 'questions': questions_today, 'error_message': answer})

            question.answer = answer
            question.save()
            print(f"Question: {question.question}")
            print(f"Answer: {question.answer}")

            return redirect('ask_astro')
        
        return render(request, 'ask_astro.html', {'form': form, 'questions': questions_today})


class LoadCountriesView(View):
    def get(self, request):
        country_list = [{'name': 'Turkey', 'code': 'TR'}]
        return JsonResponse(country_list, safe=False)
    

class LoadCitiesView(View):
    def get(self, request):
        url = 'https://turkiyeapi.dev/api/v1/provinces'
        search_term = request.GET.get('search', '')

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            if response.status_code == 200:
                data = response.json()
                city_list = [{'name': city['name']} for city in data['data'] if search_term.lower() in city['name'].lower()]
                
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            city_list = [{'name': f'Error: {str(e)}'}]

        return JsonResponse(city_list, safe=False)


class DeleteRelativeView(LoginRequiredMixin, View):
    def get(self, request, relative_id):
        Relative.objects.filter(id=relative_id, user=request.user).delete()
        return redirect('compatibility_analysis')


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile_form = UpdateProfileForm(instance=request.user)
        return render(request, 'update_profile.html', {'profile_form': profile_form})
    
    def post(self, request):
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('update_profile')
        else:
            for error in profile_form.errors.values():
                messages.error(request, error.as_text())
        return render(request, 'update_profile.html', {'profile_form': profile_form})


class SendVerificationCodeView(LoginRequiredMixin, View):
    def post(self, request):
        verification_code = random.randint(100000, 999999)
        request.session['verification_code'] = verification_code
        try:
            send_mail(
                'Your verification code',
                f'Your verification code is {verification_code}',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'A verification code has been sent to your email address.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error sending email: {e}'})


class VerifyCodeView(LoginRequiredMixin, View):
    def post(self, request):
        entered_code = request.POST.get('verification_code')
        verification_code = request.session.get('verification_code')
        try:
            if entered_code and int(entered_code) == verification_code:
                request.session['verification_successful'] = True
                messages.success(request, 'Verification successful. You can now change your password.')
                del request.session['verification_code']
                return redirect('change_password')
            else:
                messages.error(request, 'The verification code is incorrect.')
        except Exception as e:
            messages.error(request, f'Error verifying code: {e}')
        return redirect('update_profile')


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        verification_successful = request.session.get('verification_successful', False)
        if not verification_successful:
            messages.error(request, 'You must verify your email before changing your password.')
            return redirect('update_profile')

        password_form = UpdatePasswordForm()
        return render(request, 'change_password.html', {'password_form': password_form})
    
    def post(self, request):
        password_form = UpdatePasswordForm(request.POST)
        if password_form.is_valid():
            current_password = password_form.cleaned_data.get('current_password')
            new_password = password_form.cleaned_data.get('new_password')
            new_password_again = password_form.cleaned_data.get('new_password_again')

            if new_password or new_password_again:
                if not request.user.check_password(current_password):
                    messages.error(request, 'Current password is incorrect.')
                elif new_password == current_password:
                    messages.error(request, 'The new password cannot be the same as the current password.')
                elif new_password != new_password_again:
                    messages.error(request, 'The new passwords do not match.')
                else:
                    request.user.set_password(new_password)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Your password has been updated successfully.')
                    request.session['verification_successful'] = False
                    return redirect('update_profile')
        else:
            for error in password_form.errors.values():
                messages.error(request, error.as_text())
        return render(request, 'change_password.html', {'password_form': password_form})


class NatalChartView(View):
    @method_decorator(login_required)
    def get(self, request):
        
        user = request.user

        birth_date = user.birth_date
        birth_hour = user.birth_hour
        birth_place = user.birth_place

        if not (user.birth_date and user.birth_hour and user.birth_place):
            messages.error(request, 'Birth information is missing.')
            return render(request, 'natal_chart.html', {'error_message': 'Birth information is missing.'})

        try:
            get_coordinates(birth_place)

            natal_chart_data = calculate_natal_chart(user.username, birth_date, birth_hour, birth_place)
            ai_comments = {}

            for planet, sign in natal_chart_data.items():
                converted_sign = SIGN_MAP.get(sign, sign.lower())

                try:
                    position = PlanetaryPosition.objects.get(planet=planet, sign=converted_sign)
                    ai_comments[planet] = position.ai_comment
                except PlanetaryPosition.DoesNotExist:
                    ai_comments[planet] = 'No comment available.'

            return render(request, 'natal_chart.html', {
                'natal_chart_data': natal_chart_data,
                'ai_comments': ai_comments
            })

        except ValueError as e:
            messages.error(request, str(e))
            return render(request, 'natal_chart.html', {'error_message': str(e)})


