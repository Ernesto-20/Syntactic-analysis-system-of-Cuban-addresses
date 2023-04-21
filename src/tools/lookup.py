STREET_NAME_PREFIX = ['calle', 'CALL', 'ave', 'avenida', 'ave.', 'Ave', 'Ave.', 'AVE', 'AVE.', 'carretera', 'ctra',
                      'Ctra.', 'Ctra', 'carr',
                      'Carr.', 'Carr', 'carret', 'Carret.', 'Carret', 'CARRET', 'CARRETE', 'calzada', 'czda.', 'calz',
                      'Calzada', 'Czda',
                      'Calz', 'czda.', 'calz.', 'Czda.', 'Calz.', 'pasaje', 'psje', 'callejon', 'cjon', 'callejuela',
                      'acera', 'terraplan', 'terr', 'Terraplen', 'camino']
BETWEEN_PREFIX = ['e/', 'e/c', '%', 'entre', 'E\\', 'E/', 'ent.', 'etr.', 'e\c', '/', '\\']
CORNER_CONECTOR_PREFIX = ['esq', 'esquina']
BUILDING_PREFIX = ['ed', 'edif', 'edf', 'edificio', 'EDIFICIO', 'Edificio', 'EDIF.', 'ED', 'e.', 'EDF', 'casa']
PROPERTY_PREFIX = ['#', 'no', 'S/n', 'S/N', 's/N', 's/n', 'nro.', 'nu', 'num', 'no.', 'num.', 'nu.', 'número']
DISTANCE_PREFIX = ['Km.', 'KM.', 'Km', 'KM', 'K.', 'k.', 'kilometro', 'Kilometro', 'KILOMETRO', 'K\M', 'K/M', 'k/m',
                   'k\m','kmts','kmts.',]
LOCALITY_PREFIX = ['pueblo', 'pue', 'Pueblo', 'poblado', 'pob', 'Poblado', 'caserio', 'cas', 'csrio', 'Caserio',
                   'batey', 'bat', 'ciudad',
                   'reparto', 'rpto', 'rto', 'Reparto', 'rpto.', 'rto.', 'Rpto.', 'Rto.', 'barrio', 'barr', 'bo',
                   'Barr', 'Barr.', 'Bo.',
                   'BRRI', 'comunidad', 'com', 'Comunidad', 'Com', 'Com.', 'distrito' 'dist', 'Distrito', 'Dist',
                   'Dist.',
                   'finca', 'Finca', 'Zona', 'zona']
MUNICIPALITY_PREFIX = ['Mun.', 'mun.', 'Mun', 'mun', 'Municipio', 'municipio', 'MUNICIPIO']
PROVINCE_PREFIX = ['Prov.', 'prov.', 'PROV.', 'Prov', 'prov', 'Provincia', 'provicia', 'PROVINCIA', 'Pro.', 'PRO.',
                   'Pro', 'PRO', 'pro']
BUILDING_SUBDIVISION_PREFIX = ['apto', 'bloque', 'blq', 'esc', 'escalera', 'piso', 'Apto', 'apartamento', 'Bloque',
                               'apto.', 'Apto.', 'apart', 'APTO', 'ESC']
CONJUNTION = ['y', 'e']

#   PALABRAS RESERVADAS ANTERIORES
# RW_STREETS = ['C', 'calle', 'avenida', 'pasaje', 'calzada', 'Ave.', '']
# RW_HOUSE_NUMBER = ['no.', 'no', 'num', 'num.', 'nu', 'numero', '#', 'Edif', 'Edifi', 'Edificio',
#                                  'Edificio #', 'Edifi numero', '']
# RW_APARTMENT = ['apart. num', 'apt. num', 'apto', 'apto.', 'apartamento', 'apartamento num', 'apt',
#                                'apt numero', '']
# RW_NUMBER_FLOOR = ['Piso', 'P1', 'P2', 'P3', 'Piso 1', 'Piso 2', 'Piso 3', 'Alto', 'Bajos', 'Bajo',
#                                  'Altos', 'p1', 'p2', 'p3', '']
# RW_DIV_STREET = ['entre', 'e/', 'e /', '%', '/','E /']
# RW_LOCALITY = ['reparto', 'rept', 'Rept.', 'repart.', 'rpt.', 'rept.', 'rpto', 'localidad', '']
# RW_CORNER = ['esq', 'esquina']

# Listas de palabras reservadas para cada componente modelo 2:
RW_BUILDING = ['Edif.', 'Edifi', 'Edificio', 'Edifi ', 'edf', 'edi', 'edif', 'ed', 'edf.', 'edi.', 'edif.', 'ed.', '']
RW_NUMBER = ['no.', 'no', 'num', 'num.', 'nu.', 'nu', 'número', '#', 'nro', 'nro.', '']
RW_ZONE = ['', 'Zn.', 'zn.', 'zon.', 'z.', 'zona', 'zna.', 'za', 'zo.']
RW_APARTMENT_2 = ['apart.', 'apt.', 'apto', 'apto.', 'apartamento', 'apt', 'ap', 'aptto', '']
RW_MUNICIPALITY = ['municipio', 'M.', 'm.', 'm', 'mun.', 'mcpio.', 'Mno.', '']
RW_PROVINCE = ['provincia', 'prov.', 'prcia', 'provin.', 'prv.', '']
