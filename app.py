import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
Pre_Trace = np.load('/home/orion/Desktop/Prog/Python/Lab/Pre_Trace.npy')
Pos_Trace = np.load('/home/orion/Desktop/Prog/Python/Lab/Pos_Trace.npy')
indices_0 = np.load('/home/orion/Desktop/Prog/Python/Lab/indices_0.npy')
indices_1 = np.load('/home/orion/Desktop/Prog/Python/Lab/indices_1.npy')
Astd_df_clean = np.load('/home/orion/Desktop/Prog/Python/Lab/Astd_df_clean.npy')
Astd_df_clean = pd.DataFrame(Astd_df_clean)
Pre_com=np.load('/home/orion/Desktop/Prog/Python/Lab/Pre_CenterOfMass.npy')
Pos_com=np.load('/home/orion/Desktop/Prog/Python/Lab/Pos_CenterOfMass.npy')

Premean=Pre_Trace[indices_0].mean(axis=1)
Prestd=Pre_Trace[indices_0].std(axis=1)
Posmean=Pos_Trace[indices_1].mean(axis=1)
Posstd=Pos_Trace[indices_1].std(axis=1)
Amean=[Premean,Posmean]
Astd=[Prestd,Posstd]

# Streamlit text
st.write('Welcome to the neuronal activity dashboard')
st.write('Here you can analyze the activity of neurons')

# Create subplot grid with 1 row and 2 columns
fig = make_subplots(rows=1, cols=2, subplot_titles=('Before Noise Overexposure', 'After Noise Overexposure'))
fig.update_layout(title_text='Neuronal Activity traces')

option = st.selectbox('Select an Neuron:', indices_0)
selected_index = np.where(indices_0 == option)[0][0]
# Add traces to the respective subplots
fig.add_trace(go.Scatter(y=Pre_Trace[indices_0[selected_index]][963::10], mode='lines', name='B.N.O', line=dict(color='green')), row=1, col=1)
fig.add_trace(go.Scatter(y=Pos_Trace[indices_1[selected_index]][164::10], mode='lines', name='A.F.O', line=dict(color='red')), row=1, col=2)
##
fig4 = make_subplots(rows=1, cols=1, subplot_titles=('Before Noise Overexposure'))
fig4.update_layout(title_text='Center of Mass Analysis')
#fig4.add_trace(go.Scatter(x=Pre_com.T[0][indices_0], y=Pre_com.T[1][indices_0], mode='markers', name='B.N.O', marker=dict(color='green')), row=1, col=1)
#fig4.add_trace(go.Scatter(x=Pos_com.T[0][indices_1], y=Pos_com.T[1][indices_1], mode='markers', name='A.F.O', marker=dict(color='red')), row=1, col=1)
fig4.add_scatter3d(x=Pre_com.T[0][indices_0], z=Pre_com.T[1][indices_0], y=indices_0, mode='markers', name='A.N.O', marker=dict(colorscale='Hot', color=Astd[0], showscale=True))    
fig4.update_xaxes(title_text='X-axis')
fig4.update_yaxes(title_text='Y-axis')

# Render the figure as an image




# Create menu for selecting indices
# Histogram

fig2=go.Figure()
fig2.update_layout(title_text='Neuronal Activity Analysis')
fig2.add_trace(go.Histogram(x=Astd_df_clean[0], nbinsx=10, name='B.N.O Activity', marker=dict(color='green')))
fig2.add_trace(go.Histogram(x=Astd_df_clean[1], nbinsx=10, name='A.N.O Activity', marker=dict(color='red'))) 
fig2.update_xaxes(title_text='Activity [A.U%]',)
fig2.update_yaxes(title_text='Frequency')

fig3=go.Figure()
fig3.add_pie(labels=['Decreased acitivty', 'Increased activity'], values=[len(np.where(Astd_df_clean[0]>=Astd_df_clean[1])[0]), len(np.where(Astd_df_clean[0]<=Astd_df_clean[1])[0]),len(np.where(Astd_df_clean[0]==Astd_df_clean[1])[0])], marker=dict(colors=['red', 'green','blue']))
# Update layout
fig3.update_layout(title_text='Neuronal Activity Analysis', autosize=True)


fig5=go.Figure()


#fig5.add_trace(go.Scatter3d(x=Astd[0], y=Astd[1], z=indices_0, mode='markers', name='B.N.O', line=dict(colorscale='Viridis',color=indices_0, showscale=True)))

fig5.add_scatter3d(x=Astd[0], y=Astd[1], z=indices_0, mode='markers', name='A.F.O', marker=dict(colorscale='Hot', color=Amean[0], showscale=True))

fig9=go.Figure()
fig9.add_heatmap(z=Pre_Trace[indices_0])


# Render the figure in Streamlit
st.plotly_chart(fig, use_container_width=True)
# Display the image
st.plotly_chart(fig4, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig5, use_container_width=True)
st.plotly_chart(fig9,use_container_width=True)
# Save the figure as HTML file
#fig.write_html('/home/orion/Desktop/Prog/Python/neuronal_activity_analysis.html')