from db import *
import configtest
import unittest


class User_Test(unittest.TestCase):
    def test_valid_name_1(self):
        name = 'Bill'
        self.assertEqual(valid_name(name, configtest), False)

    def test_valid_name_2(self):
        name = 'Noname'
        self.assertEqual(valid_name(name, configtest), True)

    def test_add_user_1(self):
        login = 'Max'
        password = 'Max_pass'
        #print(valid_name('Max',configtest))
        db_del_user('Max', configtest)
        #print(valid_name('Max', configtest))
        db_add_user(login, password, configtest)
        #print(valid_name('Max',configtest))
        self.assertEqual(valid_name(login, configtest), False)
        #db_del_user('Max',configtest)
        #print(valid_name('Max',configtest))


    def test_add_user_2(self):
        login = 'Bill'
        password = 'Bill_pass'
        with self.assertRaises(Exception):
            db_add_user(login, password, configtest)

    def test_check_user_1(self):
        login = 'Anna'
        password = 'Anna_pass'
        self.assertEqual(db_check_user(login, password, configtest), True)

    def test_check_user_2(self):
        login = 'Bob'
        password = 'wrong_password'
        self.assertEqual(db_check_user(login, password, configtest), False)

    def test_del_user_1(self):
        login = 'Eve'
        #print(valid_name('Eve',configtest))
        db_del_user(login, configtest)
        self.assertEqual(valid_name(login, configtest), True)
        db_add_user('Eve', 'Eve_pass', configtest)

    def test_del_user_2(self):  # пытается удалить того кого нет
        login = 'new'
        with self.assertRaises(Exception):
            db_del_user(login, configtest)

    def test_dynamics_1(self):
        login = 'Mari'
        self.assertEqual(db_user_dynamics(login, configtest), [("Mari", 1.0, 60.0, 55.0)])

    def test_dynamics_2(self):

        self.assertEqual(db_user_dynamics('Eve', configtest), [])


class Stat_Test(unittest.TestCase):  # очисти попытки
    def test_attempt_1(self):
        js = {'login': 'Tom', 'curr_data': time.time(), 'cps': 10, 'cpm': 600, 'acc': 23, 'mistakes': {'t': 1}}
        id = db_add_attempt(json.dumps(js), configtest)
        self.assertEqual(in_base(['Tom', 10, 600, 23], configtest), True)
        db_del_attempt(id,configtest)


    def test_attempt_2(self):
        js = {'login': 'Noname', 'curr_data': time.time(), 'cps': 10, 'cpm': 600, 'acc': 23, 'mistakes': {'t': 1}}
        with self.assertRaises(Exception):
            db_add_attempt(json.dumps(js), configtest)

    def test_user_problem_letters_1(self):
        self.assertEqual(db_user_problem_letters('Mari', configtest), [('p', 8), ('o', 7), ('e', 2)])

    def test_user_problem_letters_2(self):
        self.assertEqual(db_user_problem_letters('Noname', configtest), [])

    def test_user_all_2(self):
        self.assertEqual(db_user_all('Mari', configtest), [(4.5, 270.0, 60.0)])

    def test_user_all_1(self):
        self.assertEqual(db_user_all('Noname', configtest), [])

    def test_user_log_1(self):
        res = [(1.0, 60.0, 55.0), (8.0, 480.0, 80.0), (5.0, 300.0, 55.0), (4.0, 240.0, 50.0)]
        self.assertEqual(db_user_log('Mari',  configtest), res)
    def test_user_log_2(self):
        self.assertEqual(db_user_log('Noname',  configtest), [])
    def test_top_users_all_1(self):
        self.assertEqual(db_top_users_all(configtest), [('Anna', 110.0, 6600.0, 100.0), ('Tom', 10.0, 600.0, 23.0), ('Mari', 4.5, 270.0, 60.0)])
    def test_get_top_letters_1(self):
        self.assertEqual(db_get_top_letters( configtest), [('p', 8), ('o', 7), ('e', 2), ('w', 1), ('t', 1)])


if __name__ == "__main__":
    unittest.main()

