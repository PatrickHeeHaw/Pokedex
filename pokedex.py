import requests
import tkinter as tk
import PIL.Image, PIL.ImageTk 
import urllib3 
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
        self.root.geometry("390x390")
        self.color =  "#BDC4D4"

        #Set the background color
        self.root.configure(bg=self.color)

        self.label = tk.Label(root, text="Enter Pokemon ID:", bg=self.color, fg ="black", font=("Andy", 15, "bold"))
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button = tk.Button(root, text="Get Poke info", command=self.get_info, font = ("Andy", 10, "bold"))
        self.button.pack()

        self.info_label = tk.Label(root, text="", bg=self.color, fg ="black")
        self.info_label.pack()

        self.image_label = tk.Label(self)
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
        

            info_text = (f"Name: {name.capitalize()}\n"
                         f"Type: {', '.join(types)}\n"
                         f"Height: {height} dm\n"
                         f"Weight: {weight} hg\n"
                         f"Pokemon Number: {pokemon_number}")
            self.info_label.config(text=info_text)

            # Get the image URL
            image_url = pokemon_info['sprites']['front_default']

            # Download and display the image 
            response = requests.get(image_url)
            image_data = response.content
            image = PIL.Image.open(BytesIO(image_data))
            photo = PIL.ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo #Keep a reference to avoid garabage collection. 
        else:
            self.info_label.config(text="Pokemon not found")

            
if __name__ == "__main__":
    root = tk.Tk()
    app = PokedexApp(root)
    root.mainloop()
