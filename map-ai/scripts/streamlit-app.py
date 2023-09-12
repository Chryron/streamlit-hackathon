import streamlit as st

import os
import pydeck as pdk
from navigator import Navigator

navigator = Navigator()

with open(os.path.join(os.path.dirname(__file__), 'styles.css')) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I am your personal navigator!"}]

############################# BODY #############################

st.title("Navigator")

with st.container():

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    prompt = st.chat_input("Ask me for direction")
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.empty():
                st.info("...")
                st.session_state.result = navigator.process_query(prompt)
                st.markdown(st.session_state.result.instructions)

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append(
            {"role": "assistant", "content": st.session_state.result.instructions})


if "result" in st.session_state and not st.session_state.result.route_df.empty:
    layer = pdk.Layer(
        type='PathLayer',
        data=st.session_state.result.route_df,
        pickable=True,
        get_color='color',
        width_scale=20,
        width_min_pixels=2,
        get_path='path',
        get_width=5)

    view_state = pdk.data_utils.compute_view(
        points=st.session_state.result.route_bbox)
    r = pdk.Deck(layers=[layer], tooltip={
                 'text': '{name}'}, initial_view_state=view_state)
    st.pydeck_chart(r)
