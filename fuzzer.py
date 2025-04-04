import os
import directories_fuzzer
import vhosts_fuzzer
import api_fuzzer
import parameters_fuzzer
import subdomain_fuzzer

if not os.path.exists("reports"):
    os.makedirs("reports")  # Ensure the reports directory exists

target_url = input("Enter the target URL (e.g., http://example.com): ").strip()

print("\nStarting Directory Fuzzing...")
directories_fuzzer.fuzz_directories(target_url)

print("\nStarting Virtual Host Fuzzing...")
vhosts_fuzzer.fuzz_virtual_hosts(target_url)

print("\nStarting API Fuzzing...")
api_fuzzer.fuzz_api_endpoints(target_url)

print("\nStarting Parameter Fuzzing...")
parameters_fuzzer.fuzz_parameters(target_url)

print("\nStarting Subdomain Fuzzing...")
subdomain_fuzzer.fuzz_subdomains(target_url)

print("\n✅ All fuzzing tasks completed! Check the 'reports/' folder for graphical reports.")
