import streamlit as st
@st.cache_data
def cached_split_sentences(text):

    return split_sentences(text)
from functools import lru_cache

from services.progress_service import (
    load_progress,
    save_progress
)

from readers.txt_reader import read_txt
from readers.docx_reader import read_docx
from readers.pdf_reader import read_pdf
from readers.epub_reader import read_epub

from services.sentence_service import split_sentences
from services.pinyin_service import get_pinyin
from services.translator_service import translate_to_vi
@st.cache_data
def cached_translate(text):

    return translate_to_vi(text)

from services.tts_service import (
    create_audio
)

import asyncio


# =====================
# CẤU HÌNH TRANG
# =====================

st.set_page_config(
    page_title="Chinese Reader Pro",
    page_icon="📖"
)

# =====================
# GIAO DIỆN
# =====================
st.title(
    "📖 Chinese Reader Pro"
)

st.caption(
    "Trần Lê Dũng VSIC"
)
st.markdown("""
<style>
[data-testid="stFileUploaderFileName"] {
    max-width: none !important;
}
</style>
""", unsafe_allow_html=True)

if "uploader_label" not in st.session_state:

    st.session_state.uploader_label = "Chọn sách"

uploaded_file = st.file_uploader(

    st.session_state.uploader_label,

    type=["txt", "docx", "pdf", "epub"]

)


# =====================
# KHI ĐÃ CHỌN FILE
# =====================

