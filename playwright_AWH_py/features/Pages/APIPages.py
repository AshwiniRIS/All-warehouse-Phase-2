import requests

class APIPages:

    def __init__(self, base_URL, header):
        self.base_URL = base_URL
        self.header = header
        self.response = None
        self.enquiry_id = None

    def create_enquiry(self, name, phone, email):

        payload = {
            "Name": name,
            "Email__c": email,
            "Mobile__c": phone
        }

        url = f"{self.base_URL}/services/data/v57.0/sobjects/Enquiry__c/"
        self.response = requests.post(url, json=payload, headers=self.header)

        print("API Response:", self.response.json())

        return self.response

    def validate_enquiry_created(self):

        assert self.response.status_code == 201, f"Failed: {self.response.text}"

        self.enquiry_id = self.response.json().get("id")
        assert self.enquiry_id is not None

        return self.enquiry_id