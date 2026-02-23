from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def chat_date_label(value):
    if not value:
        return ""

    today = timezone.localdate()
    yesterday = today - timezone.timedelta(days=1)

    msg_date = value

    if msg_date == today:
        return "Today"
    elif msg_date == yesterday:
        return "Yesterday"
    return value.strftime("%d %b %Y")