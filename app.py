from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/create_submit', methods=['POST'])
def create_planning():
    # TODO implement creation logic
    planning_id = 'a408a018-3bfb-4eaf-943d-2c5340f10a02';
    return render_template('created.html', planning_id=planning_id);


if __name__ == '__main__':
    app.run()
