import os
import mysql.connector
from flask import Flask, request, redirect

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
    )

PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Asma Haroun</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: system-ui, sans-serif; background: #F7F8FA; color: #1C1F26; padding: 2.5rem 1.2rem; }}
  .wrap {{ max-width: 680px; margin: 0 auto; }}
  h1 {{ font-size: 1.7rem; font-weight: 700; }}
  .subtitle {{ color: #6B7280; margin-top: 0.4rem; font-size: 0.95rem; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 2rem; background: #fff; border: 1px solid #E5E7EB; border-radius: 8px; overflow: hidden; }}
  th, td {{ text-align: left; padding: 0.65rem 0.9rem; font-size: 0.92rem; border-bottom: 1px solid #EEF0F3; }}
  th {{ background: #F0F2F5; font-size: 0.78rem; text-transform: uppercase; color: #6B7280; }}
  tr:last-child td {{ border-bottom: none; }}
  .del-btn {{ background: none; border: none; color: #B91C1C; cursor: pointer; font-size: 0.85rem; padding: 0; }}
  .del-btn:hover {{ text-decoration: underline; }}
  form.inline {{ display: inline; }}
  form.add-form {{ margin-top: 1.6rem; background: #fff; border: 1px solid #E5E7EB; border-radius: 8px; padding: 1.2rem; display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 0.6rem; align-items: end; }}
  label {{ font-size: 0.72rem; color: #6B7280; text-transform: uppercase; display: block; margin-bottom: 0.3rem; }}
  input {{ width: 100%; padding: 0.5rem 0.6rem; border: 1px solid #D8DBE0; border-radius: 6px; }}
  button[type="submit"] {{ background: #1C1F26; color: #fff; border: none; padding: 0.55rem 1rem; border-radius: 6px; cursor: pointer; }}
  footer {{ margin-top: 2.2rem; font-size: 0.78rem; color: #9CA3AF; }}
  @media (max-width: 560px) {{ form.add-form {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>Asma Haroun</h1>
    <p class="subtitle">Produits disponibles </p>

    <table>
      <thead><tr><th>Produit</th><th>Prix</th><th>Stock</th><th></th></tr></thead>
      <tbody>{rows}</tbody>
    </table>

    <form class="add-form" method="post" action="/ajouter">
      <div><label>Nom</label><input type="text" name="nom" required></div>
      <div><label>Prix (€)</label><input type="number" step="0.01" name="prix" required></div>
      <div><label>Stock</label><input type="number" name="stock" required></div>
      <button type="submit">Ajouter</button>
    </form>

    <footer>Nginx + Flask-python + MySQL</footer>
  </div>
</body>
</html>
"""

ROW = """<tr>
  <td>{nom}</td>
  <td>{prix:.2f} €</td>
  <td>{stock}</td>
  <td>
    <form class="inline" method="post" action="/supprimer/{id}">
      <button type="submit" class="del-btn">Supprimer</button>
    </form>
  </td>
</tr>"""

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, prix, stock FROM produits ORDER BY id DESC")
    rows_html = "".join(
        ROW.format(id=pid, nom=nom, prix=prix, stock=stock)
        for pid, nom, prix, stock in cursor.fetchall()
    )
    cursor.close()
    conn.close()
    return app.response_class(
        PAGE.format(rows=rows_html),
        mimetype="text/html; charset=utf-8",
    )

@app.route("/ajouter", methods=["POST"])
def ajouter():
    nom = request.form["nom"]
    prix = request.form["prix"]
    stock = request.form["stock"]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)",
        (nom, prix, stock),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")

@app.route("/supprimer/<int:produit_id>", methods=["POST"])
def supprimer(produit_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produits WHERE id = %s", (produit_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
