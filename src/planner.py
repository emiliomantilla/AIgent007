import enum
from typing import Dict, Any, List, Optional

# --- Enums for clarity and consistency ---

class Intent(enum.Enum):
    """
    Defines the primary intent categories for user queries.
    """
    HOUSING = "housing" #user requires housing
    FOOD = "food"
    MEDICAL = "medical"  # user requires medical attention
    UPSKILL = "upskill" #user wants to improve skills
    WORK = "work" #user looking for full or part-time work
    UNKNOWN = "unknown" # When intent cannot be clearly discerned

class TaskType(enum.Enum):
    """
    Defines the types of sub-tasks the planner can generate.
    """
    FETCH_HOUSING = "fetch_housing"
    FETCH_FOOD_SERVICES = "fetch_food_services"
    FETCH_MEDICAL_AID = "fetch_medical_aid"
    FETCH_UPSKILLING_COURSES = "fetch_upskilling_courses"
    FETCH_EMPLOYMENT_OPPORTUNITIES = "fetch_employment_opportunities"
    INTEGRATE_PREFERENCES = "integrate_preferences"
    CHECK_AVAILABILITY = "check_availability"
    SORT_BY_PROXIMITY = "sort_by_proximity"
    FORMAT_OUTPUT = "format_output"
    ESCALATE_TO_HUMAN = "escalate_to_human"

# --- Planner Module ---

