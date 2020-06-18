from faker import Faker
import pyodbc
import random
import requests
import urllib3
import json

def main():
    print('starting Generate Users Script...')
    gender = 'male'
    for _ in range(30):
        GenerateUser(gender)

def GenerateUser(gender_in):
    print('gererating user')
    faker = Faker()
    username = ''
    password = 'password'
    gender = gender_in
    knownAs = ''
    dateofbirth = faker.date_of_birth(minimum_age=18, maximum_age = 40)
    city = faker.city()
    country = faker.country()

    if gender == 'female':
        username = faker.first_name_female()
    else:
        username = faker.first_name_male()

    knownAs = username
    dateofbirth = dateofbirth.strftime("%m/%d/%Y")

    url = 'http://localhost:5000/api/auth/register'
    json_data = {
        'username': username,
        'password': password,
        'gender': gender,
        'knownAs': knownAs,
        'DateOfBirth': dateofbirth,
        'city': city,
        'country': country
    }

    r = requests.post(url, json=json_data, verify=False)
    status_code = r.status_code

    if status_code == 201:
        data = r.json()
        user_id = data['id']
        addPhoto(user_id, gender)

def addPhoto(user_id, gender):
    print('adding photo for user')
    photo_url = GetPhotoUrl(gender)
    
    url = 'http://localhost:5000/api/users/{}/photos/addphotourl'.format(user_id)
    json_data = {
        'url': photo_url,
        'UserId': user_id
    }

    requests.post(url, json=json_data, verify=False)

    print('user complete\n\n')

def GetPhotoUrl(gender):
    photo_url = ''
    url = 'https://randomuser.me/api/?inc=picture&gender={}'.format(gender)
    data = requests.get(url, verify=False).json()
    for result in data['results']:
        for pic in result['picture']['large']:
            photo_url += pic

    return photo_url


if __name__ == "__main__":
    main()