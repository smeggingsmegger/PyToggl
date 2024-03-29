import re
import requests

from datetime import datetime
from json import dumps

class PyToggl:
    '''
    PyToggl - The definative Toggl library for Python.


    To use this library:
        from PyToggl import PyToggl
        pytoggl = PyToggl('####mytoken####')

        # Query anything!
        results = pytoggl.query('/somequery', params={'somekey': 'somevalue'})


    '''
    defaults = {
        'api_version': 8,
        'api_reports_version': 2,
        'api_username': '',
        'api_password': '',
        'api_workspace_name': '',
        'api_base_url': 'https://api.track.toggl.com/api',
        'api_base_reports_url': 'https://api.track.toggl.com/reports/api',
        'user_agent': 'The PyToggl Library - https://github.com/smeggingsmegger/PyToggl',
    }

    def __init__(self, api_token, **kwargs):
        '''
        '''
        # Credentials
        self.api_token = api_token

        # The Toggl API is a little strange in that it has the concept of "Me"
        # Although you can query users that are attached to a workspace that "Me"
        # owns (or possibly is an admin of).
        self.me = None

        # All other options, overridable by kwargs.
        for key in self.defaults:
            setattr(self, key, kwargs.get(key, self.defaults.get(key, None)))

        # Create the API URLs.
        self.api_url = self.api_base_url + '/v' + str(self.api_version)
        self.api_reports_url = self.api_base_reports_url + '/v' + str(self.api_reports_version)
        self.today_str = str(datetime.now().date())

    '''
    Internal methods for doing things and abstracting away typical API copy-pasta.
    '''

    def _human_duration(self, t, milliseconds=True):
        if milliseconds:
            seconds = int(t) / 1000
        else:
            seconds = int(t)

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        weeks, days = divmod(days, 7)
        return (weeks, days, hours, minutes, seconds)

    def _pretty_duration(self, duration):
        output = ''
        if duration[0]:
            output += '{} Weeks, '.format(duration[0])
        if duration[1]:
            output += '{} Days, '.format(duration[1])
        if duration[2]:
            output += '{} Hours, '.format(duration[2])
        if duration[3]:
            output += '{} Minutes, '.format(duration[3])
        output += '{} Seconds'.format(duration[4])
        return output

    def _query(self, url, params, method, query_type=None, return_type='json'):
        if query_type == 'report':
            api_url = self.api_reports_url + url
        else:
            api_url = self.api_url + url

        auth = (self.api_token, 'api_token')
        headers = {'content-type': 'application/json'}

        if method == "POST":
            response = requests.post(api_url, auth=auth, headers=headers, params=params)
        elif method == "GET":
            response = requests.get(api_url, auth=auth, headers=headers, params=params)
        else:
            raise UserWarning('GET or POST are the only supported request methods.')

        # If the response errored, raise for that.
        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        if return_type == 'json':
            return response.json()
        else:
            return response

    def _get_timeslips(self, **kwargs):
        order_field = kwargs.get('order_field', 'date')
        subgrouping = kwargs.get('subgrouping', 'projects')
        grouping = kwargs.get('grouping', 'users')
        params = {
            'user_agent': self.user_agent,
            'grouping': grouping,
            'subgrouping': subgrouping,
            'order_field': order_field,
        }
        for key in kwargs:
            if not params.get(key):
                params[key] = kwargs.get(key)

        response = self.query_report('/details', params)

        return response


    '''
    Primary Methods

    self.query and self.query_report can be used to perform any API call.
    '''
    def query_report(self, url, params={}, method='GET', return_type='json'):
        return self._query(url, params, method, query_type='report', return_type=return_type)

    def query(self, url, params={}, method='GET', query_type='report', return_type='json'):
        return self._query(url, params, method, return_type=return_type)

    '''
    Convenience Methods
    '''

    # WorkSpaces
    def get_workspaces(self):
        workspaces = self.query('/workspaces')
        return [WorkSpace(w) for w in workspaces]

    def get_workspace(self, identifier_value, identifier='name'):
        workspace = None
        workspaces = self.get_workspaces();

        for w in workspaces:
            if getattr(w, identifier) == identifier_value:
                workspace = w

        return workspace

    # WorkSpaces / Users
    def get_workspace_users(self, workspace_id):
        if not workspace_id:
            raise UserWarning('A workspace ID is required to find users.')

        users = self.query('/workspaces/' + str(workspace_id) + '/workspace_users');
        return [User(u) for u in users]

    # Users
    def get_user_hours(self, **kwargs):
        subgrouping = kwargs.get('subgrouping', 'projects')
        grouping = kwargs.get('grouping', 'users')
        params = {
            'user_agent': self.user_agent,
            'grouping': grouping,
            'subgrouping': subgrouping,
        }
        for key in kwargs:
            if not params.get(key):
                params[key] = kwargs.get(key)

        response = self.query_report('/summary', params)

        total = 0
        if len(response['data']) > 0:
            total = response['data'][0]['time']

        return self._human_duration(total)

    def get_user(self, identifier_value, workspace_id=None, identifier='name'):
        if not workspace_id:
            raise UserWarning('A workspace ID is required to find users.')

        user = None
        users = self.get_workspace_users(workspace_id);

        for u in users:
            if getattr(u, identifier) == identifier_value:
                user = u

        return user

    # TimeSlips (detailed report)
    def get_timeslips(self, **kwargs):
        timeslips = []
        response = self._get_timeslips(**kwargs)
        data = response['data']
        per_page = response['per_page']
        total_count = response['total_count']

        if data:
            for row in data:
                timeslips.append(TimeSlip(row))

        if total_count > per_page:
            # There are more records than can be returned in one go-round.
            total_pages = total_count / per_page
            if total_count % per_page:
                total_pages += 1

            for current_page in range(total_pages):
                page = current_page + 1
                if page > 1:
                    response = self._get_timeslips(page=page, **kwargs)
                    data = response['data']
                    if data:
                        for row in data:
                            timeslips.append(TimeSlip(row))

        return timeslips


