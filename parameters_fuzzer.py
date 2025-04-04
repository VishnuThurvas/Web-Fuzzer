import requests
import time
import matplotlib.pyplot as plt
from collections import Counter

def fuzz_parameters(target_url, wordlist="wordlists/parameters.txt"):
    print(f"[*] Fuzzing Parameters for {target_url}")

    report_file = "reports/parameters_report.txt"  # Report file path

    try:
        with open(wordlist, "r") as file:
            parameters = file.read().splitlines()

        status_counts = Counter()
        response_times = []
        urls_checked = []
        results = []  # Store results to write later

        for param in parameters:
            url = f"{target_url}?{param}=test"
            try:
                start_time = time.time()
                response = requests.get(url, timeout=2)
                elapsed_time = round(time.time() - start_time, 3)

                status_counts[response.status_code] += 1
                response_times.append(elapsed_time)
                urls_checked.append(url)

                result = f"{url} - {response.status_code} - {elapsed_time}s"
                results.append(result)
                print(result)

            except requests.exceptions.Timeout:
                result = f"[!] Timeout: {url}"
                status_counts['Timeout'] += 1
                urls_checked.append(url)
                response_times.append(None)
                results.append(result)
                print(result)

            except requests.exceptions.RequestException as e:
                result = f"[X] Error: {url} - {e}"
                status_counts['Error'] += 1
                urls_checked.append(url)
                response_times.append(None)
                results.append(result)
                print(result)

        # Save results to the text file
        with open(report_file, "w") as f:
            f.write("\n".join(results))

        print(f"[*] Text report saved to {report_file}")

        # Generate a bar chart for status codes
        plt.figure(figsize=(8, 5))
        plt.bar(status_counts.keys(), status_counts.values(), color=['green', 'red', 'blue', 'orange'])
        plt.xlabel("Status Codes")
        plt.ylabel("Count")
        plt.title("Parameter Fuzzing Status Code Distribution")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig("reports/parameters_status_chart.png")
        plt.close()

        print("[*] Graphical report saved to reports/parameters_status_chart.png")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target = input("Enter the target URL (e.g., http://example.com): ").strip()
    fuzz_parameters(target)
