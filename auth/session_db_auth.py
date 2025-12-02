
from datetime import datetime, timedelta, timezone as tz
from os import getenv
import streamlit as st
from auth.auth import Auth
from models.portal.session import Session
from models.portal.student import Student
from models.portal.teacher import Teacher
from models.portal.user import User


class SessionDbAuth:
    def __init__(self):
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "84006"))
        except Exception:
            self.session_duration = 0
    
    def create_session(self, user_id=None):
        if user_id is None:
            return None
        user = User.get(user_id)
        if user is None:
            # user_id is not valid
            return None
        # Check if there is existing session by the user
        session = Session.query.filter(Session.user_id==user_id).one_or_none()
        # Check if the session is valid
        if session is not None:
            dur = timedelta(seconds=self.session_duration)
            if session.updated_at.replace(tzinfo=tz.utc) + dur > datetime.now(tz.utc):
                # Update the session if valid
                # Save the session update the session
                session.save()
                return session.id
            # Session not valid
            session.delete()
        # Create new session
        session = Session(user_id=user_id)
        session.save()
        return session.id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None or isinstance(session_id, str) is False:
            return None
        # GEt the session
        session = Session.get(session_id)
        # if session exist
        if session is not None:
            dur = timedelta(seconds=self.session_duration)
            if session.updated_at.replace(tzinfo=tz.utc) + dur > datetime.now(tz.utc):
                # Session is valid
                return session.user_id
            # Session expired
            session.delete()
        return None
    
    def current_user(self):
        if "session_id" not in st.session_state:
            return None
        session_id = st.session_state["session_id"]
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
    
    def destroy_session(self):
        if "session_id" not in st.session_state:
            return False
        session_id = st.session_state["session_id"]
        if session_id is None or self.user_id_for_session_id(session_id) is None:
            return False
        Session.get(session_id).delete()
        return True
