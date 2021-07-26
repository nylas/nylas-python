from nylas.client.restful_models import RestfulModel, Message, File, Contact
import re


def _add_options_to_body(body, options):
    options_dict = options.__dict__
    # Only append set options to body to prevent a 400 error
    options_filtered = {k: v for k, v in options_dict.items() if v is not None}
    return body.update(options_filtered)


class Neural(RestfulModel):
    def __init__(self, api):
        RestfulModel.__init__(self, Neural, api)

    def sentiment_analysis_message(self, message_ids):
        body = {"message_id": message_ids}
        return self.api._request_neural_resource(NeuralSentimentAnalysis, body)

    def sentiment_analysis_text(self, text):
        body = {"text": text}
        return self.api._request_neural_resource(NeuralSentimentAnalysis, body)

    def extract_signature(self, message_ids, parse_contacts=None, options=None):
        body = {"message_id": message_ids}
        if parse_contacts is not None and isinstance(parse_contacts, bool):
            body["parse_contacts"] = parse_contacts
        if options is not None and isinstance(options, NeuralMessageOptions):
            _add_options_to_body(body, options)
        signatures = self.api._request_neural_resource(NeuralSignatureExtraction, body)
        if parse_contacts is not False:
            for sig in signatures:
                sig.contacts = NeuralSignatureContact.create(self.api, **sig.contacts)
        return signatures

    def ocr_request(self, file_id, pages=None):
        body = {"file_id": file_id}
        if pages is not None and isinstance(pages, list):
            body["pages"] = pages
        return self.api._request_neural_resource(NeuralOcr, body)

    def categorize(self, message_ids):
        body = {"message_id": message_ids}
        categorized = self.api._request_neural_resource(NeuralCategorizer, body)
        for message in categorized:
            message.categorizer = Categorize.create(self.api, **message.categorizer)
        return categorized

    def clean_conversation(self, message_ids, options=None):
        body = {"message_id": message_ids}
        if options is not None and isinstance(options, NeuralMessageOptions):
            _add_options_to_body(body, options)
        return self.api._request_neural_resource(NeuralCleanConversation, body)


class NeuralMessageOptions:
    def __init__(
        self,
        ignore_links=None,
        ignore_images=None,
        ignore_tables=None,
        remove_conclusion_phrases=None,
        images_as_markdowns=None,
    ):
        self.ignore_links = ignore_links
        self.ignore_images = ignore_images
        self.ignore_tables = ignore_tables
        self.remove_conclusion_phrases = remove_conclusion_phrases
        self.images_as_markdowns = images_as_markdowns


class NeuralSentimentAnalysis(RestfulModel):
    attrs = [
        "account_id",
        "sentiment",
        "sentiment_score",
        "processed_length",
        "text",
    ]
    collection_name = "sentiment"

    def __init__(self, api):
        RestfulModel.__init__(self, NeuralSentimentAnalysis, api)


class NeuralSignatureExtraction(Message):
    attrs = Message.attrs + ["signature", "model_version", "contacts"]
    collection_name = "signature"

    def __init__(self, api):
        RestfulModel.__init__(self, NeuralSignatureExtraction, api)


class NeuralSignatureContact(RestfulModel):
    attrs = ["job_titles", "links", "phone_numbers", "emails", "names"]
    collection_name = "signature_contact"

    def __init__(self, api):
        RestfulModel.__init__(self, NeuralSignatureContact, api)

    def to_contact_object(self):
        contact = {}
        if self.names is not None:
            contact["given_name"] = self.names[0]["first_name"]
            contact["surname"] = self.names[0]["last_name"]
        if self.job_titles is not None:
            contact["job_title"] = self.job_titles[0]
        if self.emails is not None:
            contact["emails"] = []
            for email in self.emails:
                contact["emails"].append({"type": "personal", "email": email})
        if self.phone_numbers is not None:
            contact["phone_numbers"] = []
            for number in self.phone_numbers:
                contact["phone_numbers"].append({"type": "mobile", "number": number})
        if self.links is not None:
            contact["web_pages"] = []
            for url in self.links:
                description = url["description"] if url["description"] else "homepage"
                contact["web_pages"].append({"type": description, "url": url["url"]})

        return Contact.create(self.api, **contact)


class NeuralCategorizer(Message):
    attrs = Message.attrs + ["categorizer"]
    collection_name = "categorize"

    def __init__(self, api):
        RestfulModel.__init__(self, NeuralCategorizer, api)

    def recategorize(self, category):
        data = {"message_id": self.id, "category": category}
        self.api._request_neural_resource(
            NeuralCategorizer, data, "categorize/feedback", "POST"
        )
        data = {"message_id": self.id}
        response = self.api._request_neural_resource(NeuralCategorizer, data)
        categorize = response[0]
        if categorize.categorizer:
            categorize.categorizer = Categorize.create(
                self.api, **categorize.categorizer
            )
        return categorize


class Categorize(RestfulModel):
    attrs = ["category", "categorized_at", "model_version", "subcategories"]
    datetime_attrs = {"categorized_at": "categorized_at"}
    collection_name = "category"

    def __init__(self, api):
        RestfulModel.__init__(self, Categorize, api)


class NeuralCleanConversation(Message):
    attrs = Message.attrs + [
        "conversation",
        "model_version",
    ]
    collection_name = "conversation"

    def __init__(self, api):
        RestfulModel.__init__(self, NeuralCleanConversation, api)

    def extract_images(self):
        pattern = "[\(']cid:(.*?)[\)']"
        file_ids = re.findall(pattern, self.conversation)
        files = []
        for match in file_ids:
            files.append(self.api.files.get(match))
        return files


class NeuralOcr(File):
    attrs = File.attrs + [
        "ocr",
        "processed_pages",
    ]
    collection_name = "ocr"

    def __init__(self, api):
        RestfulModel.__init__(self, NeuralOcr, api)
