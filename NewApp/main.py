import kivy
kivy.require("2.1.0")

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.uix.screen import MDScreen
from kivy.properties import DictProperty
from kivy.core.window import Window
from kivy_garden.mapview import MapView
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.textinput import TextInput
from kivymd.uix.swiper import MDSwiper, MDSwiperItem
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import Snackbar
from database import save_to_database

##Store Location##
class StoreLocationScreen(MDScreen):
    pass

##Mail##
class MailScreen(MDScreen):
    pass

##Phonebook##
class PhonebookScreen(MDScreen):
    
    card = None
    textField_1 = None
    textField_2 = None
    listOfPeople = []
        
    def add_card(self):
        
        self.textField_1 = MDTextField(
            hint_text = "Name",
            helper_text = "Max. Num. of characters is 16",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .8},
        )
        
        self.textField_2 = MDTextField(
            hint_text = "Number",
            helper_text = "Max. Num. of characters is 12",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .45},
        )
        
        self.card = MDCard(
            MDFloatLayout(
                self.textField_1,
                self.textField_2,
                MDFlatButton(
                    text = "OK",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.85,'center_y': 0.15},
                    on_release = self.AddPerson,
                ),
                MDFlatButton(
                    text = "CANCEL",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.6,'center_y': 0.15},
                    on_release = self.Cancel,
                ),
                size = self.size
            ),
            orientation = 'vertical',
            size_hint = (.7, .2),
            pos_hint = {'center_x': 0.5,'center_y': 0.5},
            elevation = 4,
            radius = [20],
        )
        self.add_widget(self.card)
            
    def AddPerson(self, obj):
        
        name = str(self.textField_1.text)
        number = str(self.textField_2.text)
        
        if len(name) > 16 or len(number) > 12:
            Snackbar(text="Maximum number of characters exceeded!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            database = r"database.db"
            conn = save_to_database.create_connection(database)

            with conn:
                    phonebook = (str(name), str(number))
                    phonebook_id = save_to_database.create_phonebook(conn, phonebook)

                    save = []
                    save.append(str(name))
                    save.append(phonebook_id)
                    self.listOfPeople.append(save)

            self.manager.get_screen('P').ids.PhoneBookNumbers.add_widget(
                TwoLineIconListItem(
                    IconLeftWidget(
                        icon="account"
                    ),
                    text = str(name) + ' ',
                    secondary_text = "Number: " + str(number),
                    on_release = self.PressedItem,
                    bg_color = (1,1,1,1),
                    radius = [25]
                    )
            )

            self.remove_widget(self.card)
            conn.close()
    
    def Cancel(self, obj):
        self.remove_widget(self.card)
            
    def PressedItem(self, obj):
        if PerfectStoreApp.delPerson:
            PerfectStoreApp.delPerson.bg_color = (1,1,1,1)
            if PerfectStoreApp.delPerson != obj:
                PerfectStoreApp.delPerson = obj
                PerfectStoreApp.delPerson.bg_color = "#00B4D8"
            else:
                PerfectStoreApp.delPerson = None
        else:
            PerfectStoreApp.delPerson = obj
            PerfectStoreApp.delPerson.bg_color = "#00B4D8"
            
    def deleteItem(self):

        if PerfectStoreApp.delPerson:
            priority = 0
            for i in self.listOfPeople:
                nameFromList = str(i[0].strip())
                nameFromItem = str(PerfectStoreApp.delPerson.text.strip())
                if nameFromItem == nameFromList:
                    priority = i[1]
                    break
            
            database = r"database.db"
            conn = save_to_database.create_connection(database)
            with conn:
                save_to_database.delete_phonebook(conn, priority)
            
            self.manager.get_screen('P').ids.PhoneBookNumbers.remove_widget(PerfectStoreApp.delPerson)
            PerfectStoreApp.delPerson = None
            conn.close()

##Settings##
class SettingsScreen(MDScreen):
            
    def ChangeText(self, theme):
            if theme == "DARK":
                self.manager.get_screen('S').ids.ThemeLabel.text = '[b][color=FFFFFF]THEME[/color][/b]'
                self.manager.get_screen('main').ids.mainTitle.text = '[b][color=FFFFFF][size=90]P[/size][size=85]erfect[/size][/color][i][color=4073FF][size=90]S[/size]tore[/color][/i][/b]'
                self.manager.get_screen('main').ids.HelloText.text = '[b][color=FFFFFF]Hello\nWe are hoping that you have a great day[/color][/b]'
                self.manager.get_screen('main').ids.tasksLabel.text = '[b][color=FFFFFF]My Tasks:[/color][/b]'
                
            elif theme == "LIGHT":
                self.manager.get_screen('S').ids.ThemeLabel.text = '[b][color=000000]THEME[/color][/b]'
                self.manager.get_screen('main').ids.mainTitle.text = '[b][color=000000][size=90]P[/size][size=85]erfect[/size][/color][i][color=4073FF][size=90]S[/size]tore[/color][/i][/b]'
                self.manager.get_screen('main').ids.HelloText.text = '[b][color=000000]Hello\nWe are hoping that you have a great day[/color][/b]'
                self.manager.get_screen('main').ids.tasksLabel.text = '[b][color=000000]My Tasks:[/color][/b]'

class MainScreen(MDScreen):
    def ChangeScreen(self, ScreenName):
        self.manager.current = ScreenName
                  
class PerfectStoreApp(MDApp):

    #database
    TasksList = []
    ListOfSeconderyID = []
    secondery_id = 1

    #class objects
    obj_p = PhonebookScreen()
    delPerson = None
    
    #Screen properties
    Window.size = (375, 812)
    sm = ScreenManager(transition = SlideTransition())
    
    #SpeedDial data
    data = DictProperty()
    
    #Storing bill data
    string = ""
    Bill = []
    menuForDisplaying = None
    menuForDeleting = None
    
    #Data for creating a bill
    card = None
    textField_1 = None
    textField_2 = None
    textInput_3 = None
    
    #Amount sold screen data
    totalProfit = 0
    ListOfItems = []
    menuForItems = None
    InStorage = 1000
    
    #Tasks Screen
    textField_1_task = None
    textInput_2_task = None
    card_task = None
    TaskItem = None
    listOfTasks = []
    listOfButtons = []
    checkbutton = None
    deleteButton = None
    

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        
        self.data = {
            'Store Location': [
                'map-marker-outline',
                'on_release', lambda x: callback('SL')
            ],
            'Mail':[
                'email-outline',
                'on_release', lambda x: callback('M')
            ],
            'Phonebook':[
                'book-account',
                'on_release', lambda x: callback('P')
            ],
            'Settings':[
                'cog-outline',
                'on_release', lambda x: callback('S')
            ]
        }
        
        self.sm.add_widget(MainScreen(name = 'main'))
        self.sm.add_widget(StoreLocationScreen(name = 'SL'))
        self.sm.add_widget(MailScreen(name = 'M'))
        self.sm.add_widget(PhonebookScreen(name = 'P'))
        self.sm.add_widget(SettingsScreen(name = 'S'))
        
        def callback(instance):
            self.sm.get_screen('main').ids.speedDial.close_stack()
            self.sm.current = instance
            
        return self.sm
    
    def DropDownMenuForDisplaying(self):
        
        if len(self.Bill) is 0:
             Snackbar(text="Bills to select: None", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            bill_items = [
                {
                    "text": str(i['Name']),
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=str(i['Name']): self.LoadBills(x),
                }for i in self.Bill
            ]

            self.menuForDisplaying = MDDropdownMenu(
                caller = self.sm.get_screen('main').ids.SelectItem,
                items = bill_items,
                width_mult = 2,
                max_height = 300,
            )

            self.menuForDisplaying.open()
    
    def DropDownMenuForDeleting(self):
        
        if len(self.Bill) is 0:
             Snackbar(text="Bills to delete: None", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            bill_items = [
                {
                    "text": str(i['Name']),
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=str(i['Name']): self.DeleteBills(x),
                }for i in self.Bill
            ]

            self.menuForDeleting = MDDropdownMenu(
                caller = self.sm.get_screen('main').ids.DeleteItem,
                items = bill_items,
                width_mult = 2,
                max_height = 300,
            )

            self.menuForDeleting.open()
    
    def ChangeTheme(self, theme):
            if theme == "DARK":
                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "Blue"

            elif theme == "LIGHT":
                self.theme_cls.theme_style = "Light"
                self.theme_cls.primary_palette = "Blue"
        
    def CreateBillPopUp(self):
        
        self.textField_1 = MDTextField(
            hint_text = "Bill Name:",
            helper_text = "Max. Num. of characters is 12",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .9},
        )
        
        self.textField_2 = MDTextField(
            hint_text = "Date:",
            helper_text = "YYYY-MM-DD",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .72},
        )
        
        self.textInput_3 = TextInput(
            hint_text = "Items",
            font_size = 30,
            size_hint = (.8, .5),
            pos_hint = {'center_x': .5,'center_y': .35},
            multiline = True,
            background_color = (0,0,0,0),
        )
        
        self.card = MDCard(
            MDFloatLayout(
                self.textField_1,
                self.textField_2,
                self.textInput_3,
                MDFlatButton(
                    text = "OK",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.85,'center_y': 0.15},
                    on_release = self.AddBill,
                ),
                MDFlatButton(
                    text = "CANCEL",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.6,'center_y': 0.15},
                    on_release = self.Cancel,
                )
            ),
            orientation = 'vertical',
            size_hint = (.8, .4),
            pos_hint = {'center_x': 0.5,'center_y': 0.5},
            elevation = 4,
            radius = [20],
        )
        self.sm.get_screen('main').add_widget(self.card)
    
    def AddBill(self, obj):
        
        count = 1
        state = True
        for i in self.textInput_3.text:
            if i is not " " and i is not "\n":
                pass
            else: 
                count += 1
                
        for i in self.textField_2.text:
            if i is not "-" and i is not "\n":
                if i.isdigit():
                    pass
                else:
                    state = False
                    break
            else:
                if i is not "-" and i is not "\n":
                    state = False
                    break
                
        if len(self.textField_1.text) is 0 or len(self.textField_2.text) is 0 or len(self.textInput_3.text) is 0:
            Snackbar(text="Please fill in every text field!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif state is False:
            Snackbar(text="Incorrect date format!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif len(self.textField_1.text) > 12:
            Snackbar(text="Name of the bill exceeded 12 characters!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        elif (count%3) != 0:
            Snackbar(text="Missing item information!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            items = []
            string_list = []
            string = ""
            SeconderyIDList = list(set(self.ListOfSeconderyID))
            dic = {'ID': 0,'Name' : "", 'Date' : "", 'Items' : []}

            dic['Name'] = str(self.textField_1.text)
            dic['Date'] = str(self.textField_2.text + "\n")

            database = r"database.db"
            conn = save_to_database.create_connection(database)

            if len(SeconderyIDList) is not 0:
                self.secondery_id = SeconderyIDList[-1:][0] + 1

            string = ""
            item = ""
            listOfItemInfo = []
            for i in self.textInput_3.text.splitlines():
                items.append(str(i)+"\n")
                item = items[-1:][0]
                for x in item:

                    if x is not " " and x is not "\n":
                        string += x
                    else:
                        listOfItemInfo.append(string)
                        string = ""
                with conn:
                    bill = (self.secondery_id, self.textField_1.text, self.textField_2.text, str(listOfItemInfo[0]), str(listOfItemInfo[1]), str(listOfItemInfo[2]))
                    bill_id = save_to_database.create_bills(conn, bill)
                    
                self.ListOfSeconderyID.append(self.secondery_id)
                listOfItemInfo.clear()
            dic['ID'] = self.secondery_id
            self.secondery_id += 1
            dic['Items'] = items
            self.Bill.append(dic)

            for x in items:
                for y in x:
                    if y is not ' ' and y is not '\n':
                        string += y
                    else:
                        string_list.append(string)
                        string = ""

            self.TotalAmount(string_list)

            self.totalProfit = round(self.totalProfit,2)
            self.sm.get_screen('main').ids.TotalProfit.text = f"TOTAL PROFIT: {self.totalProfit}HRK"

            self.sm.get_screen('main').remove_widget(self.card)
        
    def LoadBills(self, item):
        if item is "None":
            for i in self.Bill:
                self.string += f"{str(i['Name'])}\n{str(i['Date'])}{' '.join(i['Items'])}\n"
            self.sm.get_screen('main').ids.BillContent.text = f'[b]{self.string}[/b]'
            self.string = ""
        else:
            self.menuForDisplaying.dismiss()
            for i in self.Bill:
                if i['Name'] is item:
                    self.string = f"{str(i['Name'])}\n{str(i['Date'])}{' '.join(i['Items'])}\n"
                    self.sm.get_screen('main').ids.BillContent.text = f'[b]{self.string}[/b]'
            self.string = ""
            
    def DeleteBills(self, item):
        
        minus = 0
        string_list = []
        string_list_2 = []
        string = ""
        id = 0
        for i in self.Bill:
            if i['Name'] is item:
                for x in i['Items']:
                    for x in i['Items']:
                        for y in x:
                            if y is not ' ' and y is not '\n':
                                string += y
                            else:
                                string_list.append(string)
                                string_list_2.append(string)
                                string = ""
                
                
                string_list = list(dict.fromkeys(string_list))
                id = i['ID']
                database = r"database.db"
                conn = save_to_database.create_connection(database)
                for x in self.ListOfSeconderyID:
                    if id is x:
                        with conn:
                            save_to_database.delete_bills(conn, id)
                    self.ListOfSeconderyID.remove(x)

                self.Bill.remove(i)
                print(string_list)
                print(self.ListOfItems)
                new_list = []
                x = 0
                for y in self.ListOfItems:
                    for i in range(len(string_list)):
                        if i is x:
                            if string_list[i] is not y:
                                new_list.append(y)
                            break
                    x+=3
                                
        string_list_2 = list(dict.fromkeys(string_list_2))
        test = None
        for i in range(len(string_list_2)-1):
            test = string_list_2[i]
            if test.isdigit():
                minus += int(string_list_2[i]) * float(string_list_2[i+1])
        
        self.sm.get_screen('main').ids.TotalProfit.text = f"TOTAL PROFIT: {str(self.totalProfit-round(minus,2))}HRK"
        self.menuForDeleting.dismiss()
        conn.close()
    
    def Cancel(self, obj):
        if self.card:
            self.sm.get_screen('main').remove_widget(self.card)
            self.card = None
        
        if self.card_task:
            self.sm.get_screen('main').remove_widget(self.card_task)
            self.card_task = None
              
    def DisplayItem(self):
        
        if len(self.ListOfItems) is 0:
             Snackbar(text="Items: None", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                     size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
        else:
            items_ = [
                {
                    "text": str(i),
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=str(i): self.ShowItem(x),
                }for i in self.ListOfItems
            ]
            self.menuForItems = MDDropdownMenu(
                caller = self.sm.get_screen('main').ids.SelectItem,
                items = items_,
                width_mult = 2,
                border_margin = 24,
                max_height = 350,
                ver_growth = "down",
            )

            self.menuForItems.open()
            
    def ShowItem(self, instance):
        
        total_amount = 0
        string_list = []
        string = ""
        price = ""
        
        for i in self.Bill:
            for x in i['Items']:
                for y in x:
                    if y != ' ' and y != '\n':
                        string += y
                    else:
                        string_list.append(string)
                        string = ""
                        
        for i in range(len(string_list)):
            if string_list[i] == instance:
                total_amount += int(string_list[i+1])
                price = string_list[i+2]
        
        self.sm.get_screen('main').ids.item.text = f"Item: {instance}"
        self.sm.get_screen('main').ids.amount.text = f"Amount Sold: {str(total_amount)}"
        self.sm.get_screen('main').ids.price.text = f"Price: {str(price)}HRK"
        self.sm.get_screen('main').ids.storage.text = f"In Storage: {str(self.InStorage - total_amount)}"
        self.menuForItems.dismiss()
    
    def AddSwiperItem(self):
        
        self.textField_1_task = MDTextField(
            hint_text = "Task Name",
            helper_text = "Max. Num. of characters is 16",
            helper_text_mode = "persistent",
            font_size = 25,
            size_hint_x = .8,
            pos_hint = {'center_x': .5,'center_y': .85},
        )
        
        self.textInput_2_task = TextInput(
            hint_text = "Description\nMaximum number of characters is 60",
            font_size = 35,
            hint_text_color = (0, 153/250, 1, 135/250),
            size_hint = (.8, .5),
            pos_hint = {'center_x': .5,'center_y': .45},
            multiline = True,
            background_color = (0,0,0,0),
        )
        
        self.card_task = MDCard(
            MDFloatLayout(
                self.textField_1_task,
                self.textInput_2_task,
                MDFlatButton(
                    text = "OK",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.85,'center_y': 0.15},
                    on_release = self.addTask
                ),
                MDFlatButton(
                    text = "CANCEL",
                    size_hint = (.2, .2),
                    pos_hint = {'center_x': 0.6,'center_y': 0.15},
                    on_release = self.Cancel
                )
            ),
            orientation = 'vertical',
            size_hint = (.8, .4),
            pos_hint = {'center_x': 0.5,'center_y': 0.5},
            elevation = 4,
            radius = [20],
        )
        
        self.sm.get_screen('main').add_widget(self.card_task)
    
    def addTask(self, obj):
        
        if self.card_task:
            if len(self.textField_1_task.text) > 16:
                Snackbar(text="Name of the task exceeded 12 characters!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
            elif len(self.textInput_2_task.text) > 60:
                Snackbar(text="Description of the task exceeded 12 characters!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
            elif len(self.textField_1_task.text) is 0 or len(self.textInput_2_task.text) is 0:
                Snackbar(text="Please fill in every text field!", snackbar_x=10, snackbar_y=10, size_hint_y=.08,
                         size_hint_x=(Window.width - (10 * 2)) / Window.width, bg_color=(0, 153/250, 1, 255/250)).open()
            else:
                self.creatingASwiperItem(self.textField_1_task.text, self.textInput_2_task.text)
                self.sm.get_screen('main').remove_widget(self.card_task)
                self.card_task = None

                name = self.textField_1_task.text
                description = self.textInput_2_task.text

                database = r"database.db"
                conn = save_to_database.create_connection(database)
                with conn:
                    tasks = (name,description)
                    tasks_id = save_to_database.create_task(conn,tasks)
                    self.TasksList.append(tasks_id)

                conn.close()
        
    def CheckTask(self, instance):
        
        # gray [0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0]
        # green [0.4470588235294118, 0.8, 0.3137254901960784, 1.0]
        
        if instance.md_bg_color == [0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0]:
            instance.md_bg_color = "#72CC50"
        else:
            instance.md_bg_color = "gray"
            
    def removeTask(self, instance):
        
        id = 0
        for i in range(len(self.listOfButtons)):
            if self.listOfButtons[i] is instance:
                self.sm.get_screen('main').ids.TaskSwiper.remove_widget(self.listOfTasks[i])
                self.listOfTasks.remove(self.listOfTasks[i])
                self.listOfButtons.remove(self.listOfButtons[i])
                
                id = self.TasksList[i]
                database = r"database.db"
                conn = save_to_database.create_connection(database)
                with conn:
                    save_to_database.delete_task(conn, id)
                self.TasksList.remove(self.TasksList[i])
                break
                
    def on_start(self):
        
        database = r"database.db"
        conn = save_to_database.create_connection(database)
        sql_task = """ CREATE TABLE IF NOT EXISTS tasks (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        description text NOT NULL
                    ); """
                    
        sql_phonebook = """ CREATE TABLE IF NOT EXISTS phonebook (
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            number text NOT NULL
                        ); """
                        
        sql_bills = """ CREATE TABLE IF NOT EXISTS bills(
                            id integer PRIMARY KEY,
                            secondery_id integer NOT NULL,
                            name text NOT NULL,
                            date text NOT NULL,
                            item text NOT NULL,
                            amount text NOT NULL,
                            price text NOT NULL
                        ); """
        
        if conn is not None:
            save_to_database.create_table(conn, sql_task)
            save_to_database.create_table(conn, sql_phonebook)
            save_to_database.create_table(conn, sql_bills)
        else:
            print("Error! No connection with database.")
            
        phonebookList = None
        taskList = None
        bills = None
        with conn:
            phonebookList = save_to_database.select_all_phonebook(conn)
            
        if len(phonebookList) is not 0:
            for i in phonebookList:
                self.sm.get_screen('P').ids.PhoneBookNumbers.add_widget(
                    TwoLineIconListItem(
                        IconLeftWidget(
                            icon="account"
                        ),
                        text = str(i[1]).strip('\n'),
                        secondary_text = "Number: " + str(i[2]).strip('\n'),
                        on_release = self.obj_p.PressedItem,
                        bg_color = (1,1,1,1),
                        radius = [25]
                    )
                )
                save = []
                save.append(str(i[1]))
                save.append(i[0])
                PhonebookScreen.listOfPeople.append(save)
        
        save_to_database.create_connection(database)
        with conn:
            taskList = save_to_database.select_every_task(conn)
            
        if len(taskList) is not 0:
            for i in taskList:
                self.creatingASwiperItem(i[1],i[2])
                self.TasksList.append(i[0])
                
        with conn:
            bills = save_to_database.selec_all_bills(conn)

        if len(bills) is not 0:
            
            pos = 0
            lenOfBills = 0
            items = []
            SeconderyIDList = []
            
            for i in bills:
                self.ListOfSeconderyID.append(i[1])

            SeconderyIDList = list(set(self.ListOfSeconderyID))
            lenOfBills = len(bills)
            for i in SeconderyIDList:
                dict = {'ID': 0,'Name': "",'Date': "",'Items': []}
                while bills[pos][1] is i:
                    items.append(f'{str(bills[pos][4])} {str(bills[pos][5])} {str(bills[pos][6])}\n')
                    pos += 1
                    if pos is lenOfBills:
                        break
                dict['ID'] = bills[pos-1][1]
                dict['Name'] = bills[pos-1][2]
                dict['Date'] = f'{bills[pos-1][3]}\n'
                dict['Items'] = items
                self.Bill.append(dict)
                items = []

        string = ""
        string_list = []
        for i in self.Bill:
            for x in i['Items']:
                for y in x:
                    if y is not ' ' and y is not '\n':
                        string += y
                    else:
                        string_list.append(string)
                        string = ""

        self.TotalAmount(string_list)
        
        self.totalProfit = round(self.totalProfit,2)
        self.sm.get_screen('main').ids.TotalProfit.text = f"TOTAL PROFIT: {str(self.totalProfit)}HRK"
        conn.close()
                
    def on_stop(self):
        
        self.Bill.clear()
        self.ListOfItems.clear()
        self.listOfTasks.clear()
        self.listOfButtons.clear()
        self.TasksList.clear()
        self.ListOfSeconderyID.clear()

    def TotalAmount(self, string_list):
        
        temp_list = []
        
        for i in string_list:
           test = str(i)
           res = test.replace('.','',1).isdigit()
           if res:
               if test.isdigit():
                   amount = int(test)
               if not test.isdigit():
                   self.totalProfit += float(test) * amount
           elif not res:
               temp_list.append(test)
            
        if self.ListOfItems is []:
            self.ListOfItems = list(set(temp_list))
            self.ListOfItems.sort()
        else:
            temp_list += self.ListOfItems
            self.ListOfItems = list(set(temp_list))
            self.ListOfItems.sort()
            
    def creatingASwiperItem(self, task, description):
        self.checkbutton = MDFloatingActionButton(
                           icon = 'check-bold',
                           pos_hint = {'center_x': 0.55,'center_y': 0.2},
                           md_bg_color = "gray",
                           elevation = 0,
                           on_release = self.CheckTask
                        )
        self.deleteButton = MDFloatingActionButton(
                       icon = 'delete',
                       pos_hint = {'center_x': 0.82,'center_y': 0.2},
                       md_bg_color = "red",
                       elevation = 0,
                       on_release = self.removeTask
                    )
        self.TaskItem = MDSwiperItem(
               MDFloatLayout(
                   self.checkbutton,
                   self.deleteButton,
                   MDCard(
                       MDLabel(
                           markup = True,
                           text = f'[b]{task}[/b]',
                           font_size = 55,
                           halign = 'center'
                       ),
                       orientation = 'vertical',
                       elevation = 0,
                       md_bg_color = (1,1,1,1),
                       size_hint = (0.9, 0.1),
                       pos_hint = {'center_x': 0.5,'center_y': 0.9}
                   ),
                   MDCard(
                       MDFloatLayout(
                           MDLabel(
                               markup = True,
                               text = f'[b]{description}[/b]',
                               pos_hint = {'center_x': 0.5,'center_y': 0.9},
                               font_size = 45
                           )
                       ),
                       orientation = 'vertical',
                       elevation = 0,
                       md_bg_color = (1,1,1,1),
                       size_hint = (.9, .4),
                       pos_hint = {'center_x': 0.5,'center_y': 0.6},
                       padding = 20,
                       spacing = 10
                   )
               ),
               radius = [25,],
               md_bg_color = (0, 153/250, 1, 255/250)
            )
        self.listOfTasks.append(self.TaskItem)
        self.listOfButtons.append(self.deleteButton)
        self.sm.get_screen('main').ids.TaskSwiper.add_widget(self.TaskItem)
        
if __name__ == '__main__':
    PerfectStoreApp().run()