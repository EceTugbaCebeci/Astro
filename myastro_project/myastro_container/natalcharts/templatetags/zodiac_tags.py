from django import template
from natalcharts.utils import calculate_natal_chart  

register = template.Library()

ZODIAC_SIGNS = {
    'Ari': '&#9800;',
    'Tau': '&#9801;',
    'Gem': '&#9802;',
    'Can': '&#9803;',
    'Leo': '&#9804;',
    'Vir': '&#9805;',
    'Lib': '&#9806;',
    'Sco': '&#9807;',
    'Sag': '&#9808;',
    'Cap': '&#9809;',
    'Aqu': '&#9810;',
    'Pis': '&#9811;',
}

def get_zodiac_sign(user):
    if not user.birth_date or not user.birth_hour or not user.birth_place:
        return None

    chart = calculate_natal_chart(user.username, user.birth_date, user.birth_hour, user.birth_place)
    sun_sign = chart.get('sun')
    print(f"User: {user.username}, Sun Sign: {sun_sign}")  

    return ZODIAC_SIGNS.get(sun_sign)

@register.filter
def zodiac_default_image(user):
    zodiac_sign = get_zodiac_sign(user)
    return zodiac_sign if zodiac_sign else '&#9800;' 
