from flask import Blueprint, jsonify

from data import db_session
from data.user import User


blueprint = Blueprint("user_api",
                      __name__,
                      template_folder="templates")


PUBLIC_APIKEY = "GJYE-HY34-NBSD-LN4C"
PRIVATE_APIKEY = "TRNU-N453-LDF4-UK5R"


@blueprint.route("/api/v1/users/<string:apikey>", methods=["GET"])
def get_users(apikey):
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    print(apikey)
    print(PUBLIC_APIKEY)
    print(PRIVATE_APIKEY)
    if not users:
        return jsonify({"error": "users not found"})
    if PUBLIC_APIKEY == apikey or PRIVATE_APIKEY == apikey:
        return jsonify(
            {"users":
                 [item.to_dict(only=("id", "username", "email", "created_date"))
                  for item in users]
             }
        )
    return jsonify({"error": "bad apikey"})


@blueprint.route("/api/v1/user/<string:apikey>/<int:user_id>", methods=["GET"])
def get_one_user(apikey, user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return jsonify({"error": "user not found"})
    elif apikey == PUBLIC_APIKEY or apikey == PRIVATE_APIKEY:
        return jsonify(
            {
                "user": user.to_dict(only=("id", "username", "email", "created_date"))
            }
        )
    return jsonify({"error": "bad apikey"})


@blueprint.route("/api/v1/user/delete/<string:private_apikey>/<int:user_id>")
def delete_user(private_apikey, user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not user:
        return jsonify({"error": "user not found"})
    elif private_apikey == PRIVATE_APIKEY:
        db_sess.delete(user)
        db_sess.commit()

        return jsonify({"success": "OK"})
    return jsonify({"error": "bad apikey"})
