import streamlit as st

from verifier import verify_claim
from media_analyzer import analyze_image
from media_analyzer import analyze_video


st.set_page_config(
    page_title="TrustLens",
    page_icon="🔍",
    layout="wide"
)


st.title("🔍 TrustLens")

st.markdown(
    "### Don't just trust it. Verify it."
)

st.write(
    "AI-powered digital content verification using "
    "Gemini and live web evidence."
)


tab_text, tab_image, tab_link, tab_video = st.tabs(
    [
        "📝 Text",
        "📷 Screenshot",
        "🔗 Link",
        "🎥 Video"
    ]
)


def show_result(result):

    status = result.get(
        "status",
        "Verification Needed"
    )

    if status == "Strongly Supported":
        st.success("🟢 STRONGLY SUPPORTED")

    elif status == "Contradicted":
        st.error("🔴 CONTRADICTED")

    elif status == "No Reliable Evidence Found":
        st.info("⚪ NO RELIABLE EVIDENCE FOUND")

    else:
        st.warning("🟡 VERIFICATION NEEDED")

    st.subheader("Claim")
    st.write(result.get("claim", ""))

    st.subheader("Why?")
    st.write(result.get("why", ""))

    st.subheader("Evidence")
    st.write(result.get("evidence_summary", ""))

    st.subheader("Same / Similar Information")

    similar = result.get(
        "same_similar_information",
        []
    )

    if similar:
        for item in similar:
            st.write("• " + item)
    else:
        st.write("No similar information identified.")

    st.subheader("Conflicting Information")

    conflicts = result.get(
        "conflicts",
        []
    )

    if conflicts:
        for item in conflicts:
            st.warning(item)
    else:
        st.write("No significant conflict identified.")

    st.subheader("Sources")

    sources = result.get(
        "sources",
        []
    )

    for source in sources:

        title = source.get(
            "title",
            "Source"
        )

        url = source.get(
            "url",
            ""
        )

        if url:
            st.markdown(
                f"- [{title}]({url})"
            )


# -----------------------------
# TEXT TAB
# -----------------------------

with tab_text:

    st.subheader("Verify a claim")

    text_input = st.text_area(
        "Paste the text or claim here",
        height=180,
        placeholder=(
            "Example: Government announced..."
        )
    )

    if st.button(
        "🔍 Verify Text",
        key="verify_text"
    ):

        if not text_input.strip():

            st.warning(
                "Please enter some text first."
            )

        else:

            with st.spinner(
                "Analyzing claim and searching for evidence..."
            ):

                try:

                    result = verify_claim(
                        text_input
                    )

                    show_result(result)

                except Exception as error:

                    st.error(
                        f"Something went wrong: {error}"
                    )


# -----------------------------
# IMAGE TAB
# -----------------------------

with tab_image:

    st.subheader("Verify a screenshot or image")

    image_file = st.file_uploader(
        "Upload an image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp"
        ],
        key="image_upload"
    )

    if image_file:

        st.image(
            image_file,
            caption="Uploaded image",
            use_container_width=True
        )

        if st.button(
            "🔍 Analyze Screenshot",
            key="verify_image"
        ):

            with st.spinner(
                "Reading and analyzing the image..."
            ):

                try:

                    image_bytes = image_file.getvalue()

                    analysis = analyze_image(
                        image_bytes,
                        image_file.type
                    )

                    st.subheader(
                        "Extracted Information"
                    )

                    st.write(
                        analysis.get(
                            "extracted_text",
                            ""
                        )
                    )

                    claim = analysis.get(
                        "claim",
                        ""
                    )

                    st.subheader("Detected Claim")

                    st.write(claim)

                    if claim:

                        st.divider()

                        with st.spinner(
                            "Searching for independent evidence..."
                        ):

                            result = verify_claim(
                                claim
                            )

                            show_result(result)

                except Exception as error:

                    st.error(
                        f"Something went wrong: {error}"
                    )


# -----------------------------
# LINK TAB
# -----------------------------

with tab_link:

    st.subheader("Verify a web link")

    url_input = st.text_input(
        "Paste a public URL",
        placeholder="https://example.com/article"
    )

    if st.button(
        "🔍 Verify Link",
        key="verify_link"
    ):

        if not url_input.strip():

            st.warning(
                "Please enter a URL."
            )

        else:

            with st.spinner(
                "Searching for information about this link..."
            ):

                try:

                    result = verify_claim(
                        url_input
                    )

                    show_result(result)

                except Exception as error:

                    st.error(
                        f"Something went wrong: {error}"
                    )


# -----------------------------
# VIDEO TAB
# -----------------------------

with tab_video:
    st.subheader("Analyze a video")

    st.info(
        "Upload a video to check its content and identify "
        "observable signs of possible digital manipulation."
    )

    video_file = st.file_uploader(
        "Upload a video",
        type=["mp4", "mov", "webm"],
        key="video_upload"
    )

    if video_file:
        st.video(video_file)

        if st.button("🔍 Analyze Video", key="analyze_video"):
            with st.spinner(
                "Uploading video and analyzing it with Gemini..."
            ):
                try:
                    video_bytes = video_file.getvalue()

                    analysis = analyze_video(
                        video_bytes,
                        video_file.type
                    )

                    st.subheader("🎥 Video Analysis")

                    st.write(analysis)

                except Exception as error:
                    st.error(
                        f"Something went wrong: {error}"
                    )