#from main import db
from flask_sqlalchemy import SQLAlchemy
import json, urllib.request, sqlite3
from datetime import datetime,date
from unidecode import unidecode
from sqlalchemy import func
from sqlalchemy import distinct

db = SQLAlchemy()

class casos(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column( db.Date,nullable=False)
    ciudad = db.Column(db.String,nullable=False)
    estado = db.Column(db.String,nullable=False)
    sexo = db.Column(db.String,nullable=False)


    '''def serialize(self):

        return {
            'id': self.id,
            'fecha': self.fecha,
            'ciudad': self.ciudad,
            'estado': self.estado,
            'sexo': self.sexo
        }'''
    
   

class parser:

    __casos = 0
    __ciudades = []
    __diciudades = dict()

    #Metodos
    def __init__(self):
        self.actualizarData()

    def actualizarData(self):
        with urllib.request.urlopen("https://www.datos.gov.co/api/views/gt2j-8ykr/rows.json?accessType=DOWNLOAD") as url:
            self.__data = json.loads(url.read().decode())
            self.__datos = self.__data['data']
            self.__casos = len(self.__datos)

    def traerUltimos(self, numCasos):

        return (self.__datos[-numCasos:])
        
    def traerCiudades(self):

        for target_list in self.__datos:

            if target_list[11] not in self.__ciudades:
                self.__ciudades.append(target_list[11])
                self.__diciudades[target_list[11]]=1
            else:
                self.__diciudades[target_list[11]]= self.__diciudades[target_list[11]] + 1

   
    def verCiudades(self):
        print(self.__ciudades)

    def verdic(self):
        print(self.__diciudades)

    def InsertarDatosRelevantes(self):
        for target_list in self.__datos:
            db.session.add(casos(
            fecha = datetime.strptime(target_list[23],"%Y-%m-%dT%H:%M:%S.%f")
                ,ciudad = unidecode(target_list[11]).lower(),
             estado = unidecode(target_list[13]).lower(), sexo = target_list[15].lower()))

        db.session.commit()
        return 0

    def sincronizarDB(self):
        self.actualizarData()

        for target_list in self.__datos:

            if datetime.strptime(target_list[23],"%Y-%m-%dT%H:%M:%S.%f") == datetime.now():
                db.session.add(casos(
                    fecha = datetime.strptime(target_list[23],"%Y-%m-%dT%H:%M:%S.%f")
                        ,ciudad = unidecode(target_list[11]).lower(),
                            estado = unidecode(target_list[13]).lower(), sexo = target_list[15].lower()))
            

        db.session.commit()

 #Metodos de consultas####################################################

    def TraerCasosCiudadSQL(self,ciudad):

        ##result = db.session.query(func.count(casos.ciudad),casos.ciudad).filter(casos.ciudad.like('%'+ciudad+'%')).all()
        
        result = db.session.query(func.count(casos.ciudad),casos.ciudad).filter(casos.ciudad == ciudad).all()
        
        return result

    def NumeroCasosCiudad(self):

        return (db.session.query(func.count(casos.ciudad),casos.ciudad).group_by(casos.ciudad).all())

    def CasosPorSexo(self):

        return (db.session.query(func.count(casos.sexo),casos.sexo).group_by(casos.sexo).all())
    
    def CasosPorSexoEs(self,sexo):

        return (db.session.query(func.count(casos.sexo),casos.sexo).filter(casos.sexo == sexo).group_by(casos.sexo).all())

    def CasosPorFechaAgrupados(self):

        return (db.session.query(func.count(casos.id),casos.fecha).group_by(casos.fecha).all())
    
    def CasosHoy(self):
        return (db.session.query(func.count(casos.id),casos.fecha).filter(casos.fecha == datetime.now()).all())

    def GuardarCaso(self,ciudad,estado,sexo):
        me = casos(fecha=datetime.now(),ciudad=unidecode(ciudad).lower(),estado=estado,sexo=sexo)
        db.session.add(me)
        db.session.commit()




