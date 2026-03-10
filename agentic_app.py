import streamlit as st
from groq import Groq

# Page config
st.set_page_config(
    page_title="AI News Agent",
    page_icon="📰",
    layout="centered"
)

# Title and description
st.title("📰 AI News Agent")
st.subheader("Powered by 3 AI Agents working together")
st.markdown("Enter any topic and watch 3 AI agents research, write, and edit a news article for you!")

# Sidebar for API key
st.sidebar.title("⚙️ Settings")
api_key = st.sidebar.text_input(
    "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",
    type="password",
    placeholder="gsk_..."
)
st.sidebar.markdown("Get your free key at [console.groq.com](https://console.groq.com)")

# Main input
topic = st.text_input("Enter a news topic:", placeholder="e.g. Artificial Intelligence in 2025")
run_button = st.button("🚀 Run AI Agents", use_container_width=True)

# Agent functions
def researcher_agent(client, topic):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert news researcher.
                Research the topic and return:
                1. Key Facts (at least 5 facts)
                2. Important People or Organizations involved
                3. Timeline of events
                4. Current situation
                5. Future outlook
                Be detailed and factual."""
            },
            {
                "role": "user",
                "content": f"Research this topic thoroughly: {topic}"
            }
        ]
    )
    return response.choices[0].message.content


def journalist_agent(client, topic, research):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a professional news journalist.
                Turn the research into a compelling news article with:
                - A catchy headline
                - An engaging introduction
                - Clear body paragraphs
                - A strong conclusion
                Write like you are publishing for a major newspaper."""
            },
            {
                "role": "user",
                "content": f"Write a professional news article about: {topic}\n\nUse this research:\n{research}"
            }
        ]
    )
    return response.choices[0].message.content


def editor_agent(client, topic, article):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a strict senior news editor.
                Review the article and provide:
                1. FACT CHECK - List what appears accurate
                2. CONCERNS - List anything that needs verification
                3. IMPROVEMENTS - Suggest 3 specific improvements
                4. QUALITY SCORE - Give a score out of 10
                5. FINAL VERSION - Rewrite the article with improvements applied
                Be critical but constructive."""
            },
            {
                "role": "user",
                "content": f"Review and improve this article about {topic}:\n\n{article}"
            }
        ]
    )
    return response.choices[0].message.content


# Run agents when button is clicked
if run_button:
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar!")
    elif not topic:
        st.error("Please enter a news topic!")
    else:
        client = Groq(api_key=api_key)

        # Agent 1
        with st.expander("🕵️ Agent 1 - Researcher", expanded=True):
            with st.spinner("Researching..."):
                research = researcher_agent(client, topic)
            st.success("Research Complete!")
            st.write(research)

        # Agent 2
        with st.expander("✍️ Agent 2 - Journalist", expanded=True):
            with st.spinner("Writing article..."):
                article = journalist_agent(client, topic, research)
            st.success("Article Written!")
            st.write(article)

        # Agent 3
        with st.expander("🧐 Agent 3 - Editor", expanded=True):
            with st.spinner("Fact-checking and editing..."):
                final = editor_agent(client, topic, article)
            st.success("Editing Complete!")
            st.write(final)

        st.balloons()
        st.success("All 3 agents completed their work!")
```

--- 

### 📄 File 2 — `requirements.txt`
This tells Streamlit which libraries to install. **Create a new file** with exactly this content:
```
groq
streamlit