from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
import datetime

class GarminApi:
    def __init__(self, username, password):
        self.g = Garmin(username, password)
        self.today = datetime.date.today().isoformat()

        self.g.login()

    # END __init__
        
    def get_step_data(self):
        data = self.g.get_daily_steps(self.today, self.today)[0]
        return ({
            "steps" : data["totalSteps"],
            "step_goal" : data["stepGoal"],
        })

    # END get_step_data

    def get_hr_data(self):
        data = self.g.get_heart_rates(self.today)
        return ({
            "current_hr" : data["heartRateValues"][len(data["heartRateValues"])-1][1],
            "avg_resting_hr" : data["restingHeartRate"],
        })

    # END get_hr_data

# END GarminApi Class


