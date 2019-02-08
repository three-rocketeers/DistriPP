from flask import Flask, request, render_template, url_for, redirect, json, jsonify
import requests
import psycopg2

from config import db_host, db_port, db_user, db_password, db_name, jira_base_url, jira_pass, jira_user, \
    jira_rest_sprints, jira_rest_issue, jira_rest_sprint_overview

from forms import JoinForm

app = Flask(__name__)
app.secret_key = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/create')
def create():
    sprints = get_sprints()
    return render_template('create.html', sprints=sprints)


# TODO use SQLALCHEMY for database calls
@app.route('/create_submit', methods=['POST'])
def create_planning():
    # Gather data from form
    title = request.form['title']
    password = request.form['passwordbox']
    # Removes duplicate stories from list
    stories = list(set(request.form.getlist('stories')))

    # Database calls
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO planning (title,password) VALUES (%s, %s) RETURNING id;", (title, password))
        planning_id = cursor.fetchone()[0]

        for story in stories:
            cursor.execute("INSERT INTO stories (name,planningid) VALUES (%s, %s);", (story, planning_id))
        connection.commit()
    finally:
        connection.close()

    # Return resultpage
    return render_template('created.html', planning_name=title)


@app.route('/join', methods=['GET', 'POST'])
def join():
    connection = get_db_connection()
    try:
        server_error = None
        cursor = connection.cursor()
        form = JoinForm()
        if form.validate_on_submit():
            planning_name = request.form['planning']
            password = request.form['password']
            username = request.form['name']

            # read the planning title
            query = "Select password, id from planning where title = '" + planning_name + "'"
            cursor.execute(query)
            password_db, planning_id = cursor.fetchone()
            if password_db != password:
                server_error = "Password is incorrect for the selected planning meeting."
                user = username
            else:
                # read the stories for that planning event
                query = "Select id, name from stories where planningid = '" + str(planning_id) + "'"
                cursor.execute(query)
                result = cursor.fetchall()
                stories = []
                for row in result:
                    story_id = row[0]
                    name = row[1]
                    response = requests.get(jira_base_url + jira_rest_issue + str(name) + "?fields=description,summary",
                                            auth=(jira_user, jira_pass))
                    data = response.json()
                    description = data["fields"]["description"]
                    summary = data["fields"]["summary"]
                    stories.append({'id': story_id, 'name': name, "description": description, "summary": summary})

                return render_template('estimate_main.html', planning_title=planning_name, stories=stories,
                                       username=username)

        # fetch the list of planning meetings
        query = "Select title from planning"
        cursor.execute(query)
        planning_list = list(sum(cursor.fetchall(), ()))
        return render_template('estimate_start.html', planning_list=planning_list, error=server_error, form=form)

    finally:
        connection.close()


@app.route('/save', methods=['POST'])
def save_estimates():
    data = request.get_json()["data"]
    user = request.get_json()["user"]
    connection = get_db_connection()
    try:
        for estimate in data:
            story_id = estimate["storyid"]
            comment = estimate["comment"]
            estimate = estimate["estimate"]
            cursor = connection.cursor()
            cursor.execute("INSERT INTO estimates (est_user,estimate,est_comment,storyid) VALUES (%s, %s, %s, %s)",
                           (user, estimate, comment, story_id))
        connection.commit()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
    finally:
        connection.close()


@app.route('/saved', methods=['GET'])
def saved():
    planning = request.args.get('planning')
    return render_template('estimated.html', planning_name=planning)


@app.route('/get_sprints', methods=['GET'])
def get_sprints():
    url = jira_base_url + jira_rest_sprints
    response = requests.get(url, auth=(jira_user, jira_pass))
    data = response.json()
    return data["sprints"]


@app.route('/get_stories', methods=['GET'])
def get_stories():
    url = jira_base_url + jira_rest_sprint_overview + request.args.get('sprintid')
    response = requests.get(url, auth=(jira_user, jira_pass))
    data = response.json()
    stories = []
    for story in data["contents"]["issuesNotCompletedInCurrentSprint"]:
        stories.append(story["key"])
    return jsonify(data=stories)


def get_db_connection():
    return psycopg2.connect(host=db_host, user=db_user, password=db_password,
                           dbname=db_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
