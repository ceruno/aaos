import asyncio
from connectors.bexio import BexioAPI
from connectors.sharepoint import SharePointAPI
from config.models import BexioModel, SharePointModel
from celery import shared_task
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import json
import os

import datetime
import pytz

key = bytes(os.environ.get('ENCRYPTION_KEY'), 'utf-8')
f = Fernet(key)

@shared_task
def update(args):

    bexio_config = BexioModel.objects.all().values()
    sharepoint_config = SharePointModel.objects.all().values()

    for config in list(bexio_config):
        
        api_key = (f.decrypt(config['api_key'])).decode()
        bexio_session = BexioAPI(config['bexio_url'], api_key)

        timezone = pytz.timezone('Europe/Zurich')
        today = datetime.date.today()
        letztermonat = today - datetime.timedelta(days = 31)
        test = str(letztermonat)

        ##################################################################
        ##################################################################
        ####
        #### Sharepoint Stuff
        ####
        ##################################################################
        ##################################################################

        payload_open_quotes = [
            {
                'field': 'kb_item_status_id',
                'value': '2',
                'criteria': '='
            }
        ]

        payload_win_quotes_dyn_mth = [
            {
                'field': 'kb_item_status_id',
                'value': '3',
                'criteria': '='
            },
            {
                'field': 'updated_at',
                'value': test,
                'criteria': '>'
            }
        ]

        payload_win_quotes_mth = [
            {
                'field': 'kb_item_status_id',
                'value': '3',
                'criteria': '='
            },
            {
                'field': 'updated_at',
                'value': test,  
                'criteria': '>'
            }
        ]

        payload_open_projects = [
            {
                'field': 'pr_state_id',
                'value': '3',
                'criteria': '<'
            }
        ]
        
        payload_contact_group_kunden = [
            {
                'field': 'contact_group_ids',
                'value': '2',
                'criteria': '='
            },
            {
                'field': 'contact_type_id',
                'value': '1',
                'criteria': '='
            }   
        ]

        bexio_customers = bexio_session.search_contact(payload_contact_group_kunden)
        bexio_open_quotes = bexio_session.search_quotes(payload_open_quotes,500)
        bexio_win_quotes = bexio_session.search_quotes(payload_win_quotes_dyn_mth,500)
        bexio_open_projects = bexio_session.search_projects(payload_open_projects,500)


        # Dictionary erstellen mit Bexio Kategorien IDs zu Kategorien Namen
        bexio_contact_group_dic = {}
        bexio_contact_groups = bexio_session.get_contactgroup()
        for s in bexio_contact_groups:
            bexio_contact_group_dic[s['id']] = s['name']

        # Dictionary erstellen mit Mitarbeiter-IDs zu Name damit Sales Name
        # in Kundenliste ausgegeben werden kann.
        bexio_user_dic = {}
        bexio_users = bexio_session.get_bexio_users()
        for s in bexio_users:
            bexio_user_dic[s['id']] = s['lastname']

        # Dictionary erstellen mit Bexio Kunden IDs zu Kunden Namen
        bexio_contact_dic = {}
        contacts = bexio_session.get_contacts()
        for s in contacts:
            if s['contact_type_id'] == 1:
                bexio_contact_dic[s['id']] = s['name_1']
            
        ##
        ## Umsatz pro Kunde in laufenden Jahr zusammenstellen
        ##
        # dictionary mit Kunden Nr von Bexio und Namen erstellen

        date = datetime.date.today()
        year = date.strftime('%Y')
        zeitab = year + '-01-01'

        now = datetime.datetime.now()
        print('create customer list')
        print(now.strftime('%Y-%m-%d %H:%M:%S'))

        bexio_customer_list = []
        for item in bexio_customers:
            customer_dic = {}
            customer_dic['Nr'] = str(item['id'])
            customer_dic['Title'] = item['name_1']    
            payload_invoice = [
                {
                    'field': 'contact_id',
                    'value': item['id'],
                    'criteria': '='
                    },
                {
                    'field': 'is_valid_from',
                    'value': zeitab,
                    'criteria': '>'
                }
            ]
            invoices = bexio_session.search_invoice(payload_invoice)
            umsatz = float(0.00)
            for i in invoices:
                if i['kb_item_status_id'] == 8 or i['kb_item_status_id'] == 9 : 
                    umsatz = umsatz + float(i['total_net'])
                    if i['currency_id'] == 1:
                        waerung = 'CHF'
                    elif i['currency_id'] == 2:
                        waerung = 'Euro'
                    customer_dic['Währung'] = waerung
                else:
                    customer_dic['Währung'] = None
            customer_dic['Umsatz'] = int(umsatz)
            cont = []
            cg = item['contact_group_ids'].split(',')
            for s in cg:
                group = bexio_contact_group_dic[int(s)]
                cont.append(group)
            # nun sind alle Tags in einer Liste. Diese will ich nun zu einem String zusammenfügen
            tag = ';#'.join(cont)
            customer_dic['Tags'] = tag
            if item['user_id'] != None:
                #sales = BexioAPI.get_bexio_user(item['user_id'])
                #sales = sales['lastname']
                #customer_dic['Owner'] = sales
                customer_dic['Owner'] = bexio_user_dic[item['user_id']]
            #print('Kunde: ', item['name_1'], ' :: ', sales)
            customer_dic['Bemerkungen'] = item['remarks']
            bexio_customer_list.append(customer_dic)

        #In bexio_open_projects Projekte mit Namen 'Presales' löschen, da es sich nur um interne Projekte handelt

        now = datetime.datetime.now()
        print('create project list')
        print(now.strftime('%Y-%m-%d %H:%M:%S'))

        bexio_open_project_list = []
        for item in bexio_open_projects:
            project_item = {}
            if 'Presales' in item['name']:
                continue
            else:
                payload = [
                    {
                    'field': 'pr_project_id',
                    'value': item['id'],
                    'criteria': '='
                    }
                ]
                timesheet = bexio_session.search_timesheet(payload)
                zeit = 0.0
                for s in timesheet:
                    # leider zeigt bexio die Zeitangabe in Minuten an, z.B. 4:30 was in 4.5 umgewandelt werden muss
                    if s['allowable_bill']:
                        eintrag = s['duration'].split(':')
                        eintrag[1] = int(eintrag[1])/60
                        zeit = zeit + int(eintrag[0]) + eintrag[1]
                #Kundenname rausholen
                #paylo_kunde = [
                #    {
                #    'field': 'id',
                #    'value': item['contact_id'],
                #    'criteria': '='
                #    }
                #]
                #payload = json.dumps(paylo_kunde)
                #kunde = BexioAPI.search_contact(payload)
                
                workpackage_list = bexio_session.list_work_packages(item['id'])
                budget = 0
                for i in workpackage_list:
                    budget = budget + i['estimated_time_in_hours']
                project_item['Nr'] = item['nr']
                #project_item['Kunde'] = kunde[0]['name_1']
                project_item['Kunde'] = bexio_contact_dic[item['contact_id']]
                project_item['Title'] = item['name']
                project_item['Stunden'] = zeit
                project_item['Start'] = item['start_date']
                project_item['Budget'] = budget
                bexio_open_project_list.append(project_item)

        now = datetime.datetime.now()
        print('create offene angebote')
        print(now.strftime('%Y-%m-%d %H:%M:%S'))

        bexio_open_quotes_list = []
        for item in bexio_open_quotes:
            quote_item = {}
            quote_item['AN'] = item['document_nr']
            quote_item['Title'] = item['title']
            #quote_item['is_valid_from'] = item['is_valid_from']
            quote_item['Frist'] = item['is_valid_until']
            quote_item['NettoUmsatz'] = item['total_net']
            quote_item['aktualisiert_am'] = item['updated_at']
            customer  = item['contact_address'].splitlines()[0]
            quote_item['Kunde'] = customer
            bexio_open_quotes_list.append(quote_item)

        now = datetime.datetime.now()
        print('create wins')
        print(now.strftime('%Y-%m-%d %H:%M:%S'))

        bexio_win_quotes_list = []
        for item in bexio_win_quotes:
            quote_item = {}
            quote_item['AN'] = item['document_nr']
            quote_item['Title'] = item['title']
            #quote_item['is_valid_from'] = item['is_valid_from']
            #quote_item['Frist'] = item['is_valid_until']
            quote_item['NettoUmsatz'] = item['total_net']
            quote_item['aktualisiert_am'] = item['updated_at']
            customer  = item['contact_address'].splitlines()[0]
            quote_item['Kunde'] = customer
            bexio_win_quotes_list.append(quote_item)

            
        ##################################################################
        ##################################################################
        ####
        #### Sharepoint Stuff
        ####
        ##################################################################
        ##################################################################

        now = datetime.datetime.now()
        print('update sharepoint')
        print(now.strftime('%Y-%m-%d %H:%M:%S'))

        for sp_config in list(sharepoint_config):

            password = (f.decrypt(sp_config['password'])).decode()
            sp_session = SharePointAPI(sp_config['sharepoint_url'],sp_config['sharepoint_site'],sp_config['user'],password)
            sp_site = sp_session.authenticate()

            open_quotes = 'Offene_Angebote'
            win_quotes = 'WINs'
            projects = 'Projects'
            kunden = 'Kunden'

            # Connect to the sharepoint site

            def update_sharepoint_lists(list, bexio_list, field_1 = 'ID', field_2 = 'AN'):
                '''
                Update (Delete old/unused entries, publish new entries, modify existing entries
                field_1 = ist der Wert im Bexio eines Eintrages wie die Angebots- oder Projektnummer welche wir beiziehen
                        AN oder Projekt Nr
                field_2 = ist die eindeutige ID eines Eintrages im Sharepoint
                sp_list = connect auf SHAREPOINT_LIST
                current_sharepoint_list = aktuelle Liste auf dem Sharepoint
                sharepoint_dic =  Dictionary bestehend aus key(=field_1) und Value(=field_2)
                BEXIO_LIST = übergebene Bexio Liste
                current_bexio = erstellt eine kurze Liste mit dem Feld (field_2) aller aktueller Bexio Einträge
                '''
                sp_list =  sp_session.get_sp_list(sp_site, list)
                current_sharepoint_list = sp_session.download_list_items(sp_list, fields=[field_1,field_2])

                sharepoint_dic = {}
                for s in current_sharepoint_list:
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

                print('Zu löschende Einträge auf Sharepoint: ', del_list)
                sp_session.detele_list_items(sp_list, del_list)

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

                print('Neue Bexio Elemente: ', new_bexio)
                # Neue Angebote hochladen auf sharepoint
                sp_session.create_list_items(sp_list, new_bexio_entries)
                # Um existierende Einträge zu aktualisieren benötigen wir die dazugehörigen Sharepoint IDs !!
                sp_session.update_list_items(sp_list, existing_bexio_entries) 

            print('Kunden Liste')
            update_sharepoint_lists(kunden, bexio_customer_list, 'Nr', 'ID')
            print('OFFENE ANGEBOTE')
            update_sharepoint_lists(open_quotes, bexio_open_quotes_list, 'AN', 'ID')
            print('WINS')
            update_sharepoint_lists(win_quotes, bexio_win_quotes_list, 'AN', 'ID')
            print('PROJECTS')
            update_sharepoint_lists(projects, bexio_open_project_list, 'Nr', 'ID')

            now = datetime.datetime.now()
            print('done')
            print(now.strftime('%Y-%m-%d %H:%M:%S'))