"""
  // Trustwave Password Changer //

Usage:
    main.py newpassword <new-password>
    main.py testconnection
    main.py -h | --help
    main.py --version

Options:
    -h --help   Show this screen.
    --version   Show version
"""

import csv
import json
import requests
from docopt import docopt

def updatePasswordForAllAppsTo(new_password):
    results = {
        'failed-to-update': [],
        'dev-apps-updated': 0,
        'prod-apps-updated': 0
    }
    all_dev_apps = getAppNamesAndUrlsFromCsv('dev_apps.csv')
    all_prod_apps = getAppNamesAndUrlsFromCsv('prod_apps.csv')
    print('Updating passwords in Trustwave dev...')
    for app in all_dev_apps:
        app_name = app[0]
        app_url = app[1]
        try:
            print('Updating %s' % app_name)
            changePasswordForAppTo(new_password, app_name, app_url, 'dev')
            results['dev-apps-updated'] += 1
        except:
            results['failed-to-update'].append(app_name)
    print('Updating passwords in Trustwave prod...')
    for app in all_prod_apps:
        app_name = app[0]
        app_url = app[1]
        try:
            print('Updating %s' % app_name)
            changePasswordForAppTo(new_password, app_name, app_url, 'prod')
            results['prod-apps-updated'] += 1
        except:
            results['failed-to-update'].append(app_name)
    return results

def getAppNamesAndUrlsFromCsv(filename):
    csvfile = open(filename)
    reader = csv.reader(csvfile)
    apps_and_urls = list(reader)
    return apps_and_urls

def changePasswordForAppTo(new_password, app_name, app_url, environment):
    api_url = getUrlFor(environment) # dev/prod-specific URL
    app_id = getApplicationIdByName(app_name, api_url)
    password_change = sendPasswordUpdateCallFor(app_name, app_id, app_url, api_url, new_password)
    return password_change

def getUrlFor(environment):
    dev_api_url = 'REDACTED'
    prod_api_url = 'REDACTED'
    current_api_url = ''    
    if(environment == 'dev'):
        current_api_url = dev_api_url
    elif(environment == 'prod'):
        current_api_url = prod_api_url
    return current_api_url

def getApplicationIdByName(app_name, api_url):
    headers = {'content-type': 'application/json'}
    api_call_url = api_url + 'application/' + app_name + '/id'
    api_call = requests.get(api_call_url)
    response = api_call.content
    json_response = json.loads(response)
    app_id = json_response['application-id']
    return app_id

def sendPasswordUpdateCallFor(app_name, app_id, app_url, api_url, new_password):
    username = 'REDACTED'
    headers = {'content-type': 'application/json'}
    body = {
        'application-name': app_name,
        'url': app_url,
        'application-params': {
            'traversal-params': {
                'username': username,
                'password': new_password
            }
        }
    }
    api_call_url = api_url + 'application/' + app_id
    api_call = requests.put(api_call_url, data=json.dumps(body), headers=headers)
    return api_call

def printPasswordUpdateResults(results):
    print('%d apps were updated in Trustwave Dev.' % results['dev-apps-updated'])
    print('%d apps were updated in Trustwave Prod.' % results['prod-apps-updated'])
    if(len(results['failed-to-update']) > 0):
        print('THE FOLLOWING APPS FAILED TO UPDATE: ')
        for app in results['failed-to-update']:
            print(app)

def testTrustwaveConnection():
    # TODO change to testing by status code
    test_prod_app = 'impact-prod'
    test_dev_app = 'impact-prod'
    dev_api_url = getUrlFor('dev')
    prod_api_url = getUrlFor('prod')
    dev_app_id = getApplicationIdByName(test_dev_app, dev_api_url)
    prod_app_id = getApplicationIdByName(test_prod_app, prod_api_url)
    if(dev_app_id != 'null' and dev_app_id != None):
        print('Connection to Trustwave Dev API was successful.')
    else:
        print('Connection to Trustwave Dev API FAILED.')
    if(prod_app_id != 'null' and prod_app_id != None):
        print('Connection to Trustwave Prod API was successful.')
    else:
        print('Connection to Trustwave Prod API FAILED.')

def main(user_args):
    if(user_args['testconnection']):
        print('Testing Trustwave connection...')
        testTrustwaveConnection()
    elif(user_args['newpassword']):
        print('Updating password in Trustwave...')
        results = updatePasswordForAllAppsTo(user_args['<new-password>'])
        printPasswordUpdateResults(results)

if __name__ == '__main__':
    user_args = docopt(__doc__, version='Trustwave Password Changer 0.1') # docopt parses user args into a dictionary
    main(user_args)