from flask import Blueprint, jsonify

from data import db_session
from data.trad import Trad


blueprint = Blueprint(
    "trad_api",
    __name__,
    template_folder="templates"
)


PUBLIC_APIKEY = "GJYE-HY34-NBSD-LN4C"
PRIVATE_APIKEY = "TRNU-N453-LDF4-UK5R"


@blueprint.route("/api/v1/trads/<string:apikey>", methods=["GET"])
def get_trads(apikey):
    db_sess = db_session.create_session()
    trads = db_sess.query(Trad).all()

    if not trads:
        return jsonify({"error": "trads not found"})
    elif PUBLIC_APIKEY == apikey or PRIVATE_APIKEY == apikey:
        return jsonify(
            {
                "trads": [item.to_dict(only=("id", "title", "author_id", "created_date"))
                          for item in trads]
            }
        )
    return jsonify({"error": "bad apikey"})


@blueprint.route("/api/v1/trad/<string:apikey>/<int:trad_id>")
def get_one_trad(apikey, trad_id):
    db_sess = db_session.create_session()
    trad = db_sess.query(Trad).get(trad_id)

    if not trad:
        return jsonify({"error": "trads not found"})
    elif PUBLIC_APIKEY == apikey or PRIVATE_APIKEY == apikey:
        return jsonify(
            {
                "trad": trad.to_dict(only=("id", "title", "author_id", "created_date"))
            }
        )
    return jsonify({"error": "bad apikey"})
