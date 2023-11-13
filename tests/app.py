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

        res = requests.get(addr, params={
            'columns': ['id'],
        })
        self.assertTrue(res.ok)

        res = requests.get(addr, params={})
        data = res.json()
        self.assertListEqual(data, [])

    def test_02_insert(self):
        addr = f'{self.addr}/api/db/ruleset'

        res = requests.post(addr, json='test')
        self.assertEqual(res.status_code, 400)

        res = requests.post(addr, json={
            'name': 'test',
        })
        self.assertEqual(res.status_code, 500)

        res = requests.post(
            addr,
            json={
                'id': 0,
                'name': 'test',
                'version': '1.0.0',
                'description': 'test',
                'xml': '',
            },
        )
        data = res.json()
        self.assertIn('lastrowid', data)
        self.assertEqual(data['lastrowid'], 1)

    def test_03_update(self):
        addr = f'{self.addr}/api/db/ruleset'

        res = requests.put(addr, json={
            'xml': '',
        })
        self.assertEqual(res.status_code, 400)

        res = requests.put(addr, json={
            'id': 1,
            'xml': [0],
        })
        self.assertEqual(res.status_code, 500)

        res = requests.put(addr, json={
            'id': 1,
            'xml': 'helloworld',
        })
        data = res.json()
        self.assertIn('rowcount', data)
        self.assertEqual(data['rowcount'], 1)

    def test_04_delete(self):
        addr = f'{self.addr}/api/db/ruleset'

        res = requests.delete(addr, json={
            'id': 0,
        })
        self.assertEqual(res.status_code, 400)

        res = requests.delete(addr, json={
            'ids': [],
        })
        self.assertEqual(res.status_code, 400)

        res = requests.delete(addr, json={
            'ids': [1],
        })
        data = res.json()
        self.assertIn('rowcount', data)
        self.assertEqual(data['rowcount'], 1)
