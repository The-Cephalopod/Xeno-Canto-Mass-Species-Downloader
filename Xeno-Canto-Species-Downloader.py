import os
import requests

# Define species lists:
# Original species: you already have some pages downloaded (please see comment above start_page code)
original_species = [
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

# New species: download pages for new birds
new_species = [
    ("Ficedula", "parva"),       # Red-breasted Flycatcher
    ("Garrulus", "glandarius"),  # Jay (European Jay)
    ("Otis", "tarda")            # Bustard (Great Bustard)
]

# Combined list of species
species_list = original_species + new_species

# Set the base directory to your target folder
base_directory = r'Z:\BirdNET Dataset\Test'
os.makedirs(base_directory, exist_ok=True)

total_downloaded = 0

for genus, species in species_list:
    # Folder names are in the format {genus}_{species}-TEST
    folder_name = f"{genus}_{species}-TEST"
    save_directory = os.path.join(base_directory, folder_name)
    os.makedirs(save_directory, exist_ok=True)
    print(f"\n🔍 Downloading recordings for {genus} {species} into {save_directory}")
    
    # Determine starting page:
    # For species in original_species, skip page 1 (i.e., start from page 2)
    # For new species, download starting at page 1
    # This exists because I had downloaded page 1 of a few species and wanted to download the other pages as well as add some other new species
    # Please change the start_page for original and new species as you please (you may want to start originals (already downloaded) from page 2 for example
    if (genus, species) in original_species:
        start_page = 1
        # New species here:
    else:
        start_page = 1
    
    page = start_page
    while True:
      
        api_url = f"https://xeno-canto.org/api/2/recordings?query={genus}+{species}&page={page}"
        print(f"→ Querying {api_url}")
        response = requests.get(api_url)
        if response.status_code != 200:
            print(f"API request failed for {genus} {species} on page {page}")
            break
        
        data = response.json()
        recordings = data.get('recordings', [])
        if not recordings:
            print(f"No recordings found for {genus} {species} on page {page}")
            break
        
        for recording in recordings:
            try:
                recording_id = recording['id']
                # Download URL using the recording ID
                file_url = f"https://xeno-canto.org/{recording_id}/download"
                filename = f"{genus}_{species}_{recording_id}.wav"
                save_path = os.path.join(save_directory, filename)
                
                with requests.get(file_url, stream=True) as r:
                    if r.status_code == 200:
                        with open(save_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"Downloaded {filename}")
                        total_downloaded += 1
                    else:
                        print(f"Failed to download {filename} (status: {r.status_code})")
            except Exception as e:
                print(f"Error downloading recording {recording.get('id', '?')}: {e}")
        
        # Check the maximum number of pages from the API response
        num_pages = int(data.get('numPages', 1))
        if page >= num_pages:
            print(f"Reached the last page ({page}) for {genus} {species}.")
            break
        else:
            page += 1
            print(f"Moving to page {page} for {genus} {species}.")
            
print(f"\nFinished downloading. Total files downloaded: {total_downloaded}")