if uploaded_file:
    file_name = uploaded_file.name
    st.session_state.uploader_label = (
    f"📖 Đang mở: {file_name}"
    )

    extension = uploaded_file.name.split(".")[-1].lower()

    if extension == "txt":

        text = read_txt(uploaded_file)

    elif extension == "docx":

        text = read_docx(uploaded_file)

    elif extension == "pdf":

        text = read_pdf(uploaded_file)

    elif extension == "epub":

        text = read_epub(uploaded_file)

    else:

        st.error(
            "Định dạng chưa hỗ trợ"
        )

        st.stop()

    sentences = cached_split_sentences(text)
    
    progress_data = load_progress()



    @st.cache_data
    def cached_text_processing(text):

        return split_sentences(text)


    if len(sentences) == 0:

        st.error(
            "Không tìm thấy câu nào."
        )

        st.stop()

    if "current_index" not in st.session_state:

        st.session_state.current_index = (
            progress_data.get(
                file_name,
                0
            )
        )
    if (
        st.session_state.current_index
        >= len(sentences)
    ):

        st.session_state.current_index = 0




    # Chống lỗi IndexError

    if (
        st.session_state.current_index
        >= len(sentences)
    ):

        st.session_state.current_index = 0




    current_sentence = sentences[
        st.session_state.current_index
    ]

    progress_data[file_name] = (
        st.session_state.current_index
    )

    save_progress(
        progress_data
    )


    st.divider()
    

    st.markdown(
        f"**🇨🇳 Tiếng Trung:**  \n{current_sentence}"
    )

    st.markdown(
        f"**🔤 Pinyin:**  \n{get_pinyin(current_sentence)}"
    )


    if st.button(
        "🌐 Dịch câu này"
    ):

        translation = translate_to_vi(
            current_sentence
        )

        st.session_state.translation = translation


    if "translation" in st.session_state:

        st.write(
            st.session_state.translation
        )


    st.divider()

    config_col1, config_col2, config_col3, config_col4 = st.columns(4)

    with config_col1:

        speed_option = st.select_slider(

            "🎚 Tốc độ",

            options=[
                "-50%",
                "-25%",
                "0%",
                "+25%",
                "+50%"
            ],

            value="0%"

        )

    with config_col2:

        repeat_count = st.number_input(

            "🔁 Lặp",

            min_value=1,

            max_value=20,

            value=3,

            step=1

        )

    with config_col3:

        start_sentence = st.number_input(

            "🎧 Từ",

            min_value=1,

            max_value=len(sentences),

            value=1

        )

    with config_col4:

        end_sentence = st.number_input(

            "🎧 Đến",

            min_value=1,

            max_value=len(sentences),

            value=len(sentences)

        )

    speed_map = {

        "-50%": "-50%",

        "-25%": "-25%",

        "0%": "+0%",

        "+25%": "+25%",

        "+50%": "+50%"

    }

    if "preview_text" not in st.session_state:

        st.session_state.preview_text = ""

    if "sentence_audio_file" not in st.session_state:
        st.session_state.sentence_audio_file = None

    if st.button(
        "🎵 Tạo MP3 học tập"
    ):

        if start_sentence > end_sentence:

            st.error(
                "⚠ Câu bắt đầu phải nhỏ hơn hoặc bằng câu kết thúc"
            )

        else:
            st.write(
                f"start_sentence = {start_sentence}"
            )

            st.write(
                f"end_sentence = {end_sentence}"
            )                



            selected_sentences = sentences[
                start_sentence - 1:end_sentence
            ]

            st.write(
                f"Tổng số câu trong sentences: {len(sentences)}"
            )

            st.write(
                f"Số câu được chọn: {len(selected_sentences)}"
            )

            st.session_state.preview_text = "\n".join(
                selected_sentences
            )


    if st.session_state.preview_text:

        st.markdown("### PREVIEW MP3")

        st.code(
            st.session_state.preview_text,
            language=None
        )


        study_text = ""

        for sentence in st.session_state.preview_text.split("\n"):

            sentence = sentence.strip()

            if not sentence:
                continue

            study_text += (
                (sentence + "\n")
                * repeat_count
            )
        with st.spinner(
            "🎵 Đang tạo MP3 học tập..."
        ):        

            audio_file = asyncio.run(

                create_audio(

                    study_text,

                    rate=speed_map[speed_option]

                )

            )

        st.audio(
            audio_file
        )

        with open(
            audio_file,
            "rb"
        ) as file:

            study_col1, study_col2 = st.columns([2,1])

            with study_col1:

                st.download_button(
                    label="⬇ Tải MP3 học tập",
                    data=file,
                    file_name="study_lesson.mp3",
                    mime="audio/mpeg"
                )

            with study_col2:

                if st.button(
                    "❌ Đóng MP3 học tập"
                ):

                    st.session_state.preview_text = ""

                    st.rerun()
    st.divider()

    col1, col2, col3, col4 = st.columns([3,1.5,1.5,1.5])

    with col1:

        if st.button(
            "🔊 Đọc câu hiện tại"
        ):

            st.session_state.sentence_audio_file = asyncio.run(

                create_audio(

                    "\n".join(
                        [current_sentence]
                        * repeat_count
                    ),

                    rate=speed_map[speed_option]

                )

            )

            if st.session_state.sentence_audio_file:

                st.audio(
                    st.session_state.sentence_audio_file
                )

                with open(
                    st.session_state.sentence_audio_file,
                    "rb"
                ) as file:

                    sentence_col1 = st.container()

                    with sentence_col1:

                        st.download_button(
                            label="⬇ Tải MP3 câu hiện tại",
                            data=file,
                            file_name=f"sentence_{st.session_state.current_index+1}.mp3",
                            mime="audio/mpeg"
                        )


    with col2:

        if st.button("⬅ Câu trước"):

            if st.session_state.current_index > 0:

                st.session_state.current_index -= 1
                st.session_state.sentence_audio_file = None

                st.rerun()
    with col3:

        if st.button(
            "🔄 Về đầu sách"
        ):

            st.session_state.current_index = 0
            st.session_state.sentence_audio_file = None

            st.rerun()            

    with col4:

        if st.button("➡ Câu sau"):

            if (
                st.session_state.current_index
                < len(sentences) - 1
            ):

                st.session_state.current_index += 1
                st.session_state.sentence_audio_file = None

                st.rerun()

    st.write(

        f"Câu {st.session_state.current_index + 1} / {len(sentences)}"

    )
    progress_percent = (

        (st.session_state.current_index + 1)

        / len(sentences)

    )
    st.progress(
        progress_percent
    )
    st.write(

        f"{progress_percent * 100:.2f}%"

    )