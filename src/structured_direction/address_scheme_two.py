class AddressSchemeTwo:
    def __init__(self, locality, municipality,province, building, apartment, reserve_word):
        self.locality = locality
        self.municipality = municipality
        self.province = province
        self.building = building
        self.apartment = apartment
        self.reserve_word = reserve_word

    def __str__(self):
        address_two = 'Edificio: ' + f'{self.building}' + '\n' \
            ',Apartamento: ' + f'{self.apartment}' + '\n' \
            ',Localidad: ' + f'{self.locality}' + '\n' \
            ',Municipio: ' + f'{self.municipality}' + '\n' \
            ',Provincia: ' + f'{self.province}' + '\n' \
            ',Palabras reservadas: ' + f'{self.reserve_word}' + '\n'

        return address_two