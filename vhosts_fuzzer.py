import requests
import time
import matplotlib.pyplot as plt
from collections import Counter

def fuzz_virtual_hosts(target_url, wordlist="wordlists/vhosts.txt"):
    print(f"[*] Fuzzing Virtual Hosts for {target_url}")

    report_file = "reports/vhosts_report.txt"  # Report file path

    try:
        with open(wordlist, "r") as file:
            vhosts = file.read().splitlines()

        status_counts = Counter()
        response_times = []
        urls_checked = []
        results = []  # Store results for writing

        for vhost in vhosts:
            clean_target = target_url.lstrip("http://").lstrip("https://")
            headers = {"Host": f"{vhost}.{clean_target}"}

            headers = {"Host": f"{vhost}.{target_url}"}
            url = f"http://{target_url}"  # Target URL for the request

            try:
                start_time = time.time()
                response = requests.get(url, headers=headers, timeout=2)
                elapsed_time = round(time.time() - start_time, 3)

                status_counts[response.status_code] += 1
                response_times.append(elapsed_time)
                urls_checked.append(headers["Host"])

                result = f"{headers['Host']} - {response.status_code} - {elapsed_time}s"
                results.append(result)
                print(result)

            except requests.exceptions.Timeout:
                result = f"[!] Timeout: {headers['Host']}"
                status_counts['Timeout'] += 1
                urls_checked.append(headers["Host"])
                response_times.append(None)
                results.append(result)
                print(result)

            except requests.exceptions.RequestException as e:
                result = f"[X] Error: {headers['Host']} - {e}"
                status_counts['Error'] += 1
                urls_checked.append(headers["Host"])
                response_times.append(None)
                results.append(result)
                print(result)

        # Save results to a text file
        with open(report_file, "w") as f:
            f.write("\n".join(results))

        print(f"[*] Text report saved to {report_file}")

        # Generate a bar chart for status codes
        plt.figure(figsize=(8, 5))
        plt.bar(status_counts.keys(), status_counts.values(), color=['green', 'red', 'blue', 'orange'])
        plt.xlabel("Status Codes")
        plt.ylabel("Count")
        plt.title("Virtual Hosts Fuzzing Status Code Distribution")
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig("reports/vhosts_status_chart.png")
        plt.close()

        print("[*] Graphical report saved to reports/vhosts_status_chart.png")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target = input("Enter the target domain (e.g., example.com): ").strip()
    fuzz_virtual_hosts(target)
