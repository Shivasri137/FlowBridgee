import streamlit as st

def run():
    st.subheader("Email Writer Agent (Professional)")

    purpose = st.selectbox(
        "Email Purpose",
        ["Meeting Request", "Follow-up", "Reminder", "Apology"]
    )

    tone = st.selectbox(
        "Tone",
        ["Formal", "Friendly", "Urgent"]
    )

    recipient = st.text_input("Recipient Name")
    subject_context = st.text_input("Context (optional)", placeholder="Project / topic")

    if st.button("Generate Email"):
        if not recipient.strip():
            st.warning("Please enter recipient name.")
            return

        greeting = f"Dear {recipient},"

        if purpose == "Meeting Request":
            body = "I would like to request a meeting at your convenience to discuss"
        elif purpose == "Follow-up":
            body = "I am writing to follow up on our previous discussion regarding"
        elif purpose == "Reminder":
            body = "This is a gentle reminder regarding"
        else:
            body = "Please accept my sincere apologies regarding"

        if subject_context:
            body += f" {subject_context}."
        else:
            body += " the matter discussed earlier."

        closing = "Thank you for your time."

        if tone == "Friendly":
            closing = "Looking forward to hearing from you."
        elif tone == "Urgent":
            closing = "I would appreciate your prompt response."

        email_text = f"""
{greeting}

{body}

{closing}

Best regards,
"""

        st.text_area(
            "Generated Email (Editable)",
            email_text.strip(),
            height=220
        )
