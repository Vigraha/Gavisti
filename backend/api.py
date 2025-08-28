from flask import Flask, render_template, Response, request
import cv2
import threading
from Yolo import process_video_stream # Import the function from your main script

app = Flask(__name__)

@app.route('/')
def index():
    """
    The main route that renders the HTML template.
    """
    user_agent = request.headers.get('User-Agent', '').lower()
    is_pyqt = 'qtwebengine' in user_agent
    return render_template('index.html', show_heading=not is_pyqt)

def generate_frames():
    """
    A generator function that yields frames for the web stream.
    """
    while True:
        # Get the processed frame from the main script's function
        frame = process_video_stream()
        if frame is None:
            continue

        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame in a multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """
    The route that provides the video stream.
    """
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Start the Flask web server
    app.run(host='0.0.0.0', port=5000, debug=False)

# from fastapi import FastAPI, Request
# from fastapi.responses import StreamingResponse, HTMLResponse
# from fastapi.templating import Jinja2Templates
# import cv2
#
# from Yolo import process_video_stream  # Your frame processor
#
# app = FastAPI()
# templates = Jinja2Templates(directory="templates")
#
# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     """
#     Renders the HTML template.
#     """
#     return templates.TemplateResponse("index.html", {"request": request})
#
# def generate_frames():
#     """
#     Yields frames for the video stream.
#     """
#     while True:
#         frame = process_video_stream()
#         if frame is None:
#             continue
#
#         # Encode frame as JPEG
#         ret, buffer = cv2.imencode('.jpg', frame)
#         if not ret:
#             continue
#         frame_bytes = buffer.tobytes()
#
#         # Yield multipart HTTP response
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
#
# @app.get("/video_feed")
# def video_feed():
#     """
#     Streams the video frames.
#     """
#     return StreamingResponse(generate_frames(),
#                               media_type='multipart/x-mixed-replace; boundary=frame')
