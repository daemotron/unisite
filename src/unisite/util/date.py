from django.utils.translation import ugettext_lazy as _

def month_name(month):
    if month == 1:
        return _('January')
    elif month == 2:
        return _('February')
    elif month == 3:
        return _('March')
    elif month == 4:
        return _('April')
    elif month == 5:
        return _('May')
    elif month == 6:
        return _('June')
    elif month == 7:
        return _('July')
    elif month == 8:
        return _('August')
    elif month == 9:
        return _('September')
    elif month == 10:
        return _('October')
    elif month == 11:
        return _('November')
    elif month == 12:
        return _('December')
    else:
        return ''


def day_name(day):
    if day == 1:
        return _('Monday')
    elif day == 2:
        return _('Tuesday')
    elif day == 3:
        return _('Wednesday')
    elif day == 4:
        return _('Thursday')
    elif day == 5:
        return _('Friday')
    elif day == 6:
        return _('Saturday')
    elif day == 7:
        return _('Sunday')
    else:
        return ''