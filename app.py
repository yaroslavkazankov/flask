from config import app
from models import db
from views import UserAPI, NoteAPI

if __name__ == "__main__":
    @app.before_first_request
    def create_table():
        db.create_all()

    app.add_url_rule('/users/<user_id>', view_func=UserAPI.as_view('user'))
    app.add_url_rule('/users/', view_func=UserAPI.as_view('users'))
    app.add_url_rule('/note/<note_id>', view_func=NoteAPI.as_view('note'))
    app.add_url_rule('/note/', view_func=NoteAPI.as_view('notes'))

    app.run(host='localhost', port=8000)
