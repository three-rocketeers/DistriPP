from flask import Flask, request, render_template, url_for, redirect
import uuid
import mysql.connector as mariadb

from config import db_host, db_port, db_user, db_password, db_name

from forms import JoinForm

app = Flask(__name__)
app.secret_key = '1d94e52c-1c89-4515-b87a-f48cf3cb7f0b'


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/create')
def create():
    return render_template('create.html')


# TODO use SQLALCHEMY for database calls
# TODO implement logic to check whether stories are actually in jira
@app.route('/create_submit', methods=['POST'])
def create_planning():
    # Gather and generate data
    uuid_str = str(uuid.uuid4())
    title = request.form['title']
    password = request.form['passwordbox']
    # Removes duplicate stories from list
    stories = list(set(request.form.getlist('stories')))

    # Database calls
    mariadb_connection = get_db_connection()
    try:
        cursor = mariadb_connection.cursor(buffered=True)
        cursor.execute("INSERT INTO planning VALUES (%s, %s, %s)", (uuid_str, title, password))
        for story in stories:
            cursor.execute("INSERT INTO stories (Name,PlanningID) VALUES (%s, %s)", (story, uuid_str))
        mariadb_connection.commit()
    finally:
        mariadb_connection.close()

    # Return resultpage
    return render_template('created.html', planning_id=uuid_str)


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
            password_db = cursor.fetchone()[0]
            if password_db != password:
                server_error = "Password is incorrect for the selected planning meeting."
                user = username
            else:
                planning_id = cursor.fetchone()[0]
                # read the stories for that planning event
                query = "Select Name from stories where PlanningID = '" + planning_id + "'"
                cursor.execute(query)
                stories = list(sum(cursor.fetchall(), ()))

                return render_template('estimate_main.html', planning_title=planning_name, stories=stories,
                                       username=username)

        # fetch the list of planning meetings
        query = "Select Title from planning"
        cursor.execute(query)
        planning_list = list(sum(cursor.fetchall(), ()))
        return render_template('estimate_start.html', planning_list=planning_list, error=server_error, form=form)

    finally:
        mariadb_connection.close()


def get_db_connection():
    return mariadb.connect(host=db_host, port=db_port, user=db_user, password=db_password,
                           database=db_name)


if __name__ == '__main__':
    app.run()
