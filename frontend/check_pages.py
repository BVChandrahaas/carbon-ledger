import os
import streamlit as st

print("Current working directory:", os.getcwd())
if os.path.exists('pages'):
    print("Files in pages/:", os.listdir('pages'))
else:
    print("pages/ directory not found")
