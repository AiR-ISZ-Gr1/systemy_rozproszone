import requests

def send_query(url, params):
    response = requests.get(url, params=params)
    return response.json()



if __name__ == "__main__":
    user_id = input("Podaj user_id: ")
    product_id = input("Podaj product_id: ")
    opinion = input("Podaj opinię: ")
    try:
        user_id = int(user_id)
        product_id = int(product_id)
        opinion = str(opinion)
        url = "http://127.0.0.1:8000/add_opinion/add_opinion/"
        params = {'user_id': user_id,
                  'product_id': product_id,
                  'opinion_text': opinion}
        result = send_query(url, params)
        print(f"Odpowiedź serwera: {result}")
    except ValueError:
        print("Podana wartość nie jest liczbą całkowitą.")
    except requests.exceptions.RequestException as e:
        print(f"Błąd połączenia: {e}")