from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def to_badges(value):
    skills = [skill.strip() for skill in value.split(',')]
    badges = ['<span class="badge badge-pill badge-primary">{}</span>'.format(skill) for skill in skills]
    return mark_safe(' '.join(badges))
