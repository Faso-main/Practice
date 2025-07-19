import boto3
# ---> aws configure
# Введите: Access Key, Secret Key, регион (например, us-east-1)

# Инициализация клиента EC2
ec2 = boto3.client('ec2')

# 1. Список всех EC2-инстансов
response = ec2.describe_instances()
print("Список инстансов EC2:")
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(f"ID: {instance['InstanceId']}, Status: {instance['State']['Name']}")

# 2. Запуск нового инстанса (микро-тариф, Amazon Linux)
new_instance = ec2.run_instances(
    ImageId='ami-0abcdef1234567890',  # AMI ID (зависит от региона)
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='ваш-ключ-ssh',  # Имя ключа EC2 Key Pair
    SecurityGroupIds=['sg-12345678']  # ID Security Group
)
instance_id = new_instance['Instances'][0]['InstanceId']
print(f"Запущен новый инстанс: {instance_id}")

# 3. Остановка инстанса
ec2.stop_instances(InstanceIds=[instance_id])
print(f"Инстанс {instance_id} остановлен")

# 4. Удаление инстанса
ec2.terminate_instances(InstanceIds=[instance_id])
print(f"Инстанс {instance_id} удалён")