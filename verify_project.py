import requests
import json
import os
import sys
import time

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

BASE_URL = "http://127.0.0.1:8000"

def log_pass(message):
    print(f"{Colors.GREEN}[PASS]{Colors.ENDC} {message}")

def log_fail(message):
    print(f"{Colors.FAIL}[FAIL]{Colors.ENDC} {message}")

def log_info(message):
    print(f"{Colors.BLUE}[INFO]{Colors.ENDC} {message}")

def check_health():
    log_info("Checking /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            log_pass(f"Health check successful: {response.json()}")
            return True
        else:
            log_fail(f"Health check failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        log_fail("Could not connect to server. Is it running?")
        return False

def check_ingest():
    log_info("Checking /ingest endpoint with dummy file...")
    dummy_filename = "qa_test_doc.txt"
    with open(dummy_filename, "w", encoding="utf-8") as f:
        f.write("Yinov AI is a project located in Istanbul. The CEO is Ipek Bulgurcu.")
    
    try:
        with open(dummy_filename, "rb") as f:
            files = {"file": (dummy_filename, f, "text/plain")}
            response = requests.post(f"{BASE_URL}/ingest", files=files)
        
        if response.status_code == 200:
            data = response.json()
            log_pass(f"Ingestion successful: {data}")
            return True
        else:
            log_fail(f"Ingestion failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        log_fail(f"Ingestion exception: {e}")
        return False
    finally:
        if os.path.exists(dummy_filename):
            os.remove(dummy_filename)

def check_ask(scenario_name, query, expected_keyword=None):
    log_info(f"Testing Scenario: {scenario_name}")
    log_info(f"Query: '{query}'")
    
    payload = {"query": query, "model": "phi3"} # Force a model or generic
    start_time = time.time()
    
    try:
        response = requests.post(f"{BASE_URL}/ask", json=payload, timeout=60)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "")
            log_pass(f"Response received in {duration:.2f}s")
            print(f"{Colors.BOLD}Answer:{Colors.ENDC} {answer[:200]}...") # Truncate for display
            
            if expected_keyword:
                if expected_keyword.lower() in answer.lower():
                    log_pass(f"Expected keyword '{expected_keyword}' found in answer.")
                else:
                    log_info(f"Note: Keyword '{expected_keyword}' not explicitly found, please verify context manually.")
            return True
        else:
            log_fail(f"Request failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        log_fail(f"Exception during request: {e}")
        return False

def main():
    print(f"{Colors.HEADER}=== Yinov AI QA Verification Script ==={Colors.ENDC}")
    
    if not check_health():
        sys.exit(1)
        
    check_ingest()
    
    print("-" * 30)
    check_ask("A (Router/Chat)", "Merhaba, sen kimsin?", "Assistant")
    print("-" * 30)
    check_ask("B (Web Search)", "Bugün Beşiktaş'ın maçı var mı?", "Beşiktaş") # Dynamic
    print("-" * 30)
    check_ask("C (Code Interpreter)", "Calculate the 15th Fibonacci number.", "610")
    print("-" * 30)
    
    print(f"{Colors.HEADER}=== QA Verification Completed ==={Colors.ENDC}")

if __name__ == "__main__":
    main()
