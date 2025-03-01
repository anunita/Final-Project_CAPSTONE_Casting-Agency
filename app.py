import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
#from flask_migrate import Migrate
from models import db, Actor, Movie
from auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    #migrate = Migrate(app, db)

    CORS(app, resources={r'/*': {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
        )
        return response

    # MOVIE ROUTES
    #Get details of all movies"""
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:
            movies = Movie.query.all()
            
            if len(movies) == 0:
                abort(404)
            
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies],}), 200
        
        except Exception as e:
                print(f"Error retrieving movies: {e}")
                abort(500)

    # Get details of specific movies
    @app.route('/movies/<int:id>')
    @requires_auth('get:movies')
    def get_movies_by_id(jwt, id):
        try:
            movie = Movie.query.get(id)
            
            if movie is None:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'movie': movie.format(),}), 200
        
        except Exception as e:
                print(f"Error retrieving movies: {e}")
                abort(404)

    # Add new movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(jwt):
        body = request.get_json()
        if not ('title' in body and 'release_date' in body):
            abort(422)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is None or release_date is None:
            abort(400)

        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 201
        except Exception as e:
            print(f"Error adding new movies: {e}")
            abort(500)

    # Update existing movies
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(jwt, id):

        body = request.get_json()
        movie = Movie.query.get(id)

        if movie:
            try:
                title = body.get('title')
                release_date = body.get('release_date')
                if title:
                    movie.title = title
                if release_date:
                    movie.release_date = release_date

                movie.update()

                return jsonify({
                    'success': True,
                    'movie': movie.format()
            }), 200

            except:
                abort(422)
        else:
            abort(404)

    #Delete a movie
    @app.route("/movies/<id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, id):

        movie = Movie.query.get(id)

        if movie:
            try:
                movie.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                })
            except:
                abort(422)
        else:
            abort(404)

    # ACTOR ROUTES
    #Get details of all actors"""
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        try:
            actors = Actor.query.all()
            
            if len(actors) == 0:
                abort(404)
            
            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors],}), 200
        
        except Exception as e:
                print(f"Error retrieving actors: {e}")
                abort(500)

    # Get details of specific actor
    @app.route('/actors/<int:id>')
    @requires_auth('get:actors')
    def get_actors_by_id(jwt, id):
        try:
            actor = Actor.query.get(id)
            
            if actor is None:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'actor': actor.format(),}), 200
        
        except Exception as e:
                print(f"Error retrieving actor: {e}")
                abort(404)

    # Add new actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(jwt):
        body = request.get_json()
        if not ('name' in body and 'age' in body and 'gender' in body):
            abort(422)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if name is None or age is None or gender is None:
            abort(400)

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 201
        except Exception as e:
            print(f"Error adding new actor: {e}")
            abort(500)

    # Update existing actor details
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(jwt, id):

        body = request.get_json()
        actor = Actor.query.get(id)

        if actor:
            try:
                name = body.get('name')
                age = body.get('age')
                gender = body.get('gender')
                if name:
                    actor.name = name
                if age:
                    actor.age = age
                if gender:
                    actor.gender = gender
                actor.update()

                return jsonify({
                    'success': True,
                    'actor': actor.format()
            }), 200

            except:
                abort(422)
        else:
            abort(404)

    #Delete an actor details
    @app.route("/actors/<id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, id):

        actor = Actor.query.get(id)

        if actor:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                })
            except:
                abort(422)
        else:
            abort(404)

    # Error Handling
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400,
                    "message": "bad request"}),
            400,
        )

    @app.errorhandler(500)
    def internal_server(error):
        return (
            jsonify({"success": False, "error": 500,
                    "message": "internal server error"}), 
            500,
        )

    @app.errorhandler(AuthError)
    def handle_auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            'message': e.error
        }), e.status_code
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
