import requests

def send_query(number):
    url = "http://127.0.0.1:8000/echo_number/"
    params = {'number': number}
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    number = input("Podaj liczbę do wysłania na serwer: ")
    try:
        number = int(number)
        result = send_query(number)
        print(f"Odpowiedź serwera: {result}")
    except ValueError:
        print("Podana wartość nie jest liczbą całkowitą.")
    except requests.exceptions.RequestException as e:
        print(f"Błąd połączenia: {e}")