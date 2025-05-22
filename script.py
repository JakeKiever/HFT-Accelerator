import requests
import time
import serial

API_KEY = '5nMOblcaLluhVKAoAKTBbrrhLzx2D774'
TICKER = 'MSFT'
url = f"https://api.polygon.io/v2/aggs/ticker/{TICKER}/prev?adjusted=true&apiKey={API_KEY}"

high = 0;
low = 0;

response = requests.get(url)
ser = serial.Serial("COM1" , 115200)

def convert(price):
    firstByte = price >> 8 & 0xff
    secondByte = price % 256 & 0xff
    return firstByte, secondByte

while response.status_code == 200:
    data = response.json()
    price = int(data['results'][0]['c'] * 100)
    #price = int(priceString[2 : len(priceString)])

    # print(f" {TICKER}: {price}")

    # code from fpga to buy or sell
    pBit1, pBit2 = convert(price)
    hBit1, hBit2 = convert(price)
    lBit1, lBit2 = convert(price)

    ser.write(bytes([pBit1, pBit2, hBit1, hBit2, lBit1, lBit2]))

    #ser.write(bytes([pBit1]))
    #ser.write(bytes([pBit2]))

    #ser.write(bytes([hBit1]))
    #ser.write(bytes([hBit2]))

    #ser.write(bytes([lBit1]))
    #ser.write(bytes([lBit2]))

    recievedData = ser.read(2)
    action = int.from_bytes(recievedData, byteorder='big')

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
