import json
import pandas as pd


#
#   WCZYTYWANIE PLIKÓW
#

# importujemy wszystkie detailsy z api
with open('json/map.json', 'r', encoding='utf-8') as file:
    DETAILS = json.load(file)

# importujemy wszytskich aktorów do zmiennej globalnej
with open('json/actors.json', 'r', encoding='utf-8') as file:
    ACTORS = json.load(file)

# importujemy wszytskich reżyserów do zmiennej globalnej
with open('json/directors.json', 'r', encoding='utf-8') as file:
    DIRECTORS = json.load(file)

# importujemy wszytskie gatunki do zmiennej globalnej
with open('json/genres.json', 'r', encoding='utf-8') as file:
    genres = json.load(file)
    GENRES = genres["genres"]

# importujemy wszytskie production_companies do zmiennej globalnej
with open('json/production_companies.json', 'r', encoding='utf-8') as file:
    PRODUCTION_COMPANIES = json.load(file)

# importujemy wszytskie production_countries do zmiennej globalnej
with open('json/production_countries.json', 'r', encoding='utf-8') as file:
    PRODUCTION_COUNTRIES = json.load(file)

# Read the CSV file into a DataFrame
movie_df = pd.read_csv('csv/movie.csv', delimiter=";")

task_df = pd.read_csv('csv/task.csv', delimiter=";")

train_df = pd.read_csv('csv/train.csv', delimiter=";")


#
#
#

# przyjmuje movie_id, szuka jego tmdb_id, ściąga detailsy i tworzy na ich podstawie wektor cech
def createFeatureVectorForMovie(movie_id):
    details_id = findMovieTmdb_id(movie_id)
    details = DETAILS[str(details_id)]
    # wektor cech
    feature_vector = []
    if details["adult"] == False:
        feature_vector.append(0)
    else:
        feature_vector.append(1)
    feature_vector.append(details["budget"])
    feature_vector.extend(actorsFeatureVectorCreator(details)) # 1664
    feature_vector.extend(directorsFeatureVectorCreator(details)) # 61
    feature_vector.extend(genresFeatureVectorCreator(details)) # 19
    feature_vector.append(details["popularity"])
    feature_vector.extend(productionCompaniesFeatureVectorCreator(details)) # 353
    feature_vector.extend(productionCountriesFeatureVectorCreator(details)) # 23
#     feature_vector.append(details["release_date"])
    feature_vector.append(details["revenue"])
    feature_vector.append(details["runtime"])
    if details["status"] == 'Release':
        feature_vector.append(1)
    else:
        feature_vector.append(0)
    feature_vector.append(details["vote_average"])
    feature_vector.append(details["vote_count"])
    
    return feature_vector

#
#   FUNKCJE DO OPERACJI NA JSONACH
#

# funkcja przyjmuje movie jako json (z detailsów) i zwraca prodcution_company ("name"), np. 'Pixar'
def getProductionCompanies(movie):
    list_of_production_companies = []
    for elem in movie["production_companies"]:
        list_of_production_companies.append(elem["name"])
    return list_of_production_companies

# ta funkcja przyjmuje movie jako json, zwraca listę production_countries z 1 jak występowała dane production_country, 0 jak nie
def productionCountriesFeatureVectorCreator(movie):
    indexes = [] # lista do przechowywania indexów, która production_company wystąpiła
    for productionCountry in getProductionCountries(movie):
        for productionCountryFromJson in PRODUCTION_COUNTRIES:
            if productionCountry == productionCountryFromJson["name"]:
                indexes.append(productionCountryFromJson["index"])
    production_country_feature_vector = []
    for index in range(23): # bo jest 353 production_companies
        if index in indexes:
            production_country_feature_vector.append(1)
        else:
            production_country_feature_vector.append(0)
    return production_country_feature_vector

# funkcja przyjmuje movie jako json (z detailsów) i zwraca prodcution_company ("name"), np 'United Kingdom'
def getProductionCountries(movie):
    list_of_production_countries = []
    for elem in movie["production_countries"]:
        list_of_production_countries.append(elem["name"])
    return list_of_production_countries

# ta funkcja przyjmuje movie jako json, zwraca listę production_companies z 1 jak występowała dana production_comapny, 0 jak nie
def productionCompaniesFeatureVectorCreator(movie):
    indexes = [] # lista do przechowywania indexów, która production_company wystąpiła
    for productionCompany in getProductionCompanies(movie):
        for productionCompanyFromJson in PRODUCTION_COMPANIES:
            if productionCompany == productionCompanyFromJson["name"]:
                indexes.append(productionCompanyFromJson["index"])
    production_company_feature_vector = []
    for index in range(353): # bo jest 353 production_companies
        if index in indexes:
            production_company_feature_vector.append(1)
        else:
            production_company_feature_vector.append(0)
    return production_company_feature_vector

