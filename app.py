# C:\Users\ishaan phaye\Desktop\VS Code\Projects\Flask RestAPI project
# C:\Users\ishaan phaye\Desktop\VS Code\venv\Scripts

from flask import Flask,request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
with app.app_context():
    db=SQLAlchemy(app)

# names = {'Ishaan': {'age':23, 'gender': 'Male'},
#          'Lavanya': {'age':21, 'gender': 'Female'}}

# class HelloWorld(Resource):
#     def get(self,name):
#         return names[name]
    
#     def post(self):
#         return {'data': 'Post it'}

class VideoModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Views = db.Column(db.Integer, nullable=False)
    Likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(Name = {self.Name}, Views = {self.Views}, Likes = {self.Likes})"

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('Name', type=str, help='Name of the video is required', required=True)
video_put_args.add_argument('Views', type=int, help='Views on the video is required', required=True)
video_put_args.add_argument('Likes', type=int, help='Likes on the video is required', required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('Name', type=str, help='Name of the video is required')
video_update_args.add_argument('Views', type=int, help='Views on the video is required')
video_update_args.add_argument('Likes', type=int, help='Likes on the video is required')


resource_fields =  {
    'id': fields.Integer,
    'Name': fields.String,
    'Views': fields.Integer,
    'Likes': fields.Integer
}

# videos = {}

# def abort_if_no_id(video_id):
#     if video_id not in videos:
#         abort(404,message='Video ID not valid...')

# def abort_if_video_exists(video_id):
#     if video_id in videos:
#         abort(409,message='Video already exists with that ID...')


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video not found")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message='Video ID taken...')
        video = VideoModel(id=video_id, Name=args['Name'], Views=args['Views'], Likes=args['Likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video doesn\'t exist, can\'t update...')

        if args['Name']:
            result.Name = args['Name']
        if args['Views']:
            result.Views = args['Views']
        if args['Likes']:
            result.Likes = args['Likes']
        
        db.session.commit()

        return result



    # @marshal_with(resource_fields)
    # def delete(self,video_id):
    #     del videos[video_id]
    #     return '',204

    
api.add_resource(Video, '/video/<int:video_id>')

if __name__ == "__main__":
    app.run(debug=True)