from shareplum.site import Version 
from shareplum import Site, Office365 
import sys

class SharePointAPI:

    def __init__(self, url, site, user, password):
        self.url = url
        self.site = site
        self.user = user
        self.password = password

    # Connect to the sharepoint site
    def authenticate(self): 
        """ 
        Takes a SharePoint url, site url, username and password to access the SharePoint site. 
        Returns a SharePoint Site instance if passing the authentication, returns None otherwise. 
        """ 
        site = None 
        try: 
            authcookie = Office365(self.url, username=self.user, password=self.password).GetCookies() 
            self.site_auth = Site(self.site, version=Version.v365, authcookie=authcookie)
            #site.AddList('My New List', description='Great List!', template_id='Custom List')
        except: 
            # We should log the specific type of error occurred. 
            print('Failed to connect to SP site: {}'.format(sys.exc_info()[1])) 

    def get_sp_list(self, list): 
        """ 
        Takes a SharePoint Site instance and invoke the "List" method of the instance. 
        Returns a SharePoint List instance. 
        """ 
        try: 
            self.list = self.site_auth.List(list) 
        except: 
            # We should log the specific type of error occurred. 
            print('Failed to connect to SP list: {}'.format(sys.exc_info()[1])) 

    def create_list_items(self, items): 
        """
        The SharePoint List instance provides a method "UpdateListItems()."
        We can use this method to create, update and delete SharePoint list items.
        When we pass the value "New" to the function, the function adds the data to the SharePoint list.
        Takes a SharePoint List instance and a list of disctoraries. 
        The keys in the dictionary should match the list column. 
        """ 
        if len(items) > 0: 
            try: 
                self.list.UpdateListItems(data=items, kind='New') 
            except: 
                # We should log the specific type of error occurred. 
                print('Failed to upload new list items: {}'.format(sys.exc_info()[1])) 
    
    def download_list_items(self, view_name=None, fields=None, query=None, row_limit=0): 
        """ 
        Takes a SharePoint List instance, view_name, fields, query, and row_limit. 
        The rowlimit defaulted to 0 (unlimited) 
        Returns a list of dictionaries if the call succeeds; return a None object otherwise. 
        """ 
        try: 
            self.items = self.list.GetListItems(view_name=view_name, fields=fields, query=query, row_limit=row_limit) 
        except: 
            # We should log the specific type of error occurred. 
            print('Failed to download list items {}'.format(sys.exc_info()[1])) 
            raise SystemExit('Failed to download list items {}'.format(sys.exc_info()[1])) 

    def update_list_items(self, items): 
        """ 
        Takes a SharePoint List instance and data to update the SharePoint list. 
        The data should have the "ID" column. 
        """ 
        if len(items) > 0: 
            try: 
                self.list.UpdateListItems(data=items, kind='Update') 
            except: 
                # We should log the specific type of error occurred. 
                print('Failed to update the SharePoint list itemst: {}'.format(sys.exc_info()[1])) 

    def detele_list_items(self, items): 
        """ 
        Takes a SharePoint List instance and a list of ID values. 
        """ 
        if len(items) > 0: 
            try: 
                self.list.UpdateListItems(data=items, kind='Delete') 
            except: 
                # We should log the specific type of error occurred. 
                print('Failed to delete list items: {}'.format(sys.exc_info()[1]))

    def update_sharepoint_lists(self, bexio_list, field_1 = 'ID', field_2 = 'AN'):
        """
        Update (Delete old/unused entries, publish new entries, modify existing entries
        field_1 = ist der Wert im Bexio eines Eintrages wie die Angebots- oder Projektnummer welche wir beiziehen
                AN oder Projekt Nr
        field_2 = ist die eindeutige ID eines Eintrages im Sharepoint
        sp_list = connect auf SHAREPOINT_LIST
        current_sharepoint_list = aktuelle Liste auf dem Sharepoint
        sharepoint_dic =  Dictionary bestehend aus key(=field_1) und Value(=field_2)
        BEXIO_LIST = übergebene Bexio Liste
        current_bexio = erstellt eine kurze Liste mit dem Feld (field_2) aller aktueller Bexio Einträge
        """
        self.download_list_items(self, fields=[field_1,field_2])

        sharepoint_dic = {}
        for s in self.items:
            sharepoint_dic[s[field_1]] = s[field_2]

        current_bexio = [] 
        for s in bexio_list:
            # Problematik : die Bexio Liste hat für Projekte
            current_bexio.append(s[field_1])
            
            
        # delete all entries in sharepoint list, which are not in bexio list anymore
        del_list = [] # list with IDs to delete
        for k,v in sharepoint_dic.items():
            if k in current_bexio:          
                continue
            else:
                del_list.append(v)

        print("Zu löschende Einträge auf Sharepoint: ", del_list)
        self.detele_list_items(self, del_list)

        # Neue Bexio Entries auf Sharepoint erstellen oder existierende aktualisieren
        new_bexio = []              # Liste mit neuen Einträgen im Bexio (nur mit field_2 drinnen)
        new_bexio_entries = []      # Liste mit neuen Einträgen im Bexio mit allen gewünschten Details
        existing_bexio = []         # Liste mit Sharepoint Elementen, welche auch noch in der Bexio Liste drinnen sind
        existing_bexio_entries = [] # Um existierende Einträge zu aktualisieren benötigen wir die dazugehörigen Sharepoint IDs !!
        for s in bexio_list:
            if s[field_1] in sharepoint_dic:        # Diesen Eintrag gibt es schon auf dem Sharepoint
                val = sharepoint_dic[s[field_1]]    # val enthält nun die Sharepoint ID
                s[field_2] = val                    
                existing_bexio_entries.append(s)    # BEXIO_LIST mit der ID vom Sharepoint ergänzen
                existing_bexio.append(s[field_1])
            else:
                new_bexio_entries.append(s)
                new_bexio.append(s[field_1])

        print("Neue Bexio Elemente: ", new_bexio)
        # Neue Angebote hochladen auf sharepoint
        self.create_list_items(self, new_bexio_entries)
        # Um existierende Einträge zu aktualisieren benötigen wir die dazugehörigen Sharepoint IDs !!
        self.update_list_items(self, existing_bexio_entries)