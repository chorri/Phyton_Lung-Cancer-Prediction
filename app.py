from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

responses = []

model = joblib.load('modelPredict.pkl')

@app.route('/')
def home():
    return render_template('PaginaWeb.html', bmi_result=None, responses=None)

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    responses.clear()  # Limpiar respuestas anteriores

    weight = float(request.form['weight'])
    height = float(request.form['height'])
    
    # Calculo del IMC
    bmi = weight / (height ** 2)

    # Estado del IMC
    if bmi < 18.5:
        bmi_result = f"IMC: {bmi:.1f} - Peso bajo"
        responses.append(1)
    elif 18.5 <= bmi < 24.9:
        bmi_result = f"IMC: {bmi:.1f} - Peso normal"
        responses.append(1)
    elif 25 <= bmi < 29.9:
        bmi_result = f"IMC: {bmi:.1f} - Sobrepeso"
        responses.append(2)
    else:
        bmi_result = f"IMC: {bmi:.1f} - Obeso"
        responses.append(3)
    
    # Se guarda las respuestas del cuestionario en una lista    
    responses.append(request.form.get('Coughing_of_Blood'))
    responses.append(request.form.get('Balanced_Diet'))
    responses.append(request.form.get('Passive_Smoker'))
    responses.append(request.form.get('Dust_Allergy'))
    responses.append(request.form.get('Alcohol_use'))
    responses.append(request.form.get('Genetic_Risk'))
    responses.append(request.form.get('Air_Pollution'))
    responses.append(request.form.get('Chest_Pain'))
    responses.append(request.form.get('OccuPational_Hazards'))
    responses.append(request.form.get('chronic_Lung_Disease'))
    responses.append(request.form.get('Smoking'))

    responses2 = [[int(i) for i in responses]]
        
    prediction = model.predict(responses2)[0]  # Realizar la predicción
    
    return render_template('PaginaWeb.html', bmi_result = bmi_result, prediction = prediction)

if __name__ == '__main__':
    app.run(debug=True)