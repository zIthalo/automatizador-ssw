

nome = input("Qual é o seu nome? ")
altura = float(input("Informe a sua altura em metros: "))
peso = float(input("Informe seu peso em KG: "))
imc = float(peso / (altura * altura))

if imc < 18.5:
    classificacao = "Abaixo do peso."
elif imc < 25:
    classificacao = "Com o peso normal"
elif imc < 30: 
    classificacao = "Sobrepeso (tá gordo)"
else:
    classificacao = "Obesidade (Vai treinar)"

print(f"Fala, {nome}!")
print(f"Seu IMC é: {imc:.2f} você está {classificacao}")

