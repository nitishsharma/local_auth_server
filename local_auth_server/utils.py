import logging

def log_request(request: str):
    logging.info(f"Received query: {request}")