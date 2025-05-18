# from datetime import datetime
# from pathlib import Path
# from sslyze.json.json_output import ServerScanResultAsJson, SslyzeOutputAsJson
# from sslyze.scanner.models import ServerScanRequest
# from sslyze.scanner.scanner import Scanner
# from sslyze.server_setting import ServerNetworkLocation

# def parse_scan_result(
#     all_server_scan_results,
#     date_scans_started: datetime,
#     date_scans_completed: datetime,
# ) -> str:
#     json_output = SslyzeOutputAsJson(
#         invalid_server_strings=[],  # CLI only
#         server_scan_results=[
#             ServerScanResultAsJson.model_validate(r) for r in all_server_scan_results
#         ],
#         date_scans_started=date_scans_started,
#         date_scans_completed=date_scans_completed,
#     )
#     json_output_as_str = json_output.model_dump_json()
#     path = Path("json_file.json")
#     path.write_text(json_output_as_str)



# async def ssl_tlsCheck(url : str):
#     start = datetime.now()
#     server_location=ServerNetworkLocation(hostname=url)
#     scanner = Scanner()

#     scan_request = [
#         ServerScanRequest(server_location=server_location)
#     ]

#     Scanner.queue_scans(scanner, scan_request)

#     results = []
#     for result in scanner.get_results():
#         results.append(result)
    
#     end = datetime.now()
    
#     parse_scan_result(results, start, end)

import json
import os
import subprocess
import tempfile


def ssl_tlsCheck(ip : str, url: str):
    #todo: add select frontend options for this
    #manage json return better, multiple requests, etc

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmpfile:
            output_path = tmpfile.name
    
    cmd = [
        './analysis/utils/testssl.sh/testssl.sh',
        '-s',
        '-p',
        '--ip', ip, 
        '--sneaky',
        '--ids-friendly',
        '--jsonfile-pretty', output_path,
        url
    ]


    try:
        subprocess.run(cmd,check=True)
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        return data['scanResult'][0]
        
    except subprocess.CalledProcessError:
        raise Exception("Error running testssl.sh")
    except FileNotFoundError:
        raise Exception("JSON result file not found.")
    except json.JSONDecodeError:
        raise Exception("Could not decode JSON.")

    finally:
        if os.path.exists(output_path):
            os.remove(output_path)



    