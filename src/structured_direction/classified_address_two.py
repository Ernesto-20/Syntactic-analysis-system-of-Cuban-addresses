class ClassifiedAddressTwo:
    def __init__(self, locality, municipality,province, building, apartment, reserve_word):
        self.locality = locality
        self.municipality = municipality
        self.province = province
        self.building = building
        self.apartment = apartment
        self.reserve_word = reserve_word

    def __str__(self):
        address_two = 'Edificio: ' + ' '.join(self.building) + '\n' \
            ',Apartamento: ' + ' '.join(self.apartment) + '\n' \
            ',Localidad: ' + ' '.join(self.locality) + '\n' \
            ',Municipio: ' + ' '.join(self.municipality) + '\n' \
            ',Provincia: ' + ' '.join(self.province) + '\n' \
            ',Palabras reservadas: ' + ' '.join(self.reserve_word) + '\n'

        return address_two