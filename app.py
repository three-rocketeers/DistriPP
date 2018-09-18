from flask import Flask, request, render_template, url_for, redirect, json, jsonify
import requests
import mysql.connector as mariadb

from config import db_host, db_port, db_user, db_password, db_name, jira_base_url, jira_pass, jira_rest_url, \
    jira_rest_version, jira_user

from forms import JoinForm

app = Flask(__name__)
app.secret_key = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/create')
def create():
    projects = get_projects()
    return render_template('create.html', projects=projects)


# TODO use SQLALCHEMY for database calls
# TODO implement logic to check whether stories are actually in jira
@app.route('/create_submit', methods=['POST'])
def create_planning():
    # Gather data from form
    title = request.form['title']
    password = request.form['passwordbox']
    # Removes duplicate stories from list
    stories = list(set(request.form.getlist('stories')))

    # Database calls
    mariadb_connection = get_db_connection()
    try:
        cursor = mariadb_connection.cursor(buffered=True)
        cursor.execute("INSERT INTO planning (Title,Password) VALUES (%s, %s)", (title, password))
        # TODO there must be a better way to get the ID of the last inserted item.
        query = "Select ID from planning where Title = '" + title + "'"
        cursor.execute(query)
        planning_id = cursor.fetchone()[0]

        for story in stories:
            cursor.execute("INSERT INTO stories (Name,PlanningID) VALUES (%s, %s)", (story, planning_id))
        mariadb_connection.commit()
    finally:
        mariadb_connection.close()

    # Return resultpage
    return render_template('created.html', planning_name=title)


@app.route('/join', methods=['GET', 'POST'])
def join():
    mariadb_connection = get_db_connection()
    try:
        server_error = None
        cursor = mariadb_connection.cursor(buffered=True)
        form = JoinForm()
        if form.validate_on_submit():
            planning_name = request.form['planning']
            password = request.form['password']
            username = request.form['name']

            # read the planning title
            query = "Select Password, ID from planning where Title = '" + planning_name + "'"
            cursor.execute(query)
            password_db, planning_id = cursor.fetchone()
            if password_db != password:
                server_error = "Password is incorrect for the selected planning meeting."
                user = username
            else:
                # read the stories for that planning event
                query = "Select ID, Name from stories where PlanningID = '" + str(planning_id) + "'"
                cursor.execute(query)
                result = cursor.fetchall()
                stories = []
                for row in result:
                    story_id = row[0]
                    name = row[1]
                    response = requests.get(jira_base_url + jira_rest_url + jira_rest_version + "/issue/" + str(name) + "?fields=description,summary",
                                            auth=(jira_user, jira_pass))
                    data = response.json()
                    description = data["fields"]["description"]
                    summary = data["fields"]["summary"]
                    stories.append({'id': story_id, 'name': name, "description": description, "summary": summary })

                return render_template('estimate_main.html', planning_title=planning_name, stories=stories,
                                       username=username)

        # fetch the list of planning meetings
        query = "Select Title from planning"
        cursor.execute(query)
        planning_list = list(sum(cursor.fetchall(), ()))
        return render_template('estimate_start.html', planning_list=planning_list, error=server_error, form=form)

    finally:
        mariadb_connection.close()


@app.route('/save', methods=['POST'])
def save_estimates():
    data = request.get_json()["data"]
    user = request.get_json()["user"]
    mariadb_connection = get_db_connection()
    try:
        for estimate in data:
            story_id = estimate["storyid"]
            comment = estimate["comment"]
            estimate = estimate["estimate"]
            cursor = mariadb_connection.cursor(buffered=True)
            cursor.execute("INSERT INTO estimates (User,Estimate,Comment,StoryID) VALUES (%s, %s, %s, %s)",
                           (user, estimate, comment, story_id))
        mariadb_connection.commit()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
    except:
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}
    finally:
        mariadb_connection.close()


@app.route('/saved', methods=['GET'])
def saved():
    planning = request.args.get('planning')
    return render_template('estimated.html', planning_name=planning)


@app.route('/get_projects', methods=['GET'])
def get_projects():
    response = requests.get(jira_base_url + jira_rest_url + jira_rest_version + "/project",
                            auth=(jira_user, jira_pass))
    data = response.json()
    projects = {}
    for project in data:
        projects[project['key']] = project['name']
    return projects


@app.route('/get_sprints', methods=['GET'])
def get_sprints():
    project = request.args.get('project')
    url = jira_base_url + jira_rest_url + jira_rest_version + "/search"
    data = {"jql": "project = " + project + " and sprint in (openSprints(), futureSprints()) and issuetype = Story",
            "maxResults": 200, "fields": ["customfield_10000", "summary"]}
    response = requests.post(url, json=data, auth=(jira_user, jira_pass))
    data = response.json()
    result = {}
    for issue in data['issues']:
        sprints = issue['fields']['customfield_10000']
        sprint_name = ""
        for sprint in sprints:
            splitted = sprint.split(",")
            if splitted[2][6:] in ["ACTIVE", "FUTURE"]:
                sprint_name = splitted[3][5:]
        if sprint_name in result:
            result[sprint_name].append(issue['key'])
        else:
            result[sprint_name] = [issue['key']]
    return jsonify(result=result)


def get_db_connection():
    return mariadb.connect(host=db_host, port=db_port, user=db_user, password=db_password,
                           database=db_name)


if __name__ == '__main__':
    app.run()
