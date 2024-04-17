from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/generate_playlist', methods=['POST'])
def calculate():
    data = request.json
    print("Received data:", data)
    return jsonify(message="Data received successfully")

@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    data = request.json
    songs = data['songs']
    artists = data['artists']
    genres = data['genres']

    df = pd.read_csv('./spotify_data.csv')

    # Get song attributes
    song_attributes = {}
    for song in songs:
        song_data = df[df['track_name'] == song]
        if not song_data.empty:
            attributes = {}
            attributes['popularity'] = song_data['popularity'].values[0]
            attributes['danceability'] = song_data['danceability'].values[0]
            attributes['energy'] = song_data['energy'].values[0]
            attributes['key'] = song_data['key'].values[0]
            attributes['mode'] = song_data['mode'].values[0]
            attributes['speechiness'] = song_data['speechiness'].values[0]
            attributes['acousticness'] = song_data['acousticness'].values[0]
            attributes['instrumentalness'] = song_data['instrumentalness'].values[0]
            attributes['liveness'] = song_data['liveness'].values[0]
            attributes['valence'] = song_data['valence'].values[0]
            attributes['tempo'] = song_data['tempo'].values[0]
            attributes['loudness'] = song_data['loudness'].values[0]
            song_attributes[song] = attributes
        else:
            songs.remove(song)

    # Calculate average attributes
    def calculate_average_attributes(song_attributes):
        attribute_totals = {}
        attribute_counts = {}
        for song, attributes in song_attributes.items():
            for attribute, value in attributes.items():
                attribute_totals.setdefault(attribute, 0)
                attribute_totals[attribute] += value
                attribute_counts.setdefault(attribute, 0)
                attribute_counts[attribute] += 1

        averages = {}
        for attribute, total in attribute_totals.items():
            count = attribute_counts[attribute]
            averages[attribute] = total / count

        return averages

    # Filter DataFrame and calculate similarity
    filtered_df = df.copy()
    filtered_df = filtered_df[~filtered_df['track_name'].isin(songs)]  # Remove inputted songs
    filtered_df = filtered_df[filtered_df['genre'].isin(genres)]  # Filter by genres

    attributes_matrix = filtered_df[['danceability', 'energy', 'popularity', 'key', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'loudness']].values
    avg_attributes_vector = np.array(list(calculate_average_attributes(song_attributes).values())).reshape(1, -1)
    similarities = cosine_similarity(attributes_matrix, avg_attributes_vector)

    # Sort and select top 100 songs
    filtered_df['similarity'] = similarities
    top_100_songs = filtered_df.sort_values(by='similarity', ascending=False).head(100)

    avg_input_attributes = calculate_average_attributes(song_attributes)

    return jsonify(result=top_100_songs[['track_name', 'similarity']], avg_input_attributes=avg_input_attributes)

if __name__ == '__main__':
    app.run(debug=True)
