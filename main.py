from flask import Flask, jsonify, abort, make_response, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///corona.db"
db = SQLAlchemy(app)

from data import casos,parser

controller = parser()

@app.route('/')
def index():
  txt = "Web service para monitoreo de coronavirus\n"
  txt += "\n"
  return txt


@app.route('/casos/ciudades')
def casosciudades():
  casoslist = []
  retorno = controller.NumeroCasosCiudad()
  for target_list in retorno:
    casoslist.append({'ciudad':target_list[1],'casos':target_list[0]})
  return jsonify(casoslist)

@app.route('/casos/ciudad/<ciudad>')
def buscarciudad(ciudad='cali'):
  
  oslist = []
  retorno = controller.TraerCasosCiudadSQL(ciudad)
  for target_list in retorno:
    oslist.append({'ciudad':target_list[1],'casos':target_list[0]})
  return jsonify(oslist)

@app.route('/casos/dias',methods=['GET'])
def casosdias():
  casoslist = []
  retorno = controller.CasosPorFechaAgrupados()
  for target_list in retorno:
    casoslist.append({'fecha':target_list[1],'casos':target_list[0]})

  return jsonify(casoslist)

@app.route('/casos/hoy')
def casoshoy():
  casoslist = []
  retorno = controller.CasosHoy()
  for target_list in retorno:
    casoslist.append({'fecha':target_list[1],'casos':target_list[0]})

  return jsonify(casoslist)


@app.route('/casos/sexo')
def casosallsex():
  casoslist = []
  retorno = controller.CasosPorSexo()
  for target_list in retorno:
    casoslist.append({'sexo':target_list[1],'casos':target_list[0]})

  return jsonify(casoslist)
  
@app.route('/casos/sexo/<sexo>')
def casossexo(sexo):
  casoslist = []
  retorno = controller.CasosPorSexoEs(sexo)
  for target_list in retorno:
    casoslist.append({'sexo':target_list[1],'casos':target_list[0]})

  return jsonify(casoslist)


@app.route('/casos/nuevo/',methods=['POST'])
def nuevoCaso():
  if not request.json or not 'ciudad' in request.json or not 'sexo' in request.json or not 'estado' in request.json:
      abort(400)
  else:
      ciudad = request.json['ciudad']
      sexo = request.json['sexo']
      print(sexo)
      estado = request.json['estado']
      print(estado)
      controller.GuardarCaso(ciudad,estado,sexo)
      return jsonify({'success': 'responde con exito'}), 200


'''
@app.route('/casos/meses')
def ultimosCasos():
    #param=request.args.get('nombre','undefined')
    #return "el parametro es {}".format(name)

@app.route('/casos/meses/desde/<int:mes1>')
@app.route('/casos/meses/desde/<int:mes1>/hasta/<int:mes2>')
@app.route('/casos/dias/desde/<int:dia1>/<int:mes1>/<int:ano1>/hasta/<int:dia2>/<int:mes2>/<int:ano2>')

'''


if __name__ == "__main__":
    app.run()    
