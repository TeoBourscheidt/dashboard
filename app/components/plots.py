import altair as alt

def line_plot(df, column):
    return alt.Chart(df.reset_index()).mark_line().encode(
        x="index",
        y=column
    )
