

import tkinter as tk
from geopy.distance import geodesic
import folium
from folium.plugins import MeasureControl

class Cidade:
    def __init__(self, nome, transportadora, latitude, longitude):
        self.nome = nome
        self.endereco = transportadora
        self.latitude = latitude
        self.longitude = longitude

class CalculadoraRota:
    def __init__(self):
        self.cidades = {
            "Curitiba": Cidade("Curitiba/PR", "CwbNow", -25.4284, -49.2733),
            "Londrina": Cidade("Londrina/PR", "PombosSobreRodas", -23.3045, -51.1696),
            "Foz do Iguaçu": Cidade("Foz do Iguaçu/PR", "CataratasEntregas", -25.5163, -54.5854),
            "União da Vitória": Cidade("União da Vitória/PR", "EntregaVitoriosa", -26.2219, -51.0851), #foz do iguaçu
            "Joinville": Cidade("Joinville/SC", "JoinEntregas", -26.3044, -48.8464), #chapeco
            "Chapecó": Cidade("Chapecó/SC", "ChaPneucó", -27.1048, -52.6143),#joinville
            "Porto Alegre":  Cidade("Porto Alegre/RS", "AlegreTrans", -30.0368, -51.2090),
            "Uruguaiana": Cidade("Uruguaiana/RS", "CarlosTransportes", -29.7584, -57.0863),
            "Pelotas": Cidade("Pelotas/RS", "PelotasNational", -31.7700, -52.3313)
        }
        

        

    def calcular_distancia(self, origem, destino):
        coord_origem = (self.cidades[origem].latitude, self.cidades[origem].longitude)
        coord_destino = (self.cidades[destino].latitude, self.cidades[destino].longitude)
        return geodesic(coord_origem, coord_destino).kilometers

class InterfaceGrafica:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculadora de Rota")

        self.calculadora = CalculadoraRota()

        self.label_origem = tk.Label(master, text="Cidade de Origem:")
        self.label_origem.pack()

        self.entry_origem = tk.Entry(master)
        self.entry_origem.pack()

        self.label_destino = tk.Label(master, text="Cidade de Destino:")
        self.label_destino.pack()

        self.entry_destino = tk.Entry(master)
        self.entry_destino.pack()

        self.botao_calcular = tk.Button(master, text="Calcular Rota", command=self.calcular_rota)
        self.botao_calcular.pack()

        
    

    def calcular_rota(self):
        origem = self.entry_origem.get()
        destino = self.entry_destino.get()

        if origem in self.calculadora.cidades and destino in self.calculadora.cidades:
            distancia = self.calculadora.calcular_distancia(origem, destino)
            distancia = round(distancia,2)
            custo = distancia * 20  
            velocidade_media = 80
            
            
            if distancia <= 500:
                tempo_estimado = distancia / velocidade_media
                print(f"A transportadora sairá de {origem} com destino para {destino} Confira os: Distância: {distancia} km, Custo: R${custo:.2f}, Tempo Estimado: {tempo_estimado:.2f} horas" )
            else:
                dias_viagem = distancia / 500
                dias_viagem = round(dias_viagem) 
                tempo_estimado_total = distancia / velocidade_media
                print(f"A transportadora sairá de {origem} com destino para {destino}, Confira os dados: Distância: {distancia} km, Custo: R${custo:.2f}, Dias de Viagem: {dias_viagem}, Tempo Estimado Total: {tempo_estimado_total:.2f} horas" )


        
        
            # MAPA
            mapa = folium.Map(location=[-25.4284, -49.2733], zoom_start=6)
            folium.Marker([self.calculadora.cidades[origem].latitude, self.calculadora.cidades[origem].longitude],
                          popup=origem).add_to(mapa)
            folium.Marker([self.calculadora.cidades[destino].latitude, self.calculadora.cidades[destino].longitude],
                          popup=destino).add_to(mapa)
            
            

            mapa.add_child(MeasureControl())
            

            mapa.save("mapa.html")

            import webbrowser
            webbrowser.open("mapa.html")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGrafica(root)
    root.mainloop()
    
    