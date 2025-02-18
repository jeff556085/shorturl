from flask import Flask, request, jsonify, redirect, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta
import uuid

from .db import init_db
from .models import db, URLMap
from .utils import is_valid_url

DEFAULT_EXPIRATION_DAYS = 30

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorturl.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)

    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=[]
    )

    @app.route('/api/v1/shorten', methods=['POST'])
    @limiter.limit("10 per 60")
    def create_short_url():
        data = request.get_json() or {}
        original_url = data.get('original_url', '')

        if not original_url:
            return jsonify({
                "short_url": "",
                "expiration_date": "",
                "success": False,
                "reason": "No URL provided"
            }), 400

        if len(original_url) > 2048:
            return jsonify({
                "short_url": "",
                "expiration_date": "",
                "success": False,
                "reason": "URL too long"
            }), 400

        if not is_valid_url(original_url):
            return jsonify({
                "short_url": "",
                "expiration_date": "",
                "success": False,
                "reason": "Invalid URL"
            }), 400

        short_code = uuid.uuid4().hex[:8]

        expires_at = datetime.utcnow() + timedelta(days=DEFAULT_EXPIRATION_DAYS)
        url_map = URLMap(
            original_url=original_url,
            short_code=short_code,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
            is_active=True
        )
        db.session.add(url_map)
        db.session.commit()

        scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
        host = request.headers.get("Host", "localhost:5000")
        short_url = f"{scheme}://{host}/{short_code}"

        return jsonify({
            "short_url": short_url,
            "expiration_date": expires_at.isoformat(),
            "success": True,
            "reason": ""
        }), 200

    @app.route('/<string:short_code>', methods=['GET'])
    def redirect_to_original(short_code):
        url_map = URLMap.query.filter_by(short_code=short_code).first()
        if not url_map:
            abort(404, description="Short URL not found")

        if not url_map.is_active or url_map.expires_at < datetime.utcnow():
            url_map.is_active = False
            db.session.commit()
            abort(410, description="Short URL has expired")

        return redirect(url_map.original_url, code=302)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)