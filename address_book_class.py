import pickle
from datetime import datetime                                                     
from collections import UserDict

#----------створюємо Клас Field, який буде батьківським для всіх полів.
class Field:
    def __init__(self, value) -> None:
        self._value = None                                                             
        self.value = value

#---------setter та getter логіка для атрибутів value спадкоємців Field.
    @property                                                                       
    def value(self):                                                               
        return self._value                                                            

    @value.setter                                                                
    def value(self, value):                                                     
        self._value = value                                                            
#----------створюємо Клас Name, обов'язкове поле з ім'ям.
class Name(Field):
    pass

#----------створюємо Клас Phone, необов'язкове поле з телефоном.
class Phone(Field):
    
 #-----функціонал перевірки на правильність веденого номера телефону класу Phone.   
    @Field.value.setter                                                             
    def value(self, value):                                                         
        if len(value) < 10 or len(value) > 12: # if not 10 =< len(value) =< 12      
            raise ValueError("Phone must contains 10 symbols - '0957775533', or 12 symbols - '380634101234.")  
        if not value.isdigit():                                                     
            raise ValueError("Wrong phonenumber.")                                  
        self._value = value                                                           

#--------------Додали поле для дня народження Birthday.
#------------- Це поле не обов'язкове, але може бути тільки одне.
class Birthday(Field):                                                              
    
    @Field.value.setter                                                             
    def value(self, value):                                                         
        today = datetime.now().date()                                               
        birth_date = datetime.strptime(value, "%Y-%m-%d").date()                   

#-------------функціонал перевірки на правильність веденого дня народження класу Birthday.    
        if birth_date > today:                                                      
            raise ValueError("Birthday must be less than current year and date.")   
        self._value = value                                                           

#---------створюємо Клас Record, який відповідає за логіку додавання/видалення/редагування
#---------необов'язкових полів та зберігання обов'язкового поля Name.
class Record:
    def __init__(self, name) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None                                        

    def get_info(self):
        phones_info = ""
        birthday_info = ""                                          
        
        for phone in self.phones:
            phones_info += f"{phone.value}, "
        
        if self.birthday:                                          
            birthday_info = f" Birthday : {self.birthday.value}"    

        return f"{self.name.value} : {phones_info[:]}{birthday_info}" 

#---------додавання номера
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

#---------видалення номера
    def delete_phone(self, phone):
        for record_phone in self.phones:
            if record_phone.value == phone:
                self.phones.remove(record_phone)
                return True
        return False

#---------редагування номера
    def change_phones(self, phones):
        for phone in phones:
            if not self.delete_phone(phone):
                self.add_phone(phone)

    def add_birthday(self, date):                                                
        self.birthday = Birthday(date)                                            

#------функціонал повертає кількість днів до наступного дня народження.
    def get_days_to_next_birthday(self):                                         
        if not self.birthday:                                                     
            raise ValueError("This contact doesn't have attribute birthday")      

        today = datetime.now().date()                                             
        birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()     

        next_birthday_year = today.year                                          

        if today.month >= birthday.month and today.day > birthday.day:          
            next_birthday_year += 1                              

        next_birthday = datetime(                                 
            year=next_birthday_year,                              
            month=birthday.month,                                 
            day=birthday.day                                      
        )                                                         

        return (next_birthday.date() - today).days                

#----------Клас AddressBook, який успадковується від UserDict.
class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

        self.load_contacts_from_file()

        
    def add_record(self, record):
        self.data[record.name.value] = record

        
    def get_all_record(self):
        return self.data

    
    def has_record(self, name):
        return name in self.data

    
    def get_record(self, name):
        return self.data.get(name)

    
    def remove_record(self, name):
        del self.data[name]

#-------------Функція пошуку вмісту книги контактів        
    def search(self, value):
        record_result = []                                        
        for record in self.get_all_record().values():             
            if value in record.name.value:                        
                record_result.append(record)                     
                continue                                          

            for phone in record.phones:                          
                if value in phone.value:                          
                    record_result.append(record)                 
            
        if not record_result:                                     
            raise ValueError(f"Contact {value} doesn't exist.")   
        return record_result                                      

#-2-AddressBook реалізує метод iterator, 
# який повертає генератор за записами AddressBook 
# і за одну ітерацію повертає уявлення для N записів.
    def iterator(self, count=5):                                  
        page = []                                                 
        i = 0                                                    

        for record in self.data.values():                         
            page.append(record)                                   
            i += 1                                               

            if i == count:                                        
                yield page                                        
                page = []                                        
                i = 0                                            

        if page:                                                  
            yield page                                           

#------функція збереження адресної книги у файл.
    def save_contacts_in_file(self):
        with open("ksm_address_book.pickle", "wb") as file:
            pickle.dump(self.data,file)

#------функція відновлення адресної книги з файлу.
    def load_contacts_from_file(self):
        try:
            with open("ksm_address_book.pickle", "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass
