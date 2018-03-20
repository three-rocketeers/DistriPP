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
    return render_template('created.html', planning_name = title)


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
                query = "Select Name from stories where PlanningID = '" + str(planning_id) + "'"
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
