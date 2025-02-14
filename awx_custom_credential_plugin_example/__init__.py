import json

def some_lookup_function(**kwargs):
    # Отримуємо metadata
    metadata = kwargs

    # Записуємо metadata у файл
    try:
        with open("/tmp/metadata.txt", "w") as f:
            json.dump(metadata, f, indent=4)
    except Exception as e:
        with open("/tmp/metadata_error.log", "w") as err_f:
            err_f.write(f"Error writing metadata to file: {str(e)}\n")

    # Основна логіка (залишаємо без змін)
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
