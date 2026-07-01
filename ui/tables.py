"""
Table and detail view components.
"""

import pandas as pd
import streamlit as st
from calculator.totals import CostSummary
from calculator.models import CostResult


def render_summary_cards(summary: CostSummary) -> None:
    """Render top-level summary metric cards."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Monthly Cost", f"${summary.monthly_total:.2f}")
    with col2:
        st.metric("Annual Cost", f"${summary.annual_total:.2f}")
    with col3:
        st.metric("Cost per Session", f"${summary.cost_per_session:.4f}")
    with col4:
        st.metric("Cost per Message", f"${summary.cost_per_message:.6f}")


def render_detailed_table(summary: CostSummary) -> None:
    """Render the detailed cost breakdown table."""
    rows = []
    for r in summary.all_results:
        rows.append({
            "Service": r.service,
            "Component": r.component,
            "Unit Price": r.unit_price,
            "Usage": r.usage,
            "Monthly ($)": f"${r.subtotal:.4f}",
        })

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )


def render_formula_view(summary: CostSummary) -> None:
    """Render expandable formula view for each cost component."""
    # Group by service
    services: dict[str, list[CostResult]] = {}
    for r in summary.all_results:
        services.setdefault(r.service, []).append(r)

    for service, results in services.items():
        with st.expander(f"{service} (${sum(r.subtotal for r in results):.4f}/month)"):
            for r in results:
                st.markdown(f"**{r.component}** — ${r.subtotal:.4f}")
                st.code(r.formula, language=None)
                if r.assumptions:
                    st.caption("Assumptions: " + " | ".join(r.assumptions))
                st.divider()


def render_scenarios(inputs: dict) -> list[dict]:
    """
    Render scenario comparison allowing users to see
    different cost projections based on varying inputs.
    """
    st.subheader("Scenarios")
    st.caption("Compare costs at different traffic levels.")

    from calculator.totals import calculate_total_costs

    scenarios = [
        {"label": "Low Traffic", "sessions_per_month": 100, "messages_per_session": 2},
        {"label": "Current", "sessions_per_month": inputs["sessions_per_month"], "messages_per_session": inputs["messages_per_session"]},
        {"label": "Growth (5x)", "sessions_per_month": min(inputs["sessions_per_month"] * 5, 10_000), "messages_per_session": inputs["messages_per_session"]},
        {"label": "Peak (10x)", "sessions_per_month": min(inputs["sessions_per_month"] * 10, 10_000), "messages_per_session": inputs["messages_per_session"]},
    ]

    rows = []
    for scenario in scenarios:
        summary = calculate_total_costs(
            model_name=inputs["model_name"],
            sessions_per_month=scenario["sessions_per_month"],
            messages_per_session=scenario["messages_per_session"],
            input_tokens_per_message=inputs["input_tokens_per_message"],
            output_tokens_per_message=inputs["output_tokens_per_message"],
            kb_queries_per_message=inputs["kb_queries_per_message"],
            kb_size_gb=inputs["kb_size_gb"],
            crawl_frequency=inputs["crawl_frequency"],
            lambda_duration_seconds=inputs["lambda_duration_seconds"],
            lambda_memory_mb=inputs["lambda_memory_mb"],
            api_gateway_requests=inputs["api_gateway_requests"],
        )
        rows.append({
            "Scenario": scenario["label"],
            "Sessions/mo": f"{scenario['sessions_per_month']:,}",
            "Msgs/session": scenario["messages_per_session"],
            "Monthly": f"${summary.monthly_total:.2f}",
            "Annual": f"${summary.annual_total:.2f}",
            "Per Session": f"${summary.cost_per_session:.4f}",
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    return rows
