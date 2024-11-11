from kerykeion import AstrologicalSubject
import google.generativeai as genai
import requests
from .models import PlanetaryPosition, ProbabilitiesComments, AstroFunContent
from datetime import datetime, timedelta
from myastro.settings import GENAI_API_KEY, ASK_ASTRO_GENAI_API_KEY

genai.configure(api_key=GENAI_API_KEY)

PLANETS = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'ascendant', 'descendant']
SIGNS = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']


def get_current_week_dates():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.strftime("%B %d, %Y"), end_of_week.strftime("%B %d, %Y")

def update_daily_comments():
    model = genai.GenerativeModel('gemini-1.5-flash')
    today_date = datetime.now().strftime("%B %d, %Y")

    for sun_sign in SIGNS:
        for ascendant_sign in SIGNS:
            daily_prompt = f"Generate a detailed daily horoscope for a person with Sun sign {sun_sign} and Ascendant sign {ascendant_sign} for {today_date}. Provide specific events, opportunities, and advice."

            try:
                daily_comment = model.generate_content(daily_prompt).text.strip()
            except ValueError as e:
                print(f"Error generating content for Sun: {sun_sign} and Ascendant: {ascendant_sign} - {str(e)}")
                continue

            ProbabilitiesComments.objects.update_or_create(
                sun_sign=sun_sign,
                ascendant_sign=ascendant_sign,
                defaults={'daily_comment': daily_comment}
            )
            print(f"Successfully updated daily comments for Sun: {sun_sign} and Ascendant: {ascendant_sign}")

def update_weekly_comments():
    model = genai.GenerativeModel('gemini-1.5-flash')
    week_start_date, week_end_date = get_current_week_dates()

    for sun_sign in SIGNS:
        for ascendant_sign in SIGNS:
            weekly_prompt = f"Generate a detailed weekly horoscope for a person with Sun sign {sun_sign} and Ascendant sign {ascendant_sign} for the week of {week_start_date} to {week_end_date}. Provide specific predictions and advice for each day of the week."

            try:
                weekly_comment = model.generate_content(weekly_prompt).text.strip()
            except ValueError as e:
                print(f"Error generating content for Sun: {sun_sign} and Ascendant: {ascendant_sign} - {str(e)}")
                continue

            ProbabilitiesComments.objects.update_or_create(
                sun_sign=sun_sign,
                ascendant_sign=ascendant_sign,
                defaults={'weekly_comment': weekly_comment}
            )
            print(f"Successfully updated weekly comments for Sun: {sun_sign} and Ascendant: {ascendant_sign}")

def update_monthly_comments():
    model = genai.GenerativeModel('gemini-1.5-flash')
    current_month = datetime.now().strftime("%B %Y")

    for sun_sign in SIGNS:
        for ascendant_sign in SIGNS:
            monthly_prompt = f"Generate a detailed monthly horoscope for a person with Sun sign {sun_sign} and Ascendant sign {ascendant_sign} for the month of {current_month}. Provide specific predictions and advice for each week of the month."

            try:
                monthly_comment = model.generate_content(monthly_prompt).text.strip()
            except ValueError as e:
                print(f"Error generating content for Sun: {sun_sign} and Ascendant: {ascendant_sign} - {str(e)}")
                continue

            ProbabilitiesComments.objects.update_or_create(
                sun_sign=sun_sign,
                ascendant_sign=ascendant_sign,
                defaults={'monthly_comment': monthly_comment}
            )
            print(f"Successfully updated monthly comments for Sun: {sun_sign} and Ascendant: {ascendant_sign}")

def update_yearly_comments():
    model = genai.GenerativeModel('gemini-1.5-flash')
    current_year = datetime.now().strftime("%Y")

    for sun_sign in SIGNS:
        for ascendant_sign in SIGNS:
            yearly_prompt = f"Generate a detailed yearly horoscope for a person with Sun sign {sun_sign} and Ascendant sign {ascendant_sign} for the year {current_year}. Provide specific predictions and advice for each month."

            try:
                yearly_comment = model.generate_content(yearly_prompt).text.strip()
            except ValueError as e:
                print(f"Error generating content for Sun: {sun_sign} and Ascendant: {ascendant_sign} - {str(e)}")
                continue

            ProbabilitiesComments.objects.update_or_create(
                sun_sign=sun_sign,
                ascendant_sign=ascendant_sign,
                defaults={'yearly_comment': yearly_comment}
            )
            print(f"Successfully updated yearly comments for Sun: {sun_sign} and Ascendant: {ascendant_sign}")

def populate_astrofun_content():
    model = genai.GenerativeModel('gemini-1.5-flash')

    for sun_sign in SIGNS:
        for ascendant_sign in SIGNS:
            if not AstroFunContent.objects.filter(sun_sign=sun_sign, ascendant_sign=ascendant_sign).exists():
                movie_prompt = f"Recommend a movie for someone with Sun sign {sun_sign} and Ascendant sign {ascendant_sign}."
                song_prompt = f"Recommend a song for someone with Sun sign {sun_sign} and Ascendant sign {ascendant_sign}."
                city_prompt = f"Recommend a city for someone with Sun sign {sun_sign} and Ascendant sign {ascendant_sign}."

                try:
                    movie_recommendation = model.generate_content(movie_prompt).text.strip()
                    song_recommendation = model.generate_content(song_prompt).text.strip()
                    city_recommendation = model.generate_content(city_prompt).text.strip()
                except ValueError as e:
                    print(f"Error generating content for Sun: {sun_sign} and Ascendant: {ascendant_sign} - {str(e)}")
                    continue

                AstroFunContent.objects.create(
                    sun_sign=sun_sign,
                    ascendant_sign=ascendant_sign,
                    movie_recommendation=movie_recommendation,
                    song_recommendation=song_recommendation,
                    city_recommendation=city_recommendation
                )
                print(f"Successfully added AstroFun content for Sun: {sun_sign} and Ascendant: {ascendant_sign}")

