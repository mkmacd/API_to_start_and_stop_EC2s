import json
import boto3

def lambda_handler(event, context):
    # Specify your desired filter criteria
    filters = [{'Name': 'instance-state-name', 'Values': ['running']},
               {'Name': 'tag:Project', 'Values': ['projectx']}]

    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name='eu-west-2')

    try:
        # Describe instances matching the specified filters
        response = ec2.describe_instances(Filters=filters)
        instances = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]


        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])


        if instances:
            # Stop the instances
            ec2.stop_instances(InstanceIds=instances)

            return {
                'statusCode': 200,
                'body': json.dumps(f'Success: Stopped instances - {instances}')
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps('Info: No instances matching the filter criteria')
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
