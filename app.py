"""
Amazon Bedrock Agent Cost Calculator

An interactive Streamlit application for estimating the monthly cost
of running an Amazon Bedrock AgentCore chatbot.

Run with:
    streamlit run app.py
"""

import streamlit as st
from calculator.totals import calculate_total_costs
from pricing.aws_pricing import AWSPricingProvider
from ui.sidebar import render_sidebar
from ui.charts import render_pie_chart, render_bar_chart, render_monthly_vs_annual
from ui.tables import render_summary_cards, render_detailed_table, render_formula_view, render_scenarios


def main():
    st.set_page_config(
        page_title="Bedrock Agent Cost Calculator",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Amazon Bedrock Agent Cost Calculator")
    st.caption(
        "Estimate the monthly cost of running an Amazon Bedrock AgentCore chatbot. "
        "Adjust parameters in the sidebar to see how costs change."
    )

    # --- Sidebar inputs ---
    inputs = render_sidebar()

    # --- Calculate costs ---
    summary = calculate_total_costs(
        model_name=inputs["model_name"],
        sessions_per_month=inputs["sessions_per_month"],
        messages_per_session=inputs["messages_per_session"],
        input_tokens_per_message=inputs["input_tokens_per_message"],
        output_tokens_per_message=inputs["output_tokens_per_message"],
        kb_queries_per_message=inputs["kb_queries_per_message"],
        kb_size_gb=inputs["kb_size_gb"],
        crawl_frequency=inputs["crawl_frequency"],
        lambda_duration_seconds=inputs["lambda_duration_seconds"],
        lambda_memory_mb=inputs["lambda_memory_mb"],
        api_gateway_requests=inputs["api_gateway_requests"],
    )

    # --- Summary Cards ---
    render_summary_cards(summary)

    st.divider()

    # --- Charts ---
    col_left, col_right = st.columns(2)
    with col_left:
        render_pie_chart(summary)
    with col_right:
        render_bar_chart(summary)

    render_monthly_vs_annual(summary)

    st.divider()

    # --- Detailed Table ---
    st.subheader("Detailed Cost Breakdown")
    render_detailed_table(summary)

    st.divider()

    # --- Formula View ---
    st.subheader("Formula Details")
    st.caption("Expand each service to see calculation formulas and assumptions.")
    render_formula_view(summary)

    st.divider()

    # --- Scenarios ---
    render_scenarios(inputs)

    st.divider()

    # --- Assumptions Panel ---
    st.subheader("Assumptions")
    provider = AWSPricingProvider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Region:** {provider.REGION}")
    with col2:
        st.info(f"**Pricing Source:** {provider.PRICING_SOURCE}")
    with col3:
        st.info(f"**Last Updated:** {provider.LAST_UPDATED}")

    st.caption(
        "Prices are sourced from official AWS pricing pages "
        "([Bedrock](https://aws.amazon.com/bedrock/pricing/), "
        "[AgentCore](https://aws.amazon.com/bedrock/agentcore/pricing/), "
        "[Lambda](https://aws.amazon.com/lambda/pricing/), "
        "[API Gateway](https://aws.amazon.com/api-gateway/pricing/)). "
        "Actual costs may vary based on usage patterns, reserved capacity, and free tier eligibility."
    )


if __name__ == "__main__":
    main()
