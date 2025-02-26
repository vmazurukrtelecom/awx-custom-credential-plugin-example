import collections
import logging
import os
import json  # Import the json module

# Ініціалізація логера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

CredentialPlugin = collections.namedtuple('CredentialPlugin', ['name', 'inputs', 'backend'])

def some_lookup_function(**kwargs):
    # Отримуємо всі значення з os.environ
    environment_variables = os.environ
    target_host = os.environ.get('my_custom_host')  # Наприклад, отримання 'my_custom_host' із змінних оточення
    ansible_host = os.environ.get('ansible_host')  # Отримуємо значення ansible_host із оточення

    # Записуємо у файл /tmp/metadata.txt
    try:
        with open('/tmp/metadata.txt', 'a') as f:
            # Перевірка, чи не порожній target_host перед записом
            if target_host:
                f.write(f"Target Host: {target_host}\n")
            else:
                f.write("Target Host: Not set or empty\n")  # Якщо target_host порожній, вивести повідомлення

            # Перевірка, чи не порожній ansible_host перед записом
            if ansible_host:
                f.write(f"ansible_host Host: {ansible_host}\n")
            else:
                f.write("ansible_host Host: Not set or empty\n")  # Якщо ansible_host порожній, вивести повідомлення

            # Записуємо всі змінні оточення
            f.write("\nEnvironment Variables:\n")
            for key, value in environment_variables.items():
                f.write(f"{key}: {value}\n")  # Записуємо кожну пару ключ-значення

            f.write("\n\n")
    except (IOError, TypeError) as e:
        logger.error(f"Failed to write data to file: {e}")

    # Основна логіка перевірки даних
    url = kwargs.get('url')
    token = kwargs.get('token')
    identifier = kwargs.get('identifier')

    if token != 'VALID':
        raise ValueError('Invalid token!')

    value = {
        'username': 'mary',
        'email': 'mary@example.org',
        'password': 'super-secret'
    }

    if identifier in value:
        return value[identifier]

    raise ValueError(f'Could not find a value for {identifier}.')

example_plugin = CredentialPlugin(
    'Example AWX Credential Plugin',
    # see: https://docs.ansible.com/ansible-tower/latest/html/userguide/credential_types.html
    # inputs will be used to create a new CredentialType() instance
    #
    # inputs.fields represents fields the user will specify *when they create*
    # a credential of this type; they generally represent fields
    # used for authentication (URL to the credential management system, any
    # fields necessary for authentication, such as an OAuth2.0 token, or
    # a username and password). They're the types of values you set up _once_
    # in AWX
    #
    # inputs.metadata represents values the user will specify *every time
    # they link two credentials together*
    # this is generally _pathing_ інформація про _де_ в зовнішньому
    # менеджменті системи можна знайти значення, яке вас цікавить
    #
    # "Я хочу, щоб Machine Credential A отримав своє ім'я користувача, використовуючи
    # Credential-O-Matic B за identifier=some_key"
    inputs={
        'fields': [{
            'id': 'url',
            'label': 'Server URL',
            'type': 'string',
        }, {
            'id': 'token',
            'label': 'Authentication Token',
            'type': 'string',
            'secret': True,
        }],
        'metadata': [{
            'id': 'identifier',
            'label': 'Identifier',
            'type': 'string',
            'help_text': 'The name of the key in My Credential System to fetch.'
        }],
        'required': ['url', 'token'],
    },
    # backend is a callable function which will be passed all of the values
    # defined in `inputs`; this function is responsible for taking the arguments,
    # interacting with the third party credential management system in question
    # using Python code, and returning the value from the third party
    # credential management system
    backend=some_lookup_function
)
