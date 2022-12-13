from address_book_class import AddressBook, Record

contacts_dict = AddressBook()

#----------------------Декоратор з помилками-------------
def input_error(function):

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except IndexError:
            return 'Print: name as "Oleh" and phonenumber as "1234567890"'
        except KeyError:
            return 'Enter correct name'
        except TypeError:
            return 'Wrong command.'
        except ValueError as exception:
            return exception.args[0]

    return wrapper

#----------------------Функція стартового повідомлення---------
@input_error
def start_app():
    return 'How can I help you?'

#----------------------Функція завершального повідомлення---------
@input_error
def finish_app():
    return 'Good bye!'

#----------------------Функція додавання нового контакту---------
@input_error
def add_contact(contact):
    name, phones = create_contact(contact)

    if name in contacts_dict:
        raise ValueError('This contact already exist.')
    record = Record(name)
    for phone in phones:                                             
        record.add_phone(phone)                                     
    contacts_dict.add_record(record)
    return f'You added new contact: {name} - phonenumber: {phones}.'

#----------------------Функція заміни номера існуючого контакту---------
@input_error
def change_phonenumber(contact):
    name, phones = create_contact(contact)
    record = contacts_dict[name]
    record.change_phones(phones)
    return "Phones have been changed."

#---------------------Функція виводу книги контактів---------
@input_error
def show_contactbook():
    contacts = ''
    page_number = 1                                  
    for page in contacts_dict.iterator():            
        contacts += f"Page #{page_number}\n"         

        for record in page:                         
            contacts += f'{record.get_info()}\n'     
        page_number += 1                             
    return contacts

#---------------------Функція пошуку номера існуючого контакту---------
@input_error
def search_phonenumber(value):
    search_records = ''
    records = contacts_dict.search(value.strip())

    for record in records:
        search_records += f"{record.get_info()}\n"
    return search_records

#---------------------Функція видалення існуючого контакту---------
@input_error
def del_contact(name):
    name = name.strip()
    contacts_dict.remove_record(name)
    return "Contact has been deleted."

#---------------------Функція видалення телефону---------
@input_error
def del_phone(data):
    name, phone = data.strip().split(" ")
    record = contacts_dict[name]
    if record.delete_phone(phone):
        return f"Phone {phone} for {name} contact has been deleted."
    return f"{name} contact doesn't have this phonenumber."

@input_error
def birthday(data):
    name, date = data.strip().split("")
    record = contacts_dict[name]
    record.add_birthday(date)
    return f"For {name} you added Birthday {date}"


@input_error
def next_birthday(name):
    name = name.strip()
    record = contacts_dict[name]
    return f"Next {name}'s birthday will be in {record.get_days_to_next_birthday()} days."

COMMANDS_DICT = {
    'hello': start_app,
    'add': add_contact,
    'change phone': change_phonenumber,
    'show all': show_contactbook,
    'phone': search_phonenumber,
    'delete phone': del_phone,
    'delete contact': del_contact,
    'birthday': birthday,
    'days to birthday': next_birthday,
    'exit': finish_app,
    'close': finish_app,
    'good bye': finish_app
}

#---------------------Функція перетворення і обробки введеної команди-------------
def change_input(user_input):
    new_input = user_input
    contact = ''
    for key in COMMANDS_DICT:
        if user_input.strip().lower().startswith(key):
            new_input = key
            contact = user_input[len(new_input):]
            break
    if contact:
        return reaction_func(new_input)(contact)
    return reaction_func(new_input)()

#---------------------Функція виводу відповіді (ф-ція зі словника або помилка)
def reaction_func(reaction):
    return COMMANDS_DICT.get(reaction, break_func)

#---------------------Функція повідомлення про відсутність введеної команди в словнику-------------
def break_func():
    return "Command not found."

#---------------------Функція створення нового контакту---------
def create_contact(contact):
    name, *phones = contact.strip().split(" ")
    if name.isdigit():
        raise ValueError('You entered wrong name.')
    for phone in phones:
        if not phone.isdigit():
            raise ValueError('You entered wrong phone.')
    return name, phones

#-----------------Основне тіло програми---------------------

def main():
    try:
        while True:
            user_input = input('Enter command for bot: ')
            result = change_input(user_input)
            print(result)
            if result in ['good bye', 'exit', 'close', 'Good bye!']:
                break
    finally:
        contacts_dict.save_contacts_in_file()

#---------------------Точка входу----------------------    
if __name__ == '__main__':
    main()