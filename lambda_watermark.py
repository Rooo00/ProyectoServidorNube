import boto3
import psycopg2
import time
import logging

# Variables de entorno
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/244950045432/cafeteria-queue"
DB_HOST = "database-1.cluster-c5vnxd1pixuk.us-east-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "exLNSW]WbMWn]?EEg4<b3A)Xm41k"

# Conexión a RDS
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        logging.error(f"Error de conexión a RDS: {e}")
        return None



def process_orders():
    
    sqs = boto3.client('sqs', region_name='us-east-1') 
    
    conn = get_db_connection()
    if not conn:
        logging.critical("No se pudo iniciar la aplicación sin base de datos.")
        return

    cursor = conn.cursor()
    logging.info("Escuchando pedidos...")

    while True:
        try:
            # Polling
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10 
            )

            if 'Messages' in response:
                for message in response['Messages']:
                    body = message['Body']
                    receipt_handle = message['ReceiptHandle']
                    
                    try:

                        # Formato  (Tipo de cafe | timestamp )
                        coffee_type, timestamp_str = body.split('|')
                        
                        # Insertar el pedido en la tabla coffee_orders
                        cursor.execute(
                            """
                            INSERT INTO coffee_orders (timestamp, coffee_type, order_status) 
                            VALUES (%s, %s, 'created')
                            """,
                            (timestamp_str, coffee_type)
                        )
                        
                        # Borrar el mensaje de SQS después de procesarlo
                        sqs.delete_message(
                            QueueUrl=QUEUE_URL,
                            ReceiptHandle=receipt_handle
                        )
                        logging.info(f"Pedido procesado y borrado de la cola: {coffee_type}")
                        
                    except ValueError:
                        logging.error(f"Formato de mensaje inválido: {body}. Se eliminará para no bloquear la cola.")
                        sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt_handle)
                        
                    except psycopg2.Error as db_error:
                        logging.error(f"Error al insertar en RDS: {db_error}")
                        
                        
            else:
                logging.debug("Sin pedidos nuevos en la caja...")
                
        except Exception as sqs_error:
            logging.error(f"Error de conexión/lectura con SQS: {sqs_error}")
            

if __name__ == '__main__':
    process_orders()
