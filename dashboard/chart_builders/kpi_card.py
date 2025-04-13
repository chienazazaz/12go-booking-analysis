import streamlit as st

def build_score_card(title, value, growth, growth_pct, growth_direction=1, symbol=""):
    st.markdown(f"### {title}")
    st.markdown(f"<h1 style='color: white;'>{symbol}{value:,}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {'red' if growth*growth_direction < 0 else 'green'};'>{'+' if growth*growth_direction >0 else '-' } {symbol}{growth:,} vs 2019</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {'red' if growth*growth_direction < 0 else 'green'};'>{'+' if growth*growth_direction >0 else '-' } {growth_pct}% vs 2019</p>", unsafe_allow_html=True)