import streamlit as st
import plotly.express as px
import pandas as pd
from const import DATA, COLOR_CODES

st.set_page_config(layout="wide", page_title="Travel Booking Dashboard")

st.title("Channel Performance")

bar_chart1, bar_chart2 = st.columns(2)
_subset = DATA[(DATA["vehclass_id"] != "insurance")].copy()


df = (
    _subset.groupby(["channel", _subset["createdon"].dt.year.astype(str)])
    .agg(
        total_bookings=pd.NamedAgg(column="createdon", aggfunc="count"),
        total_sysfee=pd.NamedAgg(column="sysfee_total_usd", aggfunc="sum"),
        total_usd=pd.NamedAgg(column="total_usd", aggfunc="sum"),
    )
    .reset_index()
)
confirmed_seats = (
    _subset[_subset["status_id"] == "CONFIRMED"]
    .groupby(["channel", _subset["createdon"].dt.year.astype(str)])["seats"]
    .sum()
    .reset_index()
)
df = df.merge(confirmed_seats, on=["channel", "createdon"], how="left")

df["margin_pct"] = ((df["total_sysfee"] / df["total_usd"]) * 100).astype(float).round(2)

with bar_chart1:
    st.markdown("### Bookings by channel")
    fig3 = px.bar(
        df.sort_values(by=["createdon", "total_bookings"], ascending=[False, True]),
        y="channel",
        x="total_bookings",
        color="createdon",
        orientation="h",
        barmode="group",
        title="",
        color_discrete_map={
            "2023": COLOR_CODES["blue"],
            "2019": COLOR_CODES["orange"],
        },
    )
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False,categoryorder="total ascending"),
        yaxis_title="Channel",
        xaxis_title="Bookings",
        legend_title_text="Year",
    )
    st.plotly_chart(fig3, use_container_width=True)


with bar_chart2:
    st.markdown("### %Margin by channel")

    fig3 = px.bar(
        df.sort_values(by=["createdon", "margin_pct"], ascending=[False, True]),
        y="margin_pct",
        x="channel",
        color="createdon",
        orientation="v",
        barmode="group",
        title="",
        color_discrete_map={
            "2023": COLOR_CODES["blue"],
            "2019": COLOR_CODES["orange"],
        },
    )
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False,categoryorder="total ascending"),
        yaxis=dict(showgrid=False),
        yaxis_title="%",
        xaxis_title="",
        legend_title_text="Year",
    )
    st.plotly_chart(fig3, use_container_width=True)


st.markdown("### %Margin vs Confirmed seats by channel in 2023")
scatterplot = px.scatter(
    df[df["createdon"] == "2023"],
    x="seats",
    y="margin_pct",
    color="channel",
    size="seats",
)
scatterplot.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    yaxis_title="%Margin",
    xaxis_title="Seats",
)
st.plotly_chart(scatterplot, use_container_width=True)
