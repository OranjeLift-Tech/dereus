"""Bedrijfscontacten blijven compleet zonder waarden of scripts te wijzigen."""
import unittest
import kit


class ContactlinksTest(unittest.TestCase):
    def setUp(self):
        self.ctx = kit.Ctx.__new__(kit.Ctx)
        self.ctx.iconen = set()

    def test_tekst_en_bestaande_link(self):
        bron = '<p>Bel 085 000 5647.</p><a href="tel:+31850005647">Bellen</a>'
        uit = self.ctx.contactlinks(bron)
        self.assertEqual(uit.count('data-whatsapp-business'), 2)
        self.assertEqual(self.ctx.contactlinks(uit), uit)

    def test_leesteken_blijft_achter_de_zin_staan(self):
        bron = '<p>Bel <a href="tel:+31850005647">085 000 5647</a>.</p>'
        uit = self.ctx.contactlinks(bron)
        self.assertIn('</a>.<a class="wa-link"', uit)
        self.assertTrue(uit.endswith('</a></p>'))
        self.assertEqual(uit.count('data-whatsapp-business'), 1)
        self.assertEqual(self.ctx.contactlinks(uit), uit)       # tweede ronde voegt niets toe

    def test_invoer_en_code_blijven_ongewijzigd(self):
        bron = ('<input value="085 000 5647"><textarea>085 000 5647</textarea>'
                '<script>085 000 5647</script><a href="mailto:test@example.com">085 000 5647</a>'
                '<p aria-label="085 000 5647">Klantnummer 0612345678 &amp; tekst</p>')
        self.assertEqual(self.ctx.contactlinks(bron), bron)


if __name__ == '__main__':
    unittest.main()
