from google.adk.agents import Agent
from google.cloud import videointelligence_v1 as vi
from typing import Dict
import base64
import os

def analyze_test_video(_: str = "") -> Dict:
    """
    Analyzes the test video located in resources/testVideo.mp4 using Google Cloud Video Intelligence API.
    Detects activities like crowd movement, fire, smoke, etc.
    """

    try:
        video_path = os.path.join(os.path.dirname(__file__), "..", "resources", "testVideo1.mp4")
        video_path = os.path.abspath(video_path)

        if not os.path.exists(video_path):
            return {"status": "error", "error_message": f"Video not found at {video_path}"}

        with open(video_path, "rb") as f:
            video_bytes = f.read()

        client = vi.VideoIntelligenceServiceClient()
        features = [vi.Feature.LABEL_DETECTION,vi.Feature.OBJECT_TRACKING]

        operation = client.annotate_video(
            request={"features": features, "input_content": video_bytes}
        )

        result = operation.result(timeout=300)
        annotations = result.annotation_results[0].segment_label_annotations

        report = []
        for label in annotations:
            description = label.entity.description
            for segment in label.segments:
                start = segment.segment.start_time_offset.total_seconds()
                end = segment.segment.end_time_offset.total_seconds()
                confidence = segment.confidence
                print(f"{start} {end} {confidence}")

                if confidence > 0.3:
                    report.append(
                        f"Detected '{description}' from {start:.2f}s to {end:.2f}s (confidence: {confidence:.2f})"
                    )

        if not report:
            report = ["✅ No high-confidence events detected in this video."]
            summary = report[0]
        else:
            summary = f"{len(report)} event(s) detected with confidence > 0.6."

        return {
            "status": "success",
            "summary": summary,
            "report": report
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


video_analysis_agent = Agent(
    name="video_analysis_agent",
    model="gemini-2.0-flash",
    description="Analyzes crowd situations and security threats from CCTV footage using Google Video Intelligence API.",
    instruction="Use this agent to analyze the test video file for crowd, fire, or anomalies.",
    tools=[analyze_test_video],
)
