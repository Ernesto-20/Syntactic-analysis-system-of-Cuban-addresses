STREET_NAME_PREFIX = ['calle', 'CALL', 'ave', 'avenida', 'ave.', 'Ave', 'Ave.', 'AVE', 'AVE.', 'carretera', 'ctra',
                      'Ctra.', 'Ctra', 'carr',
                      'Carr.', 'Carr', 'carret', 'Carret.', 'Carret', 'CARRET', 'CARRETE', 'calzada', 'czda.', 'calz',
                      'Calzada', 'Czda',
                      'Calz', 'czda.', 'calz.', 'Czda.', 'Calz.', 'pasaje', 'psje', 'callejon', 'cjon', 'callejuela',
                      'acera', 'terraplan', 'terr', 'Terraplen', 'camino', 'calle', 'calle', 'calle', 'calle', 'calle', 'calle', 'calle', 'calle', 'calle']
BETWEEN_PREFIX = ['e/', 'e/c', '%', 'entre', 'entre', 'entre', 'entre', 'entre', 'E\\', 'E/', 'ent.', 'etr.', 'e\c', '/', '\\', 'e /']
CORNER_CONNECTOR_PREFIX = ['esq', 'esquina']
LOCALITY_PREFIX = ['pueblo', 'localidad', 'Pueblo', 'poblado', 'pob', 'Poblado', 'caserio', 'cas', 'csrio', 'Caserio',
                   'batey', 'bat', 'ciudad','acera', 'terraplan', 'terr', 'Terraplen', 'camino']
BUILDING_PREFIX = ['ed', 'edif', 'edf', 'edificio', 'EDIFICIO', 'Edificio', 'EDIF.', 'ED', 'e.','edf.', 'edi' 'EDF','Edif.', 'Edifi', 'edif.', 'ed.','']
PROPERTY_PREFIX = ['#', 'no', 'S/n', 'S/N', 's/N', 's/n', 'nro.', 'nu', 'num', 'no.', 'num.', 'nu.', 'número', 'no','nro','']
DISTANCE_PREFIX = ['Km.', 'KM.', 'Km', 'KM', 'K.', 'k.', 'kilometro', 'Kilometro', 'KILOMETRO', 'K\M', 'K/M', 'k/m',
                   'k\m','kmts','kmts.',]
DISTANCE_SPECIFICATION_PREFIX =['½','¼','¾','1/4','1/2','3/4']
OTHER_PREFIX = ['batey', 'bat', 'ciudad','finca', 'Finca']
PLACE_PREFIX = ['Bar','Club','Restaurante','Hotel','Centro comercial','Supermercado','Tienda minorista',
                'Tienda mayorista','Mercado agropecuario','Bazar','Feria','Parque',
                'Piscina','Zonas de escalada','Finca','Clínica','Hospital','Laboratorios']
ZONE_PREFIX = ['', 'Zn.', 'zn.', 'zon.', 'z.', 'zona', 'zna.', 'za', 'zo.', 'Zona']
MUNICIPALITY_PREFIX = ['Mun.', 'mun.', 'Mun', 'mun', 'Municipio', 'municipio', 'MUNICIPIO''M.','m.','mcpio.','Mno.', ' ']
PROVINCE_PREFIX = ['Prov.', 'prov.', 'PROV.', 'Prov', 'prov', 'Provincia', 'provicia', 'PROVINCIA', 'Pro.', 'PRO.',
                   'Pro', 'PRO', 'pro','prcia','provin.', 'prv.', '']
APARTMENT_PREFIX = ['apart.', 'apt.', 'apto', 'apto.', 'apartamento', 'apt', 'ap', 'aptto', '']
BUILDING_SUBDIVISION_PREFIX = ['apto', 'bloque', 'blq', 'esc', 'escalera', 'piso', 'Apto', 'apartamento', 'Bloque',
                               'apto.', 'Apto.', 'apart', 'APTO', 'apt', 'apto']
CONJUNCTION = ['y', 'e']



# Listas de palabras reservadas para cada componente modelo 2:
RW_BUILDING = ['Edif.', 'Edifi', 'Edificio', 'Edifi ', 'edf', 'edi', 'edif', 'ed', 'edf.', 'edi.', 'edif.', 'ed.']
RW_NUMBER = ['no.', 'no', 'num', 'num.', 'nu.', 'nu', 'número', '#', 'nro', 'nro.', '']
RW_ZONE = ['', 'Zn.', 'zn.', 'zon.', 'z.', 'zona', 'zna.', 'za', 'zo.']
RW_APARTMENT_2 = ['apart.', 'apt.', 'apto', 'apto.', 'apartamento', 'apt', 'ap', 'aptto', '']
RW_MUNICIPALITY = ['municipio', 'M.', 'm.', 'm', 'mun.', 'mcpio.', 'Mno.', '']
RW_PROVINCE = ['provincia', 'prov.', 'prcia', 'provin.', 'prv.', '']
