import json
import logging
from awx.main.credential_plugins.plugin import CredentialPlugin  # Змінено імпорт для відповідності структурі AWX

# Ініціалізація логера
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MyCustomCredentialPlugin(CredentialPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_credential_data(self, context):
        """
        Метод, який отримує контекст та повертає облікові дані.
        """
        # Перевірка, чи context є словником
        if not isinstance(context, dict):
            logger.error("Context is not a dictionary!")
            raise TypeError("Context must be a dictionary")

        # Записуємо весь контекст у файл /tmp/metadata.txt
        try:
            with open('/tmp/metadata.txt', 'a') as f:
                f.write("Context Data:\n")
                f.write(json.dumps(context, indent=4))  # Записуємо весь контекст у форматі JSON
                f.write("\n\n")
        except (IOError, TypeError) as e:
            logger.error(f"Failed to write context data to file: {e}")

        # Основна логіка (залишаємо без змін)
        url = context.get('url')
        token = context.get('token')
        identifier = context.get('identifier')

        # Перевірка обов'язкових полів
        if not url or not token:
            logger.error("Missing required fields: url or token")
            raise ValueError("Missing required fields: url or token")

        if token != 'VALID':
            logger.error("Invalid token provided!")
            raise ValueError('Invalid token!')

        value = {
            'username': 'mary',
            'email': 'mary@example.org',
            'password': 'super-secret'
        }

        if identifier in value:
            return value[identifier]

        logger.error(f'Could not find a value for {identifier}.')
        raise ValueError(f'Could not find a value for {identifier}.')

# Створення плагіну
example_plugin = MyCustomCredentialPlugin(
    name='Example AWX Credential Plugin',
    inputs={
        'fields': [
            {
                'id': 'url',
                'label': 'Server URL',
                'type': 'string',
            },
            {
                'id': 'token',
                'label': 'Authentication Token',
                'type': 'string',
                'secret': True,
            }
        ],
        'metadata': [
            {
                'id': 'identifier',
                'label': 'Identifier',
                'type': 'string',
                'help_text': 'The name of the key in My Credential System to fetch.'
            }
        ],
        'required': ['url', 'token'],
    }
)
