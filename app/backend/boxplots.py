import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


LB = 23
UB = 86
user_value = 47

fig = go.Figure(layout=go.Layout(
        annotations=[
            go.layout.Annotation(
                text='YOU',
                showarrow=True,
                x=user_value,
                y=0,
                bordercolor='black',
                borderwidth=1
            )
        ]))

x = [LB - (UB-LB)/2, LB, UB, UB + (UB-LB)/2]
fig.add_trace(go.Box(x=list(range(int(LB - (UB-LB)/2), int(UB + (UB-LB)/2))), name="vitam"
                                                                                   "in x", fillcolor="crimson"))

fig.update_traces(q1= [LB], q3=[UB])


fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=user_value,
            y0=-1,
            x1=user_value,
            y1=1,
            line=dict(
                color="RoyalBlue",
                width=3
            )
))

fig.update_layout(
    height=300
)


fig.show()


