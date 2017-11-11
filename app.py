from flask import Flask, request, render_template
import uuid
import mysql.connector as mariadb

from config import db_host, db_port, db_user, db_password, db_name

app = Flask(__name__)

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
    password = request.form['passwordbox'];
    # Removes duplicate stories from list
    stories = list(set(request.form.getlist('stories')));

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
    return render_template('created.html', planning_id=uuid_str);


def get_db_connection():
    return mariadb.connect(host=db_host, port=db_port, user=db_user, password=db_password,
                           database=db_name)


if __name__ == '__main__':
    app.run()
