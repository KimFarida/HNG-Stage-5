# HNG-Stage-5
HNG Stage 5: Screen Recorder Video Upload API


# Video Processing API

This API allows users to upload, process, and stream videos. Videos are processed to extract audio and generate transcriptions.

## Setup

1. **Requirements:**
    - Python 3.x
    - MongoDB

2. **Installation:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Variables:**

    Create a `.env` file in the project directory with the following content:

    ```
    MONGODB_URI=<your_mongodb_connection_uri>
    ```

## Usage

1. **Uploading a Video:**

    - **Endpoint:** `POST /api/upload`
    - **Request:**
        - `file`: Video file to be uploaded
    - **Response:**
        - `id`: Unique identifier for the uploaded video
        - `filename`: Original filename of the uploaded video
        - `created_time`: Timestamp when the video was uploaded (ISO format)
        - `url`: Streaming URL for the video
        - `transcription`: Array of transcription objects (limited to the first 3 timestamps)

2. **Streaming a Video:**

    - **Endpoint:** `GET /api/videos/<video_id>/stream`
    - **Response:**
        - Streamed video file (video/mp4)

3. **Getting Transcription:**

    - **Endpoint:** `GET /api/transcription/<video_id>`
    - **Response:**
        - `video_id`: Identifier for the video
        - `transcription`: Array of transcription objects

4. **Getting List of Videos:**

    - **Endpoint:** `GET /api/videos`
    - **Response:**
        - `video_files`: Array of video objects containing `id`, `filename`, `created_time`, and `stream_url`

## How to Run

```bash
python app.py
```

The API server will start at `http://localhost:5000`.

## Additional Notes

- Videos are processed to extract audio and generate transcriptions.
- Videos are compressed to fit within a specified size limit (25MB).
- Transcriptions are generated every 15 seconds and associated with corresponding timestamps.

---
