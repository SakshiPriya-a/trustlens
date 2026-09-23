import requests
import streamlit as st
import base64
import time


MODEL = "gemini-3.5-flash"


def get_gemini_key():
    return st.secrets["GEMINI_API_KEY"]


def gemini_generate(prompt, image_bytes=None, image_mime=None):
    api_key = get_gemini_key()

    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/{MODEL}:generateContent"
    )

    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }

    parts = []

    if prompt:
        parts.append({"text": prompt})

    if image_bytes and image_mime:
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        parts.append({
            "inline_data": {
                "mime_type": image_mime,
                "data": encoded_image
            }
        })

    payload = {
        "contents": [
            {
                "parts": parts
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(
            f"Gemini API error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return str(data)


def gemini_analyze_video(video_bytes, video_mime, prompt):
    api_key = get_gemini_key()

    # Step 1: Start resumable upload
    upload_url = (
        "https://generativelanguage.googleapis.com/"
        "upload/v1beta/files"
    )

    start_headers = {
        "x-goog-api-key": api_key,
        "X-Goog-Upload-Protocol": "resumable",
        "X-Goog-Upload-Command": "start",
        "X-Goog-Upload-Header-Content-Length": str(len(video_bytes)),
        "X-Goog-Upload-Header-Content-Type": video_mime,
        "Content-Type": "application/json",
    }

    metadata = {
        "file": {
            "display_name": "trustlens_video"
        }
    }

    start_response = requests.post(
        upload_url,
        headers=start_headers,
        json=metadata,
        timeout=60
    )

    if start_response.status_code not in [200, 201]:
        raise Exception(
            f"Gemini upload session error "
            f"{start_response.status_code}: "
            f"{start_response.text}"
        )

    session_url = start_response.headers.get(
        "X-Goog-Upload-URL"
    )

    if not session_url:
        raise Exception(
            "Gemini did not return an upload session URL."
        )

    # Step 2: Upload video bytes
    upload_headers = {
        "Content-Length": str(len(video_bytes)),
        "X-Goog-Upload-Offset": "0",
        "X-Goog-Upload-Command": "upload, finalize",
    }

    upload_response = requests.post(
        session_url,
        headers=upload_headers,
        data=video_bytes,
        timeout=180
    )

    if upload_response.status_code not in [200, 201]:
        raise Exception(
            f"Gemini video upload error "
            f"{upload_response.status_code}: "
            f"{upload_response.text}"
        )

    file_data = upload_response.json()["file"]

    file_name = file_data["name"]

    # Step 3: Wait for video processing
    while True:

        status_url = (
            f"https://generativelanguage.googleapis.com/"
            f"v1beta/{file_name}"
        )

        status_response = requests.get(
            status_url,
            headers={
                "x-goog-api-key": api_key
            },
            timeout=60
        )

        if status_response.status_code != 200:
            raise Exception(
                f"Gemini file status error "
                f"{status_response.status_code}: "
                f"{status_response.text}"
            )

        status_data = status_response.json()
        state = status_data.get("state")

        if state == "ACTIVE":
            break

        if state == "FAILED":
            raise Exception(
                "Gemini failed to process the video."
            )

        time.sleep(3)

    # Step 4: Analyze the video
    generate_url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/{MODEL}:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    },
                    {
                        "file_data": {
                            "mime_type": video_mime,
                            "file_uri": file_data["uri"]
                        }
                    }
                ]
            }
        ]
    }

    generate_response = requests.post(
        generate_url,
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=180
    )

    if generate_response.status_code != 200:
        raise Exception(
            f"Gemini video analysis error "
            f"{generate_response.status_code}: "
            f"{generate_response.text}"
        )

    data = generate_response.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return str(data)