from flask import request, jsonify, Response
from flask.views import MethodView
from models import db, Users, Notifications
import datetime
from crypto import Crypto


class UserAPI(MethodView):

    def bad_id(self, user_id: int) -> Response:
        return jsonify({'result': f'User {user_id} not found'})

    def access_denided(self, user_id: int) -> Response:
        return jsonify({'result':
                        f'Access denided to notification: {user_id}'
                        }
                       )

    def passwords_problem(self) -> Response:
        return jsonify({'result': 'Entered passwords are different'})

    def users_overlap(self, name: str, mail: str) -> Response:
        return jsonify({'result':
                        f'User {name} with e-mail: {mail} already exists'
                        }
                       )

    def autentification(self, user_pas: str, input_pas: str) -> bool:
        return True if user_pas == input_pas else False

    def get(self, user_id=None) -> Response:
        if user_id:
            user = Users.query.get(user_id)
            if user:
                result = user.to_dict()
            else:
                result = self.bad_id(user_id)
        else:
            users = Users.query.all()
            print(users)
            users_name = [item.to_dict() for item in users]
            result = {'counts': len(users_name),
                      'result': users_name
                      }
        return jsonify(result)

    def post(self) -> Response:
        name = request.get_json()['name']
        mail = request.get_json()['e-mail']
        pas = request.get_json()['password']
        c_pas = request.get_json()['confirm-password']

        user_overlap = Users.query.filter(Users.name == name,
                                          Users.mail == mail
                                          ).first()

        if user_overlap:
            return self.users_overlap(name, mail)
        else:
            if pas == c_pas:
                user = Users(name=name,
                             mail=mail,
                             password=Crypto.cryptor(pas)
                             )
                db.session.add(user)
                db.session.commit()
                return jsonify(user.to_dict())
            else:
                return self.passwords_problem()

    def patch(self, user_id: int) -> Response:
        user = Users.query.get(user_id)
        if user:
            input_pas = Crypto.cryptor(request.get_json()['password'])
            if self.autentification(user.password, input_pas):
                new_name = request.get_json()['name']
                new_mail = request.get_json()['e-mail']
                new_password = \
                    Crypto.cryptor(request.get_json()['new_password'])
                user.name = new_name
                user.mail = new_mail
                user.password = new_password
                db.session.add(user)
                db.session.commit()
                result = user.to_dict()
            else:
                result = self.access_denided(user_id)
        else:
            result = self.bad_id(user_id)
        return jsonify(result)

    def delete(self, user_id: int) -> Response:
        user = Users.query.get(user_id)
        if user:
            input_pas = Crypto.cryptor(request.get_json()['password'])
            if self.autentification(user.password, input_pas):
                db.session.delete(user)
                db.session.commit()
                result = user.to_dict()
            else:
                result = self.access_denided(user_id)
        else:
            result = self.bad_id(user_id)
        return jsonify(result)


class NoteAPI(MethodView):

    def bad_id(self, note_id) -> Response:
        return jsonify({'result': f'Notification {note_id} not found'})

    def access_denided(self, user_name: str) -> Response:
        return jsonify({'result': f'Access denided for user: {user_name}'})

    def bad_user(self, user_name: str) -> Response:
        return jsonify({'result': f'User {user_name} not exist'})

    def autentification(self,
                        owner_name: str,
                        owner_mail: str,
                        owner_pas: str
                        ) -> int:
        owner = Users.query.filter(Users.name == owner_name,
                                   Users.mail == owner_mail
                                   ).first()
        if owner:
            if Crypto.cryptor(owner_pas) == owner.password:
                return owner.id
            else:
                return -1
        else:
            None

    def get(self, note_id=None) -> Response:
        if note_id:
            notifictaion = Notifications.query.get(note_id)
            if notifictaion:
                result = notifictaion.to_dict()
            else:
                result = self.bad_id(note_id)
        else:
            notes = Notifications.query.all()
            note_list = [item.to_dict() for item in notes]
            result = {'counts': len(note_list),
                      'result': note_list
                      }
        return jsonify(result)

    def post(self) -> Response:
        owner_name = request.get_json()['owner']
        owner_mail = request.get_json()['e-mail']
        owner_pas = request.get_json()['password']

        owner_id = self.autentification(owner_name, owner_mail, owner_pas)

        if owner_id:
            if owner_id != -1:
                title = request.get_json()['title']
                description = request.get_json()['description']
                date = datetime.datetime.now()
                notification = Notifications(title=title,
                                             description=description,
                                             date=date,
                                             owner_id=owner_id
                                             )
                db.session.add(notification)
                db.session.commit()
                result = jsonify(notification.to_dict())
            else:
                result = self.access_denided(owner_name)
        else:
            result = self.bad_user(owner_name)
        return result

    def patch(self, note_id: int) -> Response:
        note = Notifications.query.get(note_id)
        if note:
            input_name = request.get_json()['owner']
            input_mail = request.get_json()['e-mail']
            input_pas = request.get_json()['password']
            input_id = self.autentification(input_name, input_mail, input_pas)
            if input_id:
                if input_id != -1 and input_id == note.owner_id:
                    note.title = request.get_json()['title']
                    note.description = request.get_json()['description']
                    note.date = datetime.datetime.now()
                    db.session.add(note)
                    db.session.commit()
                    result = jsonify(note.to_dict())
                else:
                    result = self.access_denided(input_name)
            else:
                result = result = self.bad_user(input_name)
        else:
            result = self.bad_id(note_id)
        return result

    def delete(self, note_id: int) -> Response:
        note = Notifications.query.get(note_id)
        if note:
            input_name = request.get_json()['owner']
            input_mail = request.get_json()['e-mail']
            input_pas = request.get_json()['password']
            input_id = self.autentification(input_name, input_mail, input_pas)
            if input_id:
                if input_id != -1 and input_id == note.owner_id:
                    db.session.delete(note)
                    db.session.commit()
                    tmp = note.to_dict()
                    tmp['status'] = "removed"
                    result = tmp
                else:
                    result = self.access_denided(input_name)
            else:
                result = result = self.bad_user(input_name)
        else:
            result = self.bad_id(note_id)
        return result
