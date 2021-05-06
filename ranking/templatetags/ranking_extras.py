
from django import template

register = template.Library()

@register.filter
def get_team_short(member):
    return member.get_team_short()

@register.filter
def return_badges(member):
    html = ""
    badges_list = member.member_badges
    for i in badges_list.all():
        html += '<div class="Badge">' + i.svg + f'<span class=tooltiptext>{i.tooltip}</span>' + '</div>'
    return html
