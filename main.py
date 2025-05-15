from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import date

from data import db_session
from data.users import Users
from data.requests import Requests
from data.chats import Chats
from data.histories import History
from forms.users import LoginForm, RegisterForm
from forms.profile import ProfileForm
from forms.request import SendRequest
from forms.chat import Chat
from forms.history import AddHistory

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = '/static/img'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    try:
        return db_sess.get(Users, user_id)
    finally:
        db_sess.close()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('base.html', title='Главная')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if request.method == 'POST':
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        if form.date_of_birth.data > date.today():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Указана дата рождения из будующего")            
        user = Users(
            email=form.email.data,
            name=form.name.data,
            surname1=form.surname1.data,
            surname2=form.surname2.data,
            date_of_birth=form.date_of_birth.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title='Авторизация', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    form = ProfileForm()
    db_sess = db_session.create_session()
    info_user = db_sess.query(Users).filter(Users.id == current_user.id).first()
    photo = 'img/' + info_user.photo
    if request.method == 'POST':
        return redirect("/correction_profile")
    db_sess.close()
    return render_template('my_profile.html', title='Профиль', title2='Мой профиль', form=form, photo=photo, info_user=info_user)


@app.route('/profile/<user>')
def profile(user):
    form = ProfileForm()
    db_sess = db_session.create_session()
    info_user = db_sess.query(Users).filter(Users.id == user).first()
    photo = 'img/' + info_user.photo
    title2 = f'Профиль {info_user.surname1} {info_user.name} {info_user.surname2}'
    db_sess.close()
    return render_template('profile.html', title='Профиль', title2=title2, form=form, photo=photo, info_user=info_user)


@app.route('/correction_profile', methods=['GET', 'POST'])
def correction_profile():
    form = ProfileForm()
    if request.method == 'POST':
        if form.date_of_birth.data > date.today():
            return render_template('correction_profile.html', title='Изменение профиля', form=form, message='Указана дата рождения из будущего')
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == current_user.email).first()
        user.name = form.name.data
        user.surname1 = form.surname1.data
        user.surname2 = form.surname2.data

        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save('static/img/' + filename)
            user.photo = filename
        
        user.date_of_birth = form.date_of_birth.data
        user.info_about = form.info_about.data
        db_sess.commit()
        db_sess.close()
        return redirect("/my_profile")
    return render_template('correction_profile.html', title='Изменение профиля', form=form)


@app.route('/request')
def requests():
    return render_template('request.html', title='Запросы')


@app.route('/send_req', methods=['GET', 'POST'])
def send_req():
    form = SendRequest()
    res = []
    if request.method == 'POST':
        value = form.search.data
        all_users = value.split()
        db_sess = db_session.create_session()
        res = []
        for i in all_users:
            info = list(db_sess.query(Users).filter(Users.name == i)) + list(db_sess.query(Users).filter(Users.surname1 == i)) + list(db_sess.query(Users).filter(Users.surname2 == i))
            for j in info:
                res.append((j.id, j.surname1 + ' ' + j.name + ' ' + j.surname2))
        db_sess.close()
    return render_template('send_req.html', title='Отправить запрос', form=form, res=sorted(set(res)))


@app.route('/send_req/<user>')
def send_req_sb(user):
    db_sess = db_session.create_session()
    req = Requests(
        first=current_user.id,
        second=int(user))
    db_sess.add(req)
    db_sess.commit()
    db_sess.close()
    return redirect("/send_req")


@app.route('/sent_req')
def sent_req():
    db_sess = db_session.create_session()
    all_users = list(db_sess.query(Requests).filter(Requests.first == current_user.id))
    info = list(db_sess.query(Users))
    res = []
    for i in all_users:
        info = list(db_sess.query(Users).filter(Users.id == i.second))
        for j in info:
            res.append((j.id, j.surname1 + ' ' + j.name + ' ' + j.surname2))
    db_sess.close()
    return render_template('sent_req.html', title='Отправленные запросы', res=sorted(set(res)))


@app.route('/get_req')
def get_req():
    db_sess = db_session.create_session()
    all_users = list(db_sess.query(Requests).filter(Requests.second == current_user.id))
    info = list(db_sess.query(Users))
    res = []
    for i in all_users:
        info = list(db_sess.query(Users).filter(Users.id == i.first))
        for j in info:
            res.append((j.id, j.surname1 + ' ' + j.name + ' ' + j.surname2))
    db_sess.close()
    return render_template('get_req.html', title='Входящие запросы', res=sorted(set(res)))


@app.route('/accept_req/<user>')
def accept_req(user):
    db_sess = db_session.create_session()
    chat = Chats(
        first=current_user.id,
        second=int(user))
    db_sess.add(chat)
    db_sess.commit()
    req = db_sess.query(Requests).filter(Requests.first == user and Requests.second == current_user.id).first()
    db_sess.delete(req)
    db_sess.commit()
    db_sess.close()
    return redirect('/get_req')


@app.route('/decline_req/<user>')
def decline_req(user):
    db_sess = db_session.create_session()
    req = db_sess.query(Requests).filter(Requests.first == user and Requests.second == current_user.id).first()
    db_sess.delete(req)
    db_sess.commit()
    return redirect('/get_req')


@app.route('/chats')
def chats():
    db_sess = db_session.create_session()
    chats1 = list(db_sess.query(Chats).filter(Chats.first == current_user.id))
    chats2 = list(db_sess.query(Chats).filter(Chats.second == current_user.id))
    chats = chats1 + chats2
    res = []
    for i in chats:
        if i.first == current_user.id:
            user = db_sess.query(Users).filter(Users.id == i.second).first()
        else:
            user = db_sess.query(Users).filter(Users.id == i.first).first()
        res.append((user.id, 'img/' + user.photo,
                    user.surname1 + ' ' + user.name + ' ' + user.surname2))
    db_sess.close()
    return render_template('chats.html', title='Чаты', res=res)


