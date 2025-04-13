import streamlit as st
import plotly.express as px
import pandas as pd
from chart_builders import build_score_card, draw_line_chart
from const import DATA, COLOR_CODES

st.set_page_config(layout="wide", page_title="Travel Booking Dashboard")

st.title("Travel Booking Dashboard")

st.markdown("## Key metrics")

# KPI Scorecards Data
_subset = DATA[
    (DATA["status_id"] == "CONFIRMED") & (DATA["vehclass_id"] != "insurance")
].copy()
total_seats_2023 = _subset[(_subset["createdon"].dt.year == 2023)]["seats"].sum()
total_seats_2019 = _subset[(_subset["createdon"].dt.year == 2019)]["seats"].sum()
total_seats_growth = total_seats_2023 - total_seats_2019
total_seats_growth_pct = round((total_seats_2023 / total_seats_2019 - 1) * 100, 2)

earning_per_seat_2023 = (
    _subset[(_subset["createdon"].dt.year == 2023)]["sysfee_usd"]
    .mean()
    .astype(float)
    .round(2)
)
earning_per_seat_2019 = (
    _subset[(_subset["createdon"].dt.year == 2019)]["sysfee_usd"]
    .mean()
    .astype(float)
    .round(2)
)
earning_per_seat_growth = round(earning_per_seat_2023 - earning_per_seat_2019, 2)
earning_per_seat_growth_pct = round(
    (earning_per_seat_2023 / earning_per_seat_2019 - 1) * 100, 2
)

total_bookings_2023 = _subset[(_subset["createdon"].dt.year == 2023)][
    "createdon"
].count()
total_bookings_2019 = _subset[(_subset["createdon"].dt.year == 2019)][
    "createdon"
].count()
total_bookings_growth = total_bookings_2023 - total_bookings_2019
total_bookings_growth_pct = round(
    (total_bookings_2023 / total_bookings_2019 - 1) * 100, 2
)

seat_per_booking_2023 = (
    _subset[(_subset["createdon"].dt.year == 2023)]["seats"]
    .mean()
    .astype(float)
    .round(2)
)
seat_per_booking_2019 = (
    _subset[(_subset["createdon"].dt.year == 2019)]["seats"]
    .mean()
    .astype(float)
    .round(2)
)
seat_per_booking_growth = round(seat_per_booking_2023 - seat_per_booking_2019, 2)
seat_per_booking_growth_pct = round(
    (seat_per_booking_2023 / seat_per_booking_2019 - 1) * 100, 2
)

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

# KPI Scorecards
with kpi_col1:
    build_score_card(
        "Confirmed Seats", total_seats_2023, total_seats_growth, total_seats_growth_pct
    )

with kpi_col2:
    build_score_card(
        "Earning per Seat",
        earning_per_seat_2023,
        earning_per_seat_growth,
        earning_per_seat_growth_pct,
        symbol="$",
    )

with kpi_col3:
    build_score_card(
        "Confirmed Bookings",
        total_bookings_2023,
        total_bookings_growth,
        total_bookings_growth_pct,
    )

with kpi_col4:
    build_score_card(
        "Seats per Booking",
        seat_per_booking_2023,
        seat_per_booking_growth,
        seat_per_booking_growth_pct,
    )

st.divider()

# Line Charts
line_chart_1, line_chart_2 = st.columns(2)

line_data = (
    _subset.groupby(
        [
            _subset["createdon"].dt.month,
            _subset["createdon"].dt.month_name(),
            _subset["createdon"].dt.year,
        ]
    )
    .agg(
        total_seats=pd.NamedAgg(column="seats", aggfunc="sum"),
        avg_earning_per_seat=pd.NamedAgg(column="sysfee_usd", aggfunc="mean"),
    )
    .copy()
)
line_data["year"] = line_data.index.get_level_values(2)
line_data["month_name"] = line_data.index.get_level_values(1)
line_data["month"] = line_data.index.get_level_values(0)
line_data.reset_index(drop=True, inplace=True)

with line_chart_1:
    st.markdown("### Monthly Confirmed Seats 2023 vs 2019")
    fig1 = draw_line_chart(
        line_data[["year", "month", "month_name", "total_seats"]],
        x_col="month_name",
        xlabel="Day of Year",
        ylabel="Seats",
        y_col="total_seats",
        title="",
        color_discrete_sequence=[COLOR_CODES["orange"], COLOR_CODES["blue"]],
        color="year",
    )
    st.plotly_chart(fig1, use_container_width=True)

with line_chart_2:
    st.markdown("### Monthly Earning per seat 2023 vs 2019")
    fig1 = draw_line_chart(
        line_data[["year", "month", "month_name", "avg_earning_per_seat"]],
        x_col="month_name",
        xlabel="Day of Year",
        ylabel="USD",
        y_col="avg_earning_per_seat",
        title="",
        color_discrete_sequence=[COLOR_CODES["orange"], COLOR_CODES["blue"]],
        color="year",
    )
    st.plotly_chart(fig1, use_container_width=True)

# Top routes and purchase type proportions
bar_chart, pie_chart = st.columns(2)


with bar_chart:
    st.markdown("### Top 10 Routes by bookings in 2023")
    fig3 = px.bar(
        DATA[(DATA["vehclass_id"] != "insurance") & (DATA["createdon"].dt.year == 2023)]
        .groupby(["route_id", "status_id"])
        .agg(total_bookings=pd.NamedAgg(column="createdon", aggfunc="count"))
        .sort_values("total_bookings")
        .tail(10)
        .reset_index(),
        y="route_id",
        x="total_bookings",
        color="status_id",
        orientation="h",
        title="",
        color_discrete_map={
            "CONFIRMED": COLOR_CODES["blue"],
            "CANCELED": COLOR_CODES["orange"],
            "PAID": COLOR_CODES["green"],
            "REFUNED": COLOR_CODES["red"],
        },
    )
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        # showlegend=False,
        xaxis_title="",
        yaxis_title="Route",
    )
    st.plotly_chart(fig3, use_container_width=True)

# Booking by purchase type
with pie_chart:
    st.markdown("### Booking by Customer group")
    fig4 = px.pie(
        DATA[(DATA["vehclass_id"] != "insurance") & (DATA["createdon"].dt.year == 2023)]
        .groupby(["purchase_type"])
        .agg(total_bookings=pd.NamedAgg(column="createdon", aggfunc="count"))
        .reset_index(),
        names="purchase_type",
        values="total_bookings",
        hole=0.5,
        title="",
        color_discrete_map={
            "Repeat purchase": COLOR_CODES["orange"],
            "First purchase": COLOR_CODES["white"],
        },
    )
    fig4.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=True,
    )
    st.plotly_chart(fig4, use_container_width=True)
