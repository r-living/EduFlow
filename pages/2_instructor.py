# pages/2_instructor.py

import streamlit as st
from googleapiclient.discovery import build
import pickle
import os
from datetime import datetime
from streamlit_lottie import st_lottie
import json
from streamlit_extras.stylable_container import stylable_container

# ===== BACKEND FUNCTIONS =====
TOKEN_FILE = "token.json"

def get_credentials():
    """Load saved credentials from pickle file"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            return pickle.load(token)
    return None

def get_classroom_service():
    """Build Classroom API service"""
    creds = get_credentials()
    if creds:
        return build("classroom", "v1", credentials=creds)
    return None

def list_courses(service):
    """List all courses where user is instructor"""
    results = service.courses().list(teacherId="me").execute()
    return results.get("courses", [])

def create_course(service, course_title, course_section, description, room):
    """Create a new course"""
    course = {
        "name": course_title,
        "section": course_section,
        "descriptionHeading": "Welcome to " + course_title,
        "description": description,
        "room": room,
        "ownerId": "me",
        "courseState": "PROVISIONED"
    }
    return service.courses().create(body=course).execute()

def list_announcements(service, course_id):
    """List announcements for a course"""
    results = service.courses().announcements().list(
        courseId=course_id,
        orderBy="updateTime desc"
    ).execute()
    return results.get("announcements", [])

def create_announcement(service, course_id, text, materials=None):
    """Create a new announcement"""
    announcement = {
        "text": text,
        "state": "PUBLISHED"
    }
    if materials:
        announcement["materials"] = materials
    return service.courses().announcements().create(
        courseId=course_id,
        body=announcement
    ).execute()

def list_students(service, course_id):
    """List students in a course"""
    results = service.courses().students().list(courseId=course_id).execute()
    return results.get("students", [])

# ===== UI FUNCTIONS =====
def load_lottie(url):
    """Load Lottie animation from URL or local JSON"""
    if url.startswith('http'):
        import requests
        return requests.get(url).json()
    return json.loads(url)

def course_card(course):
    """Display a course as a styled card (simplified version)"""
    with stylable_container(
        key=f"course_{course['id']}",
        css_styles="""
        {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid #e0e0e0;
        }
        """
    ):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {course.get('name', 'Untitled Course')}")
            st.caption(f"Section: {course.get('section', 'N/A')} • Room: {course.get('room', 'N/A')}")
            if course.get('description'):
                st.markdown(f"<div style='color: #555; font-size: 0.9rem;'>{course['description']}</div>", 
                          unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**ID:** `{course['id']}`")
            if st.button("Manage", key=f"manage_{course['id']}"):
                st.session_state.current_course = course

# ===== MAIN PAGE =====
def main():
    # Authentication check
    if not os.path.exists(TOKEN_FILE):
        st.error("Please login first")
        st.stop()
    
    try:
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
        
        # Verify credentials are still valid
        if not creds or not creds.valid:
            st.error("Session expired, please login again")
            os.remove(TOKEN_FILE)
            st.stop()
            
    except Exception as e:
        st.error(f"Invalid session: {str(e)}")
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        st.stop()
    # Page config with more stable settings
    st.set_page_config(
        page_title="Instructor Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Simplified CSS that won't cause disappearing elements
    st.markdown("""
    <style>
        .stApp {
            background: #f5f7fa;
        }
        .sidebar .sidebar-content {
            background: #2563eb;
            color: white;
        }
        .sidebar .sidebar-content .stButton button {
            background: white;
            color: #2563eb;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .stButton button {
            width: 100%;
        }
        .stMarkdown h3 {
            margin-top: 0;
        }
        [data-testid="stSidebarUserContent"] {
            padding: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Check authentication
    if not os.path.exists(TOKEN_FILE):
        st.error("You need to login first")
        st.stop()

    # Get user info
    creds = get_credentials()
    if not creds:
        st.error("Failed to load credentials")
        st.stop()
        
    user_info = build("oauth2", "v2", credentials=creds).userinfo().get().execute()
    user_email = user_info["email"]

    # Initialize session state
    if 'current_course' not in st.session_state:
        st.session_state.current_course = None
    if 'show_create_course' not in st.session_state:
        st.session_state.show_create_course = False

    # More stable sidebar implementation
    with st.sidebar:
        st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <h2 style="color: white; margin-bottom: 0.5rem;">EduFlow</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0;">{user_email}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Create New Course"):
            st.session_state.show_create_course = True
            st.session_state.current_course = None

        if st.session_state.current_course:
            if st.button("Back to All Courses"):
                st.session_state.current_course = None
                st.session_state.show_create_course = False

        st.markdown("---")
        
        if st.button("Sign Out", key="sidebar_sign_out"):
            os.remove(TOKEN_FILE)
            st.session_state.clear()
            st.rerun()

    # Main content with more stable rendering
    st.title("Instructor Dashboard")

    # Get Classroom service
    service = get_classroom_service()
    if not service:
        st.error("Failed to initialize Classroom service")
        st.stop()

    # Course management view - using columns for better layout stability
    if st.session_state.show_create_course:
        with st.container():
            st.subheader("Create New Course")
            with st.form("create_course_form"):
                col1, col2 = st.columns(2)
                with col1:
                    course_title = st.text_input("Course Title", placeholder="Introduction to Computer Science")
                with col2:
                    course_section = st.text_input("Section", placeholder="Fall 2023")
                
                description = st.text_area("Description", placeholder="Course objectives and overview...")
                room = st.text_input("Room", placeholder="Building A, Room 101")
                
                submitted = st.form_submit_button("Create Course")
                if submitted:
                    with st.spinner("Creating course..."):
                        try:
                            course = create_course(service, course_title, course_section, description, room)
                            st.success(f"Course created successfully! ID: {course['id']}")
                            st.session_state.show_create_course = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error creating course: {str(e)}")

    elif st.session_state.current_course:
        # Course detail view with more stable tabs implementation
        course = st.session_state.current_course
        with st.container():
            st.markdown(f"## {course['name']}")
            st.caption(f"Section: {course.get('section', 'N/A')} • Room: {course.get('room', 'N/A')}")
            
            tab1, tab2, tab3 = st.tabs(["Announcements", "Students", "Course Details"])
            
            with tab1:
                # Announcements section
                st.subheader("Announcements")
                
                with st.expander("Create New Announcement", expanded=False):
                    with st.form("announcement_form"):
                        announcement_text = st.text_area("Announcement Text")
                        submitted = st.form_submit_button("Post Announcement")
                        if submitted and announcement_text:
                            try:
                                create_announcement(service, course['id'], announcement_text)
                                st.success("Announcement posted!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error posting announcement: {str(e)}")
                
                announcements = list_announcements(service, course['id'])
                if announcements:
                    for announcement in announcements:
                        update_time = datetime.strptime(
                            announcement['updateTime'], 
                            "%Y-%m-%dT%H:%M:%S.%fZ"
                        ).strftime("%B %d, %Y at %H:%M")
                        
                        with st.container():
                            st.markdown(announcement['text'])
                            st.caption(f"Posted on {update_time}")
                            st.divider()
                else:
                    st.info("No announcements yet")
            
            with tab2:
                # Students section
                st.subheader("Enrolled Students")
            
                students = list_students(service, course['id'])
                if students:
                    for student in students:
                        with stylable_container(
                            key=f"student_{student['userId']}",
                            css_styles="""
                            {
                            background: white;
                            border-radius: 10px;
                            padding: 1rem;
                            margin: 0.5rem 0;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        }
                        """
                        ):
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.markdown(f"**{student['profile']['name']['fullName']}**")
                            with col2:
                                st.markdown(f"`{student['profile']['emailAddress']}`")
                else:
                    st.info("No students enrolled yet")
        
            with tab3:
                # Course details section
                st.subheader("Course Information")
            
                with stylable_container(
                    key="course_details",
                    css_styles="""
                    {
                    background: white;
                    border-radius: 10px;
                    padding: 1.5rem;
                    margin: 0.5rem 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                """
                ):
                    st.markdown(f"**Course ID:** `{course['id']}`")
                    st.markdown(f"**Status:** {course.get('courseState', 'N/A')}")
                    st.markdown(f"**Created:** {datetime.strptime(course['creationTime'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%B %d, %Y')}")
                
                    if course.get('descriptionHeading'):
                        st.markdown("---")
                        st.markdown(f"### {course['descriptionHeading']}")
                
                    if course.get('description'):
                        st.markdown(course['description'])

    else:
        # Course list view with more stable rendering
        st.subheader("Your Courses")
        
        with st.spinner("Loading courses..."):
            courses = list_courses(service)
            
            if courses:
                for course in courses:
                    with st.container():
                        course_card(course)
            else:
                st.info("You don't have any courses yet")
                if st.button("Create Your First Course"):
                    st.session_state.show_create_course = True
                    st.rerun()

if __name__ == "__main__":
    main()