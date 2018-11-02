# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#class Taller1P1Pipeline(object):
#    def process_item(self, item, spider):
#        return item

import sqlite3

from scrapy.exporters import BaseItemExporter
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.utils.python import to_bytes

class formatoQuote(object):

	def process_item(self, item, spider):
		item['autor'] = item['autor']
		item['cita'] = item['cita'][0:255]
		item['tags'] = list(map(lambda t: t, item['tags']))
		
		return item

class SQliteCitasPipeline(object):


	def process_item(self, item, spider):
		#db = Accesobd()
		#db.setupDBCon()

		self.con = sqlite3.connect('quotes-bd.sqlite')
		self.cur = self.con.cursor()

		id_autor = self.cur.execute("SELECT id FROM Autor WHERE nombre=?",(item['autor'],))

		if len(id_autor.fetchall()) == 0:
			self.cur.execute("INSERT INTO Autor(nombre) VALUES(?)",(item['autor'],))
			self.con.commit()
			id_autor = self.cur.lastrowid  #recuperar ultimo id
			print "id_autor nuevo:", id_autor
		else:
			response_id_autor = self.cur.execute("SELECT id FROM Autor WHERE nombre=?",(item['autor'],))
			id_autor = response_id_autor.fetchall()[0][0]
			print "el id del viejo autor", id_autor

		self.cur.execute("INSERT INTO Cita(id_autor,cuerpo) VALUES(?,?)",(id_autor,item['cita']))
		self.con.commit()
		id_cita = self.cur.lastrowid

		print "las etiquetas:", item['tags']

		ids_etiquetas = []
		for item in item['tags']:
			print "item", item
			id_etiqueta = self.cur.execute("SELECT id FROM Etiqueta WHERE nombre=?",(item,))

			if len(id_etiqueta.fetchall()) == 0:
				self.cur.execute("INSERT INTO Etiqueta(nombre) VALUES(?)",(item,))
				self.con.commit()
				id_etiqueta = self.cur.lastrowid  #recuperar ultimo id
				print "id_etiqueta nueva:", id_etiqueta
				ids_etiquetas.append(id_etiqueta)
			else:
				response_id_etiqueta = self.cur.execute("SELECT id FROM Etiqueta WHERE nombre=?",(item,))
				id_etiqueta = response_id_etiqueta.fetchall()[0][0]
				print "el id del vieja etiqueta", id_etiqueta
				ids_etiquetas.append(id_etiqueta)
		
		for id_etiqueta in ids_etiquetas:
			print "id_etiqueta de la lista: ",id_etiqueta
			self.cur.execute("INSERT INTO Cita_etiqueta(id_cita,id_etiqueta) VALUES(?,?)",(id_cita,id_etiqueta))
			self.con.commit()
		
		#self.datosDB(item)
		self.con.close()
		return item

	def datosDB(self,item):
		id_autor = self.buscarAutor(item)
		print "asdasdsad",id_autor.fetchall()


	def buscarAutor(self,item):
		return self.cur.execute("SELECT * FROM Autor WHERE id=1")

class SqliteItemExporter(BaseItemExporter):

	def __init__(self, file, **kwargs):
		self._configure(kwargs, dont_fail=True)
		self.file = file
		self.encoder = ScrapyJSONEncoder(**kwargs)
		self.first_item = True

	def export_item(self, item):
		if self.first_item:
			self.first_item = False
		else:
			
			#itemdict = dict(self._get_serialized_fields(item))
			#self.file.write(to_bytes(self.encoder.encode(itemdict)))
			self.file.write(item.encode('utf-8'))
			self.file.write(b';\n')

class SqliteExportPipeline(object):
	def __init__(self, file_name):
		self.file_name = file_name
		self.file_handle = None

	def from_crawler(cls, crawler):
		output_file_name = crawler.settings.get('FILE_NAME')

		return cls(output_file_name)

	def open_spider(self, spider):
		file = open(self.file_name, 'wb')
		self.file_handle = file
		self.exporter = SqliteItemExporter(file)
    
	def close_spider(self, spider):
		self.file_handle.close()

	def process_item(self, item, spider):
		cita = item['cita']
		cita = cita.replace('"','')
		query_item_autor = "INSERT OR IGNORE INTO Autor(nombre) VALUES(\"%s\");\nINSERT INTO Cita(id_autor,cuerpo) VALUES((SELECT id FROM Autor WHERE nombre=\"%s\"),\"%s\")" % (item['autor'],item['autor'], cita)
		self.exporter.export_item(query_item_autor)

		#query_item_cita = "INSERT INTO Cita(id_autor,cuerpo) VALUES((SELECT id FROM Autor WHERE nombre=\"%s\"),\"%s\")" % (item['autor'], item['cita'])
		#self.exporter.export_item(query_item_cita)
		return item