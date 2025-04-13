import streamlit as st
import plotly.express as px
import pandas as pd
from const import DATA, COLOR_CODES

st.set_page_config(layout="wide", page_title="Travel Booking Dashboard")

st.title("Service Performance")

bar_chart1, bar_chart2 = st.columns(2)
_subset = DATA[(DATA["vehclass_id"] != "insurance")].copy()


df = (
    _subset.groupby(
        ["vehclass_id", "class_type", _subset["createdon"].dt.year.astype(str)]
    )
    .agg(
        total_bookings=pd.NamedAgg(column="createdon", aggfunc="count"),
        total_sysfee=pd.NamedAgg(column="sysfee_total_usd", aggfunc="sum"),
        total_usd=pd.NamedAgg(column="total_usd", aggfunc="sum"),
    )
    .reset_index()
)
confirmed_seats = (
    _subset[_subset["status_id"] == "CONFIRMED"]
    .groupby(["vehclass_id", "class_type", _subset["createdon"].dt.year.astype(str)])[
        "seats"
    ]
    .sum()
    .reset_index()
)
df = df.merge(
    confirmed_seats, on=["vehclass_id", "class_type", "createdon"], how="left"
)
df["vehicle_class"] = df.apply(
    lambda x: x["vehclass_id"] + " - " + x["class_type"], axis=1
)
df["margin_pct"] = ((df["total_sysfee"] / df["total_usd"]) * 100).astype(float).round(2)

with bar_chart1:
    st.markdown("### Bookings by Vehicle & Class")
    fig3 = px.bar(
        df.sort_values(by="total_bookings"),
        y="vehicle_class",
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
        yaxis=dict(showgrid=False, categoryorder="total ascending"),
        # showlegend=False,
        yaxis_title="Vehicle & Class",
        xaxis_title="Bookings",
        legend_title_text="Year",
    )
    st.plotly_chart(fig3, use_container_width=True)


with bar_chart2:
    st.markdown("### %Margin vs Confirmed seats by Vehicle & Class in 2023")
    scatterplot = px.scatter(
        df[df["createdon"] == "2023"],
        x="seats",
        y="margin_pct",
        color="vehicle_class",
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
        legend_title_text="Vehicle & Class",
    )
    st.plotly_chart(scatterplot, use_container_width=True)

# Dataframe for %Margin vs Confirmed seats
st.markdown("### %Margin vs Confirmed seats by Vehicle & Class in 2023")
tb_df = (
    _subset[_subset["createdon"].dt.year == 2023]
    .groupby(["vehclass_id", "class_type"])
    .agg(
        total_sysfee=pd.NamedAgg(column="sysfee_total_usd", aggfunc="sum"),
    )
)
# tb_df["total_sysfee"] = tb_df["total_sysfee"].astype(float).round(2)

confirmed_seats = (
    _subset[_subset["status_id"] == "CONFIRMED"]
    .groupby(["vehclass_id", "class_type"])["seats"]
    .sum()
    .reset_index()
)
tb_df = tb_df.merge(confirmed_seats, on=["vehclass_id", "class_type"], how="left")
tb_df.set_index(["vehclass_id", "class_type"], inplace=True)
tb_df = tb_df.unstack(level=1)
tb_df.columns = tb_df.columns.set_levels(["Earning", "Confirmed seats"], level=0)
tb_df.columns = tb_df.columns.set_names(["", "Class Type"])
tb_df.index = tb_df.index.set_names(["Vehicle Class"])
tb_df.style.format(
    {
        ("Earning", "Class II"): "{:,.2f}",
        ("Earning", "Class I"): "{:,.2f}",
        ("Confirmed seats", "Class II"): "{:,.0f}",
        ("Confirmed seats", "Class I"): "{:,.0f}",
    },
    na_rep="-",
)

df_viz = st.dataframe(tb_df, use_container_width=True)