# funkcja przyjmuje movie jako json (z detailsów) i zwraca reżysera ("name")
def getDirector(movie):
    for elem in movie["credits"]["crew"]:
        if elem["job"] == "Director":
            return elem["name"]

# ta funkcja przyjmuje movie jako json, zwraca listę reżyserów z 1 jak występował dany aktor, 0 jak nie
def directorsFeatureVectorCreator(movie):
    indexes = [] # lista do przechowywania indexów, który reżyser wystąpił
    for directorFromJson in DIRECTORS:
        if getDirector(movie) == directorFromJson["name"]:
            indexes.append(directorFromJson["index"])
    director_feature_vector = []
    for index in range(61): # bo jest 61 reżyserów
        if index in indexes:
            director_feature_vector.append(1)
        else:
            director_feature_vector.append(0)
    return director_feature_vector

# funkcja przyjmuje movie jako json (z detailsów) i zwraca listę aktorów ("name")
def getCast(movie):
    list_of_actors = []
    for actor in movie["credits"]["cast"]:
        list_of_actors.append(actor["name"]) 
    return list_of_actors

# ta funkcja przyjmuje movie jako json, zwraca listę aktorów z 1 jak występował dany aktor, 0 jak nie
def actorsFeatureVectorCreator(movie):
    indexes = [] # lista do przechowywania indexów, który aktor wystąpił
    for actor in getCast(movie):
        for actorFromJson in ACTORS:
            if actor == actorFromJson["name"]:
                indexes.append(actorFromJson["index"])
    actor_feature_vector = []
    for index in range(1664): # bo jest 1664 aktorów
        if index in indexes:
            actor_feature_vector.append(1)
        else:
            actor_feature_vector.append(0)
    return actor_feature_vector

# ta funkcja przyjmuje movie jako json, zwraca listę gatunków z 1 jak występował dany gatunek, 0 jak nie
def genresFeatureVectorCreator(movie):
    indexes = [] # lista do przechowywania indexów, który gatunek wystąpił
    for genre in movie["genres"]:
        for genreFromJson in GENRES:
            if genre["name"] == genreFromJson["name"]:
                indexes.append(genreFromJson["index"])
    genre_feature_vector = []
    for index in range(19): # bo 19 gqtunków
        if index in indexes:
            genre_feature_vector.append(1)
        else:
            genre_feature_vector.append(0)
    return genre_feature_vector

# ta funkcja przyjmuje movie jako json, zwraca listę list [name, origin_country]
def productionCompaniesConverter(movie):
    result = []
    for company in movie["production_companies"]:
        comp = []
        comp.append(company["name"])
        comp.append(company["origin_country"])
        result.append(comp)
    return result

# ta funkcja przyjmuje movie jako json, zwraca listę tickerów państw, np. EN, US
def spokenLanguagesConverter(movie):
    result = []
    for country in movie["spoken_languages"]:
        country_name = country["iso_639_1"]
        result.append(country_name)
    return result

# ta funkcja przyjmuje movie jako json, zwraca listę tickerów państw, np. EN, US
def productionCountriesConverter(movie):
    result = []
    for country in movie["production_countries"]:
        country_name = country["iso_3166_1"]
        result.append(country_name)
    return result

#
#   FUNKCJE DO OPERACJI NA DATAFRAME/CSV
#

# funkcja do filtrowania dataframe po danej wartości kolumny, głównie do odfiltrowania filmów danego dla danego person_id
# przykład użycia result = filterDataFrame("person_id", 1642, train_df)
def filterDataFrame(column_to_filter, value_to_match, df):
    # Use boolean indexing to filter the DataFrame
    filtered_df = df[df[column_to_filter] == value_to_match]

    return filtered_df

# zwraca listę movie_id, z założenia będzie przekazywany tu wynik wywołania funkcji filterDataFrame
def getPersonMovies(filteredDataFrameForPerson):
    movie_id_list = filteredDataFrameForPerson["movie_id"]
    return list(movie_id_list)

# dla danego movie_id w train, szukamy jego tmdb_id (id w detailsach)
def findMovieTmdb_id(movie_id):
    one_row = movie_df[movie_df["id"] == movie_id]
    tmdb_id = one_row["tmdb_id"].values
    return tmdb_id[0]