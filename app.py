from flask import Flask
from pony.flask import Pony
from config import config
from flask import render_template, request, json, jsonify
import requests
from forms import JoinForm, ViewForm
from models import db
from pony.orm import commit, select
from collections import Counter

app = Flask(__name__)
app.config.update(config)

Pony(app)


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/create')
def create():
    sprints = get_sprints()
    return render_template('create.html', sprints=sprints)


@app.route('/create_submit', methods=['POST'])
def create_planning():
    # Gather data from form
    title = request.form['title']
    password = request.form['passwordbox']
    # Removes duplicate stories from list
    planning = db.Planning(title=title, password=password)
    for story_name in request.form.getlist('stories'):
        planning.stories.add(db.Story(name=story_name, planning=planning))
    commit()
    return render_template('created.html', planning_name=title)


@app.route('/join', methods=['GET', 'POST'])
def join():
    server_error = None
    form = JoinForm()
    if form.validate_on_submit():
        planning_name = request.form['planning']
        password = request.form['password']
        username = request.form['name']

        planning = db.Planning.get(title=planning_name)
        if planning.password != password:
            server_error = "Password is incorrect for the selected planning meeting."
        else:
            stories = []
            for story in planning.stories:
                story_id = story.id
                name = story.name
                response = requests.get(app.config['JIRA']['base_url'] + app.config['JIRA']['rest_issue'] + str(
                    name) + "?fields=description,summary",
                                        auth=(app.config['JIRA']['user'], app.config['JIRA']['password']))
                data = response.json()
                description = data["fields"]["description"]
                summary = data["fields"]["summary"]
                # TODO move this to the creation phase and add to database
                stories.append({'id': story_id, 'name': name, "description": description, "summary": summary})

            return render_template('estimate_main.html', planning_title=planning_name, stories=stories,
                                   username=username)
    planning_list = select(p.title for p in db.Planning)
    return render_template('estimate_start.html', planning_list=planning_list, error=server_error, form=form)


@app.route('/view', methods=['GET', 'POST'])
def view():
    server_error = None
    form = ViewForm()
    if form.validate_on_submit():
        planning_name = str(request.form['planning'])
        password = request.form['password']

        planning = db.Planning.get(title=planning_name)
        if planning.password != password:
            server_error = "Password is incorrect for the selected planning meeting."
        else:
            result = {}
            for story in planning.stories:
                for estimate in story.estimates:
                    if story.name in result:
                        result[story.name]["estimates"].append(
                            {"estimate": estimate.estimate, "user": estimate.est_user, "comment": estimate.est_comment})
                    else:
                        result[story.name] = {"estimates": [{"estimate": estimate.estimate, "user": estimate.est_user,
                                                             "comment": estimate.est_comment}]}
            for key, value in result.items():
                result[key]["overall_est"] = get_estimate_string(value["estimates"])
            return render_template('view_main.html', data=result, planning_title=planning_name)
    planning_list = select(p.title for p in db.Planning)
    return render_template('view_start.html', planning_list=planning_list, error=server_error, form=form)


@app.route('/save', methods=['POST'])
def save_estimates():
    data = request.get_json()["data"]
    user = request.get_json()["user"]
    try:
        for estimate in data:
            story_id = estimate["storyid"]
            comment = estimate["comment"]
            estimate = estimate["estimate"]
            story = db.Story.get(id=story_id)
            estimate = db.Estimate(est_user=user, est_comment=comment, estimate=estimate, story=story)
            story.estimates.add(estimate)
            commit()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}


@app.route('/saved', methods=['GET'])
def saved():
    planning = request.args.get('planning')
    return render_template('estimated.html', planning_name=planning)


@app.route('/get_sprints', methods=['GET'])
def get_sprints():
    url = app.config['JIRA']['base_url'] + app.config['JIRA']['rest_sprints']
    response = requests.get(url, auth=(app.config['JIRA']['user'], app.config['JIRA']['password']))
    data = response.json()
    return data["sprints"]


@app.route('/get_stories', methods=['GET'])
def get_stories():
    url = app.config['JIRA']['base_url'] + app.config['JIRA']['rest_sprint_overview'] + request.args.get('sprintid')
    response = requests.get(url, auth=(app.config['JIRA']['user'], app.config['JIRA']['password']))
    data = response.json()
    stories = []
    for story in data["contents"]["issuesNotCompletedInCurrentSprint"]:
        stories.append(story["key"])
    return jsonify(data=stories)


def get_estimate_string(estimates):
    est_num = []
    for est in estimates:
        if est["estimate"].isdigit():
            est_num.append(int(est["estimate"]))
    all_identical = est_num[1:] == est_num[:-1]
    ranked = Counter(est_num).most_common(1)
    if ranked:
        result = str(ranked[0][0])
        if not all_identical:
            result += " (!)"
    else:
        result = '-'
    return result


if __name__ == '__main__':
    db.bind(app.config['PONY'])
    db.generate_mapping(create_tables=True)
    app.run(host='0.0.0.0')

if __name__ == 'app':
    db.bind(provider=app.config['PONY']['provider'], user=app.config['PONY']['user'],
            password=app.config['PONY']['password'], host=app.config['PONY']['host'],
            database=app.config['PONY']['database'], port=app.config['PONY']['port'])
    db.generate_mapping(create_tables=False)
    app.run(host='0.0.0.0')
