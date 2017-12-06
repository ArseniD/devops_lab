from __future__ import division

import sys

from collections import defaultdict, OrderedDict
from datetime import timedelta
from dateutil.parser import parse
from github3 import login
from numpy import array

data_collect = dict()
days_of_week = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wen',
    3: 'Thu',
    4: 'Fri',
    5: 'Sat',
    6: 'Sun',
}


def hub_connector(token, config, user, repo=None, since=None, until=None, url=None):
    git_h = login(token=token, url=url)
    data_collect.update({
        'count': 0,
        'merged': 0,
        'daysOpen': [],
        'daysOpenHistogram': defaultdict(int),
        'comments': [],
        'commentsHistogram': defaultdict(int),
        'dayOfWeekCreated': OrderedDict(),
        'dayOfWeekClosed': OrderedDict(),
        'hourOfDayCreated': OrderedDict(),
        'hourOfDayClosed': OrderedDict(),
        'weekCreated': defaultdict(int),
        'weekClosed': defaultdict(int),
        'userCreating': defaultdict(int),
        'userClosing': defaultdict(int),
        'labels': defaultdict(int),
    })

    ordered_dict(data_collect['dayOfWeekCreated'], days_of_week.values(), 0)
    ordered_dict(data_collect['dayOfWeekClosed'], days_of_week.values(), 0)
    ordered_dict(data_collect['hourOfDayCreated'], range(24), 0)
    ordered_dict(data_collect['hourOfDayClosed'], range(24), 0)

    if isinstance(since, str):
        since = parse(since)
    if isinstance(until, str):
        until = parse(until)

    if repo is None:
        repos = git_h.iter_user_repos(user)
    else:
        repos = [git_h.repository(user, repo)]

    for repo in repos:
        if not repo.has_issues:
            continue

        progress_bar = 'In %s, analyzing pull number:     ' % repo
        print(progress_bar),

        for issue in repo.iter_issues(state='closed', direction='asc', since=since):
            if until and issue.created_at >= until:
                break

            if since and issue.created_at <= since:
                continue

            if not issue.pull_request:
                continue
            pull_r = repo.pull_request(issue.number)

            print('\b\b\b\b\b%4d' % pull_r.number),
            sys.stdout.flush()

            data_collect['count'] += 1
            if config['basicStats']:
                if pull_r.is_merged():
                    data_collect['merged'] += 1
            if config['daysOpen']:
                days_o = (pull_r.closed_at - pull_r.created_at).days
                data_collect['daysOpen'].append(days_o)
                data_collect['daysOpenHistogram'][days_o] += 1
            if config['comments']:
                comments = len(list(pull_r.iter_comments()))
                data_collect['comments'].append(comments)
                data_collect['commentsHistogram'][comments] += 1
            if config['dayOfWeekCreated']:
                day_w_open = days_of_week[pull_r.created_at.weekday()]
                data_collect['dayOfWeekCreated'][day_w_open] += 1
            if config['dayOfWeekClosed']:
                day_w_close = days_of_week[pull_r.closed_at.weekday()]
                data_collect['dayOfWeekClosed'][day_w_close] += 1
            if config['hourOfDayCreated']:
                data_collect['hourOfDayCreated'][pull_r.created_at.hour] += 1
            if config['hourOfDayClosed']:
                data_collect['hourOfDayClosed'][pull_r.closed_at.hour] += 1
            if config['weekCreated']:
                # Store the first day of the week.
                weekCreated = (pull_r.created_at -
                               timedelta(days=pull_r.created_at.weekday()))
                weekCreated = weekCreated.date()  # Discard time information.
                data_collect['weekCreated'][weekCreated] += 1
            if config['weekClosed']:
                weekClosed = (pull_r.closed_at -
                              timedelta(days=pull_r.closed_at.weekday()))
                weekClosed = weekClosed.date()  # Discard time information.
                data_collect['weekClosed'][weekClosed] += 1
            if config['userCreating']:
                data_collect['userCreating'][pull_r.user.login] += 1
            if config['userClosing']:

                if pull_r.is_merged():
                    pull_r.refresh()
                    data_collect['userClosing'][pull_r.merged_by.login] += 1
            if config['labels']:
                for label in issue.labels:
                    data_collect['labels'][label.name] += 1
                if not issue.labels:
                    data_collect['labels']['<no label>'] += 1

        print('\b' * (len(progress_bar) + 1)),  # +1 for the newline
    print("\n")

    if config['basicStats']:
        percent_merged = round((data_collect['merged']) / (data_collect['count']) * 100, 2)
        print('{0}% ({1} of {2}) closed pulls merged.'.format(
               percent_merged, data_collect['merged'], data_collect['count']))

    if config['daysOpen']:
        print_report('daysOpen')
    if config['comments']:
        print_report('comments')
    if config['dayOfWeekCreated']:
        print_output(
            data_collect['dayOfWeekCreated'].items(), 'Day of Week Created')
    if config['dayOfWeekClosed']:
        print_output(
            data_collect['dayOfWeekClosed'].items(), 'Day of Week Closed')
    if config['hourOfDayCreated']:
        print_output(
            data_collect['hourOfDayCreated'].items(), 'Hour of Day Created')
    if config['hourOfDayClosed']:
        print_output(
            data_collect['hourOfDayClosed'].items(), 'Hour of Day Closed')
    if config['weekCreated']:
        print_date_report('weekCreated', 'Week Created')
    if config['weekClosed']:
        print_date_report('weekClosed', 'Week Closed')
    if config['userCreating']:
        print_output(data_collect['userCreating'].items(),
                     'User Creating Pull Request')
    if config['userClosing']:
        print_output(data_collect['userClosing'].items(),
                     'User Merging Pull Request')
    if config['labels']:
        print_output(data_collect['labels'].items(), 'Labels Attached')


