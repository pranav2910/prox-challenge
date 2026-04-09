import warnings
import streamlit as st
import os
import json
import streamlit.components.v1 as components
from agent import ask_agent

def draw_mermaid_diagram(mermaid_code: str):
    """Bypasses Streamlit's native renderer and forces Mermaid to draw using raw HTML/JS."""
    html_content = f"""
        <div class="mermaid" style="font-family: sans-serif;">
            {mermaid_code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        components.html(html_content, height=450, scrolling=True)

st.set_page_config(page_title="Prox Agent: Vulcan OmniPro 220", layout="wide")

st.title("⚡ Vulcan OmniPro 220: Technical Expert")
st.markdown("Ask deep technical questions, upload diagnostic images, or request wiring diagrams.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("E.g., How do I set up polarity for Flux-Cored welding?")
uploaded_file = st.sidebar.file_uploader("Upload a weld photo for diagnosis", type=['png', 'jpg', 'webp'])

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agent response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing technical manuals and visual charts..."):
            
            # 1. Ask the real agent!
            response_data = ask_agent(user_input)
            
            # 2. Check if Claude decided to use a tool
            if response_data["tool_used"] == "render_matrix":
                # Print the conversational text first (if Claude wrote any)
                if response_data["text"]:
                    st.markdown(response_data["text"])
                    
                st.markdown(response_data["tool_data"]["context"])
                st.markdown(response_data["tool_data"]["markdown_table"])
                
                # Save to history
                full_response = f"{response_data['text']}\n\n{response_data['tool_data']['context']}\n\n{response_data['tool_data']['markdown_table']}"
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            elif response_data["tool_used"] == "draw_diagram":
                # Print the conversational text first (if Claude wrote any)
                if response_data["text"]:
                    st.markdown(response_data["text"])
                    
                st.info(response_data["tool_data"]["caption"])
                
                # ✨ THE UI FIX: Tell Streamlit to render the Mermaid code as a visual diagram using HTML
                draw_mermaid_diagram(response_data['tool_data']['mermaid_code'])
                
                # Save to history so the app doesn't crash on refresh
                saved_code = response_data['tool_data']['mermaid_code']
                full_response = f"{response_data['text']}\n\n*(Diagram generated: {response_data['tool_data']['caption']})*\n\n```mermaid\n{saved_code}\n```"
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            else:
                # 3. If no tool was used, just print Claude's text
                final_text = response_data["text"] if response_data["text"] else "I could not find a specific diagram or matrix for that."
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})