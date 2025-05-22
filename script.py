import requests
import time
import serial

API_KEY = '5nMOblcaLluhVKAoAKTBbrrhLzx2D774'
TICKER = 'MSFT'
url = f"https://api.polygon.io/v2/aggs/ticker/{TICKER}/prev?adjusted=true&apiKey={API_KEY}"

high = 0b0;
low = 0b0;

response = requests.get(url)
ser = serial.Serial("COM1" , 115200)

def convert(price):
    firstByte = price >> 8 & 0xff
    secondByte = price % 256 & 0xff
    return firstByte, secondByte

while response.status_code == 200:
    data = response.json()
    price = bin(int(data['results'][0]['c'] * 100))[2:]
    # print(f" {TICKER}: {price}")

    # code from fpga to buy or sell
    pBit1, pBit2 = convert(price)
    hBit1, hBit2 = convert(price)
    lBit1, lBit2 = convert(price)

    ser.write(pBit1)
    ser.write(pBit2)

    ser.write(hBit1)
    ser.write(hBit2)

    ser.write(lBit1)
    ser.write(lBit2)

    action = ser.read(2)

    if action == 0b00:
        print("Sell")
        high = price

    elif action == 0b01:
        print("Hold")

    elif action == 0b10:
        print("Buy")
        low = price

    time.sleep(2)
    response = requests.get(url)

print("Error:", response.status_code, response.text)
