"""
Sidebar UI component with all user input controls.
"""

import streamlit as st
from pricing.aws_pricing import AWSPricingProvider


def render_sidebar() -> dict:
    """
    Render the sidebar with sliders and dropdowns.
    Returns a dict of all user inputs.
    """
    provider = AWSPricingProvider()

    st.sidebar.header("Configuration")

    # --- Traffic ---
    st.sidebar.subheader("Traffic")

    sessions_per_month = st.sidebar.slider(
        "Sessions per month",
        min_value=0,
        max_value=10_000,
        value=1_000,
        step=100,
        help="Number of chat sessions per month",
    )

    messages_per_session = st.sidebar.slider(
        "Messages per session",
        min_value=1,
        max_value=25,
        value=3,
        step=1,
        help="Average messages exchanged per session",
    )

    kb_queries_per_message = st.sidebar.slider(
        "KB queries per message",
        min_value=0,
        max_value=5,
        value=1,
        step=1,
        help="Knowledge Base retrieval queries per message",
    )

    # --- LLM ---
    st.sidebar.subheader("LLM")

    model_name = st.sidebar.selectbox(
        "Model",
        options=provider.get_model_names(),
        index=1,  # Default to Nova Micro
        help="Foundation model for inference",
    )

    input_tokens_per_message = st.sidebar.slider(
        "Input tokens per message",
        min_value=50,
        max_value=5_000,
        value=500,
        step=50,
        help="Average input tokens (prompt) per message",
    )

    output_tokens_per_message = st.sidebar.slider(
        "Output tokens per message",
        min_value=50,
        max_value=10_000,
        value=200,
        step=50,
        help="Average output tokens (response) per message",
    )

    # --- Knowledge Base ---
    st.sidebar.subheader("Knowledge Base")

    kb_size_gb = st.sidebar.slider(
        "Knowledge Base size (GB)",
        min_value=0.5,
        max_value=100.0,
        value=5.0,
        step=0.5,
        help="Size of the knowledge base data",
    )

    crawl_frequency = st.sidebar.selectbox(
        "Crawl frequency",
        options=["Daily", "Weekly", "Monthly"],
        index=2,  # Default to Monthly
        help="How often the KB data source is synced",
    )

    st.sidebar.text("Embedding model: Titan Text Embedding V2")

    # --- Infrastructure ---
    st.sidebar.subheader("Infrastructure")

    st.sidebar.text(f"Lambda duration: ~10 seconds")
    st.sidebar.text(f"Lambda memory: ~256 MB")
    st.sidebar.text(f"API Gateway requests: ~3,000/month")

    lambda_duration_seconds = 10.0
    lambda_memory_mb = 256
    api_gateway_requests = 3_000

    return {
        "sessions_per_month": sessions_per_month,
        "messages_per_session": messages_per_session,
        "kb_queries_per_message": kb_queries_per_message,
        "model_name": model_name,
        "input_tokens_per_message": input_tokens_per_message,
        "output_tokens_per_message": output_tokens_per_message,
        "kb_size_gb": kb_size_gb,
        "crawl_frequency": crawl_frequency,
        "lambda_duration_seconds": lambda_duration_seconds,
        "lambda_memory_mb": lambda_memory_mb,
        "api_gateway_requests": api_gateway_requests,
    }
