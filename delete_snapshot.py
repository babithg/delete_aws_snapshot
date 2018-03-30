import boto3
import datetime
from datetime import date
from boto3 import ec2

def main():
    days_back=10   ## this many days back snaphost will be removed
    
    today = datetime.datetime.now()
    earlier_day = (today - datetime.timedelta(days=days_back)).strftime("%Y-%m-%d")
    print("{} days before: {}".format(days_back,earlier_day))
    
    ec = boto3.client('ec2')
    account_ids = ['self']
    snapshot_response = ec.describe_snapshots(OwnerIds=account_ids)

    print ("*"*150+"\n")
    # print (snapshot_response['Snapshots'])
    for snap in snapshot_response['Snapshots']:
        # print ("Deleting snapshot ", snap['SnapshotId'])
        if snap['StartTime'].strftime('%Y-%m-%d') <= earlier_day:
            print("Snapshot {} Going To Remove, Description: {} ,\t Start Time: {} \n ".format(snap['SnapshotId'], snap['Description'], snap['StartTime'].strftime('%Y-%m-%d')))
            if ec.delete_snapshot(SnapshotId=snap['SnapshotId']):
                print("Snapshot Removed Successfully...")
            
    print ("*"*150+"\n")

def lambda_handler(event, context):
    main()
