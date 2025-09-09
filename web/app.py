from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy

import settings
from database import Base
from models.command import Command

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
db.init_app(app)


@app.route("/")
def index_page():
    return render_template('index.html')


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.root_path, "favicon.ico")


@app.route("/commands")
def command_list():
    all_commands = db.session.execute(db.select(Command).order_by(Command.name)).scalars().all()

    return render_template(
        'command_list.html',
        title="명령어 목록",
        commands=all_commands
    )


@app.route("/commands/<command>")
def commands(command):
    prefix = request.args.get("prefix", default="@한마루 ", type=str)

    info = db.session.get(Command, command)

    if info is None:
        return f"Command not found", 404

    return render_template(
        'command_info.html',
        title=command,
        prefix=prefix,
        name=info.name,
        aliases=info.aliases,
        help=(info.help or "설명이 없습니다.").format(prefix=prefix),
        usage=(info.usage or "사용법이 없습니다.").format(prefix=prefix)
    )


@app.route("/stats")
def stats():
    return render_template(
        'stats.html',
        title="전적"
    )


@app.route("/ranking")
def ranking():
    return render_template(
        'ranking.html',
        title="랭킹"
    )
