import altair as alt
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13],
    'label': ['A', 'B', 'C', 'D']
})

chart = alt.Chart(df).mark_circle().encode(
    x='x',
    y='y',
    tooltip='label'
)

chart.interactive()