import json
from random import random
from urllib.parse import urlencode

import requests
from fastapi.exceptions import HTTPException

from app.core.config import settings


class SymptomsService:
    base_url = settings.SYMPTOM_SERVICE_URL

    def __init__(self, birth_year: int, body_part: str, gender: str):
        self.birth_year = birth_year
        self.body_part = body_part
        self.gender = gender
        self.cookie = None

    def get(self, path):
        url = f"{self.base_url}/{path}"
        response = requests.get(url)
        return response

    def post(self, path, data):
        response = requests.post(path, data=data)
        res = response.json()
        return res

    def initialize(self):
        data = {
            "command": "changeSelectedYear",
            "year": self.birth_year,
            "rand": random(),
        }
        res = requests.post(
            f"{self.base_url}/start", data=data, cookies=self.cookie
        )
        if not res:
            return False

        self.cookie = res.cookies

        data["command"] = "changeGenderAndStatus"
        data["rand"] = random()
        data["gender"], data["status"] = self.get_gender_code(self.gender)
        res = requests.post(
            f"{self.base_url}/start", data=data, cookies=self.cookie
        )
        if not res:
            return False

        self.cookie = res.cookies

        return res.status_code == 200

    def get_gender_code(self, gender: str) -> tuple[int, int]:
        genders = {
            "male": (
                1,
                0,
            ),
            "female": (
                2,
                1,
            ),
        }
        return genders.get(gender)

    def get_body_part_code(self, body_part: str):
        parts = {
            "head": 6,
            "upperbody": 15,
            "lowerbody": 16,
            "legs": 10,
            "arms": 7,
            "general": 17,
        }
        return parts.get(body_part)

    def get_symptoms(self) -> dict[str, list[dict]]:
        part_code = self.get_body_part_code(self.body_part)

        res = self.initialize()
        if not res:
            return False

        data = {
            "command": "getSymptoms",
            "locationId": part_code,
            "rand": random(),
        }
        res = self.post(f"{self.base_url}/start", data)
        if not res:
            return False

        return {
            d["Location"]: [
                {
                    "id": y["ID"],
                    "name": y["Name"],
                    "is_critical": y["HasRedFlag"],
                }
                for y in d["Items"]
            ]
            for d in res
        }

    def get_diseases_from_symptoms(
        self, ids: list[int]
    ) -> dict[str, list[dict]]:

        data = None

        res = self.initialize()
        if not res:
            return False

        for id in ids:
            rand = random()
            data = {
                "command": "addSymptom",
                "symptomId": id,
                "has_red_flag:": False,
                "rand": rand,
            }
            res = requests.post(
                self.base_url,
                data=data,
                cookies=self.cookie,
            )
            self.cookie = res.cookies

            data = {
                "command": "getDiagnoses",
                "rand": random(),
            }
            res = requests.get(self.base_url, params=data, cookies=self.cookie)

            if not res:
                return False

            try:
                self.cookie = res.cookies
                data = res.json()
            except:
                raise HTTPException(
                    400,
                    "Unable to process the request. Please check your symptom ids.",
                )

        return {
            "diagnosis": [
                {
                    "id": y["IssueID"],
                    "name": y["Name"],
                    "accuracy": y["Accuracy"],
                }
                for y in data["DiagnosisResult"]
            ],
            "similar_symptoms": [
                {
                    "id": y["ID"],
                    "name": y["Name"],
                }
                for y in data["ProposedSymptoms"]
            ],
        }

    def get_condition_details(self, diagnosis_id: int) -> dict[str, list[dict]]:
        res = self.initialize()
        if not res:
            return False

        data = {
            "command": "getIssueInfo",
            "healthIssueId": diagnosis_id,
        }
        res = requests.get(self.base_url, params=data, cookies=self.cookie)
        if not res:
            return False
        res = res.json()

        return {
            "name": res["Name"],
            "description": res["Description"],
            "medical_term": res["ProfName"],
            "treatment": res["TreatmentDescription"],
        }
