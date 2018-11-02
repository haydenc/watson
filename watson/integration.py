import json

import requests


class WatsonRequestError(Exception): pass

class WatsonInvalidJSONError(WatsonRequestError): pass


class WatsonRequestManager:
    API_VERSION = "v3"
    SCHEMA = "https"
    BASE_URL = "watson-api-explorer.ng.bluemix.net/tone-analyzer/api"
    # Format here is (("TONE_CATEGORY", ("TONE", "TONE")), ("TONE_CATEGORY 2", ("TONE 3", "TONE 4")))
    EXTRACTED_TONES = {
        "emotion_tone": ("joy", "fear", "disgust", "anger", "sadness")
    }

    def get_url(self):
        return '{schema}://{base_url}/{version}/tone?sentences=false&version=2016-05-19'\
            .format(schema=self.SCHEMA, base_url=self.BASE_URL, version=self.API_VERSION)

    def analyse_tone(self, string_value):
        url = self.get_url()
        payload = {'text': string_value}
        print("DEF", json.dumps(payload))
        r = requests.post(url, data=None, json=payload)
        try:
            json_response = r.json()
        except ValueError:
            raise WatsonInvalidJSONError("Invalid JSON")
        else:
            self.check_response(json_response)
            return self.process_response(json_response)

    @staticmethod
    def check_response(json_response):
        # TODO: This should probably be a little more sophisticated
        if "error" in json_response:
            print(json_response)
            raise WatsonRequestError("Watson API error - {error}".format(error=json_response["error"]))

    def process_response(self, json_response):
        from watson.models import WatsonAnalysisResults # Avoiding circular imports

        print("ABC", json_response)

        extracted_tones = {}
        for tone_category in json_response["document_tone"]["tone_categories"]:
            category_extracts = self.EXTRACTED_TONES.get(tone_category["category_id"], [])
            for tone in tone_category["tones"]:
                if tone["tone_id"] in category_extracts:
                    extracted_tones[tone["tone_id"]] = tone["score"]

        result_kwargs = extracted_tones.copy()
        result_kwargs["watson_json"] = json_response

        # Note that we are returning an unsaved results object - must be saved upstream!
        results_obj = WatsonAnalysisResults(**result_kwargs)
        return results_obj
