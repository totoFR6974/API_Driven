import boto3
import json
import os

def lambda_handler(event, context):
    try:
        aws_endpoint = os.environ.get('AWS_ENDPOINT_URL')
        if not aws_endpoint:
            ls_host = os.environ.get('LOCALSTACK_HOSTNAME', '127.0.0.1')
            aws_endpoint = f"http://{ls_host}:4566"
            
        ec2 = boto3.client('ec2', endpoint_url=aws_endpoint)
        
        body_str = event.get('body', '{}')
        body = body_str if isinstance(body_str, dict) else json.loads(body_str)
            
        action = body.get('action')
        instance_id = body.get('instance_id')
        
        if not action or not instance_id:
            return {"statusCode": 400, "body": json.dumps({"message": "Erreur : 'action' ou 'instance_id' manquant."})}
            
        if action == 'start':
            ec2.start_instances(InstanceIds=[instance_id])
            message = f"L'instance {instance_id} a ete demarree."
        elif action == 'stop':
            ec2.stop_instances(InstanceIds=[instance_id])
            message = f"L'instance {instance_id} a ete arretee."
        else:
            return {"statusCode": 400, "body": json.dumps({"message": "Action non reconnue."})}
            
        return {"statusCode": 200, "body": json.dumps({"message": message})}
        
    except Exception as e:
        return {
            "statusCode": 500, 
            "body": json.dumps({"message": "Internal server error", "details": str(e)})
        }
