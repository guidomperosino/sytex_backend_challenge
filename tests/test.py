import unittest
import requests
import json


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5000/api/v1"

    def test_get_all_form_templates(self):
        response = requests.get(f"{self.base_url}/form_templates")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_form_template_by_id(self):
        response = requests.get(f"{self.base_url}/form_templates/1c2e007e-2257-447a-bceb-3ae1686c45f3")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_create_form_template_ok(self):
        valid_form_templates = ["valid_form_template_1.json","valid_form_template_1.json"]
        for template_json_file in valid_form_templates:
            with open(f"tests/test_inputs/{template_json_file}") as f:
                input_json = json.load(f)
            response = requests.post(f"{self.base_url}/form_templates", json=input_json)
            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(response.json())
    
    def test_create_form_template_fail(self):
        invalid_form_templates = [
            "invalid_form_template_input_type.json",
            "invalid_form_template_option_entry_1_option.json",
            "invalid_form_template_yes_no_label.json",
            ]
        for template_json_file in invalid_form_templates:
            with open(f"tests/test_inputs/{template_json_file}") as f:
                input_json = json.load(f)
            response = requests.post(f"{self.base_url}/form_templates", json=input_json)
            self.assertEqual(response.status_code, 422)
            self.assertIsNotNone(response.json())


    def test_get_all_form_instances(self):
        response = requests.get(f"{self.base_url}/form_instances")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_get_form_instance_by_id(self):
        response = requests.get(f"{self.base_url}/form_instances/31f28253-b705-4259-9f42-59e57a63cfbd")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_create_form_instance_ok(self):
        valid_form_instances = ["valid_form_instance.json"]
        for instance_json_file in valid_form_instances:
            with open(f"tests/test_inputs/{instance_json_file}") as f:
                input_json = json.load(f)
            response = requests.post(f"{self.base_url}/form_instances", json=input_json)
            self.assertEqual(response.status_code, 201)
            self.assertIsNotNone(response.json())
    
    def test_create_form_instance_fail(self):
        invalid_form_instances = ["invalid_form_instance_option.json"            ]
        for instance_json_file in invalid_form_instances:
            with open(f"tests/test_inputs/{instance_json_file}") as f:
                input_json = json.load(f)
            response = requests.post(f"{self.base_url}/form_instances", json=input_json)
            self.assertEqual(response.status_code, 400)
            self.assertIsNotNone(response.json())

if __name__ == "__main__":
    unittest.main()