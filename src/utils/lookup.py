STREET_NAME_PREFIX = ['calle', 'ave', 'avenida', 'ave.', 'Ave', 'Ave.', 'carretera', 'ctra',
                      'Ctra', 'Carr.', 'Carr', 'carret', 'calzada', 'czda.', 'calz', 'Calzada', 'czda.',
                      'calz.', 'pasaje', 'ca', 'calle', 'calle', 'calle', 'calle', 'calle', 'calle', 'calle', 'calle']
STREET_NAME_SUFFIX = ['ave', 'avenida', 'ave.', 'Ave', 'Ave.', 'carretera', 'ctra',
                      'Carr.', 'calzada', 'czda.', 'calz', 'Calzada', 'calle',]

BETWEEN_PREFIX = ['e/', 'e/c', '%', 'entre', 'entre', 'entre', 'entre', 'entre calles', 'E\\', 'E/', 'ent.', 'etr.', 'e\c', '/', '\\', 'e /']
CORNER_CONNECTOR_PREFIX = ['esq', 'esquina']
LOCALITY_PREFIX = ['localidad', 'poblado', 'ciudad','caserio', 'rpt', 'reparto', 'reparto', 'reparto', 'reparto', 'localidad', 'rpt', 'rpt']
BUILDING_PREFIX = ['ed', 'edif', 'edf', 'edificio', 'EDIFICIO', 'Edificio', 'EDIF.', 'edf.', 'edi', 'EDF','Edif.', 'Edifi', 'edif.', 'ed.']
PROPERTY_PREFIX = ['#', 'nro.', 'nu', 'num', 'no.', 'num.', 'nu.', 'número', 'no','nro', 'numero', '#', '#']

OTHER_PREFIX = ['batey', 'bat', 'ciudad','finca', 'Finca']
PLACE_PREFIX = ['Bar','Club','Restaurante','Hotel','Centro comercial','Supermercado','Tienda minorista',
                'Tienda mayorista','Mercado agropecuario','Bazar','Feria','Parque',
                'Piscina','Zonas de escalada','Finca','Clínica','Hospital','Laboratorios']
ZONE_PREFIX = ['', 'Zn.', 'zn.', 'zon.', 'z.', 'zona', 'zna.', 'za', 'zo.', 'Zona']
MUNICIPALITY_PREFIX = ['Mun.', 'mun.', 'Mun', 'mun', 'Municipio', 'municipio', 'MUNICIPIO','M.','m.','mcpio.','Mno.']
PROVINCE_PREFIX = ['Prov.', 'prov.', 'PROV.', 'Prov', 'prov', 'Provincia', 'provicia', 'PROVINCIA', 'Pro.', 'PRO.',
                   'Pro', 'prcia', 'provin.', 'prv.']
APARTMENT_PREFIX = ['apart.', 'apt.', 'apto', 'apto.', 'apartamento', 'apt', 'ap', 'aptto']
IMPLICIT_APARTMENT = ['altos', 'alto', 'bajos', 'bajo', 'altos', 'alto', 'bajos', 'bajo', 'altos', 'alto', 'bajos', 'bajo', 'pb'] # less likely to 'pb'
APARTMENT_SPECIFICATION = ['int', 'interior']
BUILDING_SUBDIVISION_PREFIX = ['apto', 'bloque', 'blq', 'esc', 'escalera', 'piso', 'Apto', 'apartamento', 'Bloque',
                               'apto.', 'Apto.', 'apart', 'APTO', 'apt', 'apto']
CONJUNCTION = ['y', 'e']



# Listas de palabras reservadas para cada componente modelo 2 y 3:
REAL_BUILDING_PREFIX = ['edif', 'edf', 'edificio',
                   'EDIFICIO', 'Edificio', 'EDIF','EDIF.',
                   'ED', 'edf.', 'edi' 'EDF','Edif.',
                   'Edifi', 'edif.','Edif',]
REAL_PROPERTY_PREFIX = ['#', 'no',  'nro.',  'no.',
                   'numero','número','nro',]
REAL_APARTMENT_PREFIX = ['APTO','apart.','Apt', 'apt.', 'Apto','apartamento','apto', 'apto.',  'apt', 'aptto',]
REAL_LOCALITY_PREFIX = ['poblado', 'rpt', 'Reparto', 'reparto', 'Reaparto', 'reparto', 'rpt', 'rpt']
REAL_ZONE_PREFIX = ['zona', 'zna.', 'Zona','ZONA']

REAL_STREET_NAME_PREFIX = ['calle', 'CALL','Call','call','CALLE','CALLEJON',' Callejon','callejon', 'ave', 'avenida', 'ave.', 'Ave', 'Ave.',
                           'AVE', 'AVE.', 'carretera', 'ctra',
                           'Carr.', 'Carr', 'carret', 'Carret.', 'Carret', 'CARRET', 'CARRETE','CARRETERA', 'calzada', 'czda.', 'calz',
                            'Calzada', 'Czda', 'C/','C/','C/','VIA','Via','via'
                            'Calz', 'czda.', 'calz.', 'Czda.', 'Calz.', 'pasaje', 'psje',]
DISTANCE_PREFIX = ['Km.', 'KM.', 'Km', 'KM','kilometro', 'Kilometro', 'KILOMETRO', 'K\M', 'K/M', 'k/m',
                   'k\m',]
DISTANCE_SPECIFICATION_PREFIX =['½','1/2','1 / 2']


# List of street name words possible to have suffixes
STREET_SUFFIX_POSSIBILITIES = ['1ra', 'primera', '2da', 'segunda', '3ra', 'tercera', '4ta', 'cuarta',  '5ta', 'quinta', '6ta', 'sexta',
                                '7ma', 'septima', '8va', 'octaba', '9na', 'novena', '10ma', 'decima',]
