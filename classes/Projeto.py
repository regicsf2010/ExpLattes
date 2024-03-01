class Projeto:
    
    def __init__(self, tipo, titulo, status, inicio, fim):
        self.tipo = tipo
        self.titulo = titulo
        self.status = status
        self.inicio = inicio
        self.fim = fim
        self.ano = self.inicio # convenção