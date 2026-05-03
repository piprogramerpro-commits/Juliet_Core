from flask import Flask, request, Response, render_template, redirect
from engine.models import db, User, Message
from engine.formatter import build_prompt
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()

@app.route("/")
@login_required
def home():
    return render_template("index.html", user=current_user)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("pass")

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user, remember=True)
            return redirect("/")

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form.get("user"),
            password=request.form.get("pass")
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

def stream_text(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.02)

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.json
    msg = data.get("message", "")
    mode = data.get("mode", "general")

    # límite gratis
    if not current_user.is_premium and current_user.messages_count > 20:
        return Response("⚠️ Límite gratis alcanzado", mimetype='text/plain')

    current_user.messages_count += 1
    db.session.commit()

    # historial usuario
    history = Message.query.filter_by(user_id=current_user.id).all()
    memory = [{"role": m.role, "content": m.content} for m in history]

    prompt = build_prompt(msg, memory, mode)

    # IA simulada (luego puedes conectar Groq)
    response = f"**Modo: {mode}**\n\nRespuesta generada.\n\n```print('Juliet OK')```"

    db.session.add(Message(user_id=current_user.id, role="user", content=msg))
    db.session.add(Message(user_id=current_user.id, role="bot", content=response))
    db.session.commit()

    return Response(stream_text(response), mimetype='text/plain')

if __name__ == "__main__":
    app.run()
