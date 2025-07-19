import boto3
# ---> aws configure
# Введите: Access Key, Secret Key, регион (например, us-east-1)


# Инициализация клиента S3
s3 = boto3.client('s3')

# 1. Список всех bucket'ов
response = s3.list_buckets()
print("Список bucket'ов:")
for bucket in response['Buckets']:
    print(f"- {bucket['Name']}")

# 2. Загрузка файла в S3
bucket_name = 'ваш-bucket-name'
file_path = 'local_file.txt'
s3_key = 'folder/remote_file.txt'

s3.upload_file(file_path, bucket_name, s3_key)
print(f"Файл {file_path} загружен в {bucket_name}/{s3_key}")

# 3. Скачивание файла из S3
download_path = 'downloaded_file.txt'
s3.download_file(bucket_name, s3_key, download_path)
print(f"Файл скачан как {download_path}")

# 4. Удаление файла из S3
s3.delete_object(Bucket=bucket_name, Key=s3_key)
print(f"Файл {s3_key} удалён из {bucket_name}")