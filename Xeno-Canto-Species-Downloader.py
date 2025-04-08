import os
import requests

# List of species as tuples (Genus, species)
species_list = [
    ("Certhia", "familiaris"),
    ("Troglodytes", "troglodytes"),
    ("Dryocopus", "martius"),
    ("Poecile", "montanus"),
    ("Sitta", "europaea"),
    ("Sylvia", "atricapilla"),
    ("Parus", "major"),
    ("Turdus", "merula"),
    ("Fringilla", "coelebs")
]

# Set the base path for your NAS network drive
base_directory = r'Z:\BirdNET Dataset'
os.makedirs(base_directory, exist_ok=True)

total_downloaded = 0

# Loop through each species and download its recordings
for genus, species in species_list:
    folder_name = f"{genus}_{species}"
    save_directory = os.path.join(base_directory, folder_name)
    os.makedirs(save_directory, exist_ok=True)
    print(f"\n🔍 Downloading recordings for {genus} {species} into {save_directory}")

    # Query xeno-canto API for the recordings of the species
    api_url = f'https://xeno-canto.org/api/2/recordings?query=gen:{genus}+{species}'
    response = requests.get(api_url)

    if response.status_code != 200:
        print(f"API request failed for {genus} {species}")
        continue

    data = response.json()
    recordings = data.get('recordings', [])

    for recording in recordings:
        try:
            recording_id = recording['id']
            file_url = f'https://xeno-canto.org/{recording_id}/download'
            filename = f"{genus}_{species}_{recording_id}.wav"
            save_path = os.path.join(save_directory, filename)

            with requests.get(file_url, stream=True) as r:
                if r.status_code == 200:
                    with open(save_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Downloaded {filename} to {save_path}")
                    total_downloaded += 1
                else:
                    print(f"Failed to download {filename} (status: {r.status_code})")
        except Exception as e:
            print(f"Error downloading {recording.get('id', '?')}: {e}")

print(f"Finished downloading. Total files downloaded: {total_downloaded}")
