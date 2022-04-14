from django.shortcuts import render
from django.views.generic.base import TemplateView
import requests
import json
from bs4 import BeautifulSoup

# Create your views here.

class HomePageView(TemplateView):
    template_name = "test/home.html"

    def dispatch(self, request, *args, **kwargs):
        self.ejecutar()
        return super().dispatch(request, *args, **kwargs)
    

    def ejecutar(self):
        data = {}
        data['adv'] = []

        URL = "https://www.redpiso.es/venta-viviendas/madrid"

        data_aux = self.sacar_adv_pagina(URL)

        data['adv'].append(data_aux)

        i = 2
        while(1):
            URL = "https://www.redpiso.es/venta-viviendas/madrid/pagina-" + str(i)
            print(URL)

            data_aux = self.sacar_adv_pagina(URL)

            data['adv'].append(data_aux)

            if len(data_aux['adv']) == 0:
                break

            i = i + 1   

        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

            

    def sacar_adv_pagina(self, URL):
        data = {}
        data['adv'] = []

        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")

        job_elements = soup.find_all("div", class_="col-lg-3 col-md-4 col-sm-6 col-xs-12")
       
        for job_element in job_elements:
            detalles = job_element.find("h5")
            link = ""

            for i in detalles:
                link = i['href']

            print("link", link)

            data_adv = self.sacar_datos(link)

            data['adv'].append(data_adv)

            #print(data)
            #print()
            #break

        return data  



    def sacar_datos(self, URL):
        data = {}

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        job_elements = soup.find_all("body", class_="body-property")

        for job_element in job_elements:
            elements_description = job_element.find_all("p")

            element_price = job_element.find("h2")
            element_description = elements_description[0]
            element_id = elements_description[2]
            element_date = ""
            
            element_dates = job_element.find_all("span", class_="property-visits")
            element_date = str(element_dates[1])
            elementos = element_date.split("</i>")

            fecha = ""
            caracte = ""
            
            i = 0
            for j in elementos[1]:
                fecha = fecha + j
                if i == 10:
                    break
                i = i + 1

            elements_caracteristicas = job_element.find_all("div", class_="col-lg-3 col-md-4 col-sm-6 property-features-item")

            for k in elements_caracteristicas:
                detalle = str(k).split("</i>")
                
                letra = ""
                for f in detalle[1]:
                    if f == "<":
                        break
                    letra = letra + f

                caracte = caracte + letra + ", "

            data = {
                'Id': element_id.text,
                'Precio': element_price.text,
                'Descripción': element_description.text,
                'Fecha de publicación': fecha,
                'Características': caracte,
            }

            return data

