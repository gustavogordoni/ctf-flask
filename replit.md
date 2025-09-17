# CTF Web Application - Educational Security Challenge

## Overview

This is an educational Capture The Flag (CTF) web application built with Flask that demonstrates four common web vulnerabilities through progressive challenges. The application serves as a hands-on learning platform for understanding web security concepts including HTML injection, broken access control, SQL injection, and insecure direct object references. Each phase must be completed sequentially, with flags serving as proof of successful exploitation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with a base template system
- **UI Design**: Terminal/hacker-themed styling with green/red color scheme
- **Progressive Navigation**: Phase-based progression system with locked/unlocked states
- **Responsive Layout**: CSS flexbox-based navigation and responsive design

### Backend Architecture
- **Framework**: Flask web framework with session-based state management
- **Route Structure**: RESTful endpoints for each CTF phase and validation
- **Session Management**: Flask sessions for tracking user progress and completed phases
- **Vulnerability Implementation**: Intentionally insecure code patterns for educational purposes

### Security Model (Intentionally Vulnerable)
- **Authentication**: Simulated SQL injection vulnerability in login system
- **Access Control**: Broken access control via URL parameter manipulation
- **Input Validation**: Missing HTML sanitization for injection demonstrations
- **File Access**: Insecure direct object reference for file system access

### Data Storage
- **User Database**: In-memory dictionary simulation of user records
- **Flag Storage**: Hardcoded flags in application configuration
- **Session Data**: Flask session storage for progress tracking
- **File System**: Local file storage for IDOR challenge documents

### Application Flow
- **Phase Progression**: Linear advancement through 4 security challenges
- **Flag Validation**: POST-based flag submission with server-side verification
- **State Persistence**: Session-based tracking of completed phases
- **Error Handling**: Custom error pages with educational context

## External Dependencies

### Core Framework
- **Flask**: Primary web framework for routing and templating
- **Jinja2**: Template engine (included with Flask)

### Python Standard Library
- **os**: Environment variable management and file operations
- **session**: Built-in Flask session management

### Static Assets
- **CSS**: Embedded styling in base template
- **HTML Templates**: Jinja2 template inheritance structure

### File System Dependencies
- **Document Files**: Local text files for IDOR vulnerability demonstration
- **Template Directory**: Flask template discovery and rendering
- **Session Storage**: Flask's default session implementation

Note: The application uses intentionally vulnerable patterns and should only be deployed in isolated educational environments. All security vulnerabilities are implemented by design for learning purposes.