'''| 1 | Autenticação | `POST /auth/cadastro` | Cria uma conta com nome, e-mail e senha. |'''
'''| 2 | Autenticação | `POST /auth/login` | Valida as credenciais e devolve um token de acesso. |'''
'''| 3 | Autenticação | `GET /usuarios/me` | Retorna os dados e as estatísticas do usuário logado, como plantas descobertas. |'''
'''| 4 | Identificação | `POST /identificacoes` | Recebe a foto, envia para a IA e devolve a planta provável com o nível de confiança. |'''
'''| 5 | Plantas | `GET /plantas` | Lista o catálogo de PANC, com busca por nome. |'''
'''| 6 | Plantas | `GET /plantas/{id}` | Retorna a ficha completa: nome popular, nome científico, descrição, partes comestíveis e cuidados. |'''
'''| 7 | Coleção | `POST /colecao` | Salva uma planta identificada na coleção do usuário, com a foto e a data da descoberta. |'''
'''| 8 | Coleção | `GET /colecao` | Lista as plantas já descobertas pelo usuário. |'''
'''| 9 | Coleção | `GET /colecao/{id}` | Mostra os detalhes de uma descoberta, com a foto do usuário e as receitas. |'''
'''| 10 | Coleção | `DELETE /colecao/{id}` | Remove uma planta da coleção. |'''
'''| 11 | Receitas | `GET /plantas/{id}/receitas` | Lista as receitas feitas com a planta. |'''
'''| 12 | Receitas | `GET /receitas/{id}` | Retorna uma receita com ingredientes e modo de preparo. |'''

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from models.planta import Planta

app = FastAPI(title= "Enciclopedia Digital de PANCs")

plantas = [
    Planta(id=1, nome_popular="Ora-pro-nóbis",
           nome_cientifico="Pereskia aculeata",
           descricao="Trepadeira de folhas comestíveis, rica em proteínas."),

]

@app.get("/plantas")

def listar_plantas ():
    return plantas


@app.get("/plantas/{id}")
def detalhar_planta (id: int):
    for planta in plantas:
        if planta.id == id:
            return planta
    raise HTTPException (status_code=404, detail="Planta não encontada")
