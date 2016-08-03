from flask import Blueprint
from models import Group
import requests
import pygal

groups_blueprint = Blueprint('groups', __name__, url_prefix='/wigle')


@groups_blueprint.route('/', methods=['GET'])
def get_index():
    line_chart = pygal.Line(width=500, height=250)
    line_chart.title = 'WiGLE Group Rank'

    group = Group()

    # Update
    r = requests.get('https://wigle.net/api/v1/jsonGroupStats')
    p = lambda: None
    p.__dict__ = r.json()
    for x in p.groups:
        group.add_group(x['groupid'], x['longname'], x['rank'])

    # Read
    groups = group.get_all_groups()
    d = {}
    for grp in groups:
        if grp.groupid in d:
            d[grp.groupid].append(grp.rank)
        else:
            l = []
            l.append(grp.rank)
            d[grp.groupid] = l

    # Process
    for groupid in d.keys():
            last_val = -1
            change_count = 0
            for val in d[groupid]:
                if val < last_val or last_val == -1:
                    change_count += 1
                    last_val = val
            if change_count > 1 and val < 150:
                line_chart.add(group.get_group_by_group_id(groupid).longname, d[groupid])

    return line_chart.render(), 200
