import os
import json
import base64
import anthropic
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define the tools our Agent can use
AGENT_TOOLS = [
    {
        "name": "draw_diagram",
        "description": "Use this tool to generate a visual diagram (wiring, polarity, or process flow) using Mermaid.js syntax. ALWAYS use this instead of describing a wiring setup in plain text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mermaid_code": {
                    "type": "string",
                    "description": "The raw Mermaid.js code for the diagram. CRITICAL: You must separate each statement with a newline character (\\n). Do NOT output the code on a single continuous line. Avoid using double quotes inside node labels."
                },
                "caption": {
                    "type": "string",
                    "description": "A brief explanation of what the diagram shows."
                }
            },
            "required": ["mermaid_code", "caption"]
        }
    },
    {
        "name": "render_matrix",
        "description": "Use this tool when the user asks about compatibility, duty cycles, or settings that require comparing multiple variables. Render it as a clean Markdown table.",
        "input_schema": {
            "type": "object",
            "properties": {
                "markdown_table": {
                    "type": "string",
                    "description": "The formatted markdown table."
                },
                "context": {
                    "type": "string",
                    "description": "A brief sentence explaining how to read the table."
                }
            },
            "required": ["markdown_table", "context"]
        }
    }
]

def get_base64_encoded_image(image_path):
    """Reads a local image file and converts it to a Base64 string for Claude."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ask_agent(user_query):
    # 1. Load the text AND the image paths from our JSON
    try:
        with open("knowledge.json", "r") as f:
            chunks = json.load(f)
    except FileNotFoundError:
        return {"text": "ERROR: knowledge.json not found.", "tool_used": None, "tool_data": None}

    system_prompt = """You are an elite, highly technical support agent for the Vulcan OmniPro 220 multiprocess welder. You have perfect knowledge of the manual and the attached visual charts.

CRITICAL DIRECTIVE: You must use the provided tools for technical communication. 
- If the user asks a direct question, answer it explicitly in 1 to 2 concise sentences first.
- Then, if the query involves wiring, polarity, or physical setup, immediately use the `draw_diagram` tool. Do not write long paragraphs explaining the setup.
- DIAGRAM STYLING RULES: When generating Mermaid code, you MUST use `graph LR` (Left-to-Right layout) to mimic a physical workbench. You MUST color-code polarity nodes (e.g., Red for Positive, Black for Negative) using Mermaid style tags. You MUST label the connecting cables (e.g., `-->|Red Cable|`). Use emojis to make components visually distinct.
- If asked about duty cycles, compatibility, or settings across different modes, use the `render_matrix` tool.
- PROHIBITED: You are strictly forbidden from writing ```mermaid``` markdown blocks in your conversational text response. You MUST trigger the JSON `draw_diagram` API tool to submit your code.
Manual Context:
"""
    
    # We will build a complex message array that holds BOTH text and images
    message_content = []

    # 2. Loop through the chunks to build the system text and grab images
    for chunk in chunks:
        system_prompt += f"--- Source: {chunk['source']} (Page {chunk['page']}) ---\n{chunk['text']}\n\n"
        
        # If this chunk has images (like the selection chart!), encode them and add them to the vision payload
        for img_path in chunk.get("images", []):
            if os.path.exists(img_path):
                base64_data = get_base64_encoded_image(img_path)
                message_content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_data
                    }
                })

    # 3. Finally, add the user's actual text query to the end of the message payload
    message_content.append({"type": "text", "text": user_query})

    # 4. Send it to Claude
    response = client.messages.create(
        model="claude-sonnet-4-6", # Use this or claude-3-5-sonnet-latest depending on your tier
        max_tokens=2048,
        system=system_prompt,
        tools=AGENT_TOOLS,
        messages=[{"role": "user", "content": message_content}]
    )

    result = {"text": "", "tool_used": None, "tool_data": None}

    for block in response.content:
        if block.type == 'text':
            result["text"] += block.text + "\n"
        elif block.type == 'tool_use':
            result["tool_used"] = block.name
            result["tool_data"] = block.input

    return result