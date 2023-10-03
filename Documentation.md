# API DOCUMENTATION

### 1. Upload a Video
- **Endpoint:** `/api/upload`
- **Method:** POST
- **Description:** Upload a video file for processing.
- **Curl:**
  ```bash
  curl -X POST -F "file=@path/to/your/video.mp4" https://chrome-ext-api.onrender.com/api/upload
  ```
- **Browser:** Not applicable (POST request).
-  **Response:**
  ```json
    [{"created_time":"2023-10-03 01:52:28",
      "filename":"017 When Should You Start Applying.mp4",
      "id":"2cc06ac8-ac68-4073-ba1c-10e9afa8278a",
      "message":"Video uploaded successfully and transcription started!",
      "task_id":"916c7f50-c7e5-4228-82d1-1962c1be984e",
      "url":"/api/videos/2cc06ac8-ac68-4073-ba1c-10e9afa8278a/stream"
      },
      202]

  ```

### 2. Stream a Video
- **Endpoint:** `/api/videos/<video_id>/stream`
  - E.g `https://chrome-ext-api.onrender.com/api/videos/2cc06ac8-ac68-4073-ba1c-10e9afa8278a/stream`
    - Note : This is a valid video id so you can copy to test
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
  - E.g `https://chrome-ext-api.onrender.com/api/transcription/2cc06ac8-ac68-4073-ba1c-10e9afa8278a`
    - Note : This is a valid video id so you can copy to test
- **Endpoint:** `/api/transcription/<video_id>`
- **Method:** GET
- **Description:** Retrieve transcription for a specific video by its ID.
- **Curl:**
  ```bash
  curl https://chrome-ext-api.onrender.com/api/transcription/<video_id>
  ```
- **Browser:**
  ```
  https://chrome-ext-api.onrender.com/api/transcription/<video_id>
  ```
-  **Response:**
```json
  {"transcription":[{"end_time":"0:00:15","start_time":"0:00:00","text":"when should I start applying for a job this is especially common for people who are looking for their first coding job because they're new they aren't sure how valuable their skills are and we all have heard of The Imposter syndrome where we think that everybody knows a lot more than us and that we are just an imposter pretending to be Engineers so I want to answer this question for you a short version and a long version short answer or when should you start applying is well now because you need to start looking at interviews not as a win or lose fail or pass rather as with anything it is a skill that you can improve and get better at each interview that you go to will make you a better interviewer practicing is the key here and the sooner you start interviewing the better now there's a catch here and we'll need to go into the longer answer for that one assessing Readiness is related to calculating the actual value and salary of a developer and that's tough to do when will you know that you're a front-end engineer or a back-end engineer most of the time you see on the job description items that you don't even know of or are not the master of or requiring way more experience or way more years of experience than you have first things first companies do this to filter out the week candidate as a matter of fact if you're applying to a job where you check all of the boxes and you know everything then that means you're getting a job where you already know what to do you won't grow in this world as much as tougher positions will you so you need to change your mindset here a job description is simply a guideline of what type of work you will be doing not what type of work have you done in the past with that said if you don't know how to code at all and you apply for a developer position well don't expect a positive result you need to have some fundamentals before you actually start applying luckily for you the criteria is very simple do you know the fundamental building blocks of computer science like data structures and algorithms like we're going to learn in the scores in your specific domain have you build some projects and can build something on your own other than a simple hello world project do you have one or two big projects using the related technologies that the job description has if that's the case well you should start applying your skills will continue to grow and I can count numerous times when people of my company got hired over people with more experience because hiring developers or Engineers is more than just technical knowledge once you meet a baseline that is the minimum requirement the rest comes down to non-technical parts of the interview again which we have a whole section on in this course so when should you apply now use it as practice just like with anything if you wait until you feel you're ready you're ready to Long remember this quote if you never asked the answer is always know so start applying now I'll see you in the next video bye-bye"},{"end_time":"0:00:30","start_time":"0:00:15",.....
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
- **Response**
```json
  [
    {
          "message":"Videos retrieved successfully",
          "video_files":[
                          {"created_time":"2023-10-03 01:52:28",
                          "filename":"tmpkv6y9jsl",
                          "id":"2cc06ac8-ac68-4073-ba1c-10e9afa8278a",
                          "stream_url":"/api/videos/2cc06ac8-ac68-4073-ba1c-10e9afa8278a/stream"
                          }
                          {"created_time":"2023-10-03 01:52:28",
                          "filename":"tmpkv6y9jsl",
                          "id":"2cc06ac8-ac68-4073-ba1c-10e9afa8278a",
                          "stream_url":"/api/videos/2cc06ac8-ac68-4073-ba1c-10e9afa8278a/stream"
                          }....
            ]}
              ,200]
```

### Get Video Details

Retrieve details of a specific video by its ID. `https://chrome-ext-api.onrender.com/api/videos/2cc06ac8-ac68-4073-ba1c-10e9afa8278a`

#### Endpoint

```
GET /api/videos/<string:video_id>
```

#### Parameters

- `video_id` (string, required): The unique identifier of the video.

#### Response

- **200 OK** - Video details retrieved successfully

  ```json
  {
    "message": "Video details retrieved successfully",
    "video_details": {
      "id": "string",
      "filename": "string",
      "created_time": "string (format: 'YYYY-MM-DD HH:MM:SS')",
      "stream_url": "string (URL to stream the video)",
      "transcript_url": "string (URL to view the video's transcript)"
    }
  }
  ```

- **404 Not Found** - Video not found

  ```json
  {
    "error": "Video not found"
  }
  ```

#### Example

**Request**

```
GET /api/videos/cbea7e84-c10a-41c2-870c-fcfeecaa7ac0
```

**Response**

```json
{
  "message": "Video details retrieved successfully",
  "video_details": {
    "id": "cbea7e84-c10a-41c2-870c-fcfeecaa7ac0",
    "filename": "example_video.mp4",
    "created_time": "2023-10-01 14:30:45",
    "stream_url": "/api/videos/cbea7e84-c10a-41c2-870c-fcfeecaa7ac0/stream",
    "transcript_url": "/api/transcription/cbea7e84-c10a-41c2-870c-fcfeecaa7ac0"
  }
}
```

Note:
- Replace `<video_id>` in the endpoints with the actual video ID you want to interact with.
- For `curl` commands, replace `"path/to/your/video.mp4"` with the actual path to the video file you want to upload.
