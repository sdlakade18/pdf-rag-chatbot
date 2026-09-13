import streamlit as st
import requests


st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄"
)

st.title("📄 PDF RAG Chatbot")

st.write(
    "Upload a PDF and ask questions about its content."
)


BACKEND_URL = "http://127.0.0.1:8000"


uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(f"Selected: {uploaded_file.name}")

    if st.button("Upload PDF"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        response = requests.post(
            f"{BACKEND_URL}/documents/upload",
            files=files
        )

        if response.status_code == 200:

            result = response.json()
            st.session_state["document_id"] = result["document_id"]
            st.success("PDF processed successfully!")

            st.write(
                f"Chunks stored: {result['chunks_stored']}"
            )

        else:
            st.error(
                f"Upload failed: {response.text}"
            )


st.divider()

st.subheader("💬 Ask about your document")

if "document_id" not in st.session_state:
    st.info("👆 Upload a PDF first to start asking questions.")

else:
    question = st.chat_input(
        "Ask a question about your PDF..."
    )

    if question:

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Searching the document and generating an answer..."):

                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    json={
                        "question": question,
                        "document_id": st.session_state["document_id"]
                    }
                )

            if response.status_code == 200:

                result = response.json()

                st.write(result["answer"])

                with st.expander("📚 Sources"):
                    for source in result["sources"]:
                        st.write(
                            f"📄 Page {source['page_number']} "
                            f"• Chunk {source['chunk_id']}"
                        )

            else:
                st.error(
                    f"Question failed: {response.text}"
                )