'''
Classes for return objects from the API.
'''
class Toggject:
    '''
    This is the base class for all return objects.
    '''
    def __init__(self, toggject_dict):
        for key in toggject_dict:
            setattr(self, key, toggject_dict.get(key, None))

    def __repr__(self):
        reflection = ''
        for attr in vars(self):
            reflection += "<{}>.{} = {}\n".format(self.__class__.__name__, attr, getattr(self, attr))
        return reflection

    @property
    def dict(self):
        return self.__dict__

    @property
    def json(self):
        return dumps(self.__dict__)

class Group(Toggject):
    pass


class TimeSlip(Toggject):
    updated = ''
    task = None
    end = ''
    description = ''
    tags = []
    billable = 0.0
    pid = 0
    project = ''
    start = ''
    client = None
    user = ''
    is_billable = False
    tid = None
    uid = 0
    dur = 0
    use_stop = True
    id = 0
    cur = 'USD'

    @property
    def trac_tickets(self):
        '''
        Looks for any of the following trac ticket formats in the description field:

            t12345, t 12345, T12345, T 12345, #12345, # 12345, ticket 12345, TICKET 12345
        '''
        # ticket_numbers = re.findall(re.compile("([t#]\s?[0-9]{2,})|([t#][0-9]{2,})", re.IGNORECASE), self.description)
        ticket_numbers = re.findall(r"^[tT#]\s?[0-9]+", self.description)
        ticket_numbers += re.findall(r"[tT#][0-9]+", self.description)
        ticket_numbers += re.findall(re.compile("ticket\s?[0-9]+", re.IGNORECASE), self.description)

        # Remove Duplicates
        ticket_numbers = [re.sub('[^0-9]','', t) for t in ticket_numbers]
        return list(set(ticket_numbers))


    @property
    def pull_requests(self):
        '''
        Looks for any of the following pull request formats in the description field:

            pr12345, pr 2345, PR2345, PR 2345
        '''
        pr_numbers = re.findall(r"[pP][rR]\s?[0-9]+", self.description)
        pr_numbers += re.findall(re.compile("pull\s?request\s?[0-9]+", re.IGNORECASE), self.description)

        # Remove Duplicates
        pr_numbers = [re.sub('[^0-9]','', p) for p in pr_numbers]
        return pr_numbers


class User(Toggject):
    # Default properties, here for reference if nothing else.
    id = 0
    active = False
    admin = False
    at = u''
    avatar_file_name = u''
    email = u''
    group_ids = []
    inactive = False
    name = u''
    uid = 0
    wid = 0


class WorkSpace(Toggject):
    # Default properties, here for reference if nothing else.
    id = 0
    default_currency = 'USD'
    rounding_minutes = 0
    premium = True
    name = ''
    default_hourly_rate = 0
    admin = True
    campaign_taken = True
    ical_url = ''
    rounding = 1
    only_admins_see_team_dashboard = False
    at = ''
    api_token = ''
    projects_billable_by_default = True
    logo_url = ''
    only_admins_may_create_projects = False
    only_admins_see_billable_rates = False
