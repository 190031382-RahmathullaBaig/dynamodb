from flask import Flask, render_template, request
import boto3
from botocore.exceptions import ClientError
#import sqlite3 as db;

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', endpoint_url="http://dynamodb.ap-south-1.amazonaws.com")

l = [10, 20, 30, 'abc', 40.5];
v1 = 20;
v2 = "name20"

@app.route('/index')
@app.route('/')
def index():
	return render_template ('blog/index.html', val = l, tit = "new title");

@app.route('/create_table')
def create_table():
	table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
	return render_template ('blog/index.html', val = l, tit = "new title");

@app.route('/insert_data')
def insert_data():
	table = dynamodb.Table('Movies')
	response = table.put_item(Item={'year': 2022, 'title': 'New Title', 'info': {'plot': 'plot', 'rating': 5}})
	return render_template ('blog/index.html', val = l, tit = "new title");

@app.route('/select_table')
def select_table():
	table = dynamodb.Table('Movies')
	result = "";
	try:
		response = table.get_item(Key={'year': 2022, 'title': 'New Title'})
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		result = response['Item']
		return render_template ('blog/index.html', val = l, tit = "new title", result = result);
	return render_template ('blog/index.html', val = l, tit = "new title", result = result);

@app.route('/page2')
def page2():
	return render_template ('blog/page2.html');

@app.route('/calculate', methods = ['post', 'get'])
def calculate():
	a = int(request.form.get("t1"));
	b = int(request.form.get("t2"));
	c = a+b;
	return render_template ('blog/page2.html', ans = c);

if __name__ == "__main__":
	app.run (debug = True);
