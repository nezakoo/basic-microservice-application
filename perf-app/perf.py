import asyncio
import aiohttp
import time
import json
import matplotlib.pyplot as plt
import sys
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Default output directory
output_dir = '/app/output'

async def fetch(url, session):
    start_time = time.time()
    async with session.get(url) as response:
        elapsed = time.time() - start_time
        return {'status': response.status, 'response_time': elapsed}

async def send_requests(url, total_requests=100, interval=0.1):
    results = []
    async with aiohttp.ClientSession() as session:
        for i in range(total_requests):
            result = await fetch(url, session)
            results.append(result)
            logging.info(f"Request {i + 1}: Status {result['status']}, Response Time {result['response_time']:.4f} seconds")
            time.sleep(interval)
    return results

def ensure_http(url):
    """Ensure the URL has http:// or https://, prepend http:// if missing."""
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    return url

def analyze_results(results):
    status_codes = {}
    response_times = []
    for result in results:
        status_codes[result['status']] = status_codes.get(result['status'], 0) + 1
        response_times.append(result['response_time'])

    # Generate and save a histogram of response times
    histogram_path = f'{output_dir}/response_times.png'
    plt.hist(response_times, bins=10, color='blue', edgecolor='black')
    plt.title('Response Time Distribution')
    plt.xlabel('Response Time (seconds)')
    plt.ylabel('Frequency')
    plt.savefig(histogram_path)
    plt.show()

    return status_codes, sum(response_times) / len(response_times)

def main(url, total_requests, interval):
    try:
        results = asyncio.run(send_requests(url, total_requests, interval))
        status_codes, average_response_time = analyze_results(results)
        report = {
            'total_requests': total_requests,
            'average_response_time': average_response_time,
            'status_codes': status_codes
        }
        report_path = f'{output_dir}/report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=4)
        logging.info("Report saved to %s", report_path)
    except KeyboardInterrupt:
        logging.info("Execution interrupted by user. Exiting...")
        sys.exit(0)

if __name__ == '__main__':
    # Default values and command-line arguments
    default_url = "http://localhost:5000/api"
    default_total_requests = 100
    default_interval = 0.1

    url = sys.argv[1] if len(sys.argv) > 1 else default_url
    total_requests = int(sys.argv[2]) if len(sys.argv) > 2 else default_total_requests
    interval = float(sys.argv[3]) if len(sys.argv) > 3 else default_interval

    # Ensure the URL is properly formatted
    url = ensure_http(url)

    # Use command-line argument for output directory if provided
    if len(sys.argv) > 4:
        output_dir = sys.argv[4]

    # Print messages if default values are used
    if len(sys.argv) <= 1:
        logging.info(f"URL not specified. Using default value: {default_url}")
    if len(sys.argv) <= 2:
        logging.info(f"Total requests not specified. Using default value: {default_total_requests}")
    if len(sys.argv) <= 3:
        logging.info(f"Interval not specified. Using default value: {default_interval}")

    main(url, total_requests, interval)
