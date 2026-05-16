import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import json, os

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.title("🩺 AiWA - AI Wellness Assistant")

symptoms = st.text_area("What symptoms do you have?", placeholder="e.g. headache, fever")

if st.button("Analyze", type="primary"):
    with st.spinner("Analyzing..."):

        reply = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content":
                f"User symptoms: {symptoms}. "
                "Reply ONLY with JSON, no markdown: "
                '{"disease_1":"...","confidence_1":80,"advice_1":"...",'
                '"disease_2":"...","confidence_2":55,"advice_2":"...",'
                '"disease_3":"...","confidence_3":30,"advice_3":"...",'
                '"summary":"2-3 sentences, tell user to see a doctor."}'
            }],
            max_tokens=400,
        )

        r = json.loads(reply.choices[0].message.content.strip())

    st.info(r["summary"])

    for i in range(1, 4):
        st.write(f"**{i}. {r[f'disease_{i}']}** — {r[f'confidence_{i}']}%")
        st.progress(r[f"confidence_{i}"] / 100)
        st.write(f"💊 {r[f'advice_{i}']}")
        st.divider()

    st.warning("⚠️ Not real medical advice. Always see a doctor.")