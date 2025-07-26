import json
import random
from typing import Dict, List, Any, Optional


# --- 1. Gemini API Integration (Simulated) ---

class GeminiAPI:
    """
    Simulates interaction with the Gemini API for natural language understanding
    and response generation. In a real application, this would make actual
    API calls.
    """

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.chat_history = []

    async def generate_content(self, prompt: str, schema: Optional[Dict] = None) -> Dict:
        """
        Simulates generating content using the Gemini API.
        If a schema is provided, it simulates a structured response.
        """
        print(f"DEBUG: GeminiAPI received prompt: '{prompt}'")
        self.chat_history.append({"role": "user", "parts": [{"text": prompt}]})

        # Simulate API call
        # In a real scenario, you would use a library like google-generative-ai
        # and make a fetch call as described in the instructions.
        # Example fetch structure:
        # const payload = { contents: chatHistory, generationConfig: { responseMimeType: "application/json", responseSchema: schema } };
        # const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${self.api_key}`;
        # const response = await fetch(apiUrl, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        # result = await response.json();

        # For this simulation, we'll return a placeholder response
        if schema:
            # Simulate a structured response based on a simple prompt analysis
            if "shelter" in prompt.lower():
                simulated_response = {
                    "type": "shelter_request",
                    "location_preference": "any",
                    "beds_needed": 1,
                    "pet_friendly": False
                }
            elif "job" in prompt.lower():
                simulated_response = {
                    "type": "job_request",
                    "skills": ["cooking", "cleaning"],
                    "job_type": "part-time"
                }
            elif "upskill" in prompt.lower() or "course" in prompt.lower():
                simulated_response = {
                    "type": "upskill_request",
                    "interest": "IT",
                    "time_commitment": "flexible"
                }
            else:
                simulated_response = {"message": "Understood. How can I help further?"}

            # Ensure the simulated response conforms to the schema if possible
            # This is a basic simulation; real schema validation would be more complex
            if "responseSchema" in schema:
                # For simplicity, we'll just return the simulated_response
                # In a real scenario, you'd ensure it matches the schema
                pass

            result = {"candidates": [{"content": {"parts": [{"text": json.dumps(simulated_response)}]}}]}
        else:
            result = {"candidates": [{"content": {"parts": [{"text": "I understand. Please provide more details."}]}}]}

        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0][
            "content"].get("parts"):
            response_text = result["candidates"][0]["content"]["parts"][0]["text"]
            self.chat_history.append({"role": "model", "parts": [{"text": response_text}]})
            return {"text": response_text}
        else:
            print("ERROR: Gemini API response structure unexpected.")
            return {"text": "Error: Could not process your request."}


# --- 2. Resource Database Tool (Simulated) ---

