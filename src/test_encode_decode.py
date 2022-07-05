from Price import Price



vetho = int(0.37589 * 10 ** 12)
vet = int(0.3705 * 10 ** 12)
vebank = int(10.0592 * 10 ** 12)
veusd = int(1.03464 * 10 ** 6)
print(vetho)
print(vet)
print(vebank)
print(veusd)

print()

_price_list = [vetho, vet, vebank, veusd]
_price_bit = [57 , 57, 57, 37]
encoded = Price.encode(_price_list, _price_bit)
print('encoded price = ', encoded)
print()

decoded = Price.decode(price_bit=_price_bit, encoded_value=encoded)
print("Decoded list : ", decoded)

# decoded = Price.decode(encoded)
# print(decoded)