class IntentPlanner:
    """
    A planner module for an agentic AI to discern user intent and
    generate a sequence of sub-tasks for personalized assistance to
    homeless individuals.
    """

    def __init__(self):
        """
        Initializes the IntentPlanner.
        In a real system, this might load intent classification models
        or configuration for data sources.
        """
        print("IntentPlanner initialized. Ready to discern intents and plan tasks.")

    def discern_intent(self, user_query: str) -> Intent:
        """
        Discserns the primary intent from a user's natural language query.

        Args:
            user_query (str): The raw text query from the user.

        Returns:
            Intent: The discerned primary intent (IMMEDIATE_AID, LONG_TERM_GROWTH, or UNKNOWN).

        Note:
            For this example, a simple keyword-based approach is used.
            In a production system, this would typically involve:
            -   Natural Language Understanding (NLU) models.
            -   Machine Learning (ML) for intent classification.
            -   Integration with a large language model (LLM) for more nuanced understanding.
        """
        query_lower = user_query.lower()

        # Keywords for Immediate Aid
        housing_keywords = [
            "shelter", "bed", "sleep", "food", "eat", "meal", "hungry",
            "doctor", "medical", "clinic", "emergency", "safe place", "tonight"
        ]
        if any(keyword in query_lower for keyword in housing_keywords):
            return Intent.HOUSING

        food_keywords = [
            "food", "eat", "meal", "hungry" ]
        if any(keyword in query_lower for keyword in food_keywords):
            return Intent.FOOD

        # Keywords for medical aid
        medical_keywords = [
            "doctor", "medical", "clinic", "emergency"
        ]
        if any(keyword in query_lower for keyword in medical_keywords):
            return Intent.MEDICAL

        # Keywords for upskilling
        upskill_keywords = [
            "learn", "course", "skill", "career", "training", "upskill"
        ]
        if any(keyword in query_lower for keyword in upskill_keywords):
            return Intent.UPSKILL

        # Keywords for finding work
        work_keywords = [
            "job", "work", "employment", "find a job", "get a job"
        ]
        if any(keyword in query_lower for keyword in work_keywords):
            return Intent.WORK

        return Intent.UNKNOWN

    def plan_subtasks(
        self,
        intent: Intent,
        user_preferences: Dict[str, Any],
        user_location: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Plans a sequence of sub-tasks based on the discerned intent and user data.

        Args:
            intent (Intent): The primary intent discerned from the user query.
            user_preferences (Dict[str, Any]): A dictionary of user preferences
                                                (e.g., {'housing_type': 'family', 'pets': True,
                                                'skills_interest': 'IT', 'work_availability': 'evenings'}).
            user_location (Optional[Dict[str, float]]): User's current location,
                                                         e.g., {'latitude': 51.5, 'longitude': -0.1}.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a sub-task
                                  with its type and parameters.
        """
        sub_tasks: List[Dict[str, Any]] = []

        # Always start with integrating preferences if they exist and are relevant
        if user_preferences:
            sub_tasks.append({
                "task_type": TaskType.INTEGRATE_PREFERENCES.value,
                "parameters": user_preferences
            })

        if intent in (Intent.HOUSING, Intent.FOOD, Intent.MEDICAL):
            print(f"Planning sub-tasks for IMMEDIATE_AID based on preferences: {user_preferences}")
            # Determine specific immediate aid needs based on query/preferences
            if "shelter" in user_preferences.get("aid_needs", []) or \
               "housing" in user_preferences.get("aid_needs", []) or \
               "bed" in user_preferences.get("aid_needs", []):
                sub_tasks.append({
                    "task_type": TaskType.FETCH_HOUSING.value,
                    "parameters": {"type": "emergency", **user_preferences}
                })
            if "food" in user_preferences.get("aid_needs", []) or \
               "meal" in user_preferences.get("aid_needs", []) or \
               "hungry" in user_preferences.get("aid_needs", []):
                sub_tasks.append({
                    "task_type": TaskType.FETCH_FOOD_SERVICES.value,
                    "parameters": user_preferences
                })
            if "medical" in user_preferences.get("aid_needs", []) or \
               "doctor" in user_preferences.get("aid_needs", []):
                sub_tasks.append({
                    "task_type": TaskType.FETCH_MEDICAL_AID.value,
                    "parameters": user_preferences
                })

            # Add availability and proximity checks for immediate aid
            sub_tasks.append({
                "task_type": TaskType.CHECK_AVAILABILITY.value,
                "parameters": {"service_type": "immediate_aid"}
            })
            if user_location:
                sub_tasks.append({
                    "task_type": TaskType.SORT_BY_PROXIMITY.value,
                    "parameters": {"location": user_location}
                })
            sub_tasks.append({
                "task_type": TaskType.FORMAT_OUTPUT.value,
                "parameters": {"format": "concise_list_with_contacts"}
            })

        elif intent in (Intent.UPSKILL, Intent.WORK):
            print(f"Planning sub-tasks for LONG_TERM_GROWTH based on preferences: {user_preferences}")
            # Determine specific long-term growth needs
            if "upskilling" in user_preferences.get("growth_needs", []) or \
               "learn" in user_preferences.get("growth_needs", []) or \
               "course" in user_preferences.get("growth_needs", []):
                sub_tasks.append({
                    "task_type": TaskType.FETCH_UPSKILLING_COURSES.value,
                    "parameters": {"skill_interest": user_preferences.get("skills_interest"), **user_preferences}
                })
            if "employment" in user_preferences.get("growth_needs", []) or \
               "job" in user_preferences.get("growth_needs", []) or \
               "work" in user_preferences.get("growth_needs", []):
                sub_tasks.append({
                    "task_type": TaskType.FETCH_EMPLOYMENT_OPPORTUNITIES.value,
                    "parameters": {"job_type": user_preferences.get("job_type"), **user_preferences}
                })

            # Add availability and proximity checks for long-term growth (e.g., course start dates, job locations)
            sub_tasks.append({
                "task_type": TaskType.CHECK_AVAILABILITY.value,
                "parameters": {"service_type": "long_term_growth"}
            })
            if user_location:
                sub_tasks.append({
                    "task_type": TaskType.SORT_BY_PROXIMITY.value,
                    "parameters": {"location": user_location}
                })
            sub_tasks.append({
                "task_type": TaskType.FORMAT_OUTPUT.value,
                "parameters": {"format": "detailed_list_with_links"}
            })

        elif intent == Intent.UNKNOWN:
            print("Unknown intent. Planning to ask for clarification or escalate.")
            sub_tasks.append({
                "task_type": TaskType.ESCALATE_TO_HUMAN.value,
                "parameters": {"reason": "intent_unclear", "user_query": user_query}
            })
            sub_tasks.append({
                "task_type": TaskType.FORMAT_OUTPUT.value,
                "parameters": {"format": "clarification_prompt"}
            })

        return sub_tasks

# --- Example Usage (for testing the module) ---
if __name__ == "__main__":
    planner = IntentPlanner()

    # --- Test Case 1: Immediate Aid (Shelter) ---
    print("\n--- Test Case 1: Immediate Aid (Shelter) ---")
    query1 = "I need a place to sleep tonight, somewhere safe."
    preferences1 = {"aid_needs": ["shelter"], "housing_type": "safe", "pets": False}
    location1 = {"latitude": 51.5074, "longitude": -0.1278} # London city center

    intent1 = planner.discern_intent(query1)
    print(f"User Query: '{query1}' -> Discerned Intent: {intent1.value}")
    tasks1 = planner.plan_subtasks(intent1, preferences1, location1)
    for i, task in enumerate(tasks1):
        print(f"  Task {i+1}: {task['task_type']} with parameters {task['parameters']}")

    # --- Test Case 2: Long-Term Growth (Upskilling) ---
    print("\n--- Test Case 2: Long-Term Growth (Upskilling) ---")
    query2 = "I want to learn some new skills, maybe something in IT."
    preferences2 = {"growth_needs": ["upskilling"], "skills_interest": "IT", "learning_format": "online"}
    location2 = None # User might not provide location for online courses

    intent2 = planner.discern_intent(query2)
    print(f"User Query: '{query2}' -> Discerned Intent: {intent2.value}")
    tasks2 = planner.plan_subtasks(intent2, preferences2, location2)
    for i, task in enumerate(tasks2):
        print(f"  Task {i+1}: {task['task_type']} with parameters {task['parameters']}")

    # --- Test Case 3: Immediate Aid (Food) ---
    print("\n--- Test Case 3: Immediate Aid (Food) ---")
    query3 = "I'm really hungry, where can I get a meal?"
    preferences3 = {"aid_needs": ["food"], "dietary_restrictions": "vegetarian"}
    location3 = {"latitude": 51.5154, "longitude": -0.1419} # Oxford Street area

    intent3 = planner.discern_intent(query3)
    print(f"User Query: '{query3}' -> Discerned Intent: {intent3.value}")
    tasks3 = planner.plan_subtasks(intent3, preferences3, location3)
    for i, task in enumerate(tasks3):
        print(f"  Task {i+1}: {task['task_type']} with parameters {task['parameters']}")

    # --- Test Case 4: Unknown Intent ---
    print("\n--- Test Case 4: Unknown Intent ---")
    query4 = "Tell me a joke."
    preferences4 = {}
    location4 = None

    intent4 = planner.discern_intent(query4)
    print(f"User Query: '{query4}' -> Discerned Intent: {intent4.value}")
    tasks4 = planner.plan_subtasks(intent4, preferences4, location4)
    for i, task in enumerate(tasks4):
        print(f"  Task {i+1}: {task['task_type']} with parameters {task['parameters']}")

    # --- Test Case 5: Long-Term Growth (Employment) ---
    print("\n--- Test Case 5: Long-Term Growth (Employment) ---")
    query5 = "I'm looking for part-time work, maybe in retail."
    preferences5 = {"growth_needs": ["employment"], "job_type": "retail", "work_availability": "weekends"}
    location5 = {"latitude": 51.4998, "longitude": -0.1749} # Knightsbridge area

    intent5 = planner.discern_intent(query5)
    print(f"User Query: '{query5}' -> Discerned Intent: {intent5.value}")
    tasks5 = planner.plan_subtasks(intent5, preferences5, location5)
    for i, task in enumerate(tasks5):
        print(f"  Task {i+1}: {task['task_type']} with parameters {task['parameters']}")
