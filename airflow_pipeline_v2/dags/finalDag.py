
from datetime import datetime
from requests_cache import CachedSession
from airflow.decorators import dag, task
import json

from airflow import DAG
default_args = {
    'owner': 'airflow',
    'retries': 3
}

@dag(
    schedule_interval='@daily',
    start_date=datetime(2022, 1, 1),
    catchup=False,
    default_args=default_args
)

def data_pipeline_api():
    urls_session = CachedSession('poke')

    @task()
    def data_Fetch():
        urls_response = urls_session.get('https://pokeapi.co/api/v2/evolution-chain?offset=0&limit=468')
        poke_evolution_chain_urls=urls_response.json()
        #context['ti'].xcom_push(key='poke_evolution_chain_urls', value = poke_evolution_chain_urls_results)
        return {'poke_evolution_chain_urls': poke_evolution_chain_urls}

    @task()
    def get_collection(poke_evolution_chain_urls : list):
        #poke_evolution_chain_urls = context['ti'].xcom_pull(key='poke_evolution_chain_urls',task_ids=['data_fetching_task'])
        poke_evolution_chain_collection={}
        for elem in poke_evolution_chain_urls['poke_evolution_chain_urls']['results']:
            poke_evolution_chain={}
            poke_multi_primary_evolution_list=[]
            poke_multi_secondary_evolution_list=[]
            response= urls_session.get(elem['url'])
            pokemon=response.json()
        
            if pokemon['chain']['evolves_to'] :
                for i in range(len(pokemon['chain']['evolves_to'])):
                    poke_evolution_chain.clear()
                    poke_multi_secondary_evolution_list.clear()

                    for k in range(len(pokemon['chain']['evolves_to'][i]['evolution_details'])):
                        pokemon['chain']['evolves_to'][i]['evolution_details'][k]['trigger']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['trigger']['name']
                        if pokemon['chain']['evolves_to'][i]['evolution_details'][k]['held_item'] :
                            pokemon['chain']['evolves_to'][i]['evolution_details'][k]['held_item']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['held_item']['name']
                        if pokemon['chain']['evolves_to'][i]['evolution_details'][k]['item']:
                            pokemon['chain']['evolves_to'][i]['evolution_details'][k]['item']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['item']['name']
                        if pokemon['chain']['evolves_to'][i]['evolution_details'][k]['known_move']:
                            pokemon['chain']['evolves_to'][i]['evolution_details'][k]['known_move']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['known_move']['name']
                        if pokemon['chain']['evolves_to'][i]['evolution_details'][k]['known_move_type']:
                            pokemon['chain']['evolves_to'][i]['evolution_details'][k]['known_move_type']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['known_move_type']['name']
                        if pokemon['chain']['evolves_to'][i]['evolution_details'][k]['location']:
                            pokemon['chain']['evolves_to'][i]['evolution_details'][k]['location']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['location']['name']
                        if pokemon['chain']['evolves_to'][i]['evolution_details'][k]['party_species']:
                            pokemon['chain']['evolves_to'][i]['evolution_details'][k]['party_species']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['party_species']['name']
                        if pokemon['chain']['evolves_to'][i]['evolution_details'][k]['party_type']:
                            pokemon['chain']['evolves_to'][i]['evolution_details'][k]['party_type']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['party_type']['name']
                        if pokemon['chain']['evolves_to'][i]['evolution_details'][k]['trade_species']:
                            pokemon['chain']['evolves_to'][i]['evolution_details'][k]['trade_species']=pokemon['chain']['evolves_to'][i]['evolution_details'][k]['trade_species']['name']

                    poke_multi_primary_evolution_list.append({'evolves_to': pokemon['chain']['evolves_to'][i]['species']['name'],'evolution_details':pokemon['chain']['evolves_to'][i]['evolution_details']})
                    poke_evolution_chain[pokemon['chain']['species']['name']]= poke_multi_primary_evolution_list
                    poke_evolution_chain_collection.update(poke_evolution_chain)
                    if pokemon['chain']['evolves_to'][i]['evolves_to']:
                        for j in range(len(pokemon['chain']['evolves_to'][i]['evolves_to'])):
                            poke_evolution_chain.clear
                            for k in range(len(pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'])):
                                pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['trigger']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['trigger']['name']
                                if pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['held_item']:
                                    pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['held_item']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['held_item']['name']
                                if pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['item']:
                                    pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['item']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['item']['name']
                                if pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['known_move']:
                                    pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['known_move']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['known_move']['name']
                                if pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['known_move_type']:
                                    pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['known_move_type']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['known_move_type']['name']
                                if pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['location']:
                                    pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['location']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['location']['name']
                                if pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['party_species']:
                                    pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['party_species']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['party_species']['name']
                                if pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['party_type']:
                                    pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['party_type']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['party_type']['name']
                                if pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['trade_species']:
                                    pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['trade_species']=pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details'][k]['trade_species']['name']
                                

                            
                            poke_multi_secondary_evolution_list.append({'evolves_to': pokemon['chain']['evolves_to'][i]['evolves_to'][j]['species']['name'],'evolution_details':pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolution_details']})
                            poke_evolution_chain[pokemon['chain']['evolves_to'][i]['species']['name']]=poke_multi_secondary_evolution_list       
                            poke_evolution_chain_collection.update(poke_evolution_chain)
                            if len(pokemon['chain']['evolves_to'][i]['evolves_to'][j]['evolves_to'])==0:
                                poke_evolution_chain[pokemon['chain']['evolves_to'][i]['evolves_to'][j]['species']['name']]={'evolves_to': 'null','evolution_details': 'null'}
                                poke_evolution_chain_collection.update(poke_evolution_chain)    
                                
                        
                    else:
                        poke_evolution_chain[pokemon['chain']['evolves_to'][i]['species']['name']]={'evolves_to': 'null','evolution_details': 'null'}
                        poke_evolution_chain_collection.update(poke_evolution_chain)
                    
            else:
                poke_evolution_chain[pokemon['chain']['species']['name']]={'evolves_to': 'null','evolution_details': 'null'}
                poke_evolution_chain_collection.update(poke_evolution_chain)

        return {'poke_evolution_chain_collection': poke_evolution_chain_collection}
            
        #print("poke_evolution_chain_collection executed")
        
    @task()
    def data_Dump(data):
        
        with open('poke_evolution_chain_data.json','w') as file :
            json.dump(data, file, indent=2)
    
    poke_evolution_chain_urls_results=data_Fetch()
    poke_evolution_chain_collection= get_collection(poke_evolution_chain_urls_results)
    data_Dump(poke_evolution_chain_collection)
taskflow_dag = data_pipeline_api()