import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(pokemon_id):
    url = f"{base_url}pokemon/{pokemon_id}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# GUI for the Pokedex
class PokedexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokedex")
        
        # Set window size
        self.root.geometry("600x600")

        self.label = tk.Label(root, text="Enter Pokemon ID:")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button = tk.Button(root, text="Get Info", command=self.get_info)
        self.button.pack()

        self.info_label = tk.Label(root, text="")
        self.info_label.pack()

        self.image_label = tk.Label(root)
        self.image_label.pack()

    def get_info(self):
        pokemon_id = self.entry.get()
        pokemon_info = get_pokemon_info(pokemon_id)

        if pokemon_info:
            name = pokemon_info['name']
            types = [type_info['type']['name'] for type_info in pokemon_info['types']]
            height = pokemon_info['height']
            weight = pokemon_info['weight']
            pokemon_number = pokemon_info['id']
            image_url = pokemon_info['sprites']['front_default']

            info_text = (f"Name: {name.capitalize()}\n"
                         f"Type: {', '.join(types)}\n"
                         f"Height: {height} dm\n"
                         f"Weight: {weight} hg\n"
                         f"Pokemon Number: {pokemon_number}")
            self.info_label.config(text=info_text)

            # Fetch and display the image
            if image_url:
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    image_data = image_response.content
                    image = Image.open(BytesIO(image_data))
                    image = image.resize((200, 200), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
                else:
                    print(f"Failed to retrieve image: {image_response.status_code}")
            else:
                print("No image available for this Pokémon.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokedexApp(root)
    root.mainloop()
