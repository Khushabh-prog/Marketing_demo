import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path

from data.generate_data import generate_marketing_data

st.set_page_config(
    page_title="Agentic Campaign Optimization Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path("data/marketing_campaigns.xlsx")


def add_global_styles():
    st.markdown(
        """
        <style>
        .stApp { background: #f4f7fb; }
        .reportview-container .main .block-container { padding-top: 1rem; padding-bottom: 1.5rem; }
        .css-1d391kg { padding-top: 0; }
        section[data-testid="stSidebar"] { background: #ffffffcc; border-right: 1px solid rgba(15, 23, 42, 0.08); }
        .metric-card { border-radius: 20px; background: rgba(255,255,255,0.95); box-shadow: 0 20px 45px rgba(15, 23, 42, 0.08); padding: 22px 18px; }
        .section-heading { font-size: 1.1rem; letter-spacing: 0.02em; color: #334155; margin-bottom: 4px; }
        .section-subtitle { color: #475569; margin-top: 0; margin-bottom: 12px; }
        .chart-box { border-radius: 20px; background: #ffffff; padding: 16px; box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06); }
        .sidebar-box { border-radius: 18px; padding: 18px; background: linear-gradient(180deg, #0c4a6e 0%, #0e7490 100%); color: white; margin-bottom: 18px; }
        .sidebar-step { margin: 0 0 8px 0; }
        .sidebar-step strong { color: #e2e8f0; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div style='padding:24px 28px; border-radius:24px; background: linear-gradient(135deg, #0c4a6e 0%, #0e7490 100%); color:white; box-shadow: 0 20px 55px rgba(15, 23, 42, 0.12);'>
            <h1 style='margin:0; font-size:2.3rem;'>{title}</h1>
            <p style='margin:8px 0 0; font-size:1rem; opacity:.88; line-height:1.6;'>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

@st.cache_data(show_spinner=False)
def load_data():
    df = generate_marketing_data(n_rows=500, export_path=DATA_PATH)
    return df


def render_sidebar():
    st.sidebar.markdown(
        """
        <div class='sidebar-box'>
            <h2 style='margin:0 0 6px 0;'>Agentic Campaign Engine</h2>
            <p style='margin:0 0 12px 0; opacity:0.88;'>A hands-on marketing workshop experience for AI-powered campaign optimization.</p>
            <p class='sidebar-step'><strong>1.</strong> Monitor performance in real time</p>
            <p class='sidebar-step'><strong>2.</strong> Detect anomalies and weak segments</p>
            <p class='sidebar-step'><strong>3.</strong> Optimize creative with AI-driven insights</p>
            <p class='sidebar-step'><strong>4.</strong> Reallocate budget for lift</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def campaign_dashboard(df):
    render_page_header(
        "Campaign Dashboard",
        "A polished executive view of campaign performance, powered by the agent's monitoring insights.",
    )

    add_global_styles()

    with st.expander("What the agent is watching", expanded=True):
        st.write(
            "This dashboard visualizes spend efficiency, conversion strength, and channel performance so the AI agent can detect trends and anomalies quickly."
        )

    platform_filter = st.multiselect(
        "Filter by platform",
        options=sorted(df["Platform"].unique()),
        default=sorted(df["Platform"].unique()),
    )
    audience_filter = st.multiselect(
        "Filter by audience segment",
        options=sorted(df["Audience Segment"].unique()),
        default=sorted(df["Audience Segment"].unique()),
    )

    filtered_df = df[
        df["Platform"].isin(platform_filter) & df["Audience Segment"].isin(audience_filter)
    ]

    total_spend = filtered_df["Spend ($)"].sum()
    total_conversions = filtered_df["Conversions"].sum()
    avg_cpa = filtered_df["CPA"].mean()
    avg_roas = filtered_df["ROAS"].mean()

    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    metrics_col1.markdown("<div class='metric-card'><h4 class='section-heading'>Total Spend</h4><p class='section-subtitle'>Overall budget committed today</p><h2>${:,.0f}</h2></div>".format(total_spend), unsafe_allow_html=True)
    metrics_col2.markdown("<div class='metric-card'><h4 class='section-heading'>Total Conversions</h4><p class='section-subtitle'>Conversions generated across campaigns</p><h2>{:,}</h2></div>".format(total_conversions), unsafe_allow_html=True)
    metrics_col3.markdown("<div class='metric-card'><h4 class='section-heading'>Average CPA</h4><p class='section-subtitle'>Cost per acquisition across the filtered set</p><h2>${:.2f}</h2></div>".format(avg_cpa), unsafe_allow_html=True)
    metrics_col4.markdown("<div class='metric-card'><h4 class='section-heading'>Average ROAS</h4><p class='section-subtitle'>Return on ad spend expectation</p><h2>{:.2f}</h2></div>".format(avg_roas), unsafe_allow_html=True)

    st.markdown("---")

    chart_data = filtered_df.groupby(["Platform", "Audience Segment"]).agg(
        spend=("Spend ($)", "sum"),
        conversions=("Conversions", "sum"),
        clicks=("Clicks", "sum"),
        impressions=("Impressions", "sum"),
        avg_cpa=("CPA", "mean"),
        avg_roas=("ROAS", "mean"),
    ).reset_index()
    chart_data["CTR"] = chart_data["clicks"] / chart_data["impressions"]

    fig_spend_conv = px.scatter(
        chart_data,
        x="spend",
        y="conversions",
        color="Platform",
        size="avg_roas",
        hover_data=["Audience Segment", "avg_cpa", "CTR"],
        title="Spend vs Conversions by Segment",
        labels={"spend": "Spend ($)", "conversions": "Conversions", "avg_roas": "Avg ROAS"},
        height=420,
    )
    fig_spend_conv.update_traces(marker=dict(opacity=0.84, line=dict(width=1, color="DarkSlateGrey")))
    fig_spend_conv.update_layout(template="plotly_white")

    fig_cpa_platform = px.bar(
        chart_data.groupby("Platform")["avg_cpa"].mean().reset_index(),
        x="Platform",
        y="avg_cpa",
        title="Average CPA by Platform",
        color="Platform",
        labels={"avg_cpa": "Average CPA"},
        height=420,
    )
    fig_cpa_platform.update_layout(template="plotly_white")

    fig_roas_platform = px.bar(
        chart_data.groupby("Platform")["avg_roas"].mean().reset_index(),
        x="Platform",
        y="avg_roas",
        title="Average ROAS by Platform",
        color="Platform",
        labels={"avg_roas": "Average ROAS"},
        height=420,
    )
    fig_roas_platform.update_layout(template="plotly_white")

    top_segments = chart_data.sort_values(by="conversions", ascending=False).head(8)
    fig_top_segments = px.bar(
        top_segments,
        x="conversions",
        y="Audience Segment",
        color="Platform",
        orientation="h",
        title="Top Performing Segments by Conversions",
        labels={"conversions": "Conversions", "Audience Segment": "Audience Segment"},
        height=420,
    )
    fig_top_segments.update_layout(template="plotly_white")

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown("<div class='chart-box'></div>", unsafe_allow_html=True)
        st.plotly_chart(fig_spend_conv, use_container_width=True)
    with row1_col2:
        st.markdown("<div class='chart-box'></div>", unsafe_allow_html=True)
        st.plotly_chart(fig_cpa_platform, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown("<div class='chart-box'></div>", unsafe_allow_html=True)
        st.plotly_chart(fig_roas_platform, use_container_width=True)
    with row2_col2:
        st.markdown("<div class='chart-box'></div>", unsafe_allow_html=True)
        st.plotly_chart(fig_top_segments, use_container_width=True)

    st.markdown("#### Raw campaign snapshot")
    st.dataframe(filtered_df.head(10), use_container_width=True)


def anomaly_detection(df):
    render_page_header(
        "Anomaly Detection",
        "Visualize the segments the agent labels as high-risk and explore the anomalies that need immediate attention.",
    )

    underperformers = df[(df["CPA"] > 50) | (df["CTR"] < 0.005)].copy()
    underperformers = underperformers.sort_values(by=["CPA", "CTR"], ascending=[False, True])

    summary = underperformers.groupby("Audience Segment").agg(
        campaigns=("Campaign ID", "count"),
        avg_cpa=("CPA", "mean"),
        avg_ctr=("CTR", "mean"),
        total_spend=("Spend ($)", "sum"),
    ).reset_index()

    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    metrics_col1.markdown("<div class='metric-card'><h4 class='section-heading'>Flagged Segments</h4><h2>{}</h2></div>".format(summary["Audience Segment"].nunique()), unsafe_allow_html=True)
    metrics_col2.markdown("<div class='metric-card'><h4 class='section-heading'>Average CPA</h4><h2>${:.2f}</h2></div>".format(summary['avg_cpa'].mean()), unsafe_allow_html=True)
    metrics_col3.markdown("<div class='metric-card'><h4 class='section-heading'>Average CTR</h4><h2>{:.2%}</h2></div>".format(summary['avg_ctr'].mean()), unsafe_allow_html=True)

    st.markdown("---")
    chart_col1, chart_col2 = st.columns(2)
    fig_underperforming_cpa = px.bar(
        summary.sort_values("avg_cpa", ascending=False),
        x="Audience Segment",
        y="avg_cpa",
        color="campaigns",
        title="Flagged Segment Average CPA",
        labels={"avg_cpa": "Average CPA", "campaigns": "Campaign Count"},
        height=420,
    )
    fig_underperforming_cpa.update_layout(template="plotly_white")

    fig_underperforming_ctr = px.scatter(
        summary,
        x="avg_ctr",
        y="avg_cpa",
        color="Audience Segment",
        size="campaigns",
        title="CTR vs CPA for Underperforming Segments",
        labels={"avg_ctr": "Average CTR", "avg_cpa": "Average CPA"},
        height=420,
    )
    fig_underperforming_ctr.update_layout(xaxis_tickformat=".1%", template="plotly_white")

    chart_col1.plotly_chart(fig_underperforming_cpa, use_container_width=True)
    chart_col2.plotly_chart(fig_underperforming_ctr, use_container_width=True)

    st.markdown("#### Underperforming campaigns")
    st.dataframe(underperformers.reset_index(drop=True), use_container_width=True)

    if not underperformers.empty:
        worst = underperformers.iloc[0]
        st.markdown("### Worst Offender")
        st.info(
            f"Campaign `{worst['Campaign ID']}` on {worst['Platform']} targeting `{worst['Audience Segment']}` has CPA ${worst['CPA']:.2f} and CTR {worst['CTR']:.2%}."
        )


def creative_optimization(df):
    render_page_header(
        "Agentic Creative Optimization",
        "Guide the agent through creative testing and let it recommend new copy for the lowest-performing audiences.",
    )

    st.markdown(
        """
        The agent uses audience behavior and campaign efficiency signals to diagnose why the current messaging is failing and suggest targeted ad variations.
        """
    )

    underperforming_segments = (
        df.loc[(df["CPA"] > 50) | (df["CTR"] < 0.005), "Audience Segment"].unique().tolist()
    )
    segment_choice = st.selectbox("Choose an underperforming segment", underperforming_segments)

    if segment_choice:
        segment_summary = df.groupby("Audience Segment").agg(
            avg_cpa=("CPA", "mean"),
            avg_ctr=("CTR", "mean"),
            avg_roas=("ROAS", "mean"),
            conversions=("Conversions", "sum"),
            spend=("Spend ($)", "sum"),
        ).reset_index()
        selected_metrics = segment_summary[segment_summary["Audience Segment"] == segment_choice].iloc[0]
        overall_averages = segment_summary.mean(numeric_only=True)

        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        metrics_col1.metric("Segment CPA", f"${selected_metrics['avg_cpa']:.2f}")
        metrics_col2.metric("Segment CTR", f"{selected_metrics['avg_ctr']:.2%}")
        metrics_col3.metric("Segment ROAS", f"{selected_metrics['avg_roas']:.2f}")

        fig_segment_compare = px.bar(
            pd.melt(
                pd.DataFrame(
                    {
                        "Metric": ["CPA", "CTR", "ROAS"],
                        f"{segment_choice}": [selected_metrics["avg_cpa"], selected_metrics["avg_ctr"], selected_metrics["avg_roas"]],
                        "Overall Average": [overall_averages["avg_cpa"], overall_averages["avg_ctr"], overall_averages["avg_roas"]],
                    }
                ),
                id_vars="Metric",
                var_name="Type",
                value_name="Value",
            ),
            x="Metric",
            y="Value",
            color="Type",
            barmode="group",
            title=f"{segment_choice}: Creative Performance vs Average",
            height=420,
        )
        fig_segment_compare.update_layout(yaxis_title="Value")
        st.plotly_chart(fig_segment_compare, use_container_width=True)

        if st.button("Run AI Agent"):
            with st.spinner("Agent is analyzing the creative and audience..."):
                st.progress(0)
                for percent in [20, 50, 80, 100]:
                    st.progress(percent)

                st.success("Agent analysis complete")

                st.subheader("Agent analysis")
                st.markdown(
                    f"The agent finds that the current creative for **{segment_choice}** is not resonating because the messaging is too generic and does not reflect the segment's motivations. This segment needs sharper benefits, more trust signals, and a clearer call to action."
                )

                st.subheader("Suggested ad copy variants")
                variants = [
                    {
                        "headline": "Maximize Your ROI with Tailored Lead Gen Ads",
                        "text": "Reach high-intent buyers while staying efficient. Test this new creative that speaks directly to your audience's growth goals.",
                    },
                    {
                        "headline": f"Unlock Smarter Campaigns for {segment_choice}",
                        "text": "Personalized messaging and persuasive offers help this audience click more and convert faster. Optimize for relevance and urgency.",
                    },
                    {
                        "headline": "Boost Engagement with Clear, Benefit-Led Copy",
                        "text": "Use vivid language, social proof, and a strong call to action to improve CTR and lower CPA for this segment.",
                    },
                ]
                for idx, variant in enumerate(variants, start=1):
                    st.markdown(f"**Variant {idx}**")
                    st.markdown(f"- **Headline:** {variant['headline']}"
                                f"\n- **Primary Text:** {variant['text']}\n")
        else:
            st.info("Select a segment and click Run AI Agent to generate optimization recommendations.")
    else:
        st.warning("No underperforming segments available in the current dataset.")


def budget_reallocation(df):
    render_page_header(
        "Budget Reallocation Engine",
        "See how the agent reallocates spend from weak segments to top performers and projects the expected conversion upside.",
    )

    summary = df.groupby("Audience Segment").agg(
        spend=("Spend ($)", "sum"),
        conversions=("Conversions", "sum"),
        cpa=("CPA", "mean"),
    ).reset_index()
    top_segments = summary.nsmallest(3, "cpa")
    bottom_segments = summary.nlargest(3, "cpa")

    current_budget = summary.set_index("Audience Segment")["spend"]
    recommended_budget = current_budget.copy()
    shift_amount = recommended_budget[bottom_segments["Audience Segment"]].sum() * 0.2

    if not bottom_segments.empty:
        remove_each = shift_amount / len(bottom_segments)
        recommended_budget.loc[bottom_segments["Audience Segment"]] -= remove_each
        add_each = shift_amount / len(top_segments)
        recommended_budget.loc[top_segments["Audience Segment"]] += add_each

    current_total = current_budget.sum()
    projected_conversions = df["Conversions"].sum() * 1.08

    allocation_df = pd.DataFrame({
        "Audience Segment": current_budget.index,
        "Current Budget": current_budget.values,
        "Recommended Budget": recommended_budget.values,
    })

    fig_budget_alloc = px.bar(
        allocation_df.melt(id_vars="Audience Segment", value_vars=["Current Budget", "Recommended Budget"], var_name="Budget Type", value_name="Spend"),
        x="Audience Segment",
        y="Spend",
        color="Budget Type",
        barmode="group",
        title="Current vs Recommended Budget Allocation",
        height=450,
    )
    fig_budget_alloc.update_layout(template="plotly_white")

    fig_conversion_projection = px.line(
        pd.DataFrame(
            {
                "Scenario": ["Current", "Recommended"],
                "Projected Conversions": [df["Conversions"].sum(), projected_conversions],
            }
        ),
        x="Scenario",
        y="Projected Conversions",
        markers=True,
        title="Projected Conversion Impact",
        height=420,
    )
    fig_conversion_projection.update_layout(template="plotly_white")

    st.markdown("<div class='chart-box'></div>", unsafe_allow_html=True)
    st.plotly_chart(fig_budget_alloc, use_container_width=True)
    st.plotly_chart(fig_conversion_projection, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-card'><h4 class='section-heading'>Current Total Spend</h4><h2>${:,.0f}</h2></div>".format(current_total), unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'><h4 class='section-heading'>Projected Conversions</h4><h2>{:,.0f}</h2></div>".format(projected_conversions), unsafe_allow_html=True)

    st.markdown("---")
    data_col1, data_col2 = st.columns(2)
    with data_col1:
        st.subheader("Current Budget Allocation")
        st.dataframe(current_budget.sort_values(ascending=False).head(10).reset_index(), use_container_width=True)
    with data_col2:
        st.subheader("Agent Recommended Allocation")
        st.dataframe(recommended_budget.sort_values(ascending=False).head(10).reset_index(), use_container_width=True)


def main():
    add_global_styles()
    render_sidebar()
    df = load_data()

    page = st.sidebar.radio(
        "Select a page",
        [
            "Campaign Dashboard",
            "Anomaly Detection",
            "Agentic Creative Optimization",
            "Budget Reallocation Engine",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "This workshop app demonstrates how an AI agent can monitor campaign performance, detect problems, optimize creative, and reallocate budgets automatically."
    )
    st.sidebar.markdown(f"**Excel export:** `{DATA_PATH}`")

    if page == "Campaign Dashboard":
        campaign_dashboard(df)
    elif page == "Anomaly Detection":
        anomaly_detection(df)
    elif page == "Agentic Creative Optimization":
        creative_optimization(df)
    elif page == "Budget Reallocation Engine":
        budget_reallocation(df)


if __name__ == "__main__":
    main()
