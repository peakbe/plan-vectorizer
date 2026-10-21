import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_file, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)

UPLOAD_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/detect-openings', methods=['POST'])
def detect_openings():
    """Simule l'IA qui détecte les ouvrants (portes/fenêtres) sur la photo d'un mur"""
    if 'file' not in request.files:
        return jsonify({'error': 'Aucune image fournie'}), 400
    
    # Simulation d'une détection intelligente basée sur la longueur transmise
    wall_length = float(request.form.get('wallLength', 300))
    
    # Génération d'ouvrants probables proportionnels au mur
    simulated_openings = [
        {"type": "porte", "position": round(wall_length * 0.2, 1), "width": 90},
        {"type": "fenetre", "position": round(wall_length * 0.6, 1), "width": 120}
    ]
    
    return jsonify({
        'status': 'success',
        'openings': simulated_openings
    })

@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    """Génère le PDF vectoriel architectural final au format A4"""
    pdf_path = os.path.join(UPLOAD_FOLDER, 'plan_architecte.pdf')
    
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4 # 595.27 x 841.89 points

    # Style papier chaud / Encre bleu nuit
    c.setFillColorRGB(0.98, 0.96, 0.93) # Fond chaud
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # En-tête architectural
    c.setFillColorRGB(0.06, 0.09, 0.18) # Bleu nuit
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 40, "DOSSIER ARCHITECTURAL - PLAN DE PROJET")
    
    c.setFont("Helvetica", 9)
    c.drawString(40, height - 55, "Échelle : 1:50 | Format A4 Vectoriel")

    # Cadre du plan
    c.setStrokeColorRGB(0.06, 0.09, 0.18)
    c.setLineWidth(1.5)
    c.rect(40, 80, width - 80, height - 150)

    # Simulation du dessin des murs (Terracotta & Bleu nuit)
    c.setLineWidth(4)
    c.setStrokeColorRGB(0.06, 0.09, 0.18)
    c.rect(80, height - 450, 300, 250, stroke=1, fill=0)
    
    # Touche Terracotta pour les cloisons secondaires
    c.setStrokeColorRGB(0.81, 0.38, 0.27)
    c.setLineWidth(2.5)
    c.line(230, height - 450, 230, height - 300)

    # Légende technique en bas
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, 60, "RÉCAPITULATIF DES SURFACES ET OUVRANTS")
    c.setFont("Helvetica", 8)
    c.drawString(50, 45, "Pièce principale : 18.5 m² | Chambres : 12.0 m² | Total : 30.5 m²")

    c.save()
    return send_file(pdf_path, as_attachment=True, download_name="plan_architecte.pdf")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