def get_ai_response(natal_chart_data, question):
    genai.configure(api_key=ASK_ASTRO_GENAI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Based on the following natal chart data: {natal_chart_data}, answer the following question: {question}"

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        return answer
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_ai_comment(natal_chart_data):
    try:
        planet = list(natal_chart_data.keys())[0]
        sign = natal_chart_data[planet]

        prompt = (
            f"This is a horoscope web site and it will give you the horoscope values of the user in this application and interpret it for her/him. "
            f"{planet.capitalize()} in {sign}. "
        )

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        return response.text.strip()

    except Exception as e:
        return f"Error generating comment: {str(e)}"

def populate_planetary_positions():
    for planet in PLANETS:
        for sign in SIGNS:
            if not PlanetaryPosition.objects.filter(planet=planet, sign=sign).exists():
                comment = get_ai_comment({planet: sign})
                PlanetaryPosition.objects.create(planet=planet, sign=sign, ai_comment=comment)
                print(f'Successfully added {planet} in {sign}')
            else:
                print(f'{planet} in {sign} already exists.')

def get_coordinates(birth_place):
    url = 'https://turkiyeapi.dev/api/v1/provinces'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        for city in data['data']:
            if city['name'].lower() == birth_place.lower():
                return city['coordinates']['latitude'], city['coordinates']['longitude']
        raise ValueError("Coordinates not found for the place.")
    except requests.RequestException as e:
        raise e

def calculate_natal_chart(name, birth_date, birth_hour, birth_place):
    try:
        birth_year = birth_date.year
        birth_month = birth_date.month
        birth_day = birth_date.day
        birth_minute = 0

        subject = AstrologicalSubject(name, birth_year, birth_month, birth_day, birth_hour, birth_minute, birth_place)

        natal_chart_data = {
            "sun": subject.sun['sign'],
            "moon": subject.moon['sign'],
            "mercury": subject.mercury['sign'],
            "venus": subject.venus['sign'],
            "mars": subject.mars['sign'],
            "jupiter": subject.jupiter['sign'],
            "saturn": subject.saturn['sign'],
            "ascendant": subject.first_house['sign'],
            "descendant": subject.seventh_house['sign'],
        }

        return natal_chart_data

    except Exception as e:
        return {"error": str(e)}
    
ELEMENTS = {
    'Ari': 'Fire', 'Leo': 'Fire', 'Sag': 'Fire',
    'Tau': 'Earth', 'Vir': 'Earth', 'Cap': 'Earth',
    'Gem': 'Air', 'Lib': 'Air', 'Aqu': 'Air',
    'Can': 'Water', 'Sco': 'Water', 'Pis': 'Water'
}

def element_compatibility(sign1, sign2):
    compatible_elements = {
        'Fire': ['Fire', 'Air'],
        'Air': ['Air', 'Fire'],
        'Earth': ['Earth', 'Water'],
        'Water': ['Water', 'Earth']
    }

    element1 = ELEMENTS[sign1]
    element2 = ELEMENTS[sign2]

    if element1 == element2:
        return 5  
    elif element2 in compatible_elements[element1]:
        return 3  
    else:
        return 0  

def calculate_compatibility(user_data, relative_data):
    if 'error' in user_data or 'error' in relative_data:
        return "One of the natal charts contains an error and cannot be used for compatibility analysis."

    compatibility_score = 0

    for key in ['sun', 'moon','mercury', 'venus', 'mars']:
        compatibility_score += element_compatibility(user_data[key], relative_data[key])

    role_compatibility = {
        'Parent': 2,
        'Sibling': 2,
        'Spouse': 3,
        'Friend': 2,
    }

    role = user_data.get('role', 'Other')
    
    if role in role_compatibility:
        compatibility_score += role_compatibility[role]


    if compatibility_score >= 15:
        return ("You and your relative have high compatibility! This indicates that your elemental alignments and planetary positions "
                "are strongly in sync, suggesting a natural harmony between your personalities and life paths. The strong compatibility "
                "score reflects a profound connection that can foster mutual understanding, support, and growth. Whether it's through shared "
                "goals, similar emotional responses, or complementary energies, you both have the potential to build a deeply fulfilling "
                "relationship.")
    elif compatibility_score >= 8:
        return ("You and your relative have moderate compatibility. There are notable areas of alignment in your elemental and planetary "
                "positions that suggest you share some common ground. While there may be differences that could lead to occasional "
                "misunderstandings or conflicts, the overall compatibility score indicates that these can be navigated with mutual effort "
                "and understanding. Building on your shared strengths and respecting each other's differences can lead to a balanced and "
                "rewarding relationship.")
    else:
        return ("You and your relative have low compatibility. This suggests that your elemental alignments and planetary positions may "
                "differ significantly, potentially leading to challenges in understanding and relating to each other. While this low "
                "compatibility score indicates that there could be fundamental differences in your personalities and approaches to life, "
                "it does not mean a relationship is impossible. With conscious effort and open communication, it is possible to find ways "
                "to bridge these gaps and appreciate each other's unique qualities. However, it will likely require more effort and "
                "understanding to maintain a harmonious relationship.")