class ResourceDatabase:
    """
    Simulates a database for various resources.
    In a real application, this would interact with a persistent database
    like Firestore, PostgreSQL, etc.
    """

    def __init__(self):
        self.individuals = [
            {"id": "ind001", "name": "Alice", "needs": ["shelter"], "skills": ["cooking"], "location": "Central"},
            {"id": "ind002", "name": "Bob", "needs": ["job", "upskilling"], "skills": ["cleaning", "basic IT"],
             "location": "North"},
            {"id": "ind003", "name": "Charlie", "needs": ["shelter", "job"], "skills": ["driving"],
             "location": "South"},
        ]
        self.micro_courses = [
            {"id": "mc001", "name": "Basic IT Skills", "duration": "2 weeks", "cost": 0, "availability": True,
             "skills_gained": ["basic IT"]},
            {"id": "mc002", "name": "Food Hygiene Cert", "duration": "1 week", "cost": 0, "availability": True,
             "skills_gained": ["cooking", "food prep"]},
            {"id": "mc003", "name": "Customer Service Basics", "duration": "3 weeks", "cost": 0, "availability": False,
             "skills_gained": ["customer service"]},
        ]
        self.properties = [
            {"id": "prop001", "name": "Community Shelter A", "type": "shelter", "location": "Central",
             "beds_available": 5, "pet_friendly": False, "contact": "555-1001"},
            {"id": "prop002", "name": "Northside Hostel", "type": "shelter", "location": "North", "beds_available": 2,
             "pet_friendly": True, "contact": "555-1002"},
            {"id": "prop003", "name": "South End Apartments", "type": "housing", "location": "South",
             "units_available": 1, "pet_friendly": False, "contact": "555-1003"},
        ]
        self.skills = [
            {"id": "skill001", "name": "cooking", "demand": "high"},
            {"id": "skill002", "name": "cleaning", "demand": "medium"},
            {"id": "skill003", "name": "basic IT", "demand": "high"},
            {"id": "skill004", "name": "driving", "demand": "low"},
        ]
        self.jobs = [
            {"id": "job001", "title": "Kitchen Assistant", "location": "Central", "type": "part-time",
             "skills_required": ["cooking", "food prep"], "availability": True, "contact": "555-2001"},
            {"id": "job002", "title": "Office Cleaner", "location": "North", "type": "full-time",
             "skills_required": ["cleaning"], "availability": True, "contact": "555-2002"},
            {"id": "job003", "title": "Delivery Driver", "location": "South", "type": "part-time",
             "skills_required": ["driving"], "availability": False, "contact": "555-2003"},
        ]

    def query_individuals(self, **kwargs) -> List[Dict]:
        """Queries individuals based on provided criteria."""
        results = self.individuals
        for key, value in kwargs.items():
            results = [ind for ind in results if
                       ind.get(key) == value or (isinstance(ind.get(key), list) and value in ind.get(key))]
        return results

    def query_micro_courses(self, **kwargs) -> List[Dict]:
        """Queries micro-courses based on provided criteria."""
        results = self.micro_courses
        for key, value in kwargs.items():
            results = [mc for mc in results if
                       mc.get(key) == value or (isinstance(mc.get(key), list) and value in mc.get(key))]
        return [mc for mc in results if mc["availability"]]  # Only available courses

    def query_properties(self, **kwargs) -> List[Dict]:
        """Queries properties (shelters/housing) based on provided criteria."""
        results = self.properties
        for key, value in kwargs.items():
            results = [prop for prop in results if
                       prop.get(key) == value or (isinstance(prop.get(key), list) and value in prop.get(key))]
        # Filter by availability for shelters/housing
        return [prop for prop in results if prop.get("beds_available", 0) > 0 or prop.get("units_available", 0) > 0]

    def query_jobs(self, **kwargs) -> List[Dict]:
        """Queries job opportunities based on provided criteria."""
        results = self.jobs
        for key, value in kwargs.items():
            results = [job for job in results if
                       job.get(key) == value or (isinstance(job.get(key), list) and value in job.get(key))]
        return [job for job in results if job["availability"]]  # Only available jobs


# --- 3. Personalized Matching Algorithm ---