def ordered_dict(dictionary, keys, value=None):
    '''Initialize a dictionary with a set of ordered keys.

    :param dictionary dictionary: The dictionary to initialize.
    :param iterable keys: The keys to initialize.
    :param any value: The value to set keys to.  If ``None``, don't set a value
    '''
    for key in keys:
        if value is not None:
            dictionary[key] = value


def week_range(start, finish):
    '''Create a range of weeks from start and finish dates.

    :param date start: The date of the first day in the first week.
    :param date finish: The date of the first day in the last week.
    '''
    weeks = []
    week = start
    while week < finish:
        weeks.append(week.strftime('%Y-%m-%d'))
        week += timedelta(weeks=1)
    return weeks


class Analizator(object):
    def __init__(self, data, subject=''):
        self.subject = subject
        self.min = data.min()
        self.max = data.max()

    def __str__(self):
        return '{subject}: {min} (min) {max} (max)'.format(**vars(self))


def print_report(subject):
    '''
    Do various calculations on the subject, then print the results.
    '''
    result_data = Analizator(array(data_collect[subject]), subject)
    print(result_data)

    ordered_dict(data_collect[subject + 'Histogram'],
                 range(result_data.min, result_data.max))
    print_output(data_collect[subject + 'Histogram'].items())


def print_date_report(subject, name):
    # Calculate only the min and the max
    data = array(data_collect[subject].keys())
    minWeek = data.min()
    maxWeek = data.max()

    allData = OrderedDict()
    ordered_dict(allData, week_range(minWeek, maxWeek), 0)
    for key, value in data_collect[subject].items():
        newKey = key.isoformat()
        allData[newKey] = value
    print_output(allData.items(), name)


def print_output(data, label=''):
    # Fill in percentages of the total.
    for key, datapoint in enumerate(data):
        name, value = datapoint
        percentage = (
            float(value) / data_collect['count']) * 100 if data_collect['count'] else 0
        name = '%6.2f%% %s' % (percentage, name)
        data[key] = (name, value)

    for item, amount in data:
        print("{0} ({1}) (Total - {2})".format(item, label, amount))
