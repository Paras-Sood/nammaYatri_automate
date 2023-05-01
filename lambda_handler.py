import json,os,requests,boto3,uuid

gmaps_base_url = "https://maps.googleapis.com/maps/api/"
METRICS_TABLE="botMetrics"
RIDE_DATA_TABLE="rideData"
dynamodb=boto3.client('dynamodb')

def buildResponse(statusCode,body):
    return {
        'statusCode':statusCode,
        'headers': {
            "Access-Control-Allow-Origin": "*"
        },
        'body':json.dumps(body)
    }

def addInvalidLocation(place):
    # Add the place to a table so that the company can know that which location is most demanding and is not be served by them
    pass
    
def updateMetrics(variable):
    Metrics_Item_Id=''
    data=dynamodb.scan(
        TableName=METRICS_TABLE
    )
    if data['Count']==0:
        print("Does not exist!")
        id=str(uuid.uuid4())
        dynamodb.put_item(
            TableName=METRICS_TABLE,
            Item={
                'id':{'S':id},
                'src': {'N': '0'},
                'destination': {'N': '0'},
                'numCustomers':{'N': '0'},
                'datev':{'N':'0'},
                'timev':{'N':'0'},
                'priceConfirmation':{'N':'0'},
                'complete':{'N':'0'}
            }
        )
    else:
        Metrics_Item_Id=data['Items'][0]['id']['S']
    if Metrics_Item_Id=='':
        data=dynamodb.scan(
            TableName=METRICS_TABLE
        )
        item=data['Items'][0]
        Metrics_Item_Id=item['id']['S']
    dynamodb.update_item(
        TableName = METRICS_TABLE,
        Key={'id': {'S':Metrics_Item_Id}},
        UpdateExpression=f'SET {variable} = {variable} + :val',
        ExpressionAttributeValues={':val': {'N':f"{1}"}}
    )
    return

def autoCompletePlace(place):
    url=gmaps_base_url+"place/autocomplete/json?key="+os.environ.get("MAPS_API_KEY")+"&input="+place
    response=requests.get(url)
    response=response.json()
    places=[]
    for p in response['predictions']:
        places.append({'place':p['description'],'place_id':p['place_id']})
        break # this break is for picking up the first relevant prediction
        # We can send all the predictions to user and ask him/her to select one
    message="Please choose an option"
    if len(places)==0:
        message="invalid response"
    if len(places)>5:
        places=places[:5]
    return {
        'places':places,
        'message':message
    }


def validate(slots):
    slotOptions=['Source','Destination','numCustomers','Date','Time','priceConfirmation']
    dbVal={
        'Source':'src',
        'Destination':'destination',
        'numCustomers':'numCustomers',
        'Date':'datev',
        'Time':'timev',
        'priceConfirmation': 'priceConfirmation'
    }
    for opt in slotOptions:
        if not slots[opt]:
            updateMetrics(dbVal[slots[opt]])
            return {
                'isValid': False,
                'violatedSlot': opt
            }
    return {'isValid': True}
   
def getLocation(place):
    resp=autoCompletePlace(place)
    place_id=resp['places'][0]['place_id']
    url=gmaps_base_url+"place/details/json?key="+os.environ.get("MAPS_API_KEY")+"&place_id="+place_id
    data=requests.get(url)
    data=data.json()
    return data['result']['geometry']['location']

def getDist(src,dest):
    url=gmaps_base_url+"distancematrix/json?key="+os.environ.get("MAPS_API_KEY")+"&origins="+str(src['lat'])+"%2C"+str(src['lng'])+"&destinations="+str(dest['lat'])+"%2C"+str(dest['lng'])
    resp=requests.get(url)
    resp=resp.json()
    dist=resp['rows'][0]['elements'][0]['distance']['text']
    km=dist.split(' ')
    return float(km[0])
    
def getPrice(src,dest):
    dist=getDist(src,dest)
    return dist*10
    

def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    validation_result = validate(event['sessionState']['intent']['slots'])
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                    }
                }
            }
            if validation_result['violatedSlot']=='priceConfirmation':
                srcLatLong=getLocation(slots['Source']['value']['originalValue'])
                destLatLong=getLocation(slots['Destination']['value']['originalValue'])
                price=getPrice(srcLatLong,destLatLong)
                response['messages']=[{
                    'contentType':'PlainText',
                    "content":f"The estimated price for the ride is Rs. {price}. You need to pay the driver this amount. Should I continue with the booking?"
                }]
            print(response)
            return response
        else:
            print("In elseee")
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                    }
                },
                "messages":[{
                    "contentType":"PlainText",
                    "content":"The estimated price for the ride is Rs. 150. You need to pay the driver this amount. Should I continue with the booking?"
                }]
            }
            return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        updateMetrics('complete')
        srcLatLong=getLocation(slots['Source']['value']['originalValue'])
        destLatLong=getLocation(slots['Destination']['value']['originalValue'])
        dist=getDist(srcLatLong,destLatLong)
        id=str(uuid.uuid4())
        dynamodb.put_item(
            TableName=RIDE_DATA_TABLE,
            Item={
                'id':{'S':id},
                'phoneNumber':{'S':event['sessionId'].split(':')[1]},
                'source': {'S': slots['Source']['value']['originalValue']},
                'destination': {'S': slots['Destination']['value']['originalValue']},
                'distance': {'S':f"{str(dist)} km"},
                'numCustomers':{'N': slots['numCustomers']['value']['originalValue']},
                'date':{'S':slots['Date']['value']['originalValue']},
                'time':{'S':slots['Time']['value']['originalValue']}
            }
        )
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name':intent,
                    'slots': slots,
                    'state':'Fulfilled'
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    'content':"Thank you for trusting us. Your details have been recorded. We will update you shortly with the status of your ride."
                }
            ]
        }
            
        return response
