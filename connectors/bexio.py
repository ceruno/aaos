import requests
import json


class BexioAPI:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        }
        self.params = {}

    def get_countries(self):
        """
        Diese Funktion liefert die Länder IDs
        """
        self.endpoint = "/2.0/country"
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_titles(self):
        """
        Diese Funktion liefert die Bexio User
        """
        self.endpoint = "/2.0/title"
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_salutations(self):
        """
        Diese Funktion liefert die Bexio User
        """
        self.endpoint = "/2.0/salutation"
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def fetch_bexio_contact(self, contact_id):
        """
        Get a bexio contact with contact_id as input
        """
        self.endpoint = "/2.0/contact/" + str(contact_id)
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_contact_relation(self):
        """
        Get the contact relation
        """
        self.endpoint = "/2.0/contact_relation"
        self.params.update({"limit": "5000"})
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_contact_relation_by_contact_sub_id(self, contact_sub_id):
        """
        # contact_sub_id = id des Kontaktes (Person)
        # contact_id = id der entsprechenden Firma
        Get the contact_id relation (company) from contact_sub_id (person)
        """
        self.endpoint = "/2.0/contact_relation/search"
        self.params.upate({"contact_sub_id": str(contact_sub_id)})
        response = requests.request(
            "POST",
            self.url + self.endpoint,
            data=None,
            headers=self.headers,
            params=self.params,
        )
        r = response.text
        res = json.loads(r)
        return res

    def search_contact_relation(self, payload):
        """
        Search a contract relation
        """
        self.endpoint = "/2.0/contact_relation/search"
        response = requests.request(
            "POST", self.url + self.endpoint, json=payload, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def fetch_contact_relation(self, contact_relation_id):
        """
        Fetch a contact relation
        """
        self.endpoint = "/2.0/contact_relation/" + str(contact_relation_id)
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_bexio_users(self):
        """
        Diese Funktion liefert die Bexio User
        """
        self.endpoint = "/3.0/users"
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_bexio_user(self, user_id):
        """
        Diese Funktion liefert einen Bexio User
        """
        self.endpoint = "/3.0/users/" + str(user_id)
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_contactgroup(self):
        """
        Diese Funktion liefert Kontaktgruppen
        """
        self.endpoint = "/2.0/contact_group"
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def search_contactgroup(self, payload):
        """
        Diese Funktion liefert Kontaktgruppen
        contact_group_ids	1 = Partner, 2 = Kunden, 3 = Lieferanten, 4 = Hersteller
                            5 = Rechung_elektronisch, 6 = Rechnung_postalisch
        contact_type_id	1 = Firma, 2 = Privat
        """
        self.endpoint = "/2.0/contact_group/search"
        response = requests.request(
            "POST", self.url + self.endpoint, json=payload, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_contacts(self):
        """
        Diese Funktion holt alle Contacts aus bexio raus
        """
        self.endpoint = "/2.0/contact"
        self.params.update({"limit": "2000"})
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers, params=self.params
        )
        r = response.text
        res = json.loads(r)
        return res

    def search_contact(self, payload):
        """
        Diese Funktion holt einen spezifischen Kontakt bexio raus
        """
        self.endpoint = "/2.0/contact/search"
        self.params.update({"limit": "5000"})
        response = requests.request(
            "POST",
            self.url + self.endpoint,
            json=payload,
            headers=self.headers,
            params=self.params,
        )
        r = response.text
        res = json.loads(r)
        return res

    def get_quotes(self):
        self.endpoint = "/2.0/kb_offer"
        self.params.update({"limit": "2000", "order_by_desc": "updated_at"})
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers, params=self.params
        )
        # print(response.text)

    def search_quotes(self, payload, lim):
        """
        https://docs.bexio.com/#operation/v2SearchQuotes
        Diese Funktion sucht nach Offerten
        Moegliche Parameter: https://docs.bexio.com/legacy/kb_item_status/index.html
        kb_item_status_id: 1=draft, 2=pending, 3=confirmed, 4=declined
        """
        self.endpoint = "/2.0/kb_offer/search"
        self.params.update({"limit": str(lim), "order_by_desc": "updated_at"})
        response = requests.request(
            "POST",
            self.url + self.endpoint,
            json=payload,
            headers=self.headers,
            params=self.params,
        )

        r = response.text
        res = json.loads(r)
        # res ist nun eine Liste mit den Angeboten
        return res

    def search_projects(self, payload, lim):
        """
        https://docs.bexio.com/#operation/v2SearchProjects
        Diese Funktion sucht nach offenen Projekten
        pr_state_id: 1=offen, 2=active, 3=archiviert,
        """
        self.endpoint = "/2.0/pr_project/search"
        self.params.update({"limit": str(lim)})
        response = requests.request(
            "POST",
            self.url + self.endpoint,
            json=payload,
            headers=self.headers,
            params=self.params,
        )
        r = response.text
        res = json.loads(r)
        # res ist nun eine Liste mit den Prokekten
        return res

    def search_timesheet(self, payload):
        """
        Searches the timesheet for a specific project
        """
        self.endpoint = "/2.0/timesheet/search"
        self.params.update({"limit": "2000"})
        response = requests.request(
            "POST",
            self.url + self.endpoint,
            json=payload,
            headers=self.headers,
            params=self.params,
        )
        r = response.text
        res = json.loads(r)
        return res

    def list_work_packages(self, project_id):
        """
        Get a list of the work packages for a project
        """
        self.endpoint = "/3.0/projects/" + str(project_id) + "/packages"
        response = requests.request(
            "GET", self.url + self.endpoint, headers=self.headers
        )
        r = response.text
        res = json.loads(r)
        # print('URL: ', url, res)
        return res

    def search_invoice(self, payload):
        """
        Get a list of invoices
        """
        self.endpoint = "/2.0/kb_invoice/search"
        self.params.update({"limit": "2000"})
        response = requests.request(
            "POST",
            self.url + self.endpoint,
            json=payload,
            headers=self.headers,
            params=self.params,
        )
        r = response.text
        res = json.loads(r)
        return res
