import base64
import io

client_dynamodb = None
client_s3 = None


TABLE_USERS = {
    'Name': 'Users',
    'Attributes': ['Username', 'Password', 'ProfilePhoto', 'Bio', 'Languages']
}
BUCKET_NAME = "imagenes.semi1"
URL_BUCKET = "https://s3.amazonaws.com/imagenes.semi1/"


# REGISTRAR UN USUARIO
def add_user(username: str, password: str, profile_photo: str, bio: str, languages: list) -> bool:
    # Verificar que no exista el usuario
    if 'Item' in client_dynamodb.get_item(TableName=TABLE_USERS['Name'], Key={'Username': {'S': username}}):
        print("User already exists")
        return False

    url = username+"/ProfilePhoto.jpg"
    item_users = {
        'Username': {'S': username},
        'Password': {'S': password},
        'ProfilePhoto': {'S': URL_BUCKET+url},
        'Bio': {'S': bio},
        'Languages': {'SS': languages}
    }
    try:
        print("Adding user:", item_users)
        # Guardar la foto en bucket S3
        b64_decode = base64.b64decode(profile_photo)
        client_s3.upload_fileobj(
            io.BytesIO(b64_decode), BUCKET_NAME, url,
            ExtraArgs={'ContentType': "image"}
        )
        # Insertar usuario
        client_dynamodb.put_item(
            TableName=TABLE_USERS['Name'], Item=item_users)
    except:
        print("The user has not been added")
        return False
    else:
        print("User added correctly")
        return True


# OBTENER TODA LA DATA DE UN USUARIO
def get_user(__username: str):
    key = {
        'Username': {'S': __username}
    }
    # Obtener el usuario
    user_db = client_dynamodb.get_item(TableName=TABLE_USERS['Name'], Key=key)
    # print("Usuario obtenido:", user_db)
    print("Usuario:", user_db['Item']['Username']['S'])
    print("Bio:", user_db['Item']['Bio']['S'])
    print("Idiomas:", user_db['Item']['Languages']['SS'])
    print("URL foto de perfil:", user_db['Item']['ProfilePhoto']['S'])
    return user_db


# ELIMINAR
def deleteUser(__username: str) -> bool:
    key = {'Username': {'S': __username}}
    client_dynamodb.delete_item(
        TableName=TABLE_USERS['Name'],
        Key=key
    )
    print("User deleted")
    return True
