import base64
from pathlib import Path

import ollama


def vision_agent(image_path):

    print("\n" + "=" * 60)
    print("VISION AGENT")
    print("=" * 60)

    image = Path(image_path)

    if not image.exists():
        print(f"\nImage not found: {image_path}")

        return {
            "image": image_path,
            "inspection_type": "solar_panel_inspection",
            "anomaly_detected": False,
            "anomaly_type": "image_not_found",
            "confidence": 0.0,
            "description": "Image not found."
        }

    print(f"\nImage found: {image.resolve()}")
    print("Sending image to Qwen2.5-VL...")

    try:

        response = ollama.chat(
            model="qwen2.5vl:3b",
            messages=[
                {
                    "role": "user",
                    "content": """
Analyze this drone inspection image.

Tell me:
1. What is visible in the image?
2. Is there a visible anomaly?
3. What type of anomaly is present?
4. Give a confidence percentage.

Only describe what you can actually see.
""",
                    "images": [
                        str(image)
                    ]
                }
            ]
        )

        answer = response["message"]["content"]

        print("\n" + "=" * 60)
        print("QWEN VISION RESPONSE")
        print("=" * 60)

        print(answer)

        # Simple anomaly detection
        lower_answer = answer.lower()

        anomaly_detected = (
            "anomaly" in lower_answer
            and "no anomaly" not in lower_answer
            and "no visible anomaly" not in lower_answer
        )

        result = {
            "image": image_path,
            "inspection_type": "solar_panel_inspection",
            "anomaly_detected": anomaly_detected,
            "anomaly_type": "visual_anomaly" if anomaly_detected else "none",
            "confidence": 0.0,
            "description": answer
        }

        print("\n" + "=" * 60)
        print("VISION ANALYSIS COMPLETE")
        print("=" * 60)

        print(f"Anomaly Detected: {result['anomaly_detected']}")
        print(f"Anomaly Type: {result['anomaly_type']}")

        return result

    except Exception as error:

        print("\nVISION MODEL ERROR:")
        print(error)

        return {
            "image": image_path,
            "inspection_type": "solar_panel_inspection",
            "anomaly_detected": False,
            "anomaly_type": "analysis_error",
            "confidence": 0.0,
            "description": str(error)
        }


if __name__ == "__main__":

    result = vision_agent(
        "data/images/sample_drone_image.png"
    )

    print("\n" + "=" * 60)
    print("VISION TEST COMPLETE")
    print("=" * 60)

    print(result)