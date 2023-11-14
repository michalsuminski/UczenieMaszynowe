import json
import pandas as pd


#
#   WCZYTYWANIE PLIKÓW
#

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

# Read the CSV file into a DataFrame
movie_df = pd.read_csv('csv/movie.csv', delimiter=";")

task_df = pd.read_csv('csv/task.csv', delimiter=";")

train_df = pd.read_csv('csv/train.csv', delimiter=";")


#
#   FUNKCJE DO OPERACJI NA JSONACH
#

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
    return movie_id_list

# dla danego movie_id w train, szukamy jego tmdb_id (id w detailsach)
def findMovieTmdb_id(movie_id):
    one_row = movie_df[movie_df["id"] == movie_id]
    tmdb_id = one_row["tmdb_id"].values
    return tmdb_id[0]