import requests
import time


class TripoAPI:
    def __init__(self, api_key, timeout=120):
        self.api_key = api_key
        self.api_url = "https://api.tripo3d.ai/v2/openapi"
        self.polling_interval = 2  # Poll every 2 seconds
        self.timeout = timeout  # Timeout in seconds

    def text_to_3d(self, prompt):
        start_time = time.time()
        response = self._submit_task(
            "text_to_model", {"prompt": prompt}, start_time)
        return self._handle_task_response(response, start_time)

    def image_to_3d(self, image_data):
        start_time = time.time()
        file_data = {
            "type": "png",  # Assume PNG for simplicity; adjust as needed
            "data": image_data
        }
        response = self._submit_task(
            "image_to_model", {"file": file_data}, start_time)
        return self._handle_task_response(response, start_time)
    
    def multiview_to_3d(self, image_data, side="LEFT"):
        start_time = time.time()
        file_data = [
            {
            "type": "png",  # Assume PNG for simplicity; adjust as needed
            "data": image_data[0]
            },
            {
            "type": "png",
            "data": image_data[1]
            },
            {
            "type": "png",
            "data": image_data[2]
            }
        ]
        response = self._submit_task(
            "multiview_to_model", {"files": file_data}, start_time, mode=side)
        return self._handle_task_response(response, start_time)
    
    def refine_3d(self, task_id):
        start_time = time.time()
        response = self._submit_task(
            "refine_model", {"draft_model_task_id": task_id}, start_time)
        return self._handle_task_response(response, start_time)
    
    def check_balance(self):
        response = requests.get(
                f"{self.api_url}/user/balance",
                headers={"Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"}
                )
        if response.status_code == 200:
            remain_balance = response.json()['data']['balance']
            return {
                'status': 'success',
                'balance': remain_balance,
            }
        else:
            return {
                'status': 'error',
                'message': response.json().get('message', 'An unexpected error occurred'),
            }

    def _submit_task(self, task_type, task_payload, start_time, mode=None):
        if time.time() - start_time > self.timeout:
            return {'status': 'error', 'message': 'Operation timed out', 'task_id': None}
        print(f"Submitting task: {task_type}")
        if 'prompt' in task_payload:
            print(f"Task prompt: {task_payload['prompt']}")
        if 'file' in task_payload:
            print(f"Task file type: {task_payload['file']['type']}")
        if 'files' in task_payload:
            print(f"Task files types: {task_payload['files'][0]['type']}, {task_payload['files'][1]['type']}, {task_payload['files'][2]['type']}")
        if mode is None:
            response = requests.post(
                f"{self.api_url}/task",
                headers={"Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"},
                json={"type": task_type, **task_payload}
            )
        else:
            response = requests.post(
                f"{self.api_url}/task",
                headers={"Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}"},
                json={"type": task_type, **task_payload, "mode": mode}
            )
        return response

    def _handle_task_response(self, response, start_time):
        if response.status_code == 200:
            task_id = response.json()['data']['task_id']
            print(f"Task ID: {task_id}")
            return self._poll_task_status(task_id, start_time)
        else:
            return {
                'status': 'error',
                'message': response.json().get('message', 'An unexpected error occurred'),
                'task_id': None
            }

    def _poll_task_status(self, task_id, start_time):
        last_progress = -1
        while True:
            if time.time() - start_time > self.timeout:
                print("Operation timed out.")
                return {'status': 'error', 'message': 'Operation timed out', 'task_id': task_id}

            response = requests.get(
                f"{self.api_url}/task/{task_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )

            if response.status_code == 200:
                data = response.json()['data']
                status = data['status']
                progress = data.get('progress', 0)

                # Print progress if it has changed.
                if progress != last_progress:
                    print(f"Task Progress: {progress}%")
                    last_progress = progress

                if status in ['success', 'failed', 'cancelled', 'unknown']:
                    if status == 'success':
                        print(f"Task completed successfully in {(time.time() - start_time):.2f} seconds.")
                        return self._download_model(data['output']['model'], task_id)
                    else:
                        print(
                            f"Task did not complete successfully. Status: {status}")
                        return {'status': status, 'message': 'Task did not complete successfully', 'task_id': task_id}
            else:
                print("Failed to get task status.")
                return {'status': 'error', 'message': 'Failed to get task status', 'task_id': task_id}

            time.sleep(self.polling_interval)  # Wait before polling again

    def _download_model(self, model_url, task_id):
        print(f"Downloading model: {model_url}")
        response = requests.get(model_url)
        if response.status_code == 200:
            return {'status': 'success', 'model': response.content, 'task_id': task_id}
        else:
            return {'status': 'error', 'message': 'Failed to download model', 'task_id': task_id}
    