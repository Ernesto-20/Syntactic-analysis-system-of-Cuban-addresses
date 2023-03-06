

class Classified_Address:

    def __init__( self, street_1, street_2, street_3, locality, municipality,
     province, house_number, reserved_word, probability_1, probability_2, 
     probability_3, probability_locality, probability_municipality,
     probability_province, probability_house_number, probability_reserve_word):
        self.street_1 = street_1
        self.street_2 = street_2 
        self.street_3 = street_3
        self.locality = locality
        self.municipality = municipality
        self.province = province
        self.house_number = house_number
        self.reserved_word = reserved_word
        self.probability_1 = probability_1
        self.probability_2 = probability_2
        self.probability_3 = probability_3
        self.probability_locality = probability_locality
        self.probability_municipality = probability_municipality
        self.probability_province = probability_province
        self.probability_house_number = probability_house_number
        self.probability_reserve_word = probability_reserve_word
    
    def __str__(self):
        address = 'calle principal: ' + ' '.join(self.street_1) + '    #####    Probabilidades: '+self.probability_1 + '\n' \
        'calle secundaria : ' + ' '.join(self.street_2) + '    #####    Probabilidades: '+self.probability_2 + '\n' \
        'calle secundaria: ' + ' '.join(self.street_3) + '    #####    Probabilidades: '+self.probability_3 + '\n' \
        'localidad: ' + ' '.join(self.locality) + '    #####    Probabilidades: '+self.probability_locality + '\n' \
        'municipio: ' + ' '.join(self.municipality) + '    #####    Probabilidades: '+self.probability_municipality + '\n' \
        'provincie: ' + ' '.join(self.province) + '    #####    Probabilidades: '+self.probability_province + '\n' \
        'numero casa: ' + ' '.join(self.house_number) + '    #####    Probabilidades: '+self.probability_house_number + '\n' \
        'palabra reservada: ' + ' '.join(self.reserved_word) + '    #####    Probabilidades: '+self.probability_reserve_word + '\n'
        
        
