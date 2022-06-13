from flask import Flask, render_template, request, redirect

from werkzeug.utils import secure_filename





app = Flask(__name__)

logon_id = None


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global logon_id
    if request.method == 'GET':

        return render_template('login.html')

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        cursor.execute(f'SELECT * FROM user WHERE id = "{id}";')
        table = cursor.fetchone()
        if table is None:
            return render_template('login.html', message='does not exist.')

        print(table)
        if table['pw'] == pw:

            logon_id = id
            return render_template('main.html', nickname=id)
        return render_template('login.html', message='password is wrong.', nickname=logon_id)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']

        cursor.execute(f'SELECT * FROM user WHERE id = "{id}"')
        result = cursor.fetchone()
        if result is not None:
            return render_template('signup.html', message='already exist.')

        cursor.execute(f'INSERT IGNORE INTO user (id, pw) VALUES ("{id}", {pw})')
        db.commit()

        return render_template('login.html')



# @app.route('/upload')
# def load_file():
#     return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # f.save(secure_filename(f.filename))
        f.save('static/upload/' + secure_filename(f.filename))
        print(f.filename)
        pname = upscale(f.filename)
        cursor.execute(f'INSERT INTO history (id, image) VALUES ("{logon_id}","{pname}")')
        db.commit()
        return render_template('result.html', image_name=pname, nickname=logon_id)

    if request.method == 'GET':
        return render_template('main.html', nickname=logon_id)


@app.route('/history', methods=['GET', 'POST'])
def history():
    cursor.execute(f'SELECT image FROM history WHERE id = "{logon_id}";')
    row = cursor.fetchall()
    print(row)
    history_list = []
    for i in row:
        history_list.append(list(i.values())[0])
    print(history_list)
    return render_template('history.html', nickname=logon_id, history_list=history_list)


@app.route('/logout', methods=['GET'])
def logout():
    global logon_id
    logon_id = None
    return render_template('main.html', nickname=logon_id)


def main():
    app.run('127.0.0.1', 80)


if __name__ == '__main__':
    main()
