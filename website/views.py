from flask import Blueprint, render_template, request

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    # get the value of p and genre eg. http://127.0.0.1:5000/?genre=electronic, genre = electronic
    # if page or genre is not specified, the value will be None
    page = request.args.get("p")
    genre = request.args.get("genre")

    return render_template("index.html")

@main_bp. route('/search')
def search():
    if request.args['search'] and request.args['search'] !="":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        event = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        return render_templaye('index.html', events=events)
    else:
        return redirect(url_for('main.index'))
