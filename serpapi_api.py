import requests
import streamlit as st


def get_serpapi_key():
    return st.secrets["SERPAPI_KEY"]


def search_google(query, num_results=5):
    api_key = get_serpapi_key()

    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results,
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(
            f"SerpApi error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    results = []

    for item in data.get("organic_results", []):
        results.append({
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "link": item.get("link", ""),
            "source": item.get("source", ""),
        })

    return results


def search_news(query, num_results=5):
    api_key = get_serpapi_key()

    url = "https://serpapi.com/search"

    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key,
        "num": num_results,
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(
            f"SerpApi news error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    results = []

    for item in data.get("news_results", []):
        results.append({
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "link": item.get("link", ""),
            "source": item.get("source", ""),
            "date": item.get("date", ""),
        })

    return results


def search_youtube(query, num_results=5):
    api_key = get_serpapi_key()

    url = "https://serpapi.com/search"

    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": api_key,
        "num": num_results,
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(
            f"SerpApi YouTube error {response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    results = []

    for item in data.get("video_results", []):
        results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "channel": item.get("channel", ""),
            "description": item.get("description", ""),
        })

    return results