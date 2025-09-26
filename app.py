import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecret"

# Ajusta la URI a tu usuario real (cc5002 / programacionweb si quieres)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://cc5002:programacionweb@localhost/tarea2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "img")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# --- Modelos (igual que los tuyos) ---
class Region(db.Model):
    __tablename__ = "region"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))

class Comuna(db.Model):
    __tablename__ = "comuna"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"))

class Aviso(db.Model):
    __tablename__ = "aviso_adopcion"
    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.now)
    comuna_id = db.Column(db.Integer, db.ForeignKey("comuna.id"))
    sector = db.Column(db.String(100))
    nombre = db.Column(db.String(200))
    email = db.Column(db.String(100))
    celular = db.Column(db.String(15))
    tipo = db.Column(db.Enum("gato", "perro"))
    cantidad = db.Column(db.Integer)
    edad = db.Column(db.Integer)
    unidad_medida = db.Column(db.Enum("a", "m"))
    fecha_entrega = db.Column(db.DateTime)
    descripcion = db.Column(db.Text)

class Foto(db.Model):
    __tablename__ = "foto"
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300))
    nombre_archivo = db.Column(db.String(300))
    actividad_id = db.Column(db.Integer, db.ForeignKey("aviso_adopcion.id"))

class Contacto(db.Model):
    __tablename__ = "contactar_por"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Enum("whatsapp", "telegram", "X", "instagram", "tiktok", "otra"))
    identificador = db.Column(db.String(150))
    actividad_id = db.Column(db.Integer, db.ForeignKey("aviso_adopcion.id"))

# --- Rutas ---
@app.route("/")
def index():
    return render_template("portada2.html")

@app.route("/api/regiones")
def api_regiones():
    regiones = Region.query.order_by(Region.nombre).all()
    return jsonify([{"id": r.id, "nombre": r.nombre} for r in regiones])

@app.route("/api/comunas/<int:region_id>")
def api_comunas(region_id):
    comunas = Comuna.query.filter_by(region_id=region_id).order_by(Comuna.nombre).all()
    return jsonify([{"id": c.id, "nombre": c.nombre} for c in comunas])

@app.route("/api/ultimos")
def api_ultimos():
    avisos = Aviso.query.order_by(Aviso.fecha_ingreso.desc()).limit(5).all()
    data = []
    for a in avisos:
        fotos = Foto.query.filter_by(actividad_id=a.id).all()
        comuna = Comuna.query.get(a.comuna_id)
        data.append({
            "id": a.id,
            "fechaPub": a.fecha_ingreso.strftime("%Y-%m-%d"),
            "comuna": comuna.nombre if comuna else "",
            "sector": a.sector,
            "cantidad": a.cantidad,
            "tipo": a.tipo,
            "edad": f"{a.edad} {'años' if a.unidad_medida=='a' else 'meses'}",
            "fotos": [ url_for('static', filename=f"img/{f.nombre_archivo}") for f in fotos ]
        })
    return jsonify(data)

@app.route("/api/listado")
def api_listado():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    pagination = Aviso.query.order_by(Aviso.fecha_ingreso.desc()).paginate(page=page, per_page=per_page, error_out=False)
    data = []
    for a in pagination.items:
        fotos = Foto.query.filter_by(actividad_id=a.id).all()
        comuna = Comuna.query.get(a.comuna_id)
        data.append({
            "id": a.id,
            "fechaPub": a.fecha_ingreso.strftime("%Y-%m-%d"),
            "fechaEnt": a.fecha_entrega.strftime("%Y-%m-%d") if a.fecha_entrega else "",
            "comuna": comuna.nombre if comuna else "",
            "sector": a.sector,
            "cantidad": a.cantidad,
            "tipo": a.tipo,
            "edad": f"{a.edad} {'años' if a.unidad_medida=='a' else 'meses'}",
            "nombre": a.nombre,
            "contacto": a.email,
            "fotos": [ url_for('static', filename=f"img/{f.nombre_archivo}") for f in fotos ]
        })
    return jsonify({
        "avisos": data,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "next_num": pagination.next_num if pagination.has_next else None,
        "prev_num": pagination.prev_num if pagination.has_prev else None
    })

@app.route("/api/detalle/<int:aviso_id>")
def api_detalle(aviso_id):
    a = Aviso.query.get_or_404(aviso_id)
    fotos = Foto.query.filter_by(actividad_id=a.id).all()
    comuna = Comuna.query.get(a.comuna_id)
    return jsonify({
        "id": a.id,
        "fechaPub": a.fecha_ingreso.strftime("%Y-%m-%d"),
        "fechaEnt": a.fecha_entrega.strftime("%Y-%m-%d") if a.fecha_entrega else "",
        "comuna": comuna.nombre if comuna else "",
        "sector": a.sector,
        "cantidad": a.cantidad,
        "tipo": a.tipo,
        "edad": f"{a.edad} {'años' if a.unidad_medida=='a' else 'meses'}",
        "nombre": a.nombre,
        "contacto": a.email,
        "descripcion": a.descripcion,
        "fotos": [ url_for('static', filename=f"img/{f.nombre_archivo}") for f in fotos ]
    })

@app.route("/agregar-aviso", methods=["POST"])
def agregar_aviso():
    try:
        # Lectura y validación básica
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        tipo = request.form.get("tipo")
        try:
            cantidad = int(request.form.get("cantidad", 0))
            edad = int(request.form.get("edad", 0))
        except ValueError:
            flash("Cantidad/Edad deben ser números", "error")
            return redirect(url_for("index"))

        if not nombre or len(nombre) < 3:
            flash("Nombre inválido", "error"); return redirect(url_for("index"))
        if not email or len(email) > 100:
            flash("Email inválido", "error"); return redirect(url_for("index"))
        if tipo not in ("perro", "gato"):
            flash("Tipo inválido", "error"); return redirect(url_for("index"))
        if cantidad < 1 or edad < 0:
            flash("Cantidad/Edad inválidos", "error"); return redirect(url_for("index"))

        comuna_id = request.form.get("comuna")
        sector = request.form.get("sector")
        unidad = request.form.get("unidad_medida")
        fecha_entrega_raw = request.form.get("fecha_entrega")
        descripcion = request.form.get("descripcion")

        fecha_entrega = None
        if fecha_entrega_raw:
            # datetime-local formato: YYYY-MM-DDTHH:MM
            fecha_entrega = datetime.fromisoformat(fecha_entrega_raw)

        aviso = Aviso(
            comuna_id = int(comuna_id) if comuna_id else None,
            sector = sector,
            nombre = nombre,
            email = email,
            celular = request.form.get("celular"),
            tipo = tipo,
            cantidad = cantidad,
            edad = edad,
            unidad_medida = unidad,
            fecha_entrega = fecha_entrega,
            descripcion = descripcion
        )
        db.session.add(aviso)
        db.session.flush()   # genera id en DB sin commit aún

        # Contactos: emparejar medios y ids
        medios = request.form.getlist("contactar_por")
        ids = request.form.getlist("contacto-id")
        # zip safe: empareja hasta la longitud mínima
        for medio, ident in zip(medios, ids):
            if ident and medio:
                c = Contacto(nombre=medio, identificador=ident, actividad_id=aviso.id)
                db.session.add(c)

        # Fotos
        if "foto" in request.files:
            fotos = request.files.getlist("foto")
            for f in fotos:
                if f and f.filename:
                    filename = secure_filename(f.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    f.save(filepath)
                    foto = Foto(ruta_archivo=f"/static/img/{filename}", nombre_archivo=filename, actividad_id=aviso.id)
                    db.session.add(foto)

        db.session.commit()
        flash("Aviso agregado exitosamente", "success")
        return redirect(url_for("index"))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear aviso: {e}", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