@app.route('/chat/<user1>/<user2>', methods=['GET', 'POST'])
def chat(user1, user2):
    form = Chat()
    db_sess = db_session.create_session()
    second_user = db_sess.query(Users).filter(Users.id == user2).first()
    info_user = ['img/' + second_user.photo, second_user.surname1 + ' ' + second_user.name + ' ' + second_user.surname2, second_user.id]
    res = []
    chat1 = list(db_sess.query(Chats).filter(Chats.first == int(user1), Chats.second == int(user2)))
    chat2 = list(db_sess.query(Chats).filter(Chats.first == int(user2), Chats.second == int(user1)))
    if request.method == 'POST':
        if chat1:
            ch = db_sess.query(Chats).filter(Chats.first == user1, Chats.second == user2).first()
            ch.chat = ch.chat + '|1:' + form.text.data
        if chat2:
            ch = db_sess.query(Chats).filter(Chats.first == user2, Chats.second == user1).first()
            ch.chat = ch.chat + '|2:' + form.text.data
        db_sess.commit()
    chat1 = list(db_sess.query(Chats).filter(Chats.first == int(user1), Chats.second == int(user2)))
    chat2 = list(db_sess.query(Chats).filter(Chats.first == int(user2), Chats.second == int(user1)))
    if chat1:
        text = chat1[0].chat.split('|')
        text1 = [i[2:] for i in text if i[0] == '1']
        text2 = [i[2:] for i in text if i[0] == '2']
    if chat2:
        text = chat2[0].chat.split('|')
        text1 = [i[2:] for i in text if i[0] == '2']
        text2 = [i[2:] for i in text if i[0] == '1']
    for i in text:
        if i[2:] in text1:
            res.append((i[2:], 1))
        if i[2:] in text2:
            res.append((i[2:], 2))
    db_sess.close()
    return render_template('chat.html', title='Чат', form=form, res=res, info_user=info_user)


@app.route('/history')
def history():
    return render_template('history.html', title='Истории')


@app.route('/add_history', methods=['GET', 'POST'])
def add_history():
    form = AddHistory()
    if request.method == 'POST':
        db_sess = db_session.create_session()
        if form.image.data and form.text.data:
            filename = secure_filename(form.image.data.filename)
            history = History(
                user=current_user.id,
                image=filename,
                text=form.text.data)
            form.image.data.save('static/img/' + filename)
            db_sess.add(history)
        elif form.image.data:
            filename = secure_filename(form.image.data.filename)
            history = History(
                user=current_user.id,
                image=filename)
            form.image.data.save('static/img/' + filename)
            db_sess.add(history)
        elif form.text.data:
            history = History(
                user=current_user.id,
                text=form.text.data)
            db_sess.add(history)
        db_sess.commit()
        db_sess.close()
    return render_template('add_history.html', title='Добавить историю', form=form, text='', button='Добавить историю')


@app.route('/my_history')
def my_history():
    db_sess = db_session.create_session()
    res = [('img/' + i.image, i.text, i.id) for i in list(db_sess.query(History).filter(History.user == current_user.id))]
    db_sess.close()
    return render_template('history_sb.html', title='Истории', title2='Мои истории', res=res, text='вас', correct=True)


@app.route('/correction_history/<num>', methods=['GET', 'POST'])
def correction_history(num):
    form = AddHistory()
    db_sess = db_session.create_session()
    history = db_sess.query(History).filter(History.id == num).first()
    if request.method == 'POST':
        history.text = form.text.data
        filename = secure_filename(form.image.data.filename)
        history.image = filename
        if filename:
            form.image.data.save('static/img/' + filename)
        db_sess.commit()
        db_sess.close()
        return redirect('/my_history')
    db_sess.close()
    return render_template('add_history.html', title='Измененить истории', form=form, text=history.text, button='Сохранить изменения')


@app.route('/delete_history/<num>')
def delete_history(num):
    db_sess = db_session.create_session()
    history = db_sess.query(History).filter(History.id == num).first()
    db_sess.delete(history)
    db_sess.commit()
    db_sess.close()
    return redirect('/my_history')


@app.route('/friend_history')
def friend_history():
    db_sess = db_session.create_session()
    chats1 = list(db_sess.query(Chats).filter(Chats.first == current_user.id))
    chats2 = list(db_sess.query(Chats).filter(Chats.second == current_user.id))
    chats = chats1 + chats2
    friends = []
    for i in chats:
        if i.first == current_user.id:
            user = db_sess.query(Users).filter(Users.id == i.second).first()
            friends.append(('Истории ' + user.surname1 + ' ' + user.name + ' ' + user.surname2, user.id))
        if i.second == current_user.id:
            user = db_sess.query(Users).filter(Users.id == i.first).first()
            friends.append(('Истории ' + user.surname1 + ' ' + user.name + ' ' + user.surname2, user.id))
    db_sess.close()
    return render_template('friend_history.html', title='Истории', friends=friends)


@app.route('/history_sb/<user>')
def history_sb(user):
    db_sess = db_session.create_session()
    res = [('img/' + i.image, i.text, i.id) for i in list(db_sess.query(History).filter(History.user == user))]
    info = db_sess.query(Users).filter(Users.id == user).first()
    fio = info.surname1 + ' ' + info.name + ' ' + info.surname2
    db_sess.close()
    return render_template('history_sb.html', title='Истории', title2='Истории ' + fio, res=res, text=fio, correct=False)


if __name__ == '__main__':
    db_session.global_init("db/messenger.db")
    app.run(port=8080, host='0.0.0.0')
