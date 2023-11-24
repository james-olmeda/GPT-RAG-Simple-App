# Import necessary libraries and modules
import os
import logging
import requests
import json
from flask import request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Load environment variables from a .env file
load_dotenv()

# Retrieve environment variables
ORCHESTRATOR_ENDPOINT = os.getenv('ORCHESTRATOR_ENDPOINT')
ORCHESTRATOR_URI = os.getenv('ORCHESTRATOR_URI')
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
AZURE_KEY_VAULT_NAME = os.environ["AZURE_KEY_VAULT_NAME"]

# Configure logging with the specified log level
logging.basicConfig(level=LOGLEVEL)

# Function to retrieve a secret from Azure Key Vault
def get_secret(secretName):
    keyVaultName = AZURE_KEY_VAULT_NAME
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    
    # Log the retrieval of a secret
    logging.info(f"[webbackend] retrieving {secretName} secret from {keyVaultName}.")   
    
    retrieved_secret = client.get_secret(secretName)
    return retrieved_secret.value

# Function for handling user input and making a request to the orchestrator
def chatgpt(user_input):
    conversation_id = ""
    question = user_input  
    client_principal_id = ""
    client_principal_name = ""
    
    # Log conversation and user details
    logging.info("[webbackend] conversation_id: " + conversation_id)    
    logging.info("[webbackend] question: " + question)
    logging.info(f"[webbackend] User principal: {client_principal_id}")
    logging.info(f"[webbackend] User name: {client_principal_name}")
   
    try:
        keySecretName = 'host--functionKey--default'
        
        # Retrieve the function key from Azure Key Vault
        functionKey = get_secret(keySecretName)
    except Exception as e:
        # Log and return an error if key retrieval fails
        logging.exception("[webbackend] exception in /api/host--functionKey--default")
        return jsonify({"error": f"Check orchestrator's function key was generated in Azure Portal and try again. ({keySecretName} not found in key vault)"}), 500
        
    try:
        url = ORCHESTRATOR_ENDPOINT
        
        # Prepare the payload for the orchestrator request
        payload = json.dumps({
            "conversation_id": conversation_id,
            "question": question,
            "client_principal_id": client_principal_id,
            "client_principal_name": client_principal_name
        })
        
        # Define headers with the function key for authentication
        headers = {
            'Content-Type': 'application/json',
            'x-functions-key': functionKey            
        }
        
        # Make a GET request to the orchestrator
        response = requests.request("GET", url, headers=headers, data=payload)
        
        # Log the response (limited to the first 500 characters)
        logging.info(f"[webbackend] response: {response.text[:500]}...")   
     
        return response.text
    
    except Exception as e:
        # Log and return an error if the request to the orchestrator fails
        logging.exception("[webbackend] exception in /chatgpt")
        return jsonify({"error": str(e)}), 500
