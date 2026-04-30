from website import db, create_app

app = create_app()
ctx = app.app_context()
ctx.push()

# reset db
# db.drop_all()

db.create_all()
quit()