class MatchingAlgorithm:
    """
    Implements logic to match individuals with suitable resources
    (shelter, jobs, upskilling).
    """

    def __init__(self, db: ResourceDatabase):
        self.db = db

    def match_shelter(self, user_preferences: Dict) -> List[Dict]:
        """
        Matches shelters based on user preferences.
        `user_preferences` can include location, pet_friendly, beds_needed.
        """
        location = user_preferences.get("location_preference", "any")
        pet_friendly = user_preferences.get("pet_friendly", False)
        beds_needed = user_preferences.get("beds_needed", 1)

        eligible_shelters = self.db.query_properties(type="shelter", pet_friendly=pet_friendly)

        # Filter by location
        if location != "any":
            eligible_shelters = [s for s in eligible_shelters if s["location"].lower() == location.lower()]

        # Filter by beds available
        eligible_shelters = [s for s in eligible_shelters if s.get("beds_available", 0) >= beds_needed]

        # Simple proximity simulation: prioritize based on a predefined order or just return all
        return sorted(eligible_shelters, key=lambda x: x.get("beds_available", 0), reverse=True)

    def match_jobs(self, user_preferences: Dict) -> List[Dict]:
        """
        Matches jobs based on user skills and preferences.
        `user_preferences` can include skills, job_type (full-time/part-time).
        """
        user_skills = user_preferences.get("skills", [])
        job_type = user_preferences.get("job_type", "any")

        eligible_jobs = self.db.query_jobs()

        # Filter by job type
        if job_type != "any":
            eligible_jobs = [job for job in eligible_jobs if job["type"].lower() == job_type.lower()]

        # Match based on skills: prioritize jobs requiring user's skills
        matched_jobs = []
        for job in eligible_jobs:
            required_skills = set(job.get("skills_required", []))
            if required_skills.issubset(set(user_skills)):
                matched_jobs.append(job)

        # Sort by number of matching skills (more matches first)
        matched_jobs.sort(key=lambda job: sum(1 for skill in job.get("skills_required", []) if skill in user_skills),
                          reverse=True)
        return matched_jobs

    def match_upskilling(self, user_preferences: Dict) -> List[Dict]:
        """
        Matches micro-courses based on user interests and skills.
        `user_preferences` can include interest, time_commitment.
        """
        user_interest = user_preferences.get("interest", "any")
        time_commitment = user_preferences.get("time_commitment", "any")

        eligible_courses = self.db.query_micro_courses()

        # Filter by interest (simple keyword match)
        if user_interest != "any":
            eligible_courses = [mc for mc in eligible_courses if user_interest.lower() in mc["name"].lower() or any(
                user_interest.lower() in s.lower() for s in mc.get("skills_gained", []))]

        # Filter by time commitment (simulated)
        if time_commitment == "flexible":
            # Assume all courses are flexible for this simulation
            pass

        return eligible_courses


# --- 4. Simulated "Call Initiator" Tool ---

class CallInitiator:
    """
    Simulates initiating a call to confirm availability.
    """

    def __init__(self):
        pass

    def confirm_availability(self, resource_name: str, contact_info: str) -> Dict[str, Any]:
        """
        Simulates making a call to confirm the availability of a resource.
        Returns a dictionary with 'success' (boolean) and 'message'.
        """
        print(f"DEBUG: Simulating call to {resource_name} at {contact_info}...")
        # Simulate a random outcome for demonstration
        is_available = random.choice([True, False])
        if is_available:
            message = f"Successfully confirmed availability for {resource_name}."
        else:
            message = f"Could not confirm availability for {resource_name}. It might be full or unavailable."
        return {"success": is_available, "message": message}


# --- Executor Module ---

