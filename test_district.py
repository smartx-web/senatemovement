"""District adaptation checks using disposable sample records only."""
import unittest
import app
import auth
import access
from locations import LGAS
import test_app


class DistrictTests(unittest.TestCase):
    setUp = test_app.PortalTests.setUp
    tearDown = test_app.PortalTests.tearDown

    def test_all_nine_lgas_persist_and_filter(self):
        self.assertEqual(len(set(LGAS)), 9)
        for index, lga in enumerate(LGAS):
            app.save('pu', dict(self.pu, lga=lga, code=f'SAMPLE-{index}'))
        with app.connect() as db:
            self.assertEqual({row[0] for row in db.execute('SELECT lga FROM pus')}, set(LGAS))
        for lga in LGAS:
            _, units, _, _, _ = app.filtered_records(dict(lga=lga))
            self.assertEqual([unit['lga'] for unit in units], [lga])
        with self.assertRaises(ValueError):
            app.save('pu', dict(self.pu, lga='Outside Benue', code='BAD'))

    def test_other_benue_lgas_rejected_at_every_entry(self):
        import sqlite3
        for lga in ('Makurdi', 'Gboko', 'Buruku', 'Guma', 'Gwer East', 'Gwer West',
                    'Katsina-Ala', 'Konshisha', 'Kwande', 'Logo', 'Tarka', 'Ukum', 'Ushongo', 'Vandeikya'):
            with self.subTest(lga=lga):
                data = dict(self.pu, lga=lga)
                with self.assertRaises(ValueError):
                    app.save('pu', data)
                text = ','.join(app.PU_COLUMNS) + '\n' + ','.join(data[k] for k in app.PU_COLUMNS) + '\n'
                with self.assertRaises(ValueError):
                    app.import_pus(text)
                with self.assertRaises(ValueError):
                    app.filtered_records({'lga': lga})
                with app.connect() as db:
                    with self.assertRaises(ValueError):
                        auth.manage_account(db, dict(username='outside', role='coordinator', lga=lga,
                            wards='', active='yes', password='sample-test-password-only'), None)
                with app.connect() as db:
                    with self.assertRaises(sqlite3.IntegrityError):
                        db.execute('INSERT INTO pus(lga,ward,code,name,voters,source,source_date) VALUES(?,?,?,?,?,?,?)',
                                   tuple(data[k] for k in app.PU_COLUMNS))

    def test_district_coordinator_scope_does_not_widen_access(self):
        app.save('pu', dict(self.pu, lga='Otukpo', code='SAMPLE-MAK'))
        app.save('pu', dict(self.pu, lga='Oju', code='SAMPLE-GBK'))
        with app.connect() as db:
            account_id = auth.manage_account(db, dict(username='sample-coordinator',
                role='coordinator', lga='Otukpo', wards='', active='yes',
                password='sample-test-password-only'), None)
            user = auth.user_snapshot(db.execute('SELECT * FROM users WHERE id=?', (account_id,)).fetchone())
        token = access.current_user.set(user)
        try:
            all_units, *_ = app.filtered_records({})
            self.assertEqual([unit['lga'] for unit in all_units], ['Otukpo'])
            with self.assertRaises(PermissionError):
                app.save('report', dict(pu_id='2', category='Logistics', detail='Sample'))
        finally:
            access.current_user.reset(token)

    def test_branding_and_empty_lgas_are_reserved(self):
        page = app.page()
        self.assertIn('Senate Movement for Olofu 2027', page)
        self.assertIn('Apa and Agatu only', page)
        self.assertIn('/assets/olofu-frontpage.jpg', page)
        for lga in LGAS:
            self.assertIn(f'value="{lga}"', page)
        login = auth.login_page('sample-csrf')
        self.assertIn('Senate Movement', login)
        self.assertIn('for Olofu 2027', login)
        self.assertNotIn('Hembe', login)
        self.assertNotIn('Better Benue', page + login)
        self.assertNotIn('solomon.jpg', login)
        self.assertNotIn('Engr. Solomon', login)


if __name__ == '__main__':
    unittest.main()
