import unittest
from api_client import formatar_clube
from commands import handle_commands


class TestFuncoes(unittest.TestCase):

    def test_formatar_clube(self):
        # Mock (simulação) de um clube
        clube_mock = {
            "id": "gb3899e",
            "name": "Hogwarts Code Club",
            "code_club_id": 2,
            "community_id": 2,
            "contact": {
                "id": 1,
                "name": "Professor Dumbledore",
                "skype": "professor_dumbledore"
            },
            "venue": {
                "id": 1,
                "name": "Hogwarts Academy",
                "phone": "",
                "url": "",
                "address": {
                    "id": 1,
                    "address_1": "Hogwarts",
                    "address_2": "Stoatshead Hill",
                    "city": "Ottery St Catchpole",
                    "postcode": "BS36 1DN",
                    "region": "Devon",
                    "latitude": "41.613032",
                    "longitude": "-70.970479",
                    "country_id": 80
                }
            }
        }

        resultado_esperado = "Hogwarts Code Club | Stoatshead Hill Ottery St Catchpole Devon | Professor Dumbledore"
        resultado = formatar_clube(clube_mock)
        self.assertEqual(resultado, resultado_esperado)


if __name__ == '__main__':
    unittest.main()
