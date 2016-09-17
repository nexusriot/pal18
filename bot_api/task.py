# -*- coding: utf-8 -*

import calendar
import datetime

# todo: just a stub now
when_map = {
    'night': [u'вечером', 'at night'],
    'weekend': [u'выходных', 'weekend'],
    'today': [u'сегодня', 'today'],
    'lunch': [u'обед', 'lunch'],
    'tomorrow': [u'завтра', 'tomorrow']
}


# todo: also stub function
def get_criteria_list(text):
    criteria = []
    actual_criteria = text.split()
    for static_crit, crit_list in when_map.iteritems():
        for crit in crit_list:
            if crit in actual_criteria:
                criteria.append(static_crit)
    return list(set(criteria))


# todo: another stub
def set_date(criteria_list):

    now = datetime.datetime.utcnow()
    date_set = datetime.datetime.utcnow()

    if 'tomorrow' in criteria_list:
        date_set = date_set.replace(day=date_set.day + 1)

    if 'lunch' in criteria_list:
        date_set = date_set.replace(hour=10)
        if date_set < now:
            date_set = now

    if 'night' in criteria_list:
        date_set = date_set.replace(hour=17)
        if date_set < now:
            date_set = now

    return date_set
