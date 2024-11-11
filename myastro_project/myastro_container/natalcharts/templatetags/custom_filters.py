import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def format_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'## (.*?)\n', r'<h2>\1</h2>\n', text)
    text = re.sub(r'\* (.*?)\n', r'<li>\1</li>\n', text)
    text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', text)
    return mark_safe(text)

@register.filter
def full_sign(sign):
    sign_map = {
        'Ari': 'Aries',
        'Tau': 'Taurus',
        'Gem': 'Gemini',
        'Can': 'Cancer',
        'Leo': 'Leo',
        'Vir': 'Virgo',
        'Lib': 'Libra',
        'Sco': 'Scorpio',
        'Sag': 'Sagittarius',
        'Cap': 'Capricorn',
        'Aqu': 'Aquarius',
        'Pis': 'Pisces'
    }
    return sign_map.get(sign, sign)

@register.filter
def dict_get_lower(d, key):
    return d.get(key.lower(), 'No comment available')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)