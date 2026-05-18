import requests

class APIPages:
    
    def __init__(self,base_URL, header):
        self.base_URL = base_URL
        self.header = header
        self.response = None

    def create_enquiry(self):
     payload1 = { 
        "Name": "API test enquiry 2",
        "Email__c": "api@test1.com",
        "Mobile__c": "1232567803"
        
    }

     url = f"{self.base_URL}/services/data/v57.0/sobjects/Enquiry__c/"
     self.response = requests.post(url, json=payload1, headers=self.header)

     return payload1 

    def validate_enquiry_created(self):
        assert self.response.status_code == 201, f"Failed: {self.response.text}"
        assert "id" in self.response.json()
