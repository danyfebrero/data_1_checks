# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 23:39:06 2022

@author: Daniel Jimenez
"""
import requests
import pandas as pd
import json


def pokemon_limit():
    """
    Gets the actual max amount of pokemons

    Returns
    -------
    total_pokemons : int

    """
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1'
    response = requests.get(url)
    json_data = response.json()
    raw_df = pd.DataFrame.from_dict(json_data)
    total_pokemons = raw_df['count'][0]
    return total_pokemons

    
def get_data_api(limit):
    """
    Get the pokemon data from the api

    Returns
    -------
    df : dataframe
        list of pokemons 

    """
    url = f'https://pokeapi.co/api/v2/pokemon?limit={limit}'
    response = requests.get(url)
    json_data = response.json()
    raw_df = pd.DataFrame.from_dict(json_data)
    json_string = raw_df["results"]
    df = pd.json_normalize(json_string) 
    return df


def get_pokemon_types():
    url = 'https://pokeapi.co/api/v2/type/'
    response = requests.get(url)
    json_data = response.json()
    raw_df = pd.DataFrame.from_dict(json_data)
    json_string = raw_df["results"]
    df = pd.json_normalize(json_string) 
    return df


def get_pokemon(url):
    pokemon_data = {
        'number': '',
        'name': '',
        'height': '',
        'weight': '',
        'types': '',
        'types_amount': '',
        'abilities': '',
        'abilities_amount': '',
        'moves':'',
        'moves_amount':''
        }
    
    response = requests.get(url)
    json_data = response.json()
    
    pokemon_data['number'] = json_data['id']
    pokemon_data['name'] = json_data['name']
    pokemon_data['height'] = json_data['height']
    pokemon_data['weight'] = json_data['weight']
    
    types_json = json_data['types']
    types_list = []
    for types in types_json:
        types_list.append((types['type']['name']))
    pokemon_data['types'] = types_list
    pokemon_data['types_amount'] = len(types_list)
    
    abilities_json = json_data['abilities']
    abilities_list = []
    for ability in abilities_json:
        abilities_list.append((ability['ability']['name']))
    pokemon_data['abilities'] = abilities_list
    pokemon_data['abilities_amount'] = len(abilities_list)
    
    moves_json = json_data['moves']
    moves_list = []
    for move in moves_json:
        moves_list.append((move['move']['name']))
    pokemon_data['moves'] = moves_list
    pokemon_data['moves_amount'] = len(moves_list)

    return pokemon_data

     
def create_pokedex(pokemon_urls):
    pokedex = pd.DataFrame(columns = ['number', 'name', 'height', 'weight',
                                      'types', 'types_amount', 'abilities',
                                      'abilities_amount', 'moves',
                                      'moves_amount'])
    for url in pokemon_urls:
        pokemon = get_pokemon(url)
        pokedex.loc[pokedex.shape[0]] = pokemon
    return pokedex
    

def main():
    limit = '25'
    url_df = get_data_api(limit)
    pokemon_urls = url_df['url'].unique()
    print('Loading pokemons from the API, please wait...\n')
    pokedex = create_pokedex(pokemon_urls)
    
    print(f'For this project I selected {limit} from a total of {str(pokemon_limit())} pokemons.')
    print(f'This pokemons have an average of {int(pokedex["abilities_amount"].mean())} abilities and {int(pokedex["moves_amount"].mean())} moves.')    
    print(f'All them togheter have a weight of: {pokedex["weight"].sum()}.')
    print(f'The smaller one has a height of {pokedex["weight"].min()}.')
    print(f'The tallest one has a height of {pokedex["weight"].max()}.')
    print(f'The median height is {pokedex["weight"].median()}.\n')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print('This are the first 4 pokemons:')
        print(pokedex[['number', 'name', 'height', 'weight', 'types']].head(4),'\n')
    print('Selecting and printing the second and thrid column: ')
    print(pokedex.iloc[:, [2,3]].head(),'\n')
    
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print('Filtering pokemons with a numbers between 10 and 20:')
        print(pokedex.query("number >= 10 & number <= 20")[['number', 'name', 'height', 'weight']])
    
        
if __name__ == '__main__':
    main()