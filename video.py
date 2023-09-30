from pymongo import MongoClient
import datetime
import uuid
import os
import speech_recognition as sr
from gridfs import GridFS
from moviepy.editor import VideoFileClip


# Create a MongoDB client and connect to your database
client = MongoClient(os.environ['MONGODB_URI'])
db = client['HNG']
fs = GridFS(db)


class Videos:
    def __init__(self, filepath):
        self.id = str(uuid.uuid4())
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.created_time = datetime.datetime.now()


    def save(self):
        # Save the video information to the MongoDB collection
        video_collection = db['Videos']
        video_collection.insert_one({
            'id': self.id,
            'filename': self.filename,
            'filepath': self.filepath,
            'created_time': self.created_time
        })

        # Store the video file in GridFS
        with open(self.filepath, 'rb') as file:
            file_id = fs.put(file, filename=self.filename)

        # Update the video document with the GridFS file ID
        video_collection.update_one({'id': self.id}, {'$set': {'file_id': file_id}})
        video_collection.update_one({'id': self.id}, {'$set': {'filepath': self.filepath}})

    def get_video_url(self):
        #Retrieve the video file ID from the Videos collection
        video = Videos.find_by_id(self.id)
        if video is not None and 'file_id' in video:
            file_id = video['file_id']
            streaming_url = f'/api/videos/{self.id}/stream'
            return streaming_url
        else:
            return None


    def compress_video(self, target_size):
        # Compress and convert the video to MP4 format
        video = VideoFileClip(self.filepath)
        video_resized = video.resize(height=360)  # Adjust the height as desired
        temp_filepath = f"temp_{self.filename}"
        video_resized.write_videofile(temp_filepath, codec="libx264", audio_codec="aac")

        # Check if the compressed video size is still too big
        if os.path.getsize(temp_filepath) > target_size:
            os.remove(temp_filepath)
            return False

        # Replace the original video file with the compressed version
        os.remove(self.filepath)
        os.rename(temp_filepath, self.filepath)
        return True
    

    def extract_audio(self):
        # Load the video
        video = VideoFileClip(self.filepath)

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

        # Print the timestamps with corresponding transcripts
        # for i, timestamp in enumerate(timestamps):
        #     print(f"{timestamp['start_time']} - {timestamp['end_time']}: {timestamp['text']}")

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