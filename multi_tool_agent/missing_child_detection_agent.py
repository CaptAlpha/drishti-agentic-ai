# multi_tool_agent/missing_child_detection_agent.py

from google.adk.agents import Agent
from typing import Dict
import os
from google.cloud import vision
from google.cloud import videointelligence_v1 as vi
from PIL import Image
import io
import cv2
import tempfile


def extract_faces_from_image(image_bytes: bytes):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.face_detection(image=image)
    return response.face_annotations


def detect_faces_in_video(_: str = "") -> Dict:
    """
    Detects faces in a video and compares them with the provided missing child's image.
    """
    try:
        test_video_path = os.path.join(os.path.dirname(__file__), "..", "resources", "testVideo.mp4")
        missing_child_path = os.path.join(os.path.dirname(__file__), "..", "resources", "missing_child.jpg")

        if not os.path.exists(test_video_path):
            return {"status": "error", "error_message": f"Video not found at {test_video_path}"}

        if not os.path.exists(missing_child_path):
            return {"status": "error", "error_message": f"Missing child image not found at {missing_child_path}"}

        # Step 1: Extract faces from missing child image
        with open(missing_child_path, "rb") as f:
            missing_child_bytes = f.read()
        child_faces = extract_faces_from_image(missing_child_bytes)
        if not child_faces:
            return {"status": "error", "error_message": "No face detected in the missing child image."}

        # Step 2: Read video and extract frames
        video = cv2.VideoCapture(test_video_path)
        matched_frames = []
        frame_count = 0

        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % 15 != 0:
                continue  # Analyze every 15th frame for speed

            # Convert OpenCV frame (BGR) to JPEG bytes
            _, jpeg_bytes = cv2.imencode('.jpg', frame)
            image_bytes = jpeg_bytes.tobytes()

            faces = extract_faces_from_image(image_bytes)

            if not faces:
                continue

            # Matching logic (simplified via bounding box comparison)
            for child_face in child_faces:
                for detected_face in faces:
                    if abs(detected_face.bounding_poly.vertices[0].x - child_face.bounding_poly.vertices[0].x) < 10 and \
                       abs(detected_face.bounding_poly.vertices[0].y - child_face.bounding_poly.vertices[0].y) < 10:
                        matched_frames.append(frame_count)
                        break

        video.release()

        if matched_frames:
            return {
                "status": "success",
                "matches_found": True,
                "matched_frames": matched_frames,
                "message": f"Possible match found in frames: {matched_frames}"
            }
        else:
            return {
                "status": "success",
                "matches_found": False,
                "message": "No matching faces found in the video."
            }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


missing_child_detection_agent = Agent(
    name="missing_child_detection_agent",
    model="gemini-1.5-pro",
    description="Detects and matches missing child faces from CCTV video using Google Cloud Vision and Video Intelligence APIs.",
    instruction="Use this agent to locate a missing child from surveillance video feed by matching the input face.",
    tools=[detect_faces_in_video],
)
