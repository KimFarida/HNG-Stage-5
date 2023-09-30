import os
from flask import Flask, request, jsonify,  send_file
from werkzeug.utils import secure_filename
from video import Videos, db, fs
from bson import ObjectId
from flask import send_file
from video import Videos, db


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

from bson.objectid import ObjectId


@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}, 400)

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'File has no name'}, 400)

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        video = Videos(file_path)
        video.save()

        #Extract audio from video
        video.extract_audio()

        # Compress the video and check if size is still too big (10GB limit)
        if not video.compress_video(10 * 1024 * 1024 * 1024):
            return jsonify({'error': 'Video size is still too big after compression'}, 400)

        video_url = video.get_video_url()

        # Retrieve the transcription from the MongoDB collection
        audio_collection = db['Audio']
        audio = audio_collection.find_one({'video_id': video.id})
        timestamps = audio['timestamps'] if audio else []

        response = {
            'message': 'Video uploaded and compressed successfully!',
            'id': video.id,
            'filename': video.filename,
            'created_time': video.created_time.isoformat(),
            'url': video_url,
            'transcription': []
        }

        for timestamp in timestamps:
            response['transcription'].append({
                'text': timestamp['text'],
                'start_time': timestamp['start_time'],
                'end_time': timestamp['end_time']

                
            })

        response['transcription'] = response['transcription'][:1]  # Limit to the first 3 timestamps
        message = 'Video uploaded and compressed successfully!'
        return jsonify(message, response, 201)
        

    return jsonify({'error': 'Failed to upload video'}, 400)

@app.route('/api/videos', methods=['GET'])
# Get all videos
def video():
    video_collection = db['Videos']
    videos = video_collection.find()
    video_files = []

    for video in videos:
        video_files.append({
            'id': video['id'],
            'filename': video['filename'],
            'created_time': video['created_time'].isoformat(),
            'stream_url': f'/api/videos/{video["id"]}/stream'
        })

    return jsonify({
        'message': 'Videos retrieved successfully',
        'video_files': video_files
        }, 200)


@app.route('/api/videos/<video_id>/stream', methods=['GET'])
# Stream a video
def stream_video(video_id):
    video = Videos.find_by_id(video_id)
    if video is None:
        return jsonify({'error': 'Video not found'})

    # Open a GridOut object for streaming the video file
    grid_out = fs.get(ObjectId(video['file_id']))

    # Stream the video file using Flask's send_file function
    return send_file(grid_out, mimetype='video/mp4')


@app.route('/api/transcription/<video_id>', methods=['GET'])
# Get the transcription for a video
def get_transcription(video_id):
    video = Videos.find_by_id(video_id)
    if video is None:
        return jsonify({'error': 'Video not found'})

    audio_collection = db['Audio']
    audio = audio_collection.find_one({'video_id': video_id})
    if audio is None:
        return jsonify({'error': 'Transcription not available for this video'},404)

    transcription = audio['timestamps'] if 'timestamps' in audio else []

    response = {
        'video_id': video_id,
        'transcription': []
    }

    for timestamp in transcription:
        response['transcription'].append({
            'text': timestamp['text'],
            'start_time': timestamp['start_time'],
            'end_time': timestamp['end_time']
        })

    return jsonify(response, 200)







# import cloudinary
# import cloudinary.uploader, cloudinary.exceptions
# import cloudinary.api


# # app.config['CLOUDINARY_URL'] = # Set your Cloudinary URL here

# # cloudinary.config(

# # @app.route('/api/upload', methods=['POST'])
# # # 
# # def upload_video():
# #     # Check if a video file was uploaded
# #     if 'video' not in request.files:
# #         return jsonify({'error': 'No video file provided'}), 400

# #     video_file = request.files['video']

# #     # Set the eager transformation options for video compression
# #     eager_options = {
# #         "format": "mp4",
# #         "transformation": [
# #             {"video_codec": "h264", "bit_rate": "500k"}
# #         ]
# #     }

# #     try:
# #         # Upload the video file to Cloudinary with eager transformations
# #         upload_result = cloudinary.uploader.upload(
# #             video_file,
# #             resource_type="video",
# #             eager=eager_options
# #         )

# #         # Create a Video object with the uploaded video's details
# #         video = Videos(video_file.filename, upload_result['public_id'])

# #         # Save the video to the database
# #         video.save()

# #         # Return the video details
# #         return jsonify({
# #             'id': video.id, 
# #             'filename': video.filename,
# #             'url': video.get_video_url(),
# #             'created_time': video.created_time,
# #         }), 200

# #     except cloudinary.exceptions.Error as e:
# #         return jsonify({'error': 'Video upload failed: ' + str(e)}), 400

# # video_collection = db['Videos']

# # @app.route('/api/videos/<video_id>', methods=['GET'])
# # def get_video_by_id(video_id):
# #     # Retrieve the video from the database using the provided video_id
# #     video = video_collection.find_one({'id': video_id})

# #     if video:
# #         return jsonify({
# #             "message": "Video retrieved successfully",
# #             'id': video['id'],
# #             'filename': video['filename'],
# #             'url': video['url'],
# #             'created_time': video['created_time']
# #         }), 200
# #     else:
# #         return jsonify({'error': 'Video not found'}), 404

# # @app.route('/api/videos', methods=['GET'])
# # def get_all_videos():
# #     # Retrieve all videos from the database
# #     videos = video_collection.find()

# #     video_list = []
# #     for video in videos:
# #         video_list.append({
# #             'id': video['id'],
# #             'filename': video['filename'],
# #             'url': video['url'],
# #             'created_time': video['created_time']
# #         })

# #     return jsonify({"message": "Videos retrieved successfully",
# #                     "data": video_list
# #                     }), 200
if __name__ == '__main__':
    app.run()
    #debug=True
