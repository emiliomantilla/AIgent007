AIgent007 London Aid and Growth Navigator
------------------------------------------
The project London Aid & Growth Navigator, is an AI-powered, mobile-first web tool designed for homeless individuals in London who possess smartphones. Its core purpose is twofold:
1.	Immediate Assistance: Intelligently match users with available shelters and food banks, prioritizing based on proximity, simulated real-time availability, and personalized preferences/past experiences.
2.	Medium-to-Long-Term Growth: Connect users with libraries and micro-learning courses to address skill gaps and enhance job market readiness.
The application will leverage the Google Gemini API for natural language understanding, intelligent matching, and conversational guidance, aiming to support both immediate needs and personal development.

Synthetic Data
----------------
o	Data for shelters, food banks, libraries, and micro-learning courses.
o	Ensure shelter data includes fields for simulated availability, location (lat/lon), and descriptive notes for matching preferences (e.g., "quiet," "women-only," "pet-friendly").
o	Include relevant details for libraries (e.g., computer access) and learning courses (e.g., topic, online/in-person).
o	Define a fixed "kiosk location" (still useful for demonstrating public access points, but primary focus is mobile).

Agent Development (Mobile-First Web UI)
-------------------------------------------
•	Responsive Web UI: Design the chatbot interface to be highly usable on smartphones, with adaptability for larger screens (e.g., library kiosks).
o	Implement intuitive touch screen options and a prominent voice input button.
o	Develop a clear conversational flow for both immediate aid and learning queries.
o	Include a mechanism for users to input personal preferences or past experiences for matching.
•	planner.py Module:
o	Develop logic to discern user intent for either immediate aid (shelter/food) or long-term growth (learning).
o	Plan sub-tasks for personalized matching, including preference integration, availability checks, and proximity sorting.
•	executor.py Module:
o	Gemini API Integration: Core for natural language understanding, intelligent decision-making, and generating tailored conversational responses.
o	Resource Database Tool: Query your synthetic data for all resource types (shelters, food banks, libraries, courses).
o	Personalized Matching Algorithm: Implement logic to combine availability, proximity, and user preferences to recommend the most suitable resources.
o	Simulated "Call Initiator" Tool: For shelter confirmation.
•	memory.py Module:
o	Crucial for storing user preferences, past interactions, and potentially learning interests within a session to enable personalized responses.
