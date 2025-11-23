# EduFlow

**EduFlow** is a learning platform designed for PSUT students who want to tutor and manage private classes. It was mainly made as an alternative to traditional MOOC systems by integrating with Google Classroom.  
The platform allows students and instructors to:  
  
- Create and manage courses.
- Share learning materials.
- Communicate with enrolled students.
- Track assignments and course activity.
- Participate as students, instructor, or even both.  
  
## Prototype (Existing Version):

The current version of **Eduflow** was built as a prototype, mainly as a proof of concept to showcase the main idea, but definitely isn't a full production system as it has no true backend, minimal UI, and limited functionlities, and it was initially made as the end of semester project for *Software Engineering course*. It was built using:  
  
- _Streamlit framework_ for frontend.
- _Python scripts_ for backend logic.
- _Google Classroom API_ for course operations.
- _Google OAuth_ 2.0 for authentication.  
  
## The New Version:

The website _**is now being redesigned**_ to a cleaner, maintainable full-stack application using the following tech stack:  
  
- _Vue.js_ for frontend.
- _FastAPI_ for backend.
- _Google Classroom API_ for course operations (for now as well).
- _Google OAuth 2.0_ with better backend session handling.
- _Updated UX_ based on UX research and design workflow with real users.  
  
### Features (for now):  

- User authentication using Google's OAuth.
- Instructor dashboard.
- Student dashboard.
- Course creation and management tools
- Material and resource upload
- Messaging and announcements
- Activity feed
- User role management
- Discussion forums
- Assignment tracking  
  

## Installation (Prototype Version)

To run the existing Streamlit prototype:  
  
```bash
git clone https://github.com/r-living/EduFlow
cd EduFlow
pip install -r requirements.txt
streamlit run streamlit_app.py  
```
## Installation (Application's new version)

_Soon_
