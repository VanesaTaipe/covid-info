import streamlit as st


class CustomSelectedInput(st.s):

    def __init__(self, arg):
        super(CustomSelectedInput, st.selectbox).__init__()
        self.arg = arg

    def __enter__(self):
        return
