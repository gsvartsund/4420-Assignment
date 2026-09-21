from data_generator import generate_fitness_data
import random

# Uses the baseline values, and later in the code compares it to the given new values -
# -to see if the person is recovering, resting or in high activity.

class Participant:
    def __init__(self, profile):
        self.participant_id = profile["participant_id"]
        self.baseline_heart_rate = profile["baseline_heart_rate"]
        self.baseline_skin_response = profile["baseline_skin_response"]
        self.baseline_temperature = profile["baseline_temperature"]

# My observation class read a signle sensor reading at the given timestamp.
# If the reading fails in session.validate(), it is marked as invalid and the reason is stated.
class Observation:
    def __init__(self, data):
        self.timestamp = data["timestamp"]
        self.heart_rate = data["heart_rate"]
        self.skin_response = data["skin_response"]
        self.temperature = data["temperature"]
        self.activity_level = data["activity_level"]
        self.signal_quality = data["signal_quality"]
        self.valid = True
        self.reason = ""

    # If as mentioned earlier is invalid, it explains it why here.
    def invalidate(self, reason):
        self.valid = False
        self.reason = reason

# Session is the class for the persons data over the given time period.
# It takes the data given from tata generator and converts it, validates and analyzes it.
class Session:
    def __init__(self, profile, observations):
        self.participant = Participant(profile)
        self.observations = [Observation(o) for o in observations]
        self.rejected = []

    # Checks each observation against valid given ranges.
    # If a bad obsercvation is found, it is rejected and the reason is given.
    def validate(self):
        for obs in self.observations:
            reasons = []

            if obs.timestamp is None or obs.timestamp <= 0:
                reasons.append("timestamp invalid")

            if obs.heart_rate is None:
                reasons.append("missing heart rate")
            elif not (35 <= obs.heart_rate <= 205):
                reasons.append("heart rate out of range")

            if obs.skin_response is None or not (0 <= obs.skin_response <= 5):
                reasons.append("skin response out of range")

            if obs.temperature is None or not (25 <= obs.temperature <= 42):
                reasons.append("temperature out of range")

            if obs.activity_level is None:
                reasons.append("missing activity level")
            elif not (0 <= obs.activity_level <= 1):
                reasons.append("activity level out of range")

            if obs.signal_quality is None:
                reasons.append("missing signal quality")
            elif obs.signal_quality < 0.5:
                reasons.append("low signal quality")

            if reasons:
                obs.invalidate("; ".join(reasons))
                self.rejected.append((obs, obs.reason))

    # Uses only valid observations to calculate average values.
    # This gives the summmary later classifies it.
    def summarize(self):
        valid = [o for o in self.observations if o.valid]
        if not valid:
            return {"usable_count": 0}

        heart_rates = [o.heart_rate for o in valid]
        activities = [o.activity_level for o in valid]
        skin_responses = [o.skin_response for o in valid]
        temperatures = [o.temperature for o in valid]

        return {
            "usable_count": len(valid),
            "avg_heart_rate": sum(heart_rates) / len(heart_rates),
            "avg_skin_response": sum(skin_responses) / len(skin_responses),
            "avg_temperature": sum(temperatures) / len(temperatures),
            "avg_activity": sum(activities) / len(activities),
        }

    # Classifies the session based on the average activity level and heart rate observed.
    # This is a rule based approach that turns sensor data into a label, without being too complicated.
    def classify(self):
        summary = self.summarize()
        usable = summary.get("usable_count", 0)

        if usable < 3:
            return "insufficient data, unable to classify"

        avg_hr = summary["avg_heart_rate"]
        avg_activity = summary["avg_activity"]

        if avg_activity < 0.2 and avg_hr < self.participant.baseline_heart_rate * 1.1:
            return "resting"
        if avg_activity > 0.7:
            return "high activity"
        if avg_activity >= 0.25:
            return "moderate activity"
        return "recovering"

# This class is only good for presenting the results.
# The output is seperate from the actual logic, which made it easier for me to understand.
class SessionReport:
    def __init__(self, session):
        self.session = session

    # Given the example in the assignment, i am presenting it the same way to not make it harder for myself..
    def display(self):
        print(self.session.summarize())
        print(self.session.classify())


# This small snippet is where it chooses a random seed so that the data can be different-
# -each time it is ran, so i dont get the same results. Making it easier to test.
# Returns a participant profile and a list of observations.
profile, observations = generate_fitness_data(
    participant_id="P001",
    scenario="random",
    seed=random.randint(0, 10000000),
    number_of_windows=12
)

# Lastly builds the session object, validates each reading, and then prints the results.
session = Session(profile, observations)
session.validate()
report = SessionReport(session)
report.display()