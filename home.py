import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
import os

# ===== PAGE SETUP =====
st.set_page_config(
    page_title="EduFlow - Smart Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Solid background (safe alternative)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
with stylable_container(
    key="header_container",
    css_styles="""
    {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    """
):
    st.title("🎓 EduFlow")
    st.markdown("""
    <h3 style='color: #2563eb; font-weight: 300;'>
        Your Personalized Learning Journey Starts Here
    </h3>
    """, unsafe_allow_html=True)

# ===== HERO SECTION =====
colored_header(
    label="",
    description="",
    color_name="blue-70"
)

col1, col2 = st.columns([2, 1])
with col1:
    st.header("Transform Your Learning Experience")
    st.markdown("""
    <div style='font-size: 1.1rem; line-height: 1.6;'>
    ✨ <strong>Interactive courses</strong> tailored to your pace<br>
    🎯 <strong>Real-time progress tracking</strong> with smart analytics<br>
    👨‍🏫 <strong>Expert instructors</strong> available 24/7<br>
    </div>
    """, unsafe_allow_html=True)
    
    with stylable_container(
        key="cta_button",
        css_styles="""
        button {
            background: linear-gradient(to right, #2563eb, #1e40af);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
        }
        """
    ):
        if st.button("🚀 Start Learning Now"):
            st.switch_page("pages/1_login.py")  # Link to your login page

with col2:
    st.image("hero_image.png", width=300)  # Replace with your image

# ===== FEATURES SECTION =====
st.header("🌟 Why Choose EduFlow?")
features = st.columns(3)

# Feature 1
with features[0]:
    with stylable_container(
        key="feature_card_1",
        css_styles="""
        {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 0.5rem;
            padding: 1.5rem;
            height: 280px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        """
    ):
        st.subheader("🧠 Adaptive Learning")
        st.markdown("Our AI adjusts content difficulty based on your performance")

# Feature 2
with features[1]:
    with stylable_container(
        key="feature_card_2",
        css_styles="""
        {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 0.5rem;
            padding: 1.5rem;
            height: 280px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        """
    ):
        st.subheader("📊 Progress Analytics")
        st.markdown("Detailed dashboards track your strengths and weaknesses")

# Feature 3
with features[2]:
    with stylable_container(
        key="feature_card_3",
        css_styles="""
        {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 0.5rem;
            padding: 1.5rem;
            height: 280px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        """
    ):
        st.subheader("👥 Community Support")
        st.markdown("Connect with peers and instructors in discussion forums")

# ===== TESTIMONIALS =====
st.header("💬 What Our Students Say")
testimonials = st.columns(2)

# Testimonial 1
with testimonials[0]:
    with stylable_container(
        key="testimonial_card_1",
        css_styles="""
        {
            background: rgba(37, 99, 235, 0.1);
            border-radius: 0.5rem;
            padding: 1.5rem;
            border-left: 4px solid #2563eb;
        }
        """
    ):
        st.markdown("> \"EduFlow helped me master Python in just 3 months!\"")
        st.markdown("**— Sarah K., Data Science Student**")

# Testimonial 2
with testimonials[1]:
    with stylable_container(
        key="testimonial_card_2",
        css_styles="""
        {
            background: rgba(37, 99, 235, 0.1);
            border-radius: 0.5rem;
            padding: 1.5rem;
            border-left: 4px solid #2563eb;
        }
        """
    ):
        st.markdown("> \"As a teacher, I love how easy it is to track progress.\"")
        st.markdown("**— Prof. James L., Computer Science Instructor**")

# ===== FOOTER =====
st.markdown("---")
footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown("**Quick Links**")
    st.markdown("[Home](#)")  # Link to current page
    st.markdown("[Login](pages/1_login.py)")  # Link to login page
    st.markdown("[Courses](#)")  # Link to courses page

with footer_cols[1]:
    st.markdown("**Contact Us**")
    st.write("📧 contact@eduflow.com")
    st.write("📞 +1 (555) 123-4567")

with footer_cols[2]:
    st.markdown("**Follow Us**")
    st.write("[Twitter](https://twitter.com) | [LinkedIn](https://linkedin.com)")

if __name__ == "__main__":
    # Removed the auto-redirect code
    pass