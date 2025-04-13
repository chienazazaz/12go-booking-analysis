import plotly.express as px

def draw_line_chart(df, x_col, y_col, title, color,color_discrete_sequence,xlabel=None,ylabel=None):
    fig = px.line(df, x=x_col, y=y_col, title=title, line_shape="spline", color_discrete_sequence=color_discrete_sequence, color=color,)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        # showlegend=False,
        xaxis_title=xlabel, 
        yaxis_title=ylabel
    )
    return fig