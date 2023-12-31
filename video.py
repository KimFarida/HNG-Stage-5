from pymongo import MongoClient
import datetime
import uuid
import os
import speech_recognition as sr
from gridfs import GridFS
from moviepy.editor import VideoFileClip
import tempfile
from dotenv import load_dotenv
load_dotenv() 


client = MongoClient(os.getenv('MONGODB_URI'))
db = client['HNG']
video_collection = db['Videos']
fs = GridFS(db)

class Videos:
    def __init__(self, temp_filename):
        self.temp_filename = temp_filename
        self.id = str(uuid.uuid4())
        self.created_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.url = f'/api/videos/{self.id}/stream'
        self.filename = os.path.basename(temp_filename)
        self.compressed_filename = None  
        self.file_id = None
        self.transcript = None  

    def to_json(self):
        return {
            'id': self.id,
            'temp_filename': self.temp_filename,
            'created_time': self.created_time,
            'url': self.url,
            'filename': self.filename,
            'compressed_filename': self.compressed_filename,
            'file_id': self.file_id,
            'transcript': self.transcript
        }

    def save(self):
        # Saves the video information to the MongoDB collection
        video_collection.insert_one({
            'id': self.id,
            'filename': self.filename,
            #'compressed_filename': self.compressed_filename, 
            'created_time': self.created_time,
            'url': self.url,
            'transcript': self.transcript  # Save the transcript
        })

        # Read the video file contents as bytes
        with open(self.temp_filename, 'rb') as file:
            file_data = file.read()

        # Save the video file in GridFS
        file_id = fs.put(file_data, filename=self.filename)

        # Update the video document with the GridFS file ID
        video_collection.update_one({'id': self.id}, {'$set': {'file_id': file_id}})

    def compress_video(self, max_size):
        video = VideoFileClip(self.temp_filename)
        video_resized = video.resize(width=720)  # Resize the video to width of 720px

        temp_filepath = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
        self.compressed_filename = os.path.basename(temp_filepath)  # Set the compressed filename
        video_resized.write_videofile(temp_filepath, codec="libx264", audio_codec="aac")

        # Check if the compressed video size is within the specified limit
        if os.path.getsize(temp_filepath) > max_size:
            return False

        # Save the compressed video file in GridFS
        file_id = fs.put(open(temp_filepath, 'rb'), filename=self.compressed_filename)

        # Save the video information to the MongoDB collection
        video_collection = db['Videos']
        video_collection.insert_one({
            'id': self.id,
            'filename': self.filename,
            'file_id': file_id,  # Save the compressed video file ID
            'created_time': self.created_time,
            'url': f'/api/videos/{self.id}/stream',
            'transcript': self.transcript  # Save the transcript
        })

        return True

    def extract_audio(self):
        # Load the video
        video = VideoFileClip(self.temp_filename)

        # Extract the audio from the video
        audio_file = video.audio
        audio_file.write_audiofile("audio.wav")

        # Initialize recognizer
        r = sr.Recognizer()

        # Load the audio file
        with sr.AudioFile("audio.wav") as source:
            data = r.record(source)

        # Convert speech to text
        result = r.recognize_google(data, show_all=True)

        # Process the transcription and generate timestamps manually
        timestamps = []
        audio_duration = video.duration
        interval_duration = 15  # Interval duration in seconds
        num_intervals = int(audio_duration / interval_duration)
        current_time = 0.0

        for i in range(num_intervals):
            start_time = current_time
            end_time = current_time + interval_duration
            current_time += interval_duration

            # Convert timestamps to timedelta objects
            start_time = datetime.timedelta(seconds=start_time)
            end_time = datetime.timedelta(seconds=end_time)

            # Find the corresponding transcript for the interval
            transcript = ""
            alternatives = result.get('alternative', [])
            if alternatives:
                alternative = alternatives[0]  # Get the first alternative
                if 'transcript' in alternative:
                    transcript = alternative['transcript']

            # Append the timestamped transcript
            timestamps.append({
                'start_time': str(start_time),
                'end_time': str(end_time),
                'text': transcript.strip()
            })

        # Save the transcription and timestamps to the MongoDB collection
        audio_collection = db['Audio']
        audio_collection.insert_one({
            'video_id': self.id,
            'timestamps': timestamps
        })

        self.transcript = timestamps
        # video_collection = db['Videos']
        # video_collection.insert_one({
        #     'id': self.id,
        #     'filename': self.filename,
        #     'created_time': self.created_time,
        #     'url': self.url,
        #     'transcript': timestamps  # Save the transcript
        # })

    def get_video_url(self):
        # Retrieve the video file ID from the Videos collection
        video = Videos.find_by_id(self.id)
        if video is not None:
            streaming_url = f'/api/videos/{self.id}/stream'
            return streaming_url
        else:
            return None
       
    @staticmethod
    def find_by_id(video_id):
        video_collection = db['Videos']
        return video_collection.find_one({'id': video_id})
    




















# class Videos:
#     def __init__(self, filename, cloudinary_public_id):
#         self.id = str(uuid.uuid4()) 
#         self.filename = filename
#         self.cloudinary_public_id = cloudinary_public_id
#         self.created_time = datetime.now()

#     def save(self):
#         # Save the video information to the MongoDB collection
#         video_collection = db['Videos']
#         video_collection.insert_one({
#             'id': self.id,
#             'filename': self.filename,
#             'url': self.get_video_url(),
#             'created_time': self.created_time
#         })

#     def get_video_url(self):
#         # Retrieve the video URL from Cloudinary based on the public ID
#         # Replace 'your_cloud_name' with your actual Cloudinary cloud name
#         return f'https://res.cloudinary.com/duanh7tsg/video/upload/{self.cloudinary_public_id}'
