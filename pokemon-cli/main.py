import httpx
from models import Pokemon


def main():
    response = httpx.get("https://pokeapi.co/api/v2/pokemon/pikachu")
    rawData = response.json()
    pokemon = Pokemon(**rawData)
    print(f"response data: {pokemon.name}")


if __name__ == "__main__":
    main()