class AgentExecutor:
    """
    The main executor module that orchestrates the agent's actions,
    integrating Gemini API, database queries, matching algorithms,
    and call initiation.
    """

    def __init__(self, gemini_api_key: str = ""):
        self.gemini = GeminiAPI(api_key=gemini_api_key)
        self.db = ResourceDatabase()
        self.matcher = MatchingAlgorithm(db=self.db)
        self.caller = CallInitiator()

    async def execute_request(self, user_query: str) -> Dict:
        """
        Processes a user query, uses Gemini for understanding,
        queries resources, performs matching, and simulates calls.
        """
        print(f"Executor received user query: '{user_query}'")

        # Step 1: Use Gemini to understand the user's intent and extract preferences
        # Define a schema for structured output from Gemini
        intent_schema = {
            "type": "OBJECT",
            "properties": {
                "intent": {"type": "STRING", "enum": ["shelter", "job", "upskill", "general_query"]},
                "details": {
                    "type": "OBJECT",
                    "properties": {
                        "location_preference": {"type": "STRING"},
                        "beds_needed": {"type": "INTEGER"},
                        "pet_friendly": {"type": "BOOLEAN"},
                        "skills": {"type": "ARRAY", "items": {"type": "STRING"}},
                        "job_type": {"type": "STRING", "enum": ["full-time", "part-time", "any"]},
                        "interest": {"type": "STRING"},
                        "time_commitment": {"type": "STRING"}
                    }
                }
            }
        }

        gemini_response = await self.gemini.generate_content(
            f"Analyze the following user request and extract their primary intent (shelter, job, upskill, general_query) and any relevant details (location, beds needed, pet friendly, skills, job type, interest, time commitment) in JSON format:\n\nUser request: '{user_query}'",
            schema={"responseSchema": intent_schema}
        )

        try:
            parsed_gemini_response = json.loads(gemini_response["text"])
            intent = parsed_gemini_response.get("intent")
            details = parsed_gemini_response.get("details", {})
            print(f"DEBUG: Parsed Gemini Intent: {intent}, Details: {details}")
        except json.JSONDecodeError:
            print(f"ERROR: Could not parse Gemini response: {gemini_response['text']}")
            return {"status": "error", "message": "Could not understand your request. Please try again."}

        response_message = ""
        recommended_resources = []

        if intent == "shelter":
            recommended_resources = self.matcher.match_shelter(details)
            if recommended_resources:
                response_message = "Here are some shelters that match your criteria:\n"
                for res in recommended_resources:
                    response_message += f"- {res['name']} ({res['location']}), Beds: {res.get('beds_available', 'N/A')}, Pet-friendly: {res['pet_friendly']}. Contact: {res['contact']}\n"
                    # Simulate call confirmation for the first one
                    call_result = self.caller.confirm_availability(res['name'], res['contact'])
                    response_message += f"  (Call confirmation: {call_result['message']})\n"
            else:
                response_message = "I couldn't find any shelters matching your preferences at the moment."

        elif intent == "job":
            recommended_resources = self.matcher.match_jobs(details)
            if recommended_resources:
                response_message = "Here are some job opportunities that match your skills:\n"
                for res in recommended_resources:
                    response_message += f"- {res['title']} ({res['location']}), Type: {res['type']}, Skills: {', '.join(res.get('skills_required', []))}. Contact: {res['contact']}\n"
                    # Simulate call confirmation for the first one
                    call_result = self.caller.confirm_availability(res['title'], res['contact'])
                    response_message += f"  (Call confirmation: {call_result['message']})\n"
            else:
                response_message = "I couldn't find any job opportunities matching your skills at the moment."

        elif intent == "upskill":
            recommended_resources = self.matcher.match_upskilling(details)
            if recommended_resources:
                response_message = "Here are some micro-courses for upskilling:\n"
                for res in recommended_resources:
                    response_message += f"- {res['name']} (Duration: {res['duration']}), Skills gained: {', '.join(res.get('skills_gained', []))}. Available: {res['availability']}\n"
                    # For courses, we might not need a "call initiator" but a direct check
                    # For simulation, we'll just show availability
            else:
                response_message = "I couldn't find any upskilling courses matching your interests at the moment."

        else:  # general_query or fallback
            response_message = gemini_response["text"]  # Use the direct Gemini response for general queries

        return {
            "status": "success",
            "message": response_message,
            "recommended_resources": recommended_resources
        }


# Example Usage (for testing the module)
async def main():
    executor = AgentExecutor(gemini_api_key="YOUR_GEMINI_API_KEY")  # Replace with your actual key

    print("\n--- Test Case 1: Shelter Request ---")
    response = await executor.execute_request("I need a shelter, preferably in the North, and I have a small dog.")
    print(response["message"])

    print("\n--- Test Case 2: Job Request ---")
    response = await executor.execute_request("I'm looking for a part-time job. I have skills in cooking and basic IT.")
    print(response["message"])

    print("\n--- Test Case 3: Upskilling Request ---")
    response = await executor.execute_request("I want to learn something new, maybe in IT, and I'm flexible with time.")
    print(response["message"])

    print("\n--- Test Case 4: General Query ---")
    response = await executor.execute_request("What kind of help can you provide?")
    print(response["message"])

# To run this example, uncomment the following lines and execute the script:
# import asyncio
# if __name__ == "__main__":
#     asyncio.run(main())
