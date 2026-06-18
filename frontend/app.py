import streamlit as st
import requests

st.set_page_config(
    page_title="Vestaff RAG Assistant",
    page_icon="🤖"
)

st.title("📄 AWS Customer Agreement Assistant")

query = st.text_input(
    "Ask a question about the AWS Customer Agreement"
)

if st.button("Ask"):

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={
            "query": query
        }
    )

    result = response.json()

    st.subheader("Answer")

    st.write(result["answer"])

    st.subheader("Source")

    st.write(result["source"])

    st.metric(
        "Latency (ms)",
        result["latency_ms"]
    )
st.divider()

st.header("📊 Analytics")

if st.button("Load Analytics"):

    analytics = requests.get(
        "http://127.0.0.1:8000/analytics"
    ).json()

    st.metric(
        "Total Queries",
        analytics["total_queries"]
    )

    st.metric(
        "Unanswered Queries",
        analytics["unanswered_queries"]
    )

    st.metric(
        "Average Latency (ms)",
        analytics["average_latency_ms"]
    )

    st.subheader(
        "Most Frequent Questions"
    )

    st.table(
        analytics["most_frequent_questions"]
    )