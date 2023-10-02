# API DOCUMENTATION

### 1. Upload a Video
- **Endpoint:** `/api/upload`
- **Method:** POST
- **Description:** Upload a video file for processing.
- **Curl:**
  ```bash
  curl -X POST -F "file=@path/to/your/video.mp4" https://chrome-ext-api.onrender.com)/api/upload
  ```
- **Browser:** Not applicable (POST request).

### 2. Stream a Video
- **Endpoint:** `/api/videos/<video_id>/stream`
- **Method:** GET
- **Description:** Stream a specific video by its ID.
- **Curl:**
  ```bash
  curl https://chrome-ext-api.onrender.com/api/videos/<video_id>/stream
  ```
- **Browser:**
  ```
  https://chrome-ext-api.onrender.com/api/videos/<video_id>/stream 
  ```
  
### 3. Get Transcription for a Video
- **Endpoint:** `/api/transcription/<video_id>`
- **Method:** GET
- **Description:** Retrieve transcription for a specific video by its ID.
- **Curl:**
  ```bash
  curl https://chrome-ext-api.onrender.com/api/transcription/<video_id>
  ```
- **Browser:**
  ```
  https://chrome-ext-api.onrender.com)api/transcription/<video_id>
  ```

### 4. Get All Videos
- **Endpoint:** `/api/videos`
- **Method:** GET
- **Description:** Retrieve a list of all available videos.
- **Curl:**
  ```bash
  curl https://chrome-ext-api.onrender.com/api/videos
  ```
- **Browser:**
  ```
  https://chrome-ext-api.onrender.com/api/videos
  ```

Note:
- Replace `<video_id>` in the endpoints with the actual video ID you want to interact with.
- For `curl` commands, replace `"path/to/your/video.mp4"` with the actual path to the video file you want to upload.
