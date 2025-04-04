import requests
import time
import matplotlib.pyplot as plt
from collections import Counter

def fuzz_api_endpoints(target_url, wordlist="wordlists/api_endpoints.txt"):
    print(f"[*] Fuzzing API Endpoints for {target_url}")
    
    try:
        with open(wordlist, "r") as file:
            endpoints = file.read().splitlines()

        status_counts = Counter()
        response_times = []
        urls_checked = []
        results = {}  # Dictionary to store endpoint results
        
        for endpoint in endpoints:
            url = f"{target_url}/{endpoint}"
            try:
                start_time = time.time()
                response = requests.get(url, timeout=2)
                elapsed_time = round(time.time() - start_time, 3)
                
                status_counts[response.status_code] += 1
                response_times.append(elapsed_time)
                urls_checked.append(url)
                results[url] = response.status_code  # Store results
                
                print(f"{url} - {response.status_code} - {elapsed_time}s")
            
            except requests.exceptions.Timeout:
                print(f"[!] Timeout: {url}")
                status_counts['Timeout'] += 1
                urls_checked.append(url)
                response_times.append(None)
                results[url] = "Timeout"
            except requests.exceptions.RequestException as e:
                print(f"[X] Error: {url} - {e}")
                status_counts['Error'] += 1
                urls_checked.append(url)
                response_times.append(None)
                results[url] = "Error"
        
        # Save results to reports/api_report.txt
        with open("reports/api_report.txt", "w") as file:
            for url, status in results.items():
                file.write(f"{url}: {status}\n")
        
        print("[*] Report saved to reports/api_report.txt")
        
        # Generate a bar chart for status codes
        plt.figure(figsize=(8, 5))
        plt.bar(status_counts.keys(), status_counts.values(), color=['green', 'red', 'blue', 'orange'])
        plt.xlabel("Status Codes")
        plt.ylabel("Count")
        plt.title("API Fuzzing Status Code Distribution")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig("reports/api_status_chart.png")
        plt.close()
        
        print("[*] Graphical report saved to reports/api_status_chart.png")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target = input("Enter the target URL (e.g., http://example.com): ").strip()
    fuzz_api_endpoints(target)
