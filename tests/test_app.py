import unittest

import requests


class AppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.addr = 'http://localhost:5000'

    @classmethod
    def tearDownClass(cls):
        ...

    def test_00_index(self):
        res = requests.get(self.addr)
        self.assertTrue(res.ok)

    def test_01_select(self):
        addr = f'{self.addr}/api/db/ruleset'

        res = requests.get(addr, params={
            'columns': ['time'],
        })
        self.assertEqual(res.status_code, 500)
        print(res.text)

        res = requests.get(addr, params={
            'columns': ['id'],
            'mode': 'normal',
        })
        self.assertTrue(res.ok)

        res = requests.get(addr, params={})
        self.assertTrue(res.ok)

    def test_02_insert(self):
        addr = f'{self.addr}/api/db/ruleset'

        res = requests.post(addr, json='test')
        self.assertEqual(res.status_code, 400)
        print(res.text)

        res = requests.post(addr, json={
            'name': 'test',
        })
        self.assertEqual(res.status_code, 500)
        print(res.text)

        res = requests.post(
            addr,
            json={
                'id': 0,
                'name': 'test',
                'version': '1.0.0',
                'description': 'test',
                'mode': 'normal',
                'xml': '',
            },
        )
        self.assertTrue(res.ok)

    def test_03_update(self):
        addr = f'{self.addr}/api/db/ruleset'

        res = requests.put(addr, json={
            'xml': '',
        })
        self.assertEqual(res.status_code, 400)
        print(res.text)

        res = requests.put(addr, json={
            'id': 1,
            'xml': [0],
        })
        self.assertEqual(res.status_code, 500)
        print(res.text)

        res = requests.put(addr, json={
            'id': 1,
            'xml': 'helloworld',
        })
        self.assertTrue(res.ok)

    def test_04_delete(self):
        addr = f'{self.addr}/api/db/ruleset'

        res = requests.delete(addr, json={
            'id': 0,
        })
        self.assertEqual(res.status_code, 400)
        print(res.text)

        res = requests.delete(addr, json={
            'ids': 'test',
        })
        self.assertEqual(res.status_code, 500)
        print(res.text)

        res = requests.delete(addr, json={
            'ids': [1],
        })
        self.assertTrue(res.ok